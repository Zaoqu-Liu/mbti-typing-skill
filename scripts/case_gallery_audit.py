#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "filterRail",
    "caseGrid",
    "caseDetail",
    "promptOutput",
    "copyPrompt",
    "copyIssueSeed",
    "issueLink",
    "visibleCount",
]


REQUIRED_TERMS = [
    "MBTI Typing Skill Benchmark Arena",
    "Benchmark Arena",
    "Case Matrix",
    "Use $mbti-typing",
    "Submit Benchmark Case",
    "Not psychometric ground truth",
    "runner-up",
    "Strongest falsifier",
    "Trap",
    "local-first",
]


REQUIRED_CASE_IDS = [
    "bench-entj-intj-001",
    "bench-intj-entj-002",
    "bench-infp-infj-003",
    "bench-infj-infp-004",
    "bench-estj-entj-005",
    "bench-entp-enfp-006",
    "bench-isfj-infj-007",
    "bench-estp-entp-008",
]


FORBIDDEN_TERMS = [
    "<script src",
    " src=",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
    "eval(",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run(path: Path) -> int:
    html = read_text(path)
    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Benchmark Arena</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("js:case_count", html.count("bench-") >= 8, "benchmark case ids are embedded"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:filters", "filterRail" in html and "activeFilter" in html and "getVisibleCases" in html, "case filters are implemented"),
        Check("js:issue_seed", "buildIssueSeed" in html and "benchmark_case.yml" in html, "issue seed and benchmark issue link exist"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"case:{case_id}", case_id in html, "required benchmark case appears") for case_id in REQUIRED_CASE_IDS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Case Gallery Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/case-gallery.html")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
