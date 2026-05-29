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
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "CONVENTIONS.md",
    "opencode.json",
    ".rules",
    ".roomodes",
    ".aider.conf.yml",
    ".gemini/settings.json",
    "kilo.jsonc",
    ".amazonq/cli-agents/mbti-typing.json",
    ".claude/skills/mbti-typing/SKILL.md",
    ".claude/commands/mbti-type.md",
    ".cursor/rules/mbti-typing.mdc",
    ".github/copilot-instructions.md",
    ".github/instructions/mbti-typing.instructions.md",
    ".github/skills/mbti-typing/SKILL.md",
    ".cline/skills/mbti-typing/SKILL.md",
    ".clinerules/mbti-typing.md",
    ".continue/rules/mbti-typing.md",
    ".windsurf/rules/mbti-typing.md",
    ".roo/rules-mbti-typing/mbti-typing.md",
    ".kilo/rules/mbti-typing.md",
    ".junie/AGENTS.md",
    ".junie/commands/mbti-type.md",
    "gpts/mbti-typing-gpt-instructions.md",
    "agent-adapters/manifest.json",
    "agent-adapters/README.md",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/benchmark_case.yml",
    ".github/ISSUE_TEMPLATE/benchmark_replay_improvement.yml",
    ".github/ISSUE_TEMPLATE/calibration_result.yml",
    ".github/ISSUE_TEMPLATE/blind_review.yml",
    ".github/ISSUE_TEMPLATE/consented_followup.yml",
    ".github/ISSUE_TEMPLATE/type_duel_improvement.yml",
    ".github/ISSUE_TEMPLATE/question_improvement.yml",
    ".github/ISSUE_TEMPLATE/response_eval_improvement.yml",
    ".github/ISSUE_TEMPLATE/agent_adapter_improvement.yml",
    ".github/ISSUE_TEMPLATE/agent_portability_request.yml",
    "prompts/prompt-recipes.md",
    "examples/session-state-example.json",
    "examples/evidence-ledger-example.md",
    "examples/blind-review-matrix.json",
    "examples/consented-followup-packet.json",
    "examples/response-eval-cases.json",
    "docs/assets/mbti-typing-hero.png",
    "docs/assets/typing-journey-map.png",
    "docs/assets/social-preview.jpg",
    "docs/assets/response-eval-command-center.png",
    "docs/assets/experience-hub-route-map.svg",
    "docs/assets/repository-experience-map.svg",
    "docs/assets/typing-engine-blueprint.svg",
    "docs/assets/trust-loop-dashboard.svg",
    "docs/assets/benchmark-arena-pipeline.svg",
    "docs/assets/benchmark-replay-loop.svg",
    "docs/assets/type-coverage-matrix.svg",
    "docs/assets/calibration-loop-map.svg",
    "docs/assets/blind-review-arena.svg",
    "docs/assets/consent-feedback-loop.svg",
    "docs/assets/type-duel-decision-map.svg",
    "docs/assets/adaptive-question-loop.svg",
    "docs/assets/agent-adapter-matrix.svg",
    "docs/assets/agent-compatibility-grid.svg",
    "docs/assets/agent-pack-export-flow.svg",
    "docs/assets/agent-adapter-lab-flow.svg",
    "docs/assets/universal-agent-bridge-map.svg",
    "docs/assets/response-quality-radar.svg",
    "docs/assets/response-eval-lab-flow.svg",
    "docs/evaluation.md",
    "docs/experience-principles.md",
    "docs/github-ux.md",
    "docs/visual-tour.md",
    "docs/agent-adapters.md",
    "docs/blind-review-protocol.md",
    "docs/consent-redaction-protocol.md",
    "docs/demo-session.md",
    "docs/sample-report.md",
    "docs/session-lab.html",
    "docs/case-gallery.html",
    "docs/benchmark-replay-lab.html",
    "docs/calibration-lab.html",
    "docs/question-lab.html",
    "docs/type-duel-lab.html",
    "docs/agent-adapter-lab.html",
    "docs/agent-portability-lab.html",
    "docs/follow-up-lab.html",
    "docs/response-eval-lab.html",
    "docs/playground.html",
    "docs/index.html",
    "scripts/session_lab_audit.py",
    "scripts/sync_case_gallery.py",
    "scripts/case_gallery_audit.py",
    "scripts/sync_benchmark_replay_lab.py",
    "scripts/benchmark_replay_lab_audit.py",
    "scripts/sync_calibration_lab.py",
    "scripts/calibration_lab_audit.py",
    "scripts/blind_review_audit.py",
    "scripts/consent_redaction_audit.py",
    "scripts/sync_question_lab.py",
    "scripts/question_lab_audit.py",
    "scripts/sync_type_duel_lab.py",
    "scripts/type_duel_lab_audit.py",
    "scripts/follow_up_lab_audit.py",
    "scripts/index_hub_audit.py",
    "scripts/response_eval_lab_audit.py",
    "scripts/agent_adapter_audit.py",
    "scripts/export_agent_pack.py",
    "scripts/agent_pack_export_audit.py",
    "scripts/sync_agent_adapter_lab.py",
    "scripts/agent_adapter_lab_audit.py",
    "scripts/sync_agent_portability_lab.py",
    "scripts/agent_portability_lab_audit.py",
    "scripts/response_eval_audit.py",
    "skill/mbti-typing/SKILL.md",
]


README_REQUIRED_TERMS = [
    "docs/assets/mbti-typing-hero.png",
    "docs/assets/typing-journey-map.png",
    "docs/assets/social-preview.jpg",
    "docs/assets/response-eval-command-center.png",
    "docs/assets/experience-hub-route-map.svg",
    "docs/assets/repository-experience-map.svg",
    "docs/assets/typing-engine-blueprint.svg",
    "docs/assets/trust-loop-dashboard.svg",
    "docs/assets/benchmark-arena-pipeline.svg",
    "docs/assets/benchmark-replay-loop.svg",
    "docs/assets/type-coverage-matrix.svg",
    "docs/assets/calibration-loop-map.svg",
    "docs/assets/blind-review-arena.svg",
    "docs/assets/consent-feedback-loop.svg",
    "docs/assets/type-duel-decision-map.svg",
    "docs/assets/adaptive-question-loop.svg",
    "docs/assets/agent-adapter-matrix.svg",
    "docs/assets/agent-compatibility-grid.svg",
    "docs/assets/agent-pack-export-flow.svg",
    "docs/assets/agent-adapter-lab-flow.svg",
    "docs/assets/universal-agent-bridge-map.svg",
    "docs/assets/response-quality-radar.svg",
    "docs/assets/response-eval-lab-flow.svg",
    "GitHub social preview",
    "Response Eval Command Center",
    "Experience Hub Route Map",
    "Agent Adapter Matrix",
    "Agent Compatibility Grid",
    "Agent Pack Export Flow",
    "Agent Adapter Lab Flow",
    "Universal Agent Bridge Map",
    "Response Quality Radar",
    "Response Eval Lab Flow",
    "docs/agent-adapters.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "CONVENTIONS.md",
    ".aider.conf.yml",
    ".gemini/settings.json",
    ".rules",
    ".roomodes",
    "kilo.jsonc",
    ".amazonq/cli-agents/mbti-typing.json",
    ".roo/rules-mbti-typing/mbti-typing.md",
    ".kilo/rules/mbti-typing.md",
    ".junie/AGENTS.md",
    ".junie/commands/mbti-type.md",
    "gpts/mbti-typing-gpt-instructions.md",
    "ChatGPT GPTs",
    "Zed Agent Panel",
    "Devin",
    "JetBrains Junie",
    "Amazon Q Developer CLI",
    "Roo Code",
    "Kilo Code",
    "Claude Code",
    ".claude/skills/mbti-typing/SKILL.md",
    ".claude/commands/mbti-type.md",
    "Cursor",
    ".cursor/rules/mbti-typing.mdc",
    "opencode",
    "opencode.json",
    "Gemini CLI",
    "GitHub Copilot",
    ".github/copilot-instructions.md",
    ".github/instructions/mbti-typing.instructions.md",
    ".github/skills/mbti-typing/SKILL.md",
    "Windsurf",
    ".windsurf/rules/mbti-typing.md",
    "Cline",
    ".cline/skills/mbti-typing/SKILL.md",
    ".clinerules/mbti-typing.md",
    "Continue",
    ".continue/rules/mbti-typing.md",
    "aider",
    "agent-adapters/manifest.json",
    "scripts/agent_adapter_audit.py",
    "scripts/export_agent_pack.py",
    "scripts/agent_pack_export_audit.py",
    "scripts/sync_agent_adapter_lab.py",
    "scripts/agent_adapter_lab_audit.py",
    "scripts/sync_agent_portability_lab.py",
    "scripts/agent_portability_lab_audit.py",
    "scripts/response_eval_audit.py",
    "Agent Adapter Lab",
    "Agent Adapter Lab Audit",
    "docs/agent-adapter-lab.html",
    "https://zaoqu-liu.github.io/mbti-typing-skill/agent-adapter-lab.html",
    "agent_adapter_improvement.yml",
    "Agent Portability Lab",
    "Universal Agent Bridge",
    "docs/agent-portability-lab.html",
    "https://zaoqu-liu.github.io/mbti-typing-skill/agent-portability-lab.html",
    "agent_portability_request.yml",
    "agent-portability-lab/v1",
    "capability-first",
    "unknown host",
    "AGENT_PACK_MANIFEST.json",
    "Agent Adapter Audit",
    "Agent Pack Export Audit",
    "Response Eval Audit",
    "Response Eval Lab",
    "Response Eval Lab Audit",
    "examples/response-eval-cases.json",
    "docs/response-eval-lab.html",
    "https://zaoqu-liu.github.io/mbti-typing-skill/response-eval-lab.html",
    "scripts/response_eval_lab_audit.py",
    "response_eval_improvement.yml",
    "sticky precision",
    "negative_blocked",
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
    "Calibration Lab",
    "https://zaoqu-liu.github.io/mbti-typing-skill/calibration-lab.html",
    "docs/calibration-lab.html",
    "Follow-Up Lab",
    "https://zaoqu-liu.github.io/mbti-typing-skill/follow-up-lab.html",
    "docs/follow-up-lab.html",
    "Question Lab",
    "https://zaoqu-liu.github.io/mbti-typing-skill/question-lab.html",
    "docs/question-lab.html",
    "Type Duel Lab",
    "https://zaoqu-liu.github.io/mbti-typing-skill/type-duel-lab.html",
    "docs/type-duel-lab.html",
    "Blind Review Protocol",
    "docs/blind-review-protocol.md",
    "Blind Review Arena",
    "examples/blind-review-matrix.json",
    "Consent Redaction Protocol",
    "docs/consent-redaction-protocol.md",
    "Consent Feedback Loop",
    "examples/consented-followup-packet.json",
    "scripts/consent_redaction_audit.py",
    "scripts/sync_question_lab.py",
    "scripts/question_lab_audit.py",
    "scripts/sync_type_duel_lab.py",
    "scripts/type_duel_lab_audit.py",
    "scripts/follow_up_lab_audit.py",
    "type_duel_improvement.yml",
    "question_improvement.yml",
    "Interactive Playground",
    "https://zaoqu-liu.github.io/mbti-typing-skill/playground.html",
    "docs/playground.html",
    "One-Minute Demo",
    "Experience Hub",
    "docs/index.html",
    "https://zaoqu-liu.github.io/mbti-typing-skill/",
    "scripts/index_hub_audit.py",
    "Index Hub Audit",
    "Product Experience Blueprints",
    "GitHub Visitor Experience Map",
    "Typing Engine Blueprint",
    "Trust Loop Dashboard",
    "Benchmark Arena Pipeline",
    "Benchmark Replay Loop",
    "Benchmark Replay Lab",
    "docs/benchmark-replay-lab.html",
    "https://zaoqu-liu.github.io/mbti-typing-skill/benchmark-replay-lab.html",
    "Replay Receipt",
    "benchmark_replay_improvement.yml",
    "scripts/sync_benchmark_replay_lab.py",
    "scripts/benchmark_replay_lab_audit.py",
    "Benchmark Type Coverage Matrix",
    "16 / 16 covered",
    "Calibration Loop Map",
    "Blind Review Arena",
    "Adaptive Question Loop",
    "Type Duel Decision Map",
    "source-of-truth sync",
    "scripts/sync_case_gallery.py",
    "scripts/sync_calibration_lab.py",
    "scripts/blind_review_audit.py",
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


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG file")
    index = 2
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while index < len(data):
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(data):
            break
        length = struct.unpack(">H", data[index : index + 2])[0]
        if length < 2 or index + length > len(data):
            raise ValueError("invalid JPEG segment length")
        if marker in sof_markers:
            if length < 7:
                raise ValueError("invalid JPEG SOF segment")
            height, width = struct.unpack(">HH", data[index + 3 : index + 7])
            return int(width), int(height)
        index += length
    raise ValueError("JPEG dimensions not found")


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


def check_social_preview(root: Path) -> list[Check]:
    return check_jpeg_asset(root, "docs/assets/social-preview.jpg", "social_preview")


def check_response_eval_command_center(root: Path) -> list[Check]:
    return check_png_asset(root, "docs/assets/response-eval-command-center.png", "response_eval_command_center")


def check_visual_blueprints(root: Path) -> list[Check]:
    checks: list[Check] = []
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/experience-hub-route-map.svg",
            "experience_hub_route_map",
            ("Experience Hub Route Map", "MBTI Typing Skill Experience Hub", "Start typing", "Install or adapt", "Session Lab", "Type Duel Lab", "Response Eval Lab", "Benchmark Replay", "Follow-Up", "User-facing proof", "Contribution routes", "Release gate", "scripts/index_hub_audit.py", "repository_scorecard.py", "candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary"),
        )
    )
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
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/benchmark-replay-loop.svg",
            "benchmark_replay_loop",
            ("Benchmark Replay Loop", "benchmark-replay-lab.html", "sync_benchmark_replay_lab.py", "benchmark_replay_lab_audit.py", "Replay Receipt", "Blind Prompt", "Reveal Reference", "Repair Prompt", "benchmark_replay_improvement.yml", "local-first"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/type-coverage-matrix.svg",
            "type_coverage_matrix",
            ("Benchmark Type Coverage Matrix", "16 / 16 covered", "bench-enfp-entp-016", "bench-istp-intp-011"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/calibration-loop-map.svg",
            "calibration_loop_map",
            ("Calibration Loop Map", "Blind Calibration Loop", "Repair Prompt", "Issue Seed"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/blind-review-arena.svg",
            "blind_review_arena",
            ("Blind Review Arena", "Sanitized Packet", "Aggregate Metrics", "Top-2 Matters"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/consent-feedback-loop.svg",
            "consent_feedback_loop",
            ("Consent Feedback Loop", "Consent", "Redaction", "Consent Redaction Audit"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/type-duel-decision-map.svg",
            "type_duel_decision_map",
            ("Type Duel Decision Map", "pair-duels.md", "type-duel-lab.html", "type_duel_lab_audit.py"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/adaptive-question-loop.svg",
            "adaptive_question_loop",
            ("Adaptive Question Loop", "question-bank.md", "question-lab.html", "question_lab_audit.py"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/agent-adapter-matrix.svg",
            "agent_adapter_matrix",
            ("Agent Adapter Matrix", "Codex", "Claude Code", "Cursor", "opencode", "AGENTS.md", ".claude/skills", ".cursor/rules", "opencode.json", "agent_adapter_audit.py"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/agent-compatibility-grid.svg",
            "agent_compatibility_grid",
            ("Agent Compatibility Grid", "18 adapters", "one protocol", "ChatGPT GPTs", "Zed", "Devin", "Gemini CLI", "GitHub Copilot", "Windsurf", "Cline", "Continue", "aider", "JetBrains Junie", "Amazon Q", "Roo Code", "Kilo Code", "agent_adapter_audit.py"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/agent-pack-export-flow.svg",
            "agent_pack_export_flow",
            ("Agent Pack Export Flow", "scripts/export_agent_pack.py", "agent-adapters/manifest.json", "AGENT_PACK_MANIFEST.json", "scripts/agent_pack_export_audit.py", "make test", "Target Repo"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/agent-adapter-lab-flow.svg",
            "agent_adapter_lab_flow",
            ("Agent Adapter Lab Flow", "agent-adapters/manifest.json", "Target selector", "Pack command", "AGENT_PACK_MANIFEST.json", "scripts/export_agent_pack.py", "scripts/agent_adapter_lab_audit.py", "agent_adapter_improvement.yml", "18 adapters", "one protocol"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/universal-agent-bridge-map.svg",
            "universal_agent_bridge_map",
            ("Universal Agent Bridge Map", "Known host catalog", "Unknown host intake", "Agent Portability Lab", "agent-portability-lab/v1", "sync_agent_portability_lab.py", "agent_portability_lab_audit.py", "agent_portability_request.yml", "candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/response-quality-radar.svg",
            "response_quality_radar",
            ("Response Quality Radar", "examples/response-eval-cases.json", "scripts/response_eval_audit.py", "candidate set", "runner-up", "falsifier", "Anti-Flattery", "make test"),
        )
    )
    checks.extend(
        check_svg_asset(
            root,
            "docs/assets/response-eval-lab-flow.svg",
            "response_eval_lab_flow",
            ("Response Eval Lab Flow", "Paste answer", "Mode-aware gates", "Quality radar", "JSON receipt", "Repair prompt", "response_eval_improvement.yml", "scripts/response_eval_lab_audit.py", "local-first", "Sticky precision"),
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


def check_jpeg_asset(root: Path, rel: str, prefix: str) -> list[Check]:
    path = root / rel
    checks: list[Check] = []
    try:
        width, height = jpeg_size(path)
    except Exception as exc:
        return [Check(f"{prefix}:jpeg", False, f"{rel} is readable JPEG: {exc}")]

    ratio = width / height
    checks.append(Check(f"{prefix}:min_width", width >= 1200, f"width={width}"))
    checks.append(Check(f"{prefix}:min_height", height >= 630, f"height={height}"))
    checks.append(Check(f"{prefix}:wide_ratio", 1.70 <= ratio <= 1.90, f"ratio={ratio:.2f}"))
    checks.append(Check(f"{prefix}:social_size", path.stat().st_size <= 1_000_000, f"bytes={path.stat().st_size}"))
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
        Check("readme:blueprint_images", all(asset in readme for asset in ("experience-hub-route-map.svg", "repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg", "benchmark-replay-loop.svg", "type-coverage-matrix.svg", "calibration-loop-map.svg", "blind-review-arena.svg", "consent-feedback-loop.svg", "type-duel-decision-map.svg", "adaptive-question-loop.svg", "agent-adapter-matrix.svg", "agent-compatibility-grid.svg", "agent-pack-export-flow.svg", "agent-adapter-lab-flow.svg", "universal-agent-bridge-map.svg", "response-quality-radar.svg", "response-eval-lab-flow.svg")), "English README displays all blueprint visuals"),
        Check("readme:session_lab_link", "GitHub Pages Session Lab" in readme and "docs/session-lab.html" in readme, "English README links hosted and local Session Lab"),
        Check("readme:question_lab_link", "GitHub Pages Question Lab" in readme and "docs/question-lab.html" in readme, "English README links hosted and local Question Lab"),
        Check("readme:type_duel_lab_link", "GitHub Pages Type Duel Lab" in readme and "docs/type-duel-lab.html" in readme, "English README links hosted and local Type Duel Lab"),
        Check("readme:agent_adapter_lab_link", "GitHub Pages Agent Adapter Lab" in readme and "docs/agent-adapter-lab.html" in readme, "English README links hosted and local Agent Adapter Lab"),
        Check("readme:agent_portability_lab_link", "GitHub Pages Agent Portability Lab" in readme and "docs/agent-portability-lab.html" in readme, "English README links hosted and local Agent Portability Lab"),
        Check("readme:follow_up_lab_link", "GitHub Pages Follow-Up Lab" in readme and "docs/follow-up-lab.html" in readme, "English README links hosted and local Follow-Up Lab"),
        Check("readme:response_eval_lab_link", "GitHub Pages Response Eval Lab" in readme and "docs/response-eval-lab.html" in readme, "English README links hosted and local Response Eval Lab"),
        Check("readme:playground_link", "GitHub Pages playground" in readme and "docs/playground.html" in readme, "English README links hosted and local playground"),
        Check("readme:prompt_recipes", "Copy-paste prompt recipes" in readme, "English README links copy-paste recipes"),
        Check("readme:mermaid_count", mermaid_count >= 4, f"{mermaid_count} Mermaid diagrams found"),
        Check("readme:zh_hero", "docs/assets/mbti-typing-hero.png" in zh_readme, "Chinese README references hero image"),
        Check("readme:zh_journey", "docs/assets/typing-journey-map.png" in zh_readme, "Chinese README references journey image"),
        Check("readme:zh_social_preview", "docs/assets/social-preview.jpg" in zh_readme, "Chinese README references social preview asset"),
        Check("readme:zh_response_eval_command_center", "docs/assets/response-eval-command-center.png" in zh_readme, "Chinese README references Response Eval command center"),
        Check("readme:zh_blueprints", all(asset in zh_readme for asset in ("experience-hub-route-map.svg", "repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg", "benchmark-replay-loop.svg", "type-coverage-matrix.svg", "calibration-loop-map.svg", "blind-review-arena.svg", "consent-feedback-loop.svg", "type-duel-decision-map.svg", "adaptive-question-loop.svg", "agent-adapter-matrix.svg", "agent-compatibility-grid.svg", "agent-pack-export-flow.svg", "agent-adapter-lab-flow.svg", "universal-agent-bridge-map.svg", "response-quality-radar.svg", "response-eval-lab-flow.svg")), "Chinese README references all blueprint visuals"),
    ]
    for term in README_REQUIRED_TERMS:
        checks.append(Check(f"readme:term:{term}", term in readme, "English README contains required UX/proof term"))
    return checks


def check_docs(root: Path) -> list[Check]:
    ux = read_text(root / "docs/github-ux.md")
    evaluation = read_text(root / "docs/evaluation.md")
    experience = read_text(root / "docs/experience-principles.md")
    visual = read_text(root / "docs/visual-tour.md")
    agent_adapters_doc = read_text(root / "docs/agent-adapters.md")
    agent_adapters_readme = read_text(root / "agent-adapters/README.md")
    agent_manifest = json.loads(read_text(root / "agent-adapters/manifest.json"))
    root_agents = read_text(root / "AGENTS.md")
    claude_root = read_text(root / "CLAUDE.md")
    gemini_root = read_text(root / "GEMINI.md")
    conventions = read_text(root / "CONVENTIONS.md")
    opencode_config = json.loads(read_text(root / "opencode.json"))
    gemini_config = json.loads(read_text(root / ".gemini/settings.json"))
    aider_config = read_text(root / ".aider.conf.yml")
    claude_skill = read_text(root / ".claude/skills/mbti-typing/SKILL.md")
    claude_command = read_text(root / ".claude/commands/mbti-type.md")
    cursor_rule = read_text(root / ".cursor/rules/mbti-typing.mdc")
    github_copilot = read_text(root / ".github/copilot-instructions.md")
    github_instructions = read_text(root / ".github/instructions/mbti-typing.instructions.md")
    github_skill = read_text(root / ".github/skills/mbti-typing/SKILL.md")
    cline_skill = read_text(root / ".cline/skills/mbti-typing/SKILL.md")
    cline_rule = read_text(root / ".clinerules/mbti-typing.md")
    continue_rule = read_text(root / ".continue/rules/mbti-typing.md")
    windsurf_rule = read_text(root / ".windsurf/rules/mbti-typing.md")
    blind_review = read_text(root / "docs/blind-review-protocol.md")
    consent_protocol = read_text(root / "docs/consent-redaction-protocol.md")
    demo = read_text(root / "docs/demo-session.md")
    sample = read_text(root / "docs/sample-report.md")
    session_lab = read_text(root / "docs/session-lab.html")
    case_gallery = read_text(root / "docs/case-gallery.html")
    benchmark_replay_lab = read_text(root / "docs/benchmark-replay-lab.html")
    calibration_lab = read_text(root / "docs/calibration-lab.html")
    question_lab = read_text(root / "docs/question-lab.html")
    type_duel_lab = read_text(root / "docs/type-duel-lab.html")
    agent_adapter_lab = read_text(root / "docs/agent-adapter-lab.html")
    agent_portability_lab = read_text(root / "docs/agent-portability-lab.html")
    follow_up_lab = read_text(root / "docs/follow-up-lab.html")
    response_eval_lab = read_text(root / "docs/response-eval-lab.html")
    playground = read_text(root / "docs/playground.html")
    index = read_text(root / "docs/index.html")
    pages = read_text(root / ".github/workflows/pages.yml")
    makefile = read_text(root / "Makefile")
    session_lab_audit = read_text(root / "scripts/session_lab_audit.py")
    sync_case_gallery = read_text(root / "scripts/sync_case_gallery.py")
    case_gallery_audit = read_text(root / "scripts/case_gallery_audit.py")
    sync_benchmark_replay_lab = read_text(root / "scripts/sync_benchmark_replay_lab.py")
    benchmark_replay_lab_audit = read_text(root / "scripts/benchmark_replay_lab_audit.py")
    sync_calibration_lab = read_text(root / "scripts/sync_calibration_lab.py")
    calibration_lab_audit = read_text(root / "scripts/calibration_lab_audit.py")
    sync_question_lab = read_text(root / "scripts/sync_question_lab.py")
    question_lab_audit = read_text(root / "scripts/question_lab_audit.py")
    sync_type_duel_lab = read_text(root / "scripts/sync_type_duel_lab.py")
    type_duel_lab_audit = read_text(root / "scripts/type_duel_lab_audit.py")
    sync_agent_adapter_lab = read_text(root / "scripts/sync_agent_adapter_lab.py")
    agent_adapter_lab_audit = read_text(root / "scripts/agent_adapter_lab_audit.py")
    sync_agent_portability_lab = read_text(root / "scripts/sync_agent_portability_lab.py")
    agent_portability_lab_audit = read_text(root / "scripts/agent_portability_lab_audit.py")
    blind_review_audit = read_text(root / "scripts/blind_review_audit.py")
    consent_redaction_audit = read_text(root / "scripts/consent_redaction_audit.py")
    follow_up_lab_audit = read_text(root / "scripts/follow_up_lab_audit.py")
    response_eval_lab_audit = read_text(root / "scripts/response_eval_lab_audit.py")
    index_hub_audit = read_text(root / "scripts/index_hub_audit.py")
    agent_adapter_audit = read_text(root / "scripts/agent_adapter_audit.py")
    export_agent_pack = read_text(root / "scripts/export_agent_pack.py")
    agent_pack_export_audit = read_text(root / "scripts/agent_pack_export_audit.py")
    agent_adapter_issue_template = read_text(root / ".github/ISSUE_TEMPLATE/agent_adapter_improvement.yml")
    agent_portability_issue_template = read_text(root / ".github/ISSUE_TEMPLATE/agent_portability_request.yml")
    benchmark_replay_issue_template = read_text(root / ".github/ISSUE_TEMPLATE/benchmark_replay_improvement.yml")
    response_eval_audit = read_text(root / "scripts/response_eval_audit.py")
    response_eval_payload = json.loads(read_text(root / "examples/response-eval-cases.json"))
    question_bank = read_text(root / "skill/mbti-typing/references/question-bank.md")
    pair_duels = read_text(root / "skill/mbti-typing/references/pair-duels.md")
    benchmark_payload = json.loads(read_text(root / "skill/mbti-typing/examples/benchmark-cases.json"))
    benchmark_cases = [case for case in benchmark_payload.get("cases", []) if isinstance(case, dict)]
    benchmark_ids = [str(case.get("id")) for case in benchmark_cases]
    leading_types = {str(case.get("expected_leading")) for case in benchmark_cases}
    required_types = {"ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP", "INTJ", "INFJ", "ENTJ", "ENFJ", "INTP", "INFP", "ENTP", "ENFP"}
    question_headings = re.findall(r"^### (.+)$", question_bank, flags=re.MULTILINE)
    duel_pairs = re.findall(r"^### ([A-Z]{4} vs [A-Z]{4})$", pair_duels, flags=re.MULTILINE)
    return [
        Check("docs:ux_mermaid", "```mermaid" in ux, "GitHub UX document contains a visitor journey diagram"),
        Check("docs:evaluation_repo_gate", "repository_scorecard.py" in evaluation, "Evaluation docs mention repository scorecard"),
        Check("docs:experience_no_fake_certainty", "Fake certainty" in experience, "Experience docs reject manipulative certainty"),
        Check("docs:ux_blueprint_rules", all(term in ux for term in ("experience-hub-route-map.svg", "repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg", "benchmark-replay-loop.svg", "type-coverage-matrix.svg", "calibration-loop-map.svg", "blind-review-arena.svg", "consent-feedback-loop.svg", "type-duel-decision-map.svg", "adaptive-question-loop.svg", "agent-adapter-matrix.svg", "agent-compatibility-grid.svg", "agent-pack-export-flow.svg", "agent-adapter-lab-flow.svg", "universal-agent-bridge-map.svg", "response-quality-radar.svg", "response-eval-lab-flow.svg")), "GitHub UX document keeps blueprint visuals in the maintenance rules"),
        Check("docs:ux_social_preview", "GitHub social preview" in ux and "social-preview.jpg" in ux, "GitHub UX document keeps the social preview asset visible"),
        Check("docs:visual_images", all(term in visual for term in ("typing-journey-map.png", "mbti-typing-hero.png", "social-preview.jpg", "response-eval-command-center.png", "experience-hub-route-map.svg", "repository-experience-map.svg", "typing-engine-blueprint.svg", "trust-loop-dashboard.svg", "benchmark-arena-pipeline.svg", "benchmark-replay-loop.svg", "type-coverage-matrix.svg", "calibration-loop-map.svg", "blind-review-arena.svg", "consent-feedback-loop.svg", "type-duel-decision-map.svg", "adaptive-question-loop.svg", "agent-adapter-matrix.svg", "agent-compatibility-grid.svg", "agent-pack-export-flow.svg", "agent-adapter-lab-flow.svg", "universal-agent-bridge-map.svg", "response-quality-radar.svg", "response-eval-lab-flow.svg")), "Visual tour references bitmap, social preview, and blueprint assets"),
        Check("docs:evaluation_visual_gate", "experience-hub-route-map.svg" in evaluation and "repository-experience-map.svg" in evaluation and "benchmark-replay-loop.svg" in evaluation and "blind-review-arena.svg" in evaluation and "consent-feedback-loop.svg" in evaluation and "type-duel-decision-map.svg" in evaluation and "adaptive-question-loop.svg" in evaluation and "agent-adapter-matrix.svg" in evaluation and "agent-compatibility-grid.svg" in evaluation and "agent-pack-export-flow.svg" in evaluation and "agent-adapter-lab-flow.svg" in evaluation and "universal-agent-bridge-map.svg" in evaluation and "response-quality-radar.svg" in evaluation and "response-eval-lab-flow.svg" in evaluation, "Evaluation docs describe the visual blueprint gate"),
        Check("docs:evaluation_response_eval", all(term in evaluation for term in ("Response Eval Audit", "Response Eval Lab Audit", "examples/response-eval-cases.json", "scripts/response_eval_audit.py", "scripts/response_eval_lab_audit.py", "sticky precision", "negative_blocked")), "Evaluation docs describe the response quality audit layer"),
        Check("docs:experience_response_quality_loop", all(term in experience for term in ("Response Quality Loop", "response-eval-cases.json", "Response Eval Audit", "candidate set", "Anti-Flattery")), "Experience docs define the response quality loop"),
        Check("docs:experience_universal_agent_bridge_loop", all(term in experience for term in ("Universal Agent Bridge Loop", "Agent Portability Lab", "agent-portability-lab/v1", "agent_portability_request.yml", "capability-first")), "Experience docs define the future-host portability loop"),
        Check("docs:experience_hub_loop", all(term in experience for term in ("Experience Hub Loop", "docs/index.html", "Index Hub Audit", "Experience Hub Route Map", "starter prompt")), "Experience docs define the Pages root route loop"),
        Check("agent_adapters:manifest_targets", sorted(target.get("id") for target in agent_manifest.get("targets", [])) == ["aider", "amazon-q", "chatgpt-gpts", "claude-code", "cline", "codex", "continue", "cursor", "devin", "gemini-cli", "generic-agents-md", "github-copilot", "jetbrains-junie", "kilo-code", "opencode", "roo-code", "windsurf", "zed"], "Agent adapter manifest covers eighteen mainstream target entrypoints"),
        Check("agent_adapters:manifest_pack_export", agent_manifest.get("pack_exporter") == "scripts/export_agent_pack.py" and agent_manifest.get("pack_audit") == "scripts/agent_pack_export_audit.py", "Agent adapter manifest points to pack export gates"),
        Check("agent_adapters:root_contract", all(term in root_agents for term in ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifiers", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Root AGENTS.md preserves the portable typing contract"),
        Check("agent_adapters:root_contexts", all(term in claude_root + gemini_root + conventions for term in ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "CLAUDE.md, GEMINI.md, and CONVENTIONS.md preserve the portable contract"),
        Check("agent_adapters:claude_code", all(term in claude_skill + claude_command for term in ("name: mbti-typing", "$ARGUMENTS", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Claude Code skill and command preserve invocation and safety terms"),
        Check("agent_adapters:cursor", all(term in cursor_rule for term in ("description:", '"**/*"', "alwaysApply: false", "skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifiers", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Cursor MDC rule preserves source references and safety terms"),
        Check("agent_adapters:opencode", all(term in opencode_config.get("instructions", []) for term in ("AGENTS.md", "agent-adapters/README.md", "skill/mbti-typing/SKILL.md")), "opencode.json aggregates the portable instruction files"),
        Check("agent_adapters:gemini", all(term in gemini_config.get("context", {}).get("fileName", []) for term in ("AGENTS.md", "GEMINI.md")) and "@./AGENTS.md" in gemini_root, "Gemini CLI context imports shared instructions"),
        Check("agent_adapters:github_copilot", all(term in github_copilot + github_instructions + github_skill for term in ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")) and 'applyTo: "**/*"' in github_instructions, "GitHub Copilot instructions and skill preserve source references and safety terms"),
        Check("agent_adapters:windsurf", all(term in windsurf_rule for term in ("trigger: model_decision", "skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Windsurf rule preserves activation, source references, and safety terms"),
        Check("agent_adapters:cline", all(term in cline_skill + cline_rule for term in ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Cline skill and rule preserve source references and safety terms"),
        Check("agent_adapters:continue", all(term in continue_rule for term in ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifier", "clinical", "hiring", "legal", "medical", "financial", "deterministic")), "Continue rule preserves source references and safety terms"),
        Check("agent_adapters:aider", "CONVENTIONS.md" in aider_config and "AGENTS.md" in aider_config and "skill/mbti-typing/SKILL.md" in conventions, "aider config reads portable conventions"),
        Check("agent_adapters:audit_script", "Agent Adapter Audit" in agent_adapter_audit and "EXPECTED_TARGETS" in agent_adapter_audit, "Agent adapters have a dedicated audit script"),
        Check("agent_adapters:audit_make_target", "agent-adapter-audit" in makefile and "scripts/agent_adapter_audit.py" in makefile, "Makefile runs Agent Adapter audit"),
        Check("agent_adapters:pack_exporter", all(term in export_agent_pack for term in ("PACK_SCHEMA", "BASELINE_PATHS", "AGENT_PACK_MANIFEST.json", "destination is not empty")), "Agent pack exporter has schema, baseline, receipt, and write guard"),
        Check("agent_adapters:pack_audit_script", all(term in agent_pack_export_audit for term in ("Agent Pack Export Audit", "dry_run", "all_export", "selective_export", "unknown_target")), "Agent pack export has a dedicated audit script"),
        Check("agent_adapters:pack_audit_make_target", "agent-pack-export-audit" in makefile and "scripts/agent_pack_export_audit.py" in makefile, "Makefile runs Agent Pack Export audit"),
        Check("agent_adapter_lab:title", "MBTI Typing Skill Agent Adapter Lab" in agent_adapter_lab, "Agent Adapter Lab has a clear product title"),
        Check("agent_adapter_lab:no_external_runtime", "<script src" not in agent_adapter_lab and " src=" not in agent_adapter_lab, "Agent Adapter Lab has no external runtime dependency"),
        Check("agent_adapter_lab:interactive_regions", all(term in agent_adapter_lab for term in ("targetSearch", "supportFilter", "targetList", "packCommandOutput", "installChecklistOutput", "adapterReceiptOutput", "issueSeedOutput")), "Agent Adapter Lab contains selector, command, checklist, receipt, and issue seed regions"),
        Check("agent_adapter_lab:source_markers", "BEGIN GENERATED AGENT ADAPTER MANIFEST" in agent_adapter_lab and "END GENERATED AGENT ADAPTER MANIFEST" in agent_adapter_lab, "Agent Adapter Lab marks generated manifest data"),
        Check("agent_adapter_lab:source_sync_script", "Agent Adapter Lab Source Sync" in sync_agent_adapter_lab and "build_lab_manifest" in sync_agent_adapter_lab, "Agent Adapter Lab has a manifest source-of-truth sync script"),
        Check("agent_adapter_lab:source_sync_audit", "Agent Adapter Lab Audit" in agent_adapter_lab_audit and "extract_embedded_manifest" in agent_adapter_lab_audit, "Agent Adapter Lab audit compares embedded manifest with canonical JSON"),
        Check("agent_adapter_lab:source_sync_make_target", "agent-adapter-lab-sync" in makefile and "scripts/sync_agent_adapter_lab.py" in makefile, "Makefile checks Agent Adapter Lab source sync"),
        Check("agent_adapter_lab:audit_make_target", "agent-adapter-lab-audit" in makefile and "scripts/agent_adapter_lab_audit.py" in makefile, "Makefile runs Agent Adapter Lab audit"),
        Check("agent_adapter_lab:copy_outputs", "Copy Pack Command" in agent_adapter_lab and "Copy Install Checklist" in agent_adapter_lab and "Copy Adapter JSON" in agent_adapter_lab and "Copy Issue Seed" in agent_adapter_lab, "Agent Adapter Lab can copy command, checklist, JSON, and issue outputs"),
        Check("agent_adapter_lab:dom_safety", "textContent" in agent_adapter_lab and "replaceChildren" in agent_adapter_lab and "innerHTML" not in agent_adapter_lab, "Agent Adapter Lab renders data without HTML injection"),
        Check("agent_adapter_lab:safety_boundary", "not a promise" in agent_adapter_lab and "local-first" in agent_adapter_lab, "Agent Adapter Lab keeps safety boundary visible"),
        Check("agent_adapter_lab:issue_template", all(term in agent_adapter_issue_template for term in ("Agent adapter improvement", "candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary")), "Agent Adapter Lab has a dedicated issue template"),
        Check("agent_adapter_lab:flow_docs", all(term in visual + evaluation + ux for term in ("agent-adapter-lab-flow.svg", "Agent Adapter Lab Flow", "agent_adapter_improvement.yml")), "Agent Adapter Lab flow is documented across UX, visual tour, and evaluation docs"),
        Check("agent_portability_lab:title", "MBTI Typing Skill Agent Portability Lab" in agent_portability_lab, "Agent Portability Lab has a clear product title"),
        Check("agent_portability_lab:no_external_runtime", "<script src" not in agent_portability_lab and " src=" not in agent_portability_lab, "Agent Portability Lab has no external runtime dependency"),
        Check("agent_portability_lab:interactive_regions", all(term in agent_portability_lab for term in ("targetSelect", "hostNameInput", "capabilityList", "bridgePlanOutput", "portableInstallOutput", "adapterDraftOutput", "portabilityIssueOutput")), "Agent Portability Lab contains target, unknown host, capability, plan, install, draft, and issue regions"),
        Check("agent_portability_lab:source_markers", "BEGIN GENERATED AGENT PORTABILITY MANIFEST" in agent_portability_lab and "END GENERATED AGENT PORTABILITY MANIFEST" in agent_portability_lab, "Agent Portability Lab marks generated manifest data"),
        Check("agent_portability_lab:source_sync_script", "Agent Portability Lab Source Sync" in sync_agent_portability_lab and "build_portability_manifest" in sync_agent_portability_lab, "Agent Portability Lab has a manifest source-of-truth sync script"),
        Check("agent_portability_lab:source_sync_audit", "Agent Portability Lab Audit" in agent_portability_lab_audit and "extract_embedded_manifest" in agent_portability_lab_audit, "Agent Portability Lab audit compares embedded manifest with canonical JSON"),
        Check("agent_portability_lab:source_sync_make_target", "agent-portability-lab-sync" in makefile and "scripts/sync_agent_portability_lab.py" in makefile, "Makefile checks Agent Portability Lab source sync"),
        Check("agent_portability_lab:audit_make_target", "agent-portability-lab-audit" in makefile and "scripts/agent_portability_lab_audit.py" in makefile, "Makefile runs Agent Portability Lab audit"),
        Check("agent_portability_lab:copy_outputs", "Copy Bridge Plan" in agent_portability_lab and "Copy Portable Install" in agent_portability_lab and "Copy Adapter JSON" in agent_portability_lab and "Copy Issue Seed" in agent_portability_lab, "Agent Portability Lab can copy plan, install, JSON, and issue outputs"),
        Check("agent_portability_lab:dom_safety", "textContent" in agent_portability_lab and "replaceChildren" in agent_portability_lab and "innerHTML" not in agent_portability_lab, "Agent Portability Lab renders data without HTML injection"),
        Check("agent_portability_lab:safety_boundary", "unknown host" in agent_portability_lab and "local-first" in agent_portability_lab and "safety boundary" in agent_portability_lab, "Agent Portability Lab keeps capability and safety boundaries visible"),
        Check("agent_portability_lab:issue_template", all(term in agent_portability_issue_template for term in ("Agent portability request", "unknown host", "candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary")), "Agent Portability Lab has a dedicated issue template"),
        Check("agent_portability_lab:flow_docs", all(term in visual + evaluation + ux for term in ("universal-agent-bridge-map.svg", "Universal Agent Bridge Map", "agent_portability_request.yml")), "Agent Portability Lab flow is documented across UX, visual tour, and evaluation docs"),
        Check("response_eval:audit_script", all(term in response_eval_audit for term in ("Response Eval Audit", "sticky_precision", "negative_blocked", "OVERCLAIM_RE", "FLATTERY_RE")), "Response evaluation has a dedicated audit script"),
        Check("response_eval:audit_cases", response_eval_payload.get("schema_version") == "response-eval/v1" and len(response_eval_payload.get("cases", [])) >= 4, "Response evaluation cases use schema v1 and cover at least four fixtures"),
        Check("response_eval:audit_make_target", "response-eval-audit" in makefile and "scripts/response_eval_audit.py" in makefile, "Makefile runs Response Eval audit"),
        Check("response_eval_lab:title", "MBTI Typing Skill Response Eval Lab" in response_eval_lab, "Response Eval Lab has a clear product title"),
        Check("response_eval_lab:no_external_runtime", "<script src" not in response_eval_lab and " src=" not in response_eval_lab, "Response Eval Lab has no external runtime dependency"),
        Check("response_eval_lab:interactive_regions", all(term in response_eval_lab for term in ("modeSelect", "promptInput", "responseInput", "gateGrid", "radarSvg", "receiptOutput", "repairPromptOutput", "issueSeedOutput")), "Response Eval Lab contains mode, prompt, response, radar, receipt, repair prompt, and issue seed regions"),
        Check("response_eval_lab:mode_gates", all(term in response_eval_lab for term in ("live_round", "type_duel", "final_report", "anti_pattern", "REQUIRED_BY_MODE")), "Response Eval Lab has mode-aware gates"),
        Check("response_eval_lab:copy_outputs", "Copy Repair Prompt" in response_eval_lab and "Copy Eval JSON" in response_eval_lab and "Copy Issue Seed" in response_eval_lab, "Response Eval Lab can copy repair, JSON, and issue outputs"),
        Check("response_eval_lab:dom_safety", "textContent" in response_eval_lab and "replaceChildren" in response_eval_lab and "innerHTML" not in response_eval_lab, "Response Eval Lab renders data without HTML injection"),
        Check("response_eval_lab:safety_boundary", "not psychometric ground truth" in response_eval_lab and "local-first" in response_eval_lab, "Response Eval Lab keeps safety boundary visible"),
        Check("response_eval_lab:audit_script", "Response Eval Lab Audit" in response_eval_lab_audit and "Copy Repair Prompt" in response_eval_lab_audit, "Response Eval Lab has a dedicated audit script"),
        Check("response_eval_lab:audit_make_target", "response-eval-lab-audit" in makefile and "scripts/response_eval_lab_audit.py" in makefile, "Makefile runs Response Eval Lab audit"),
        Check("response_eval_lab:flow_docs", all(term in visual + evaluation + ux for term in ("response-eval-lab-flow.svg", "Response Eval Lab Flow", "response_eval_improvement.yml")), "Response Eval Lab flow is documented across UX, visual tour, and evaluation docs"),
        Check("docs:agent_adapter_docs", all(term in agent_adapters_doc + agent_adapters_readme for term in ("Codex", "Claude Code", "Cursor", "opencode", "Gemini CLI", "GitHub Copilot", "Windsurf", "Cline", "Continue", "aider", "AGENTS.md", "agent_adapter_audit.py", "runner-up", "falsifier", "safety boundary")), "Agent adapter docs explain tools, contract, and release gate"),
        Check("docs:agent_pack_export_docs", all(term in agent_adapters_doc + agent_adapters_readme for term in ("scripts/export_agent_pack.py", "scripts/agent_pack_export_audit.py", "AGENT_PACK_MANIFEST.json", "Agent Pack Export Flow")), "Agent adapter docs explain pack export path"),
        Check("docs:blind_review_protocol", all(term in blind_review for term in ("Blind Review Protocol", "Case Packet Requirements", "Reviewer Output Requirements", "Top-1 hit", "Top-2 hit", "Acceptance Threshold")), "Blind Review Protocol defines packet, output, metrics, and acceptance rules"),
        Check("docs:blind_review_sources", all(term in blind_review for term in ("themyersbriggs.com", "10.1111/j.1467-6494.1989.tb00759.x", "10.1177/0013164410375112")), "Blind Review Protocol cites source-backed guardrails"),
        Check("docs:consent_redaction_protocol", all(term in consent_protocol for term in ("Consent Redaction Protocol", "Packet Requirements", "Redaction Rules", "Acceptance Threshold", "[PERSON_A]")), "Consent Redaction Protocol defines packet, redaction, and acceptance rules"),
        Check("docs:consent_redaction_boundary", all(term in consent_protocol for term in ("not a legal compliance certification", "Raw private chat logs", "withdrawal")), "Consent Redaction Protocol keeps legal and raw-data boundaries visible"),
        Check("docs:demo_candidate_set", "Current working candidates" in demo and "Round 2: Targeted Duel" in demo, "Demo session shows candidate set and duel loop"),
        Check("docs:sample_falsifiers", "Falsifiers" in sample and "Why INTJ Remains Serious" in sample, "Sample report preserves runner-up and falsifiers"),
        Check("session_lab:title", "MBTI Typing Skill Session Lab" in session_lab, "Session Lab has a clear product title"),
        Check("session_lab:no_external_runtime", "<script src" not in session_lab and " src=" not in session_lab, "Session Lab has no external runtime dependency"),
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
        Check("case_gallery:benchmark_cases", len(benchmark_cases) >= 16 and all(case_id in case_gallery for case_id in benchmark_ids), "Case Gallery exposes all current benchmark cases"),
        Check("case_gallery:all_16_leading_types", required_types <= leading_types, f"{len(leading_types & required_types)} leading types covered"),
        Check("case_gallery:source_markers", "BEGIN GENERATED BENCHMARK CASES" in case_gallery and "END GENERATED BENCHMARK CASES" in case_gallery, "Case Gallery marks generated benchmark data"),
        Check("case_gallery:source_sync_script", "Case Gallery Source Sync" in sync_case_gallery and "make_gallery_cases" in sync_case_gallery, "Case Gallery has a JSON source-of-truth sync script"),
        Check("case_gallery:source_sync_audit", "source:json_match" in case_gallery_audit and "make_gallery_cases" in case_gallery_audit, "Case Gallery audit compares embedded cases with canonical JSON"),
        Check("case_gallery:source_sync_make_target", "case-gallery-sync" in makefile and "scripts/sync_case_gallery.py" in makefile, "Makefile checks Case Gallery source sync"),
        Check("case_gallery:safety_boundary", "Not psychometric ground truth" in case_gallery and "not clinical or hiring instruments" in case_gallery, "Case Gallery keeps safety boundary visible"),
        Check("case_gallery:copy_prompt", "navigator.clipboard.writeText" in case_gallery and "Use $mbti-typing" in case_gallery, "Case Gallery can copy reusable prompts"),
        Check("case_gallery:dom_safety", "textContent" in case_gallery and "replaceChildren" in case_gallery and "innerHTML" not in case_gallery, "Case Gallery renders data without HTML injection"),
        Check("case_gallery:audit_script", "Case Gallery Audit" in case_gallery_audit and "Submit Benchmark Case" in case_gallery_audit, "Case Gallery has a dedicated audit script"),
        Check("case_gallery:audit_make_target", "case-gallery-audit" in makefile and "scripts/case_gallery_audit.py" in makefile, "Makefile runs Case Gallery audit"),
        Check("benchmark_replay_lab:title", "MBTI Typing Skill Benchmark Replay Lab" in benchmark_replay_lab, "Benchmark Replay Lab has a clear product title"),
        Check("benchmark_replay_lab:no_external_runtime", "<script src" not in benchmark_replay_lab and " src=" not in benchmark_replay_lab, "Benchmark Replay Lab has no external runtime dependency"),
        Check("benchmark_replay_lab:interactive_regions", all(term in benchmark_replay_lab for term in ("caseSelect", "blindPromptOutput", "leadingGuess", "runnerGuess", "falsifierGuess", "replayScoreGrid", "referencePanel", "replayReceiptOutput", "repairPromptOutput", "issueSeedOutput")), "Benchmark Replay Lab contains case, blind prompt, guesses, reference, receipt, repair prompt, and issue seed regions"),
        Check("benchmark_replay_lab:benchmark_cases", len(benchmark_cases) >= 16 and all(case_id in benchmark_replay_lab for case_id in benchmark_ids), "Benchmark Replay Lab exposes all current benchmark cases"),
        Check("benchmark_replay_lab:all_16_leading_types", required_types <= leading_types, f"{len(leading_types & required_types)} leading types covered"),
        Check("benchmark_replay_lab:source_markers", "BEGIN GENERATED BENCHMARK REPLAY CASES" in benchmark_replay_lab and "END GENERATED BENCHMARK REPLAY CASES" in benchmark_replay_lab, "Benchmark Replay Lab marks generated benchmark data"),
        Check("benchmark_replay_lab:source_sync_script", "Benchmark Replay Lab Source Sync" in sync_benchmark_replay_lab and "make_replay_cases" in sync_benchmark_replay_lab, "Benchmark Replay Lab has a JSON source-of-truth sync script"),
        Check("benchmark_replay_lab:source_sync_audit", "source:json_match" in benchmark_replay_lab_audit and "make_replay_cases" in benchmark_replay_lab_audit, "Benchmark Replay Lab audit compares embedded cases with canonical JSON"),
        Check("benchmark_replay_lab:source_sync_make_target", "benchmark-replay-lab-sync" in makefile and "scripts/sync_benchmark_replay_lab.py" in makefile, "Makefile checks Benchmark Replay Lab source sync"),
        Check("benchmark_replay_lab:copy_outputs", "Copy Blind Prompt" in benchmark_replay_lab and "Copy Replay JSON" in benchmark_replay_lab and "Copy Repair Prompt" in benchmark_replay_lab and "Copy Issue Seed" in benchmark_replay_lab, "Benchmark Replay Lab can copy prompt, JSON, repair, and issue outputs"),
        Check("benchmark_replay_lab:dom_safety", "textContent" in benchmark_replay_lab and "replaceChildren" in benchmark_replay_lab and "innerHTML" not in benchmark_replay_lab, "Benchmark Replay Lab renders data without HTML injection"),
        Check("benchmark_replay_lab:safety_boundary", "not psychometric ground truth" in benchmark_replay_lab and "local-first" in benchmark_replay_lab, "Benchmark Replay Lab keeps safety boundary visible"),
        Check("benchmark_replay_lab:audit_script", "Benchmark Replay Lab Audit" in benchmark_replay_lab_audit and "Copy Repair Prompt" in benchmark_replay_lab_audit, "Benchmark Replay Lab has a dedicated audit script"),
        Check("benchmark_replay_lab:audit_make_target", "benchmark-replay-lab-audit" in makefile and "scripts/benchmark_replay_lab_audit.py" in makefile, "Makefile runs Benchmark Replay Lab audit"),
        Check("benchmark_replay_lab:issue_template", all(term in benchmark_replay_issue_template for term in ("Benchmark replay improvement", "case id", "replay score", "leading guess", "runner-up guess", "public-safe")), "Benchmark Replay Lab has a dedicated issue template"),
        Check("benchmark_replay_lab:flow_docs", all(term in visual + evaluation + ux for term in ("benchmark-replay-loop.svg", "Benchmark Replay Loop", "benchmark_replay_improvement.yml")), "Benchmark Replay Lab flow is documented across UX, visual tour, and evaluation docs"),
        Check("calibration_lab:title", "MBTI Typing Skill Calibration Lab" in calibration_lab, "Calibration Lab has a clear product title"),
        Check("calibration_lab:no_external_runtime", "<script src" not in calibration_lab and " src=" not in calibration_lab, "Calibration Lab has no external runtime dependency"),
        Check("calibration_lab:interactive_regions", all(term in calibration_lab for term in ("caseSelect", "reportInput", "resultGrid", "receiptOutput", "repairPromptOutput", "issueSeedOutput")), "Calibration Lab contains case, report, result, receipt, repair prompt, and issue seed regions"),
        Check("calibration_lab:benchmark_cases", len(benchmark_cases) >= 16 and all(case_id in calibration_lab for case_id in benchmark_ids), "Calibration Lab exposes all current benchmark cases"),
        Check("calibration_lab:all_16_leading_types", required_types <= leading_types, f"{len(leading_types & required_types)} leading types covered"),
        Check("calibration_lab:source_markers", "BEGIN GENERATED CALIBRATION CASES" in calibration_lab and "END GENERATED CALIBRATION CASES" in calibration_lab, "Calibration Lab marks generated benchmark data"),
        Check("calibration_lab:source_sync_script", "Calibration Lab Source Sync" in sync_calibration_lab and "make_calibration_cases" in sync_calibration_lab, "Calibration Lab has a JSON source-of-truth sync script"),
        Check("calibration_lab:source_sync_audit", "source:json_match" in calibration_lab_audit and "make_calibration_cases" in calibration_lab_audit, "Calibration Lab audit compares embedded cases with canonical JSON"),
        Check("calibration_lab:source_sync_make_target", "calibration-lab-sync" in makefile and "scripts/sync_calibration_lab.py" in makefile, "Makefile checks Calibration Lab source sync"),
        Check("calibration_lab:copy_outputs", "Copy Repair Prompt" in calibration_lab and "Copy Calibration JSON" in calibration_lab and "Copy Failure Issue Seed" in calibration_lab, "Calibration Lab can copy repair, JSON, and issue outputs"),
        Check("calibration_lab:dom_safety", "textContent" in calibration_lab and "replaceChildren" in calibration_lab and "innerHTML" not in calibration_lab, "Calibration Lab renders data without HTML injection"),
        Check("calibration_lab:safety_boundary", "Not psychometric ground truth" in calibration_lab and "not a clinical" in calibration_lab, "Calibration Lab keeps safety boundary visible"),
        Check("calibration_lab:audit_script", "Calibration Lab Audit" in calibration_lab_audit and "Copy Repair Prompt" in calibration_lab_audit, "Calibration Lab has a dedicated audit script"),
        Check("calibration_lab:audit_make_target", "calibration-lab-audit" in makefile and "scripts/calibration_lab_audit.py" in makefile, "Makefile runs Calibration Lab audit"),
        Check("question_lab:title", "MBTI Typing Skill Question Lab" in question_lab, "Question Lab has a clear product title"),
        Check("question_lab:no_external_runtime", "<script src" not in question_lab and " src=" not in question_lab, "Question Lab has no external runtime dependency"),
        Check("question_lab:interactive_regions", all(term in question_lab for term in ("questionSearch", "categoryFilter", "cardList", "questionDetail", "questionList", "roundPromptOutput", "issueSeedOutput")), "Question Lab contains search, list, detail, questions, prompt, and issue seed regions"),
        Check("question_lab:source_cards", len(question_headings) >= 17 and all(heading in question_lab for heading in question_headings), "Question Lab exposes every current question-bank subsection"),
        Check("question_lab:source_markers", "BEGIN GENERATED QUESTION CARDS" in question_lab and "END GENERATED QUESTION CARDS" in question_lab, "Question Lab marks generated question data"),
        Check("question_lab:source_sync_script", "Question Lab Source Sync" in sync_question_lab and "parse_question_bank" in sync_question_lab, "Question Lab has a Markdown source-of-truth sync script"),
        Check("question_lab:source_sync_audit", "source:markdown_match" in question_lab_audit and "parse_question_bank" in question_lab_audit, "Question Lab audit compares embedded cards with question-bank.md"),
        Check("question_lab:source_sync_make_target", "question-lab-sync" in makefile and "scripts/sync_question_lab.py" in makefile, "Makefile checks Question Lab source sync"),
        Check("question_lab:copy_outputs", "Copy Round Prompt" in question_lab and "Copy Issue Seed" in question_lab and "question_improvement.yml" in question_lab, "Question Lab can copy prompt and issue outputs"),
        Check("question_lab:dom_safety", "textContent" in question_lab and "replaceChildren" in question_lab and "innerHTML" not in question_lab, "Question Lab renders data without HTML injection"),
        Check("question_lab:safety_boundary", "not a clinical instrument" in question_lab and "local-first" in question_lab, "Question Lab keeps safety boundary visible"),
        Check("question_lab:audit_script", "Question Lab Audit" in question_lab_audit and "Copy Round Prompt" in question_lab_audit, "Question Lab has a dedicated audit script"),
        Check("question_lab:audit_make_target", "question-lab-audit" in makefile and "scripts/question_lab_audit.py" in makefile, "Makefile runs Question Lab audit"),
        Check("type_duel_lab:title", "MBTI Typing Skill Type Duel Lab" in type_duel_lab, "Type Duel Lab has a clear product title"),
        Check("type_duel_lab:no_external_runtime", "<script src" not in type_duel_lab and " src=" not in type_duel_lab, "Type Duel Lab has no external runtime dependency"),
        Check("type_duel_lab:interactive_regions", all(term in type_duel_lab for term in ("pairSearch", "clusterFilter", "pairList", "duelDetail", "questionList", "losingConditions", "duelPromptOutput", "issueSeedOutput")), "Type Duel Lab contains search, list, detail, questions, losing conditions, prompt, and issue seed regions"),
        Check("type_duel_lab:all_16_types", all(type_code in type_duel_lab for type_code in required_types), "Type Duel Lab keeps all 16 types visible"),
        Check("type_duel_lab:source_pairs", len(duel_pairs) >= 18 and all(pair in type_duel_lab for pair in duel_pairs), "Type Duel Lab exposes every current pair duel"),
        Check("type_duel_lab:source_markers", "BEGIN GENERATED TYPE DUELS" in type_duel_lab and "END GENERATED TYPE DUELS" in type_duel_lab, "Type Duel Lab marks generated duel data"),
        Check("type_duel_lab:source_sync_script", "Type Duel Lab Source Sync" in sync_type_duel_lab and "parse_pair_duels" in sync_type_duel_lab, "Type Duel Lab has a Markdown source-of-truth sync script"),
        Check("type_duel_lab:source_sync_audit", "source:markdown_match" in type_duel_lab_audit and "parse_pair_duels" in type_duel_lab_audit, "Type Duel Lab audit compares embedded duels with pair-duels.md"),
        Check("type_duel_lab:source_sync_make_target", "type-duel-lab-sync" in makefile and "scripts/sync_type_duel_lab.py" in makefile, "Makefile checks Type Duel Lab source sync"),
        Check("type_duel_lab:copy_outputs", "Copy Duel Prompt" in type_duel_lab and "Copy Issue Seed" in type_duel_lab and "type_duel_improvement.yml" in type_duel_lab, "Type Duel Lab can copy prompt and issue outputs"),
        Check("type_duel_lab:dom_safety", "textContent" in type_duel_lab and "replaceChildren" in type_duel_lab and "innerHTML" not in type_duel_lab, "Type Duel Lab renders data without HTML injection"),
        Check("type_duel_lab:safety_boundary", "not a clinical instrument" in type_duel_lab and "local-first" in type_duel_lab, "Type Duel Lab keeps safety boundary visible"),
        Check("type_duel_lab:audit_script", "Type Duel Lab Audit" in type_duel_lab_audit and "Copy Duel Prompt" in type_duel_lab_audit, "Type Duel Lab has a dedicated audit script"),
        Check("type_duel_lab:audit_make_target", "type-duel-lab-audit" in makefile and "scripts/type_duel_lab_audit.py" in makefile, "Makefile runs Type Duel Lab audit"),
        Check("blind_review:audit_script", "Blind Review Audit" in blind_review_audit and "Blind Review Metrics" in blind_review_audit, "Blind Review has a dedicated audit script"),
        Check("blind_review:audit_make_target", "blind-review-audit" in makefile and "scripts/blind_review_audit.py" in makefile, "Makefile runs Blind Review audit"),
        Check("consent_redaction:audit_script", "Consent Redaction Audit" in consent_redaction_audit and "Consent Redaction Metrics" in consent_redaction_audit, "Consent Redaction has a dedicated audit script"),
        Check("consent_redaction:audit_make_target", "consent-redaction-audit" in makefile and "scripts/consent_redaction_audit.py" in makefile, "Makefile runs Consent Redaction audit"),
        Check("follow_up_lab:title", "MBTI Typing Skill Follow-Up Lab" in follow_up_lab, "Follow-Up Lab has a clear product title"),
        Check("follow_up_lab:no_external_runtime", "<script src" not in follow_up_lab and " src=" not in follow_up_lab, "Follow-Up Lab has no external runtime dependency"),
        Check("follow_up_lab:interactive_regions", all(term in follow_up_lab for term in ("candidateSetInput", "obsNormal", "privacyScore", "safetyGrid", "packetOutput", "issueSeedOutput")), "Follow-Up Lab contains candidate, observation, gate, packet, and issue seed regions"),
        Check("follow_up_lab:all_16_types", all(type_code in follow_up_lab for type_code in ("INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP")), "Follow-Up Lab keeps all 16 types visible"),
        Check("follow_up_lab:privacy_engine", "scanForSensitiveText" in follow_up_lab and "HIGH_RISK_TERMS" in follow_up_lab and "auditPacket" in follow_up_lab, "Follow-Up Lab includes a local privacy gate"),
        Check("follow_up_lab:copy_outputs", "Copy Follow-Up JSON" in follow_up_lab and "Download JSON" in follow_up_lab and "Copy Issue Seed" in follow_up_lab, "Follow-Up Lab can copy and download packet outputs"),
        Check("follow_up_lab:dom_safety", "textContent" in follow_up_lab and "replaceChildren" in follow_up_lab and "innerHTML" not in follow_up_lab, "Follow-Up Lab renders data without HTML injection"),
        Check("follow_up_lab:safety_boundary", "not a clinical instrument" in follow_up_lab and "public-safe" in follow_up_lab, "Follow-Up Lab keeps safety boundary visible"),
        Check("follow_up_lab:audit_script", "Follow-Up Lab Audit" in follow_up_lab_audit and "Copy Follow-Up JSON" in follow_up_lab_audit, "Follow-Up Lab has a dedicated audit script"),
        Check("follow_up_lab:audit_make_target", "follow-up-lab-audit" in makefile and "scripts/follow_up_lab_audit.py" in makefile, "Makefile runs Follow-Up Lab audit"),
        Check("playground:title", "MBTI Typing Skill Playground" in playground, "Playground has a clear product title"),
        Check("playground:no_external_runtime", "<script src" not in playground and " src=" not in playground, "Playground has no external runtime dependency"),
        Check("playground:interactive_regions", all(term in playground for term in ("scenarioList", "candidateList", "evidenceList", "duelList", "promptOutput")), "Playground contains scenario, candidate, evidence, duel, and prompt regions"),
        Check("playground:copy_prompt", "navigator.clipboard.writeText" in playground and "Copy Prompt" in playground, "Playground can copy the generated prompt"),
        Check("playground:scenario_count", playground.count("Use $mbti-typing") >= 3, "Playground includes multiple live prompt starts"),
        Check("playground:safety_boundary", "not a clinical instrument" in playground, "Playground keeps safety boundary visible"),
        Check("index_hub:title", "MBTI Typing Skill Experience Hub" in index, "Pages root has a clear Experience Hub title"),
        Check("index_hub:not_redirect", "http-equiv=\"refresh\"" not in index and "url=session-lab.html" not in index, "Pages root is a real command center, not a redirect"),
        Check("index_hub:route_cards", index.count('data-route-card="') >= 6, "Experience Hub exposes task-based workflow cards"),
        Check("index_hub:route_map", "assets/experience-hub-route-map.svg" in index and "Experience Hub Route Map" in index, "Experience Hub renders the route-map visual"),
        Check("index_hub:starter_prompt", "starterPrompt" in index and "Copy Starter Prompt" in index and "Use $mbti-typing" in index, "Experience Hub provides a copyable starter prompt"),
        Check("index_hub:direct_routes", all(term in index for term in ("session-lab.html", "question-lab.html", "type-duel-lab.html", "response-eval-lab.html", "calibration-lab.html", "benchmark-replay-lab.html", "case-gallery.html", "follow-up-lab.html", "agent-adapter-lab.html", "agent-portability-lab.html")), "Experience Hub links every public workflow route"),
        Check("index_hub:safety_boundary", all(term in index for term in ("candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary", "not a clinical instrument")), "Experience Hub keeps the safety and uncertainty contract visible"),
        Check("index_hub:audit_script", "Index Hub Audit" in index_hub_audit and "Experience Hub Route Map" in index_hub_audit, "Experience Hub has a dedicated audit script"),
        Check("index_hub:audit_make_target", "index-hub-audit" in makefile and "scripts/index_hub_audit.py" in makefile, "Makefile runs Index Hub audit"),
        Check("pages:github_readme_links", all("https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in page for page in (session_lab, case_gallery, benchmark_replay_lab, calibration_lab, question_lab, type_duel_lab, agent_adapter_lab, agent_portability_lab, follow_up_lab, response_eval_lab, playground)), "Public pages link README buttons to GitHub instead of a broken parent path"),
        Check("pages:agent_lab_nav", all("agent-adapter-lab.html" in page for page in (session_lab, case_gallery, benchmark_replay_lab, calibration_lab, question_lab, type_duel_lab, agent_portability_lab, follow_up_lab, response_eval_lab, playground)), "Public pages link to Agent Adapter Lab"),
        Check("pages:agent_portability_nav", all("agent-portability-lab.html" in page for page in (session_lab, case_gallery, benchmark_replay_lab, calibration_lab, question_lab, type_duel_lab, agent_adapter_lab, follow_up_lab, response_eval_lab, playground)), "Public pages link to Agent Portability Lab"),
        Check("pages:benchmark_replay_nav", all("benchmark-replay-lab.html" in page for page in (session_lab, case_gallery, benchmark_replay_lab, calibration_lab, question_lab, type_duel_lab, agent_adapter_lab, agent_portability_lab, follow_up_lab, response_eval_lab, playground)), "Public pages link to Benchmark Replay Lab"),
        Check("pages:github_prompt_links", "https://github.com/Zaoqu-Liu/mbti-typing-skill/blob/main/prompts/prompt-recipes.md" in session_lab and "https://github.com/Zaoqu-Liu/mbti-typing-skill/blob/main/prompts/prompt-recipes.md" in playground, "Public prompt recipe links resolve on GitHub Pages"),
        Check("pages:no_parent_readme", "../README.md" not in session_lab + case_gallery + benchmark_replay_lab + calibration_lab + question_lab + type_duel_lab + agent_adapter_lab + agent_portability_lab + follow_up_lab + response_eval_lab + playground and "../prompts/" not in session_lab + playground, "Public pages avoid parent-directory links that break after Pages deploy"),
        Check("pages:index_hub", "MBTI Typing Skill Experience Hub" in index and "http-equiv=\"refresh\"" not in index, "Docs index is a usable Experience Hub"),
        Check("pages:workflow", "actions/deploy-pages@v4" in pages and "path: docs" in pages, "GitHub Pages workflow deploys docs"),
    ]


def check_activation_assets(root: Path) -> list[Check]:
    prompts = read_text(root / "prompts/prompt-recipes.md")
    ledger = read_text(root / "examples/evidence-ledger-example.md")
    state = json.loads(read_text(root / "examples/session-state-example.json"))
    benchmark_payload = json.loads(read_text(root / "skill/mbti-typing/examples/benchmark-cases.json"))
    fixture_payload = json.loads(read_text(root / "skill/mbti-typing/examples/golden-reports.json"))
    blind_matrix = json.loads(read_text(root / "examples/blind-review-matrix.json"))
    consent_followup = json.loads(read_text(root / "examples/consented-followup-packet.json"))
    response_eval = json.loads(read_text(root / "examples/response-eval-cases.json"))
    benchmark_cases = benchmark_payload.get("cases", [])
    fixtures = fixture_payload.get("fixtures", [])
    blind_cases = blind_matrix.get("cases", [])
    followup_packets = consent_followup.get("packets", [])
    response_cases = response_eval.get("cases", [])
    reviewer_outputs = [
        output
        for case in blind_cases
        if isinstance(case, dict)
        for output in case.get("reviewer_outputs", [])
        if isinstance(output, dict)
    ]
    followup_observations = [
        observation
        for packet in followup_packets
        if isinstance(packet, dict)
        for observation in packet.get("follow_up_observations", [])
        if isinstance(observation, dict)
    ]
    consented_packets = [
        packet
        for packet in followup_packets
        if isinstance(packet, dict)
        and packet.get("consent", {}).get("subject_consent") is True
        and packet.get("consent", {}).get("public_issue_ok") is True
    ]
    privacy_safe_packets = [
        packet
        for packet in followup_packets
        if isinstance(packet, dict)
        and packet.get("privacy", {}).get("direct_identifiers_removed") is True
        and packet.get("privacy", {}).get("third_party_details_removed") is True
        and packet.get("privacy", {}).get("data_minimized") is True
        and packet.get("privacy", {}).get("contains_private_chat") is False
    ]
    positive_response_cases = [
        case
        for case in response_cases
        if isinstance(case, dict) and case.get("expected", {}).get("should_pass") is True
    ]
    negative_response_cases = [
        case
        for case in response_cases
        if isinstance(case, dict) and case.get("expected", {}).get("should_pass") is False
    ]
    response_modes = {str(case.get("mode")) for case in response_cases if isinstance(case, dict)}
    return [
        Check("activation:prompt_count", prompts.count("Use $mbti-typing") >= 6, "Prompt recipes include at least six copy-paste starts"),
        Check("activation:ledger_sections", "Candidate Set" in ledger and "Contradiction Gate" in ledger, "Evidence ledger example includes candidate and contradiction sections"),
        Check("activation:state_candidates", len(state.get("candidate_set", [])) >= 3, "Session state example starts from at least three candidates"),
        Check("activation:state_falsifiers", bool(state.get("falsifiers")), "Session state example includes falsifiers"),
        Check("activation:fixture_coverage", isinstance(benchmark_cases, list) and isinstance(fixtures, list) and len(benchmark_cases) == len(fixtures) and len(fixtures) >= 16, "Golden fixtures cover every expanded benchmark case"),
        Check("activation:blind_review_cases", isinstance(blind_cases, list) and len(blind_cases) >= 3, "Blind review matrix includes at least three cases"),
        Check("activation:blind_review_outputs", len(reviewer_outputs) >= 6 and all(output.get("boundary_included") is True for output in reviewer_outputs), "Blind review matrix includes reviewer outputs with safety boundaries"),
        Check("activation:followup_packets", isinstance(followup_packets, list) and len(followup_packets) >= 2, "Consented follow-up packet includes at least two cases"),
        Check("activation:followup_observations", len(followup_observations) >= 6, "Consented follow-up packet includes delayed observations"),
        Check("activation:followup_consent", len(consented_packets) == len(followup_packets), "Every follow-up packet has subject consent and public issue permission"),
        Check("activation:followup_privacy", len(privacy_safe_packets) == len(followup_packets), "Every follow-up packet is marked privacy-safe"),
        Check("activation:response_eval_cases", isinstance(response_cases, list) and len(response_cases) >= 4, "Response evaluation dataset includes at least four fixtures"),
        Check("activation:response_eval_polarity", len(positive_response_cases) >= 3 and len(negative_response_cases) >= 1, "Response evaluation dataset includes positive fixtures and a blocked anti-pattern"),
        Check("activation:response_eval_modes", {"live_round", "type_duel", "final_report", "anti_pattern"} <= response_modes, "Response evaluation covers live, duel, final, and anti-pattern modes"),
    ]


def run(root: Path) -> int:
    checks: list[Check] = []
    checks.extend(check_required_files(root))
    checks.extend(check_hero(root))
    checks.extend(check_journey_map(root))
    checks.extend(check_social_preview(root))
    checks.extend(check_response_eval_command_center(root))
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
