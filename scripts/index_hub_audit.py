#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "starterPrompt",
    "copyStarterPrompt",
    "toast",
]

REQUIRED_LINKS = [
    "session-lab.html",
    "question-lab.html",
    "type-duel-lab.html",
    "response-eval-lab.html",
    "calibration-lab.html",
    "benchmark-replay-lab.html",
    "case-gallery.html",
    "follow-up-lab.html",
    "agent-adapter-lab.html",
    "agent-portability-lab.html",
    "assets/experience-hub-route-map.svg",
    "assets/universal-agent-bridge-map.svg",
    "https://github.com/Zaoqu-Liu/mbti-typing-skill/blob/main/prompts/prompt-recipes.md",
    "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme",
    "https://github.com/Zaoqu-Liu/mbti-typing-skill/issues/new/choose",
    "agent_portability_request.yml",
]

REQUIRED_TERMS = [
    "MBTI Typing Skill Experience Hub",
    "Experience Hub",
    "Start Typing",
    "Review Answer",
    "Install Agent",
    "Portability",
    "Type Someone Now",
    "Validate A Result",
    "Study Failure Cases",
    "Install In An Agent",
    "Map A Future Host",
    "Contribute Evidence",
    "Experience Hub Route Map",
    "candidate set",
    "serious runner-up",
    "evidence ledger",
    "falsifier",
    "safety boundary",
    "not a clinical instrument",
    "not a clinical instrument, hiring tool, legal/medical/financial classifier, deterministic label generator, or psychometric ground truth source",
    "Use $mbti-typing",
    "Copy Starter Prompt",
    "local-first",
    "18",
    "16",
    "0",
]

FORBIDDEN_TERMS = [
    "<meta http-equiv=\"refresh\"",
    "<script src",
    " src=\"http://",
    " src=\"https://",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
    "eval(",
]

SVG_REQUIRED_TERMS = [
    "Experience Hub Route Map",
    "MBTI Typing Skill Experience Hub",
    "Start typing",
    "Install or adapt",
    "Session Lab",
    "Type Duel Lab",
    "Response Eval Lab",
    "Benchmark Replay",
    "Follow-Up",
    "User-facing proof",
    "Contribution routes",
    "Release gate",
    "scripts/index_hub_audit.py",
    "repository_scorecard.py",
    "candidate set",
    "serious runner-up",
    "evidence ledger",
    "falsifier",
    "safety boundary",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def audit(index_path: Path, svg_path: Path) -> list[Check]:
    html = read_text(index_path)
    svg = read_text(svg_path)
    svg_dependency_scan = svg.replace('xmlns="http://www.w3.org/2000/svg"', "")
    cards = html.count('data-route-card="')
    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Experience Hub</title>" in html, "product title is present"),
        Check("html:root_not_redirect", "http-equiv=\"refresh\"" not in html and "url=session-lab.html" not in html, "Pages root is a real hub, not a redirect"),
        Check("html:no_external_runtime", "<script src" not in html and " src=\"http" not in html, "page has no external runtime dependency"),
        Check("html:workflow_cards", cards >= 6, f"{cards} workflow route cards found"),
        Check("html:copy_prompt", "navigator.clipboard.writeText" in html and "document.execCommand(\"copy\")" in html, "starter prompt copy has clipboard fallback"),
        Check("html:dom_safety", "textContent" in html and "innerHTML" not in html and "insertAdjacentHTML" not in html, "page avoids unsafe HTML injection"),
        Check("html:route_map_img", 'src="assets/experience-hub-route-map.svg"' in html, "Experience Hub route map is rendered"),
        Check("svg:shape", "<svg" in svg and "viewBox=" in svg, "route map is SVG with viewBox"),
        Check("svg:accessibility", 'role="img"' in svg and "<title>" in svg and "<desc>" in svg, "route map has accessibility metadata"),
        Check("svg:no_remote_or_script", "<script" not in svg_dependency_scan and "http://" not in svg_dependency_scan and "https://" not in svg_dependency_scan, "route map has no script or remote dependency"),
    ]

    for element_id in REQUIRED_IDS:
        checks.append(Check(f"id:{element_id}", f'id="{element_id}"' in html, "required interactive element id exists"))
    for link in REQUIRED_LINKS:
        checks.append(Check(f"link:{link}", link in html, "required workflow link exists"))
    for term in REQUIRED_TERMS:
        checks.append(Check(f"term:{term}", term in html, "required product/safety term exists"))
    for term in FORBIDDEN_TERMS:
        checks.append(Check(f"forbid:{term}", term not in html, "page avoids redirects, external runtime, and unsafe HTML injection"))
    for term in SVG_REQUIRED_TERMS:
        checks.append(Check(f"svg_term:{term}", term in svg, "required route-map term exists"))
    return checks


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: index_hub_audit.py <docs/index.html> <docs/assets/experience-hub-route-map.svg>")
        return 2

    checks = audit(Path(sys.argv[1]), Path(sys.argv[2]))
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Index Hub Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
