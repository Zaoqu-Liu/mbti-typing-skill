#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


START_MARKER = "    // BEGIN GENERATED TYPE DUELS"
END_MARKER = "    // END GENERATED TYPE DUELS"

DUEL_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

DUEL_CONST_RE = re.compile(r"\s*const TYPE_DUELS = (?P<duels>\[.*\]);\s*$", re.DOTALL)

HEADING_RE = re.compile(r"^### (?P<a>[A-Z]{4}) vs (?P<b>[A-Z]{4})\s*$", re.MULTILINE)
SECTION_RE = re.compile(r"^## (?P<title>.+?)\s*$", re.MULTILINE)
QUESTION_RE = re.compile(r"^\d+\.\s+\"(?P<question>.+?)\"\s*$")
LOSE_RE = re.compile(r"^(?P<type>[A-Z]{4}) loses if:\s*(?P<condition>.+?)\s*$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_cluster(title: str) -> str:
    title = title.strip()
    if title.lower() == "nt and nf duels":
        return "NT/NF"
    if title.lower() == "sj and sp duels":
        return "SJ/SP"
    if title.lower() == "cross-temperament mistypes":
        return "Cross-temperament"
    return title


def section_for_position(markdown: str, position: int) -> str:
    active = "General"
    for match in SECTION_RE.finditer(markdown):
        if match.start() > position:
            break
        active = normalize_cluster(match.group("title"))
    return active


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def parse_duel_body(body: str) -> dict[str, Any]:
    shared_surface = ""
    questions: list[str] = []
    losing_conditions: dict[str, str] = {}
    notes: list[str] = []

    in_questions = False
    for raw_line in body.splitlines():
        line = clean_line(raw_line)
        if not line:
            continue
        if line.startswith("Shared surface:"):
            shared_surface = line.removeprefix("Shared surface:").strip()
            in_questions = False
            continue
        if line == "Killer questions:":
            in_questions = True
            continue
        question_match = QUESTION_RE.match(line)
        if in_questions and question_match:
            questions.append(question_match.group("question"))
            continue
        lose_match = LOSE_RE.match(line)
        if lose_match:
            losing_conditions[lose_match.group("type")] = lose_match.group("condition")
            in_questions = False
            continue
        if not line.startswith("```"):
            notes.append(line)

    return {
        "sharedSurface": shared_surface,
        "killerQuestions": questions,
        "losingConditions": losing_conditions,
        "notes": notes,
    }


def parse_pair_duels(path: Path) -> list[dict[str, Any]]:
    markdown = read_text(path)
    heading_matches = list(HEADING_RE.finditer(markdown))
    if not heading_matches:
        raise ValueError(f"{path} contains no type-pair headings")

    duels: list[dict[str, Any]] = []
    for index, match in enumerate(heading_matches):
        start = match.end()
        next_heading = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(markdown)
        template_heading = markdown.find("## Duel Output Template", start)
        end = min(next_heading, template_heading) if template_heading != -1 else next_heading
        type_a = match.group("a")
        type_b = match.group("b")
        body = markdown[start:end]
        parsed = parse_duel_body(body)
        pair = f"{type_a} vs {type_b}"
        duels.append(
            {
                "id": pair.lower().replace(" ", "-"),
                "pair": pair,
                "types": [type_a, type_b],
                "cluster": section_for_position(markdown, match.start()),
                "sourceHeading": f"### {pair}",
                **parsed,
            }
        )

    return duels


def render_duel_block(duels: list[dict[str, Any]]) -> str:
    rendered = json.dumps(duels, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const TYPE_DUELS = {rendered};\n{END_MARKER}"


def extract_embedded_duels(html: str) -> list[dict[str, Any]]:
    block_match = DUEL_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("type duel lab is missing generated type duel markers")
    const_match = DUEL_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("type duel lab generated block does not contain const TYPE_DUELS JSON")
    duels = json.loads(const_match.group("duels"))
    if not isinstance(duels, list):
        raise ValueError("type duel lab TYPE_DUELS payload must be a list")
    return duels


def sync_html(html: str, duels: list[dict[str, Any]]) -> str:
    replacement = render_duel_block(duels)
    if not DUEL_BLOCK_RE.search(html):
        raise ValueError("type duel lab is missing generated type duel markers")
    updated = DUEL_BLOCK_RE.sub(replacement, html, count=1)
    question_count = sum(len(duel.get("killerQuestions", [])) for duel in duels)
    condition_count = sum(len(duel.get("losingConditions", {})) for duel in duels)
    replacements = {
        r'(<strong id="metricPairs">).*?(</strong>)': str(len(duels)),
        r'(<strong id="metricQuestions">).*?(</strong>)': str(question_count),
        r'(<strong id="metricConditions">).*?(</strong>)': str(condition_count),
        r'(<span id="visiblePairCount">).*?(</span>)': str(len(duels)),
    }
    for pattern, value in replacements.items():
        updated = re.sub(pattern, rf"\g<1>{value}\2", updated, count=1)
    return updated


def check(pair_duels_path: Path, html_path: Path) -> int:
    expected = parse_pair_duels(pair_duels_path)
    actual = extract_embedded_duels(read_text(html_path))
    if actual == expected:
        print(f"Type Duel Lab Source Sync: PASS ({len(expected)} duels match)")
        return 0

    expected_ids = [str(item["id"]) for item in expected]
    actual_ids = [str(item.get("id", "")) for item in actual if isinstance(item, dict)]
    print("Type Duel Lab Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(pair_duels_path: Path, html_path: Path) -> int:
    expected = parse_pair_duels(pair_duels_path)
    html = read_text(html_path)
    updated = sync_html(html, expected)
    if updated == html:
        print(f"Type Duel Lab Source Sync: PASS ({len(expected)} duels already current)")
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Type Duel Lab Source Sync: UPDATED ({len(expected)} duels written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/type-duel-lab.html duel data from pair-duels.md.")
    parser.add_argument("pair_duels_path", nargs="?", default="skill/mbti-typing/references/pair-duels.md")
    parser.add_argument("html_path", nargs="?", default="docs/type-duel-lab.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated TYPE_DUELS block.")
    args = parser.parse_args()

    pair_duels_path = Path(args.pair_duels_path)
    html_path = Path(args.html_path)
    try:
        if args.write:
            return write(pair_duels_path, html_path)
        return check(pair_duels_path, html_path)
    except Exception as exc:
        print(f"Type Duel Lab Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
