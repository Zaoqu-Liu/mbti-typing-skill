#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "Makefile",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/benchmark_case.yml",
    "prompts/prompt-recipes.md",
    "examples/session-state-example.json",
    "examples/evidence-ledger-example.md",
    "docs/assets/mbti-typing-hero.png",
    "docs/assets/typing-journey-map.png",
    "docs/evaluation.md",
    "docs/experience-principles.md",
    "docs/github-ux.md",
    "docs/visual-tour.md",
    "docs/demo-session.md",
    "docs/sample-report.md",
    "docs/playground.html",
    "docs/index.html",
    "skill/mbti-typing/SKILL.md",
]


README_REQUIRED_TERMS = [
    "docs/assets/mbti-typing-hero.png",
    "docs/assets/typing-journey-map.png",
    "Interactive Playground",
    "https://zaoqu-liu.github.io/mbti-typing-skill/playground.html",
    "docs/playground.html",
    "One-Minute Demo",
    "docs/visual-tour.md",
    "docs/demo-session.md",
    "docs/sample-report.md",
    "prompts/prompt-recipes.md",
    "Visual System Map",
    "Adaptive Typing Loop",
    "Evidence Ledger Flow",
    "Quality Gate Pipeline",
    "Trust Architecture",
    "make test",
    "Score: 35/35",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return int(width), int(height)


def check_required_files(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        checks.append(Check(f"file:{rel}", path.exists(), "required repository file exists"))
    return checks


def check_hero(root: Path) -> list[Check]:
    return check_png_asset(root, "docs/assets/mbti-typing-hero.png", "hero")


def check_journey_map(root: Path) -> list[Check]:
    return check_png_asset(root, "docs/assets/typing-journey-map.png", "journey")


def check_png_asset(root: Path, rel: str, prefix: str) -> list[Check]:
    path = root / rel
    checks: list[Check] = []
    try:
        width, height = png_size(path)
    except Exception as exc:
        return [Check(f"{prefix}:png", False, f"{rel} is readable PNG: {exc}")]

    ratio = width / height
    checks.append(Check(f"{prefix}:min_width", width >= 1200, f"width={width}"))
    checks.append(Check(f"{prefix}:min_height", height >= 650, f"height={height}"))
    checks.append(Check(f"{prefix}:wide_ratio", 1.55 <= ratio <= 1.95, f"ratio={ratio:.2f}"))
    return checks


def check_readme(root: Path) -> list[Check]:
    readme = read_text(root / "README.md")
    zh_readme = read_text(root / "README.zh-CN.md")
    mermaid_count = len(re.findall(r"```mermaid", readme))
    checks = [
        Check("readme:hero_image", "![MBTI Typing Skill hero]" in readme, "English README displays hero image"),
        Check("readme:journey_image", "![Typing journey map]" in readme, "English README displays journey image"),
        Check("readme:playground_link", "GitHub Pages playground" in readme and "docs/playground.html" in readme, "English README links hosted and local playground"),
        Check("readme:prompt_recipes", "Copy-paste prompt recipes" in readme, "English README links copy-paste recipes"),
        Check("readme:mermaid_count", mermaid_count >= 4, f"{mermaid_count} Mermaid diagrams found"),
        Check("readme:zh_hero", "docs/assets/mbti-typing-hero.png" in zh_readme, "Chinese README references hero image"),
        Check("readme:zh_journey", "docs/assets/typing-journey-map.png" in zh_readme, "Chinese README references journey image"),
    ]
    for term in README_REQUIRED_TERMS:
        checks.append(Check(f"readme:term:{term}", term in readme, "English README contains required UX/proof term"))
    return checks


def check_docs(root: Path) -> list[Check]:
    ux = read_text(root / "docs/github-ux.md")
    evaluation = read_text(root / "docs/evaluation.md")
    experience = read_text(root / "docs/experience-principles.md")
    visual = read_text(root / "docs/visual-tour.md")
    demo = read_text(root / "docs/demo-session.md")
    sample = read_text(root / "docs/sample-report.md")
    playground = read_text(root / "docs/playground.html")
    index = read_text(root / "docs/index.html")
    pages = read_text(root / ".github/workflows/pages.yml")
    return [
        Check("docs:ux_mermaid", "```mermaid" in ux, "GitHub UX document contains a visitor journey diagram"),
        Check("docs:evaluation_repo_gate", "repository_scorecard.py" in evaluation, "Evaluation docs mention repository scorecard"),
        Check("docs:experience_no_fake_certainty", "Fake certainty" in experience, "Experience docs reject manipulative certainty"),
        Check("docs:visual_images", "typing-journey-map.png" in visual and "mbti-typing-hero.png" in visual, "Visual tour references both bitmap assets"),
        Check("docs:demo_candidate_set", "Current working candidates" in demo and "Round 2: Targeted Duel" in demo, "Demo session shows candidate set and duel loop"),
        Check("docs:sample_falsifiers", "Falsifiers" in sample and "Why INTJ Remains Serious" in sample, "Sample report preserves runner-up and falsifiers"),
        Check("playground:title", "MBTI Typing Skill Playground" in playground, "Playground has a clear product title"),
        Check("playground:no_external_runtime", "https://" not in playground and "http://" not in playground and " src=" not in playground, "Playground has no external runtime dependency"),
        Check("playground:interactive_regions", all(term in playground for term in ("scenarioList", "candidateList", "evidenceList", "duelList", "promptOutput")), "Playground contains scenario, candidate, evidence, duel, and prompt regions"),
        Check("playground:copy_prompt", "navigator.clipboard.writeText" in playground and "Copy Prompt" in playground, "Playground can copy the generated prompt"),
        Check("playground:scenario_count", playground.count("Use $mbti-typing") >= 3, "Playground includes multiple live prompt starts"),
        Check("playground:safety_boundary", "not a clinical instrument" in playground, "Playground keeps safety boundary visible"),
        Check("pages:index_redirect", "playground.html" in index and "http-equiv=\"refresh\"" in index, "Docs index redirects to playground"),
        Check("pages:workflow", "actions/deploy-pages@v4" in pages and "path: docs" in pages, "GitHub Pages workflow deploys docs"),
    ]


def check_activation_assets(root: Path) -> list[Check]:
    prompts = read_text(root / "prompts/prompt-recipes.md")
    ledger = read_text(root / "examples/evidence-ledger-example.md")
    state = json.loads(read_text(root / "examples/session-state-example.json"))
    return [
        Check("activation:prompt_count", prompts.count("Use $mbti-typing") >= 6, "Prompt recipes include at least six copy-paste starts"),
        Check("activation:ledger_sections", "Candidate Set" in ledger and "Contradiction Gate" in ledger, "Evidence ledger example includes candidate and contradiction sections"),
        Check("activation:state_candidates", len(state.get("candidate_set", [])) >= 3, "Session state example starts from at least three candidates"),
        Check("activation:state_falsifiers", bool(state.get("falsifiers")), "Session state example includes falsifiers"),
    ]


def run(root: Path) -> int:
    checks: list[Check] = []
    checks.extend(check_required_files(root))
    checks.extend(check_hero(root))
    checks.extend(check_journey_map(root))
    checks.extend(check_readme(root))
    checks.extend(check_docs(root))
    checks.extend(check_activation_assets(root))

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Repository UX Score: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    return run(root.resolve())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
