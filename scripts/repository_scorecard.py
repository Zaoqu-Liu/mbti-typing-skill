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
    "docs/assets/repository-experience-map.svg",
    "docs/assets/typing-engine-blueprint.svg",
    "docs/assets/trust-loop-dashboard.svg",
    "docs/assets/benchmark-arena-pipeline.svg",
    "docs/evaluation.md",
    "docs/experience-principles.md",
    "docs/github-ux.md",
    "docs/visual-tour.md",
    "docs/demo-session.md",
    "docs/sample-report.md",
    "docs/session-lab.html",
    "docs/case-gallery.html",
    "docs/playground.html",
    "docs/index.html",
    "scripts/session_lab_audit.py",
    "scripts/sync_case_gallery.py",
    "scripts/case_gallery_audit.py",
    "skill/mbti-typing/SKILL.md",
]


README_REQUIRED_TERMS = [
    "docs/assets/mbti-typing-hero.png",
    "docs/assets/typing-journey-map.png",
    "docs/assets/repository-experience-map.svg",
    "docs/assets/typing-engine-blueprint.svg",
    "docs/assets/trust-loop-dashboard.svg",
    "docs/assets/benchmark-arena-pipeline.svg",
    "Session Lab",
    "https://zaoqu-liu.github.io/mbti-typing-skill/session-lab.html",
    "docs/session-lab.html",
    "local-first",
    "session state export",
    "share link",
    "Import JSON",
    "Benchmark Arena",
    "docs/case-gallery.html",
    "case gallery",
    "Interactive Playground",
    "https://zaoqu-liu.github.io/mbti-typing-skill/playground.html",
    "docs/playground.html",
    "One-Minute Demo",
    "Product Experience Blueprints",
    "GitHub Visitor Experience Map",
    "Typing Engine Blueprint",
    "Trust Loop Dashboard",
    "Benchmark Arena Pipeline",
    "source-of-truth sync",
    "scripts/sync_case_gallery.py",
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


def check_visual_blueprints(root: Path) -> list[Check]:
    checks: list[Check] = []
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/repository-experience-map.svg",
            "repo_experience_map",
            ("GitHub Visitor Experience Map", "Visitor intent", "First-run product path", "Proof and action"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/typing-engine-blueprint.svg",
            "typing_engine_blueprint",
            ("Typing Engine Blueprint", "Candidate universe", "Evidence", "Ledger", "Falsifier bank"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/trust-loop-dashboard.svg",
            "trust_loop_dashboard",
            ("Trust Loop Dashboard", "Live evidence intake", "Verification stack", "Release and community"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/benchmark-arena-pipeline.svg",
            "benchmark_arena_pipeline",
            ("Benchmark Arena Pipeline", "benchmark-cases.json", "sync_case_gallery.py", "case-gallery.html"),
        )
    )
    return checks


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


def check_svg_asset(root: Path, rel: str, prefix: str, required_terms: tuple[str, ...]) -> list[Check]:
    path = root / rel
    if not path.exists():
        return [Check(f"{prefix}:svg", False, f"{rel} exists")]

    svg = read_text(path)
    dependency_scan = svg.replace('xmlns="http://www.w3.org/2000/svg"', "")
    return [
        Check(f"{prefix}:svg", "<svg" in svg and "viewBox=" in svg, f"{rel} is an SVG with a viewBox"),
        Check(f"{prefix}:accessibility", 'role="img"' in svg and "<title" in svg and "<desc" in svg, f"{rel} has title, desc, and role"),
        Check(f"{prefix}:no_remote_or_script", "<script" not in dependency_scan and "http://" not in dependency_scan and "https://" not in dependency_scan, f"{rel} has no script or remote dependency"),
        Check(f"{prefix}:labels", all(term in svg for term in required_terms), f"{rel} contains expected product labels"),
    ]


def check_readme(root: Path) -> list[Check]:
    readme = read_text(root / "README.md")
    zh_readme = read_text(root / "README.zh-CN.md")
    mermaid_count = len(re.findall(r"```mermaid", readme))
    checks = [
        Check("readme:hero_image", "![MBTI Typing Skill hero]" in readme, "English README displays hero image"),
        Check("readme:journey_image", "![Typing journey map]" in readme, "English README displays journey image"),
        Check("readme:blueprint_images", all(asset in readme for asset in ("repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg")), "English README displays all blueprint visuals"),
        Check("readme:session_lab_link", "GitHub Pages Session Lab" in readme and "docs/session-lab.html" in readme, "English README links hosted and local Session Lab"),
        Check("readme:playground_link", "GitHub Pages playground" in readme and "docs/playground.html" in readme, "English README links hosted and local playground"),
        Check("readme:prompt_recipes", "Copy-paste prompt recipes" in readme, "English README links copy-paste recipes"),
        Check("readme:mermaid_count", mermaid_count >= 4, f"{mermaid_count} Mermaid diagrams found"),
        Check("readme:zh_hero", "docs/assets/mbti-typing-hero.png" in zh_readme, "Chinese README references hero image"),
        Check("readme:zh_journey", "docs/assets/typing-journey-map.png" in zh_readme, "Chinese README references journey image"),
        Check("readme:zh_blueprints", all(asset in zh_readme for asset in ("repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg")), "Chinese README references all blueprint visuals"),
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
    session_lab = read_text(root / "docs/session-lab.html")
    case_gallery = read_text(root / "docs/case-gallery.html")
    playground = read_text(root / "docs/playground.html")
    index = read_text(root / "docs/index.html")
    pages = read_text(root / ".github/workflows/pages.yml")
    makefile = read_text(root / "Makefile")
    session_lab_audit = read_text(root / "scripts/session_lab_audit.py")
    sync_case_gallery = read_text(root / "scripts/sync_case_gallery.py")
    case_gallery_audit = read_text(root / "scripts/case_gallery_audit.py")
    return [
        Check("docs:ux_mermaid", "```mermaid" in ux, "GitHub UX document contains a visitor journey diagram"),
        Check("docs:evaluation_repo_gate", "repository_scorecard.py" in evaluation, "Evaluation docs mention repository scorecard"),
        Check("docs:experience_no_fake_certainty", "Fake certainty" in experience, "Experience docs reject manipulative certainty"),
        Check("docs:ux_blueprint_rules", all(term in ux for term in ("repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg")), "GitHub UX document keeps blueprint visuals in the maintenance rules"),
        Check("docs:visual_images", all(term in visual for term in ("typing-journey-map.png", "mbti-typing-hero.png", "repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg")), "Visual tour references bitmap and blueprint assets"),
        Check("docs:evaluation_visual_gate", "repository-experience-map.svg" in evaluation and "benchmark-arena-pipeline.svg" in evaluation, "Evaluation docs describe the visual blueprint gate"),
        Check("docs:demo_candidate_set", "Current working candidates" in demo and "Round 2: Targeted Duel" in demo, "Demo session shows candidate set and duel loop"),
        Check("docs:sample_falsifiers", "Falsifiers" in sample and "Why INTJ Remains Serious" in sample, "Sample report preserves runner-up and falsifiers"),
        Check("session_lab:title", "MBTI Typing Skill Session Lab" in session_lab, "Session Lab has a clear product title"),
        Check("session_lab:no_external_runtime", "https://" not in session_lab and "http://" not in session_lab and " src=" not in session_lab, "Session Lab has no external runtime dependency"),
        Check("session_lab:interactive_regions", all(term in session_lab for term in ("claimInput", "evidenceInput", "candidateGrid", "ledgerTable", "duelGrid", "questionStack", "sessionStateOutput")), "Session Lab contains intake, candidate, ledger, duel, question, and state regions"),
        Check("session_lab:all_16_types", all(type_code in session_lab for type_code in ("INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP")), "Session Lab keeps all 16 types in the candidate universe"),
        Check("session_lab:mode_controls", session_lab.count("data-mode=") >= 4 and "modeSelector" in session_lab, "Session Lab exposes live, duel, transcript, and report modes"),
        Check("session_lab:evidence_signals", all(term in session_lab for term in ("SIGNALS", "supports", "weakens", "nextProbe")), "Session Lab generates evidence-ledger signals"),
        Check("session_lab:export_controls", "Copy Report" in session_lab and "Download JSON" in session_lab and "Copy Codex Prompt" in session_lab, "Session Lab exports report, prompt, and JSON"),
        Check("session_lab:share_controls", "Copy Share Link" in session_lab and "Import JSON" in session_lab, "Session Lab can share and import sessions"),
        Check("session_lab:hash_restore", "window.location.hash" in session_lab and "loadSessionFromHash" in session_lab, "Session Lab restores sessions from URL hash"),
        Check("session_lab:hashchange_restore", 'window.addEventListener("hashchange", loadSessionFromHash)' in session_lab, "Session Lab refreshes same-tab share links"),
        Check("session_lab:unicode_share", "TextEncoder" in session_lab and "TextDecoder" in session_lab, "Session Lab share links support unicode evidence"),
        Check("session_lab:persistence", "localStorage.setItem" in session_lab and "mbti-typing-session-lab-state" in session_lab, "Session Lab can persist local work"),
        Check("session_lab:safety_boundary", "not a clinical instrument" in session_lab and "not a psychometric result" in session_lab, "Session Lab keeps safety and uncertainty boundaries visible"),
        Check("session_lab:dom_safety", "textContent" in session_lab and "replaceChildren" in session_lab, "Session Lab avoids injecting user notes as HTML in core renderers"),
        Check("session_lab:download_json", "new Blob" in session_lab and "application/json" in session_lab, "Session Lab downloads structured JSON"),
        Check("session_lab:codex_prompt", "Use $mbti-typing" in session_lab and "generated_prompt" in session_lab, "Session Lab creates a reusable Codex prompt"),
        Check("session_lab:audit_script", "Session Lab Audit" in session_lab_audit and "Copy Share Link" in session_lab_audit, "Session Lab has a dedicated audit script"),
        Check("session_lab:audit_make_target", "session-lab-audit" in makefile and "scripts/session_lab_audit.py" in makefile, "Makefile runs Session Lab audit"),
        Check("case_gallery:title", "MBTI Typing Skill Benchmark Arena" in case_gallery, "Case Gallery has a clear product title"),
        Check("case_gallery:no_external_runtime", "<script src" not in case_gallery and " src=" not in case_gallery, "Case Gallery has no external runtime dependency"),
        Check("case_gallery:interactive_regions", all(term in case_gallery for term in ("filterRail", "caseGrid", "caseDetail", "promptOutput", "copyIssueSeed")), "Case Gallery contains filters, cases, detail, prompt, and issue seed regions"),
        Check("case_gallery:benchmark_cases", all(case_id in case_gallery for case_id in ("bench-entj-intj-001", "bench-intj-entj-002", "bench-infp-infj-003", "bench-infj-infp-004", "bench-estj-entj-005", "bench-entp-enfp-006", "bench-isfj-infj-007", "bench-estp-entp-008")), "Case Gallery exposes all current benchmark cases"),
        Check("case_gallery:source_markers", "BEGIN GENERATED BENCHMARK CASES" in case_gallery and "END GENERATED BENCHMARK CASES" in case_gallery, "Case Gallery marks generated benchmark data"),
        Check("case_gallery:source_sync_script", "Case Gallery Source Sync" in sync_case_gallery and "make_gallery_cases" in sync_case_gallery, "Case Gallery has a JSON source-of-truth sync script"),
        Check("case_gallery:source_sync_audit", "source:json_match" in case_gallery_audit and "make_gallery_cases" in case_gallery_audit, "Case Gallery audit compares embedded cases with canonical JSON"),
        Check("case_gallery:source_sync_make_target", "case-gallery-sync" in makefile and "scripts/sync_case_gallery.py" in makefile, "Makefile checks Case Gallery source sync"),
        Check("case_gallery:safety_boundary", "Not psychometric ground truth" in case_gallery and "not clinical or hiring instruments" in case_gallery, "Case Gallery keeps safety boundary visible"),
        Check("case_gallery:copy_prompt", "navigator.clipboard.writeText" in case_gallery and "Use $mbti-typing" in case_gallery, "Case Gallery can copy reusable prompts"),
        Check("case_gallery:dom_safety", "textContent" in case_gallery and "replaceChildren" in case_gallery and "innerHTML" not in case_gallery, "Case Gallery renders data without HTML injection"),
        Check("case_gallery:audit_script", "Case Gallery Audit" in case_gallery_audit and "Submit Benchmark Case" in case_gallery_audit, "Case Gallery has a dedicated audit script"),
        Check("case_gallery:audit_make_target", "case-gallery-audit" in makefile and "scripts/case_gallery_audit.py" in makefile, "Makefile runs Case Gallery audit"),
        Check("playground:title", "MBTI Typing Skill Playground" in playground, "Playground has a clear product title"),
        Check("playground:no_external_runtime", "https://" not in playground and "http://" not in playground and " src=" not in playground, "Playground has no external runtime dependency"),
        Check("playground:interactive_regions", all(term in playground for term in ("scenarioList", "candidateList", "evidenceList", "duelList", "promptOutput")), "Playground contains scenario, candidate, evidence, duel, and prompt regions"),
        Check("playground:copy_prompt", "navigator.clipboard.writeText" in playground and "Copy Prompt" in playground, "Playground can copy the generated prompt"),
        Check("playground:scenario_count", playground.count("Use $mbti-typing") >= 3, "Playground includes multiple live prompt starts"),
        Check("playground:safety_boundary", "not a clinical instrument" in playground, "Playground keeps safety boundary visible"),
        Check("pages:index_redirect", "session-lab.html" in index and "http-equiv=\"refresh\"" in index, "Docs index redirects to Session Lab"),
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
    checks.extend(check_visual_blueprints(root))
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
