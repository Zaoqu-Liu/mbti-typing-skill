#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


START_MARKER = "    // BEGIN GENERATED QUESTION CARDS"
END_MARKER = "    // END GENERATED QUESTION CARDS"

CARD_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

CARD_CONST_RE = re.compile(r"\s*const QUESTION_CARDS = (?P<cards>\[.*\]);\s*$", re.DOTALL)
SECTION_RE = re.compile(r"^## (?P<title>.+?)\s*$", re.MULTILINE)
SUBSECTION_RE = re.compile(r"^### (?P<title>.+?)\s*$", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def normalize_category(title: str) -> str:
    title = title.strip()
    aliases = {
        "Core Function Probes": "Core probes",
        "Adjacent-Type Discriminators": "Adjacent discriminators",
        "Stress And Recovery Probes": "Stress/recovery",
        "Big Five Cross-Checks": "Big Five cross-checks",
        "Contradiction Follow-Ups": "Contradiction follow-ups",
        "Round Templates": "Round templates",
        "Usage Rules": "Usage rules",
    }
    return aliases.get(title, title)


def split_sections(markdown: str) -> list[tuple[str, str]]:
    matches = list(SECTION_RE.finditer(markdown))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group("title")
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections.append((title, markdown[start:end].strip()))
    return sections


def split_subsections(section_body: str) -> list[tuple[str, str]]:
    matches = list(SUBSECTION_RE.finditer(section_body))
    subsections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = match.group("title")
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section_body)
        subsections.append((title, section_body[start:end].strip()))
    return subsections


def extract_quoted_questions(body: str) -> list[str]:
    questions: list[str] = []
    for quoted in re.findall(r'"([^"\n]*\?)"', body):
        question = clean_line(quoted)
        if question and question not in questions:
            questions.append(question)
    return questions


def extract_bullets(body: str) -> list[str]:
    bullets: list[str] = []
    for line in body.splitlines():
        cleaned = clean_line(line)
        if cleaned.startswith("- "):
            bullets.append(cleaned[2:])
    return bullets


def extract_numbered(body: str) -> list[str]:
    numbered: list[str] = []
    for line in body.splitlines():
        cleaned = clean_line(line)
        match = re.match(r"^\d+\.\s+(.+)$", cleaned)
        if match:
            numbered.append(match.group(1))
    return numbered


def parse_core_probe(title: str, category: str, body: str) -> dict[str, Any]:
    scene_match = re.search(r'Scene:\s+"(?P<scene>.+?)"', body)
    followup_match = re.search(r'Follow-up:\s+"(?P<followup>.+?)"', body)
    options: list[dict[str, str]] = []
    for line in body.splitlines():
        cleaned = clean_line(line)
        match = re.match(r"^-\s+(?P<label>[A-D])\.\s+(?P<text>.+?)\s+`(?P<signal>[^`]+)`$", cleaned)
        if match:
            options.append(
                {
                    "label": match.group("label"),
                    "text": match.group("text"),
                    "signal": match.group("signal"),
                }
            )

    questions = [scene_match.group("scene")] if scene_match else []
    if followup_match:
        questions.append(followup_match.group("followup"))

    return {
        "id": slugify(f"{category}-{title}"),
        "title": title,
        "category": category,
        "kind": "forced-choice scene",
        "sourceHeading": f"### {title}",
        "scene": scene_match.group("scene") if scene_match else "",
        "options": options,
        "questions": questions,
        "followups": [followup_match.group("followup")] if followup_match else [],
        "guidance": ["Ask the scene before revealing the function tags.", "After the answer, ask what feels irresponsible to skip."],
    }


def parse_adjacent(title: str, category: str, body: str) -> dict[str, Any]:
    questions = extract_quoted_questions(body)
    bullets = extract_bullets(body)
    return {
        "id": slugify(f"{category}-{title}"),
        "title": title,
        "category": category,
        "kind": "adjacent-type discriminator",
        "sourceHeading": f"### {title}",
        "scene": "",
        "options": [],
        "questions": questions,
        "followups": [],
        "guidance": bullets[:8],
    }


def parse_round_template(title: str, category: str, body: str) -> dict[str, Any]:
    bullets = extract_bullets(body)
    goal_match = re.search(r"Goal:\s*(?P<goal>.+)", body)
    questions = bullets[:]
    if goal_match:
        questions.append(f"Goal: {goal_match.group('goal')}")
    return {
        "id": slugify(f"{category}-{title}"),
        "title": title,
        "category": category,
        "kind": "round template",
        "sourceHeading": f"### {title}",
        "scene": "",
        "options": [],
        "questions": questions,
        "followups": [],
        "guidance": [goal_match.group("goal")] if goal_match else bullets,
    }


def parse_simple_section(title: str, category: str, body: str) -> dict[str, Any]:
    questions = extract_quoted_questions(body)
    if not questions:
        questions = extract_numbered(body)
    if not questions:
        questions = extract_bullets(body)
    return {
        "id": slugify(category),
        "title": title,
        "category": category,
        "kind": "question set",
        "sourceHeading": f"## {title}",
        "scene": "",
        "options": [],
        "questions": questions,
        "followups": [],
        "guidance": extract_bullets(body)[:8],
    }


def parse_question_bank(path: Path) -> list[dict[str, Any]]:
    markdown = read_text(path)
    cards: list[dict[str, Any]] = []
    for section_title, section_body in split_sections(markdown):
        if section_title == "Table of Contents":
            continue
        category = normalize_category(section_title)
        subsections = split_subsections(section_body)
        if not subsections:
            cards.append(parse_simple_section(section_title, category, section_body))
            continue
        for title, body in subsections:
            if category == "Core probes":
                cards.append(parse_core_probe(title, category, body))
            elif category == "Adjacent discriminators":
                cards.append(parse_adjacent(title, category, body))
            elif category == "Round templates":
                cards.append(parse_round_template(title, category, body))
            else:
                cards.append(parse_simple_section(title, category, body))

    useful_cards = [card for card in cards if card["questions"] or card["guidance"] or card["options"]]
    if not useful_cards:
        raise ValueError(f"{path} produced no question cards")
    return useful_cards


def render_card_block(cards: list[dict[str, Any]]) -> str:
    rendered = json.dumps(cards, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const QUESTION_CARDS = {rendered};\n{END_MARKER}"


def extract_embedded_cards(html: str) -> list[dict[str, Any]]:
    block_match = CARD_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("question lab is missing generated question markers")
    const_match = CARD_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("question lab generated block does not contain const QUESTION_CARDS JSON")
    cards = json.loads(const_match.group("cards"))
    if not isinstance(cards, list):
        raise ValueError("question lab QUESTION_CARDS payload must be a list")
    return cards


def sync_html(html: str, cards: list[dict[str, Any]]) -> str:
    replacement = render_card_block(cards)
    if not CARD_BLOCK_RE.search(html):
        raise ValueError("question lab is missing generated question markers")
    updated = CARD_BLOCK_RE.sub(replacement, html, count=1)
    question_count = sum(len(card.get("questions", [])) for card in cards)
    template_count = sum(1 for card in cards if card.get("category") == "Round templates")
    replacements = {
        r'(<strong id="metricCards">).*?(</strong>)': str(len(cards)),
        r'(<strong id="metricQuestions">).*?(</strong>)': str(question_count),
        r'(<strong id="metricTemplates">).*?(</strong>)': str(template_count),
        r'(<span id="visibleQuestionCount">).*?(</span>)': str(len(cards)),
    }
    for pattern, value in replacements.items():
        updated = re.sub(pattern, rf"\g<1>{value}\2", updated, count=1)
    return updated


def check(question_bank_path: Path, html_path: Path) -> int:
    expected = parse_question_bank(question_bank_path)
    actual = extract_embedded_cards(read_text(html_path))
    if actual == expected:
        print(f"Question Lab Source Sync: PASS ({len(expected)} cards match)")
        return 0

    expected_ids = [str(item["id"]) for item in expected]
    actual_ids = [str(item.get("id", "")) for item in actual if isinstance(item, dict)]
    print("Question Lab Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(question_bank_path: Path, html_path: Path) -> int:
    expected = parse_question_bank(question_bank_path)
    html = read_text(html_path)
    updated = sync_html(html, expected)
    if updated == html:
        print(f"Question Lab Source Sync: PASS ({len(expected)} cards already current)")
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Question Lab Source Sync: UPDATED ({len(expected)} cards written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/question-lab.html question data from question-bank.md.")
    parser.add_argument("question_bank_path", nargs="?", default="skill/mbti-typing/references/question-bank.md")
    parser.add_argument("html_path", nargs="?", default="docs/question-lab.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated QUESTION_CARDS block.")
    args = parser.parse_args()

    question_bank_path = Path(args.question_bank_path)
    html_path = Path(args.html_path)
    try:
        if args.write:
            return write(question_bank_path, html_path)
        return check(question_bank_path, html_path)
    except Exception as exc:
        print(f"Question Lab Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
