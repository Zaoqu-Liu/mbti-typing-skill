#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sync_benchmark_replay_lab import extract_embedded_cases, load_cases, make_replay_cases


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "caseSelect",
    "blindPromptOutput",
    "leadingGuess",
    "runnerGuess",
    "falsifierGuess",
    "replayScoreGrid",
    "replayTimeline",
    "referencePanel",
    "replayReceiptOutput",
    "repairPromptOutput",
    "issueSeedOutput",
    "copyBlindPrompt",
    "copyReplayJSON",
    "copyRepairPrompt",
    "copyIssueSeed",
    "revealReference",
]


REQUIRED_TERMS = [
    "MBTI Typing Skill Benchmark Replay Lab",
    "Blind Replay",
    "Reveal Reference",
    "Copy Blind Prompt",
    "Copy Replay JSON",
    "Copy Repair Prompt",
    "Copy Issue Seed",
    "benchmark_replay_improvement.yml",
    "not psychometric ground truth",
    "local-first",
    "runner-up",
    "Strongest falsifier",
    "Replay Receipt",
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


def run(path: Path, cases_path: Path, issue_template_path: Path) -> int:
    html = read_text(path)
    issue_template = read_text(issue_template_path)
    source_cases = make_replay_cases(load_cases(cases_path))
    leading_types = {str(item["leading"]) for item in source_cases}
    required_types = {"ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP", "INTJ", "INFJ", "ENTJ", "ENFJ", "INTP", "INFP", "ENTP", "ENFP"}
    try:
        embedded_cases = extract_embedded_cases(html)
        source_sync_error = ""
    except Exception as exc:
        embedded_cases = []
        source_sync_error = str(exc)

    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Benchmark Replay Lab</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("js:case_count", html.count("bench-") >= 16, "benchmark replay case ids are embedded"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:reveal_flow", "revealReference" in html and "referencePanel" in html and "state.revealed" in html, "blind replay reveal flow is implemented"),
        Check("js:receipt", "buildReplayReceipt" in html and "replay-lab/v1" in html, "Replay Receipt JSON is implemented"),
        Check("js:repair_prompt", "buildRepairPrompt" in html and "Use $mbti-typing" in html, "repair prompt is implemented"),
        Check("js:issue_seed", "buildIssueSeed" in html and "benchmark_replay_improvement.yml" in html, "issue seed and benchmark replay issue link exist"),
        Check("source:generated_markers", "BEGIN GENERATED BENCHMARK REPLAY CASES" in html and "END GENERATED BENCHMARK REPLAY CASES" in html, "generated replay case block is marked"),
        Check("source:json_match", embedded_cases == source_cases, source_sync_error or "embedded replay cases match canonical benchmark JSON"),
        Check("source:case_count", len(embedded_cases) == len(source_cases) and len(source_cases) >= 16, f"{len(embedded_cases)} embedded / {len(source_cases)} source cases"),
        Check("source:all_16_leading", required_types <= leading_types, f"{len(leading_types & required_types)} leading types covered"),
        Check("issue_template:title", "Benchmark replay improvement" in issue_template, "dedicated replay issue template exists"),
        Check("issue_template:fields", all(term in issue_template for term in ("case id", "replay score", "leading guess", "runner-up guess", "falsifier", "public-safe")), "issue template captures replay failure fields"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"case:{case_id}", case_id in html, "required benchmark replay case appears") for case_id in [item["id"] for item in source_cases])

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Benchmark Replay Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/benchmark-replay-lab.html")
    cases_path = Path(argv[2]) if len(argv) > 2 else path.parent.parent / "skill/mbti-typing/examples/benchmark-cases.json"
    issue_template_path = Path(argv[3]) if len(argv) > 3 else path.parent.parent / ".github/ISSUE_TEMPLATE/benchmark_replay_improvement.yml"
    return run(path, cases_path, issue_template_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
