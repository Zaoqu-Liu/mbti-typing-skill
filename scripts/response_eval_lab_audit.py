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
    "modeSelect",
    "promptInput",
    "responseInput",
    "runAudit",
    "loadStrongExample",
    "loadBadExample",
    "clearLab",
    "scoreValue",
    "failedGateCount",
    "qualityLabel",
    "radarSvg",
    "qualityPolygon",
    "gateGrid",
    "receiptOutput",
    "repairPromptOutput",
    "issueSeedOutput",
    "copyRepairPrompt",
    "copyEvalJson",
    "downloadJson",
    "copyIssueSeed",
]

REQUIRED_TERMS = [
    "MBTI Typing Skill Response Eval Lab",
    "Response Quality Lab",
    "candidate set",
    "serious runner-up",
    "evidence movement",
    "falsifier",
    "safety boundary",
    "Anti-Flattery",
    "Copy Repair Prompt",
    "Copy Eval JSON",
    "Copy Issue Seed",
    "response_eval_improvement.yml",
    "Use $mbti-typing",
    "not psychometric ground truth",
    "local-first",
    "response-eval-lab/v1",
]

REQUIRED_GATE_IDS = [
    "candidate_set",
    "runner_up",
    "evidence_movement",
    "next_questions",
    "scene_questions",
    "duel_losing_conditions",
    "final_report_shape",
    "cross_framework_boundary",
    "falsifier",
    "safety_boundary",
    "calibrated_confidence",
    "no_overclaim",
    "no_flattery",
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
        Check("html:title", "<title>MBTI Typing Skill Response Eval Lab</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:download_json", "new Blob" in html and "application/json" in html, "JSON download is implemented"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-response-eval-lab-state" in html, "response eval drafts persist locally"),
        Check("js:analysis_engine", "analyzeResponse" in html and "buildReceipt" in html and "OVERCLAIM_RE" in html and "FLATTERY_RE" in html, "response analysis engine exists"),
        Check("js:mode_aware_required_gates", "REQUIRED_BY_MODE" in html and "live_round" in html and "type_duel" in html and "final_report" in html and "anti_pattern" in html, "mode-aware required gates exist"),
        Check("js:repair_prompt", "makeRepairPrompt" in html and "Failed gates" in html and "Use $mbti-typing" in html, "repair prompt builder exists"),
        Check("js:issue_seed", "makeIssueSeed" in html and "response_eval_improvement.yml" in html, "response eval issue seed exists"),
        Check("js:fixtures", "STRONG_FIXTURE" in html and "BAD_FIXTURE" in html, "strong and bad fixtures are embedded"),
        Check("js:radar", "qualityPolygon" in html and "renderRadar" in html, "radar rendering exists"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"gate:{item}", item in html, "required response quality gate exists") for item in REQUIRED_GATE_IDS)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Response Eval Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/response-eval-lab.html")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
