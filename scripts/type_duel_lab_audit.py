#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sync_type_duel_lab import extract_embedded_duels, parse_pair_duels


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "pairSearch",
    "clusterFilter",
    "pairList",
    "visiblePairCount",
    "duelDetail",
    "questionList",
    "losingConditions",
    "duelPromptOutput",
    "issueSeedOutput",
    "copyDuelPrompt",
    "copyIssueSeed",
    "resetFilters",
]


REQUIRED_TERMS = [
    "MBTI Typing Skill Type Duel Lab",
    "Pair Duel Matrix",
    "Killer Questions",
    "Losing Conditions",
    "Copy Duel Prompt",
    "Copy Issue Seed",
    "type_duel_improvement.yml",
    "Use $mbti-typing",
    "not a clinical instrument",
    "local-first",
    "runner-up",
    "falsifier",
    "pair-duels.md",
]


FORBIDDEN_TERMS = [
    "<script src",
    " src=",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
    "eval(",
]


TYPE_CODES = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run(path: Path, pair_duels_path: Path) -> int:
    html = read_text(path)
    source_duels = parse_pair_duels(pair_duels_path)
    source_pairs = [str(item["pair"]) for item in source_duels]
    try:
        embedded_duels = extract_embedded_duels(html)
        source_sync_error = ""
    except Exception as exc:
        embedded_duels = []
        source_sync_error = str(exc)

    clusters = {str(item.get("cluster", "")) for item in embedded_duels if isinstance(item, dict)}
    question_count = sum(len(item.get("killerQuestions", [])) for item in embedded_duels if isinstance(item, dict))
    losing_count = sum(len(item.get("losingConditions", {})) for item in embedded_duels if isinstance(item, dict))

    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Type Duel Lab</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("html:issue_template_link", "issues/new?template=type_duel_improvement.yml" in html, "page links to the type-duel issue template"),
        Check("js:all_16_types", all(type_code in html for type_code in TYPE_CODES), "all 16 type codes remain visible"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-type-duel-lab-state" in html, "selected duel state persists locally"),
        Check("js:prompt_builder", "buildDuelPrompt" in html and "Use $mbti-typing" in html, "duel prompt builder exists"),
        Check("js:issue_seed", "buildIssueSeed" in html and "type_duel_improvement.yml" in html, "issue seed builder exists"),
        Check("source:generated_markers", "BEGIN GENERATED TYPE DUELS" in html and "END GENERATED TYPE DUELS" in html, "generated duel block is marked"),
        Check("source:markdown_match", embedded_duels == source_duels, source_sync_error or "embedded duels match pair-duels.md"),
        Check("source:duel_count", len(embedded_duels) == len(source_duels) and len(source_duels) >= 18, f"{len(embedded_duels)} embedded / {len(source_duels)} source duels"),
        Check("source:cluster_count", {"NT/NF", "SJ/SP", "Cross-temperament"} <= clusters, f"clusters={', '.join(sorted(clusters))}"),
        Check("source:question_count", question_count >= 45, f"{question_count} killer questions embedded"),
        Check("source:losing_condition_count", losing_count >= 34, f"{losing_count} losing conditions embedded"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"pair:{pair}", pair in html, "required pair duel appears") for pair in source_pairs)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Type Duel Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/type-duel-lab.html")
    pair_duels_path = Path(argv[2]) if len(argv) > 2 else path.parent.parent / "skill/mbti-typing/references/pair-duels.md"
    return run(path, pair_duels_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
