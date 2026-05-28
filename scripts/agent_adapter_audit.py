#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_FILES = (
    "AGENTS.md",
    "opencode.json",
    ".claude/skills/mbti-typing/SKILL.md",
    ".claude/commands/mbti-type.md",
    ".cursor/rules/mbti-typing.mdc",
    "agent-adapters/manifest.json",
    "agent-adapters/README.md",
    "docs/agent-adapters.md",
    "docs/assets/agent-adapter-matrix.svg",
)

EXPECTED_TARGETS = ("codex", "claude-code", "cursor", "opencode")

SAFETY_TERMS = (
    "clinical",
    "hiring",
    "legal",
    "medical",
    "financial",
    "deterministic",
)

CORE_PROTOCOL_TERMS = (
    "skill/mbti-typing/SKILL.md",
    "question-bank.md",
    "pair-duels.md",
    "evidence ledger",
    "runner-up",
    "falsifier",
)

SVG_TERMS = (
    "Agent Adapter Matrix",
    "Codex",
    "Claude Code",
    "Cursor",
    "opencode",
    "AGENTS.md",
    ".claude/skills",
    ".claude/commands",
    ".cursor/rules",
    "opencode.json",
    "skill/mbti-typing/SKILL.md",
    "agent_adapter_audit.py",
    "make test",
    "runner-up",
    "falsifier",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def contains_all(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return all(term.lower() in lower for term in terms)


def check_required_files(root: Path) -> list[Check]:
    return [
        Check(f"file:{rel}", (root / rel).exists(), "required adapter file exists")
        for rel in REQUIRED_FILES
    ]


def check_manifest(root: Path) -> list[Check]:
    path = root / "agent-adapters/manifest.json"
    try:
        manifest = load_json(path)
    except Exception as exc:
        return [Check("manifest:json", False, f"manifest parses as JSON: {exc}")]

    targets = manifest.get("targets", [])
    target_ids = [target.get("id") for target in targets if isinstance(target, dict)]
    checks = [
        Check("manifest:schema", manifest.get("schema") == "mbti-typing-agent-adapters/v1", "adapter manifest schema is pinned"),
        Check("manifest:canonical_skill", manifest.get("canonical_skill") == "skill/mbti-typing/SKILL.md", "manifest points at canonical skill"),
        Check("manifest:canonical_contract", manifest.get("canonical_contract") == "AGENTS.md", "manifest points at root contract"),
        Check("manifest:adapter_audit", manifest.get("adapter_audit") == "scripts/agent_adapter_audit.py", "manifest points at adapter audit"),
        Check("manifest:targets", sorted(target_ids) == sorted(EXPECTED_TARGETS), f"targets={target_ids}"),
    ]

    shared_refs = manifest.get("shared_references", [])
    for rel in shared_refs:
        checks.append(Check(f"manifest:shared_ref:{rel}", isinstance(rel, str) and (root / rel).exists(), "shared reference exists"))

    for target in targets:
        if not isinstance(target, dict):
            checks.append(Check("manifest:target_shape", False, "every target is an object"))
            continue
        target_id = str(target.get("id", "unknown"))
        entrypoints = target.get("entrypoints", [])
        checks.append(Check(f"manifest:{target_id}:entrypoints", isinstance(entrypoints, list) and bool(entrypoints), "target has entrypoints"))
        checks.append(Check(f"manifest:{target_id}:invoke", bool(target.get("invoke")), "target has invocation guidance"))
        checks.append(Check(f"manifest:{target_id}:install", bool(target.get("install")), "target has install guidance"))
        checks.append(Check(f"manifest:{target_id}:contract", bool(target.get("contract")), "target has contract guidance"))
        for rel in entrypoints:
            checks.append(Check(f"manifest:{target_id}:entrypoint:{rel}", isinstance(rel, str) and (root / rel).exists(), "entrypoint file exists"))

    return checks


def check_contract(root: Path) -> list[Check]:
    agents = read_text(root / "AGENTS.md")
    return [
        Check("contract:canonical_refs", contains_all(agents, CORE_PROTOCOL_TERMS), "root contract preserves protocol references"),
        Check("contract:safety", contains_all(agents, SAFETY_TERMS), "root contract preserves safety boundary"),
        Check("contract:output_minimum", contains_all(agents, ("leading formulation", "serious runner-up", "decisive evidence", "revision triggers")), "root contract defines final output minimum"),
        Check("contract:verification", "make test" in agents and "scripts/agent_adapter_audit.py" in agents, "root contract requires adapter verification"),
    ]


def check_tool_adapters(root: Path) -> list[Check]:
    claude_skill = read_text(root / ".claude/skills/mbti-typing/SKILL.md")
    claude_command = read_text(root / ".claude/commands/mbti-type.md")
    cursor_rule = read_text(root / ".cursor/rules/mbti-typing.mdc")
    opencode = load_json(root / "opencode.json")
    instructions = opencode.get("instructions", []) if isinstance(opencode, dict) else []
    return [
        Check("claude_skill:frontmatter", "name: mbti-typing" in claude_skill and "when_to_use:" in claude_skill, "Claude Code skill has discovery frontmatter"),
        Check("claude_skill:canonical_refs", contains_all(claude_skill, ("skill/mbti-typing/SKILL.md", "runner-up", "falsifier", "question-bank.md", "pair-duels.md")), "Claude Code skill points back to canonical protocol"),
        Check("claude_skill:safety", contains_all(claude_skill, SAFETY_TERMS), "Claude Code skill preserves safety boundary"),
        Check("claude_command:arguments", "$ARGUMENTS" in claude_command, "Claude command forwards user arguments"),
        Check("claude_command:mode_refs", contains_all(claude_command, ("question-bank.md", "pair-duels.md", "evidence-ledger-template.md", "quality-gates.md")), "Claude command routes to mode references"),
        Check("claude_command:safety", contains_all(claude_command, SAFETY_TERMS), "Claude command preserves safety boundary"),
        Check("cursor_rule:frontmatter", "description:" in cursor_rule and "alwaysApply: false" in cursor_rule and '"**/*"' in cursor_rule, "Cursor rule has explicit MDC frontmatter"),
        Check("cursor_rule:canonical_refs", contains_all(cursor_rule, ("skill/mbti-typing/SKILL.md", "question-bank.md", "pair-duels.md", "runner-up", "falsifiers")), "Cursor rule points back to canonical protocol"),
        Check("cursor_rule:safety", contains_all(cursor_rule, SAFETY_TERMS[:-1]) and "deterministic claims" in cursor_rule, "Cursor rule preserves safety boundary"),
        Check("opencode:instructions", isinstance(instructions, list) and all(rel in instructions for rel in ("AGENTS.md", "agent-adapters/README.md", "skill/mbti-typing/SKILL.md")), "opencode aggregates project, adapter, and skill instructions"),
    ]


def check_docs_and_visual(root: Path) -> list[Check]:
    adapter_readme = read_text(root / "agent-adapters/README.md")
    docs = read_text(root / "docs/agent-adapters.md")
    svg = read_text(root / "docs/assets/agent-adapter-matrix.svg")
    makefile = read_text(root / "Makefile")
    dependency_scan = svg.replace('xmlns="http://www.w3.org/2000/svg"', "")
    required_tool_terms = ("Codex", "Claude Code", "Cursor", "opencode")
    return [
        Check("docs:adapter_readme_tools", contains_all(adapter_readme, required_tool_terms), "adapter README covers all target tools"),
        Check("docs:adapter_readme_contract", contains_all(adapter_readme, ("candidate set", "runner-up", "evidence ledger", "falsifier", "safety boundary")), "adapter README preserves universal contract"),
        Check("docs:agent_adapters_tools", contains_all(docs, required_tool_terms), "agent adapter docs cover all target tools"),
        Check("docs:agent_adapters_sources", contains_all(docs, ("docs.anthropic.com", "docs.cursor.com", "opencode.ai", "github.com/openai/codex")), "agent adapter docs cite current source conventions"),
        Check("makefile:agent_adapter_target", "agent-adapter-audit" in makefile and "scripts/agent_adapter_audit.py" in makefile, "Makefile runs adapter audit"),
        Check("svg:shape", "<svg" in svg and "viewBox=" in svg, "adapter matrix is an SVG with viewBox"),
        Check("svg:accessibility", 'role="img"' in svg and "<title" in svg and "<desc" in svg, "adapter matrix has accessibility metadata"),
        Check("svg:no_remote_or_script", "<script" not in dependency_scan and "http://" not in dependency_scan and "https://" not in dependency_scan, "adapter matrix has no script or remote dependency"),
        Check("svg:labels", contains_all(svg, SVG_TERMS), "adapter matrix contains expected labels"),
    ]


def run(root: Path) -> int:
    checks: list[Check] = []
    checks.extend(check_required_files(root))
    checks.extend(check_manifest(root))
    checks.extend(check_contract(root))
    checks.extend(check_tool_adapters(root))
    checks.extend(check_docs_and_visual(root))

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Agent Adapter Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    return run(root.resolve())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
