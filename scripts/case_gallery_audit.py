#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sync_case_gallery import extract_embedded_cases, load_cases, make_gallery_cases


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


def run(path: Path, cases_path: Path) -> int:
    html = read_text(path)
    source_cases = make_gallery_cases(load_cases(cases_path))
    try:
        embedded_cases = extract_embedded_cases(html)
        source_sync_error = ""
    except Exception as exc:
        embedded_cases = []
        source_sync_error = str(exc)

    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Benchmark Arena</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("js:case_count", html.count("bench-") >= 8, "benchmark case ids are embedded"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:filters", "filterRail" in html and "activeFilter" in html and "getVisibleCases" in html, "case filters are implemented"),
        Check("js:issue_seed", "buildIssueSeed" in html and "benchmark_case.yml" in html, "issue seed and benchmark issue link exist"),
        Check("source:generated_markers", "BEGIN GENERATED BENCHMARK CASES" in html and "END GENERATED BENCHMARK CASES" in html, "generated case block is marked"),
        Check("source:json_match", embedded_cases == source_cases, source_sync_error or "embedded cases match canonical benchmark JSON"),
        Check("source:case_count", len(embedded_cases) == len(source_cases) and len(source_cases) >= 8, f"{len(embedded_cases)} embedded / {len(source_cases)} source cases"),
        Check("source:display_metadata", all(item.get("cluster") and item.get("title") for item in source_cases), "source cases include gallery cluster and display title"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"case:{case_id}", case_id in html, "required benchmark case appears") for case_id in [item["id"] for item in source_cases])

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Case Gallery Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/case-gallery.html")
    cases_path = Path(argv[2]) if len(argv) > 2 else path.parent.parent / "skill/mbti-typing/examples/benchmark-cases.json"
    return run(path, cases_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
