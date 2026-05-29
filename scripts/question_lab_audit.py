#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sync_question_lab import extract_embedded_cards, parse_question_bank


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "questionSearch",
    "categoryFilter",
    "cardList",
    "visibleQuestionCount",
    "targetConflictInput",
    "roundTemplateSelect",
    "questionDetail",
    "questionList",
    "roundPromptOutput",
    "issueSeedOutput",
    "copyRoundPrompt",
    "copyIssueSeed",
    "resetQuestionFilters",
]


REQUIRED_TERMS = [
    "MBTI Typing Skill Question Lab",
    "Adaptive Question Bank",
    "Round Builder",
    "Copy Round Prompt",
    "Copy Issue Seed",
    "question_improvement.yml",
    "Use $mbti-typing",
    "not a clinical instrument",
    "local-first",
    "question-bank.md",
    "4-6 questions",
    "target uncertainty",
    "runner-up",
    "falsifier",
    "low-typing",
    "native question UI",
    "Other / none of these",
]


FORBIDDEN_TERMS = [
    "<script src",
    " src=",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
    "eval(",
]


REQUIRED_CATEGORIES = {
    "Usage rules",
    "Core probes",
    "Adjacent discriminators",
    "Stress/recovery",
    "Big Five cross-checks",
    "Contradiction follow-ups",
    "Round templates",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run(path: Path, question_bank_path: Path) -> int:
    html = read_text(path)
    source_cards = parse_question_bank(question_bank_path)
    source_titles = [str(item["title"]) for item in source_cards]
    try:
        embedded_cards = extract_embedded_cards(html)
        source_sync_error = ""
    except Exception as exc:
        embedded_cards = []
        source_sync_error = str(exc)

    categories = {str(item.get("category", "")) for item in embedded_cards if isinstance(item, dict)}
    question_count = sum(len(item.get("questions", [])) for item in embedded_cards if isinstance(item, dict))
    option_count = sum(len(item.get("options", [])) for item in embedded_cards if isinstance(item, dict))
    template_count = sum(1 for item in embedded_cards if item.get("category") == "Round templates")

    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Question Lab</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("html:issue_template_link", "issues/new?template=question_improvement.yml" in html, "page links to the question improvement issue template"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-question-lab-state" in html, "question lab state persists locally"),
        Check("js:prompt_builder", "buildRoundPrompt" in html and "Use $mbti-typing" in html, "round prompt builder exists"),
        Check("js:issue_seed", "buildIssueSeed" in html and "question_improvement.yml" in html, "issue seed builder exists"),
        Check("source:generated_markers", "BEGIN GENERATED QUESTION CARDS" in html and "END GENERATED QUESTION CARDS" in html, "generated question block is marked"),
        Check("source:markdown_match", embedded_cards == source_cards, source_sync_error or "embedded cards match question-bank.md"),
        Check("source:card_count", len(embedded_cards) == len(source_cards) and len(source_cards) >= 20, f"{len(embedded_cards)} embedded / {len(source_cards)} source cards"),
        Check("source:category_count", REQUIRED_CATEGORIES <= categories, f"categories={', '.join(sorted(categories))}"),
        Check("source:question_count", question_count >= 35, f"{question_count} questions embedded"),
        Check("source:option_count", option_count >= 20, f"{option_count} forced-choice options embedded"),
        Check("source:template_count", template_count >= 5, f"{template_count} round templates embedded"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"card:{title}", title in html, "required source card title appears") for title in source_titles)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Question Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/question-lab.html")
    question_bank_path = Path(argv[2]) if len(argv) > 2 else path.parent.parent / "skill/mbti-typing/references/question-bank.md"
    return run(path, question_bank_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
