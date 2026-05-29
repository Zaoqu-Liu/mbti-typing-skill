#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


START_MARKER = "    // BEGIN GENERATED AGENT PORTABILITY MANIFEST"
END_MARKER = "    // END GENERATED AGENT PORTABILITY MANIFEST"

MANIFEST_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

MANIFEST_CONST_RE = re.compile(r"\s*const AGENT_PORTABILITY_MANIFEST = (?P<payload>\{.*\});\s*$", re.DOTALL)

CAPABILITY_AXES = [
    {
        "id": "project_instruction",
        "label": "Project instruction file",
        "proof": "AGENTS.md, CLAUDE.md, GEMINI.md, CONVENTIONS.md, or equivalent repository context file",
        "entrypoint_hint": "AGENTS.md",
    },
    {
        "id": "native_skill",
        "label": "Native skill directory",
        "proof": "A directory containing SKILL.md, references, scripts, and optional metadata",
        "entrypoint_hint": "skill/mbti-typing/SKILL.md",
    },
    {
        "id": "project_rule",
        "label": "Project rule or mode file",
        "proof": "A checked-in rule file such as .cursor/rules, .rules, .roomodes, .continue/rules, or similar",
        "entrypoint_hint": ".cursor/rules/mbti-typing.mdc",
    },
    {
        "id": "custom_agent",
        "label": "Custom agent JSON or profile",
        "proof": "A named agent profile with prompt, resources, tools, or allowed tool grants",
        "entrypoint_hint": ".amazonq/cli-agents/mbti-typing.json",
    },
    {
        "id": "slash_command",
        "label": "Slash command or command recipe",
        "proof": "A command file that forwards user input and points to the canonical protocol",
        "entrypoint_hint": ".claude/commands/mbti-type.md",
    },
    {
        "id": "chat_project",
        "label": "Chat project or custom GPT instructions",
        "proof": "A hosted chat instructions field plus uploaded knowledge files",
        "entrypoint_hint": "gpts/mbti-typing-gpt-instructions.md",
    },
    {
        "id": "config_instruction_array",
        "label": "Config instruction array",
        "proof": "A JSON/YAML config that aggregates multiple instruction files",
        "entrypoint_hint": "opencode.json",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(read_text(path))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    if payload.get("schema") != "mbti-typing-agent-adapters/v1":
        raise ValueError("unsupported adapter manifest schema")
    targets = payload.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ValueError("adapter manifest has no targets")
    return payload


def capability_ids_for_entrypoints(entrypoints: list[str]) -> list[str]:
    joined = "\n".join(entrypoints)
    capabilities: list[str] = []
    if any(path in entrypoints for path in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONVENTIONS.md")):
        capabilities.append("project_instruction")
    if "SKILL.md" in joined:
        capabilities.append("native_skill")
    if any(
        marker in joined
        for marker in (
            ".cursor/rules",
            ".rules",
            ".roomodes",
            ".continue/rules",
            ".windsurf/rules",
            ".clinerules",
            ".roo/rules",
            ".kilo/rules",
            ".github/instructions",
        )
    ):
        capabilities.append("project_rule")
    if any(marker in joined for marker in (".amazonq/cli-agents", "kilo.jsonc")):
        capabilities.append("custom_agent")
    if "/commands/" in joined:
        capabilities.append("slash_command")
    if any(marker in joined for marker in ("gpts/", "GPT", "Project")):
        capabilities.append("chat_project")
    if any(marker in joined for marker in ("opencode.json", ".gemini/settings.json", ".aider.conf.yml", "kilo.jsonc")):
        capabilities.append("config_instruction_array")
    return sorted(set(capabilities))


def normalize_target(target: dict[str, Any]) -> dict[str, Any]:
    entrypoints = target.get("entrypoints")
    if not isinstance(entrypoints, list):
        entrypoints = []
    normalized_entrypoints = [str(item) for item in entrypoints]
    return {
        "id": str(target.get("id", "")),
        "display": str(target.get("display", "")),
        "support_level": str(target.get("support_level", "")),
        "source_url": str(target.get("source_url", "")),
        "entrypoints": normalized_entrypoints,
        "invoke": str(target.get("invoke", "")),
        "install": str(target.get("install", "")),
        "contract": str(target.get("contract", "")),
        "capabilities": capability_ids_for_entrypoints(normalized_entrypoints),
    }


def build_portability_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "mbti-typing-agent-portability-lab/v1",
        "source_schema": manifest.get("schema"),
        "canonical_skill": manifest.get("canonical_skill"),
        "canonical_contract": manifest.get("canonical_contract"),
        "adapter_manifest": "agent-adapters/manifest.json",
        "adapter_audit": manifest.get("adapter_audit"),
        "pack_exporter": manifest.get("pack_exporter"),
        "pack_audit": manifest.get("pack_audit"),
        "checked_on": manifest.get("checked_on"),
        "capability_axes": CAPABILITY_AXES,
        "targets": [normalize_target(target) for target in manifest.get("targets", []) if isinstance(target, dict)],
        "safety_contract": [
            "candidate set with serious runner-up",
            "evidence ledger",
            "falsifier and revision trigger",
            "no clinical, hiring, legal, medical, financial, or deterministic use",
        ],
    }


def render_manifest_block(payload: dict[str, Any]) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const AGENT_PORTABILITY_MANIFEST = {rendered};\n{END_MARKER}"


def extract_embedded_manifest(html: str) -> dict[str, Any]:
    block_match = MANIFEST_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("agent portability lab is missing generated manifest markers")
    const_match = MANIFEST_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("agent portability lab generated block does not contain AGENT_PORTABILITY_MANIFEST JSON")
    payload = json.loads(const_match.group("payload"))
    if not isinstance(payload, dict):
        raise ValueError("agent portability lab manifest payload must be an object")
    return payload


def sync_html(html: str, payload: dict[str, Any]) -> str:
    if not MANIFEST_BLOCK_RE.search(html):
        raise ValueError("agent portability lab is missing generated manifest markers")
    updated = MANIFEST_BLOCK_RE.sub(render_manifest_block(payload), html, count=1)
    replacements = {
        r'(<strong id="metricTargets">).*?(</strong>)': str(len(payload.get("targets", []))),
        r'(<strong id="metricCapabilities">).*?(</strong>)': str(len(payload.get("capability_axes", []))),
        r'(<span id="checkedOn">).*?(</span>)': str(payload.get("checked_on", "")),
    }
    for pattern, value in replacements.items():
        updated = re.sub(pattern, rf"\g<1>{value}\2", updated, count=1)
    return updated


def check(manifest_path: Path, html_path: Path) -> int:
    expected = build_portability_manifest(load_manifest(manifest_path))
    actual = extract_embedded_manifest(read_text(html_path))
    if actual == expected:
        print(
            "Agent Portability Lab Source Sync: PASS "
            f"({len(expected['targets'])} targets, {len(expected['capability_axes'])} capabilities match)"
        )
        return 0

    expected_ids = [str(item.get("id", "")) for item in expected.get("targets", []) if isinstance(item, dict)]
    actual_ids = [str(item.get("id", "")) for item in actual.get("targets", []) if isinstance(item, dict)]
    print("Agent Portability Lab Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(manifest_path: Path, html_path: Path) -> int:
    expected = build_portability_manifest(load_manifest(manifest_path))
    html = read_text(html_path)
    updated = sync_html(html, expected)
    if updated == html:
        print(
            "Agent Portability Lab Source Sync: PASS "
            f"({len(expected['targets'])} targets already current)"
        )
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Agent Portability Lab Source Sync: UPDATED ({len(expected['targets'])} targets written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/agent-portability-lab.html from agent-adapters/manifest.json.")
    parser.add_argument("manifest_path", nargs="?", default="agent-adapters/manifest.json")
    parser.add_argument("html_path", nargs="?", default="docs/agent-portability-lab.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated AGENT_PORTABILITY_MANIFEST block.")
    args = parser.parse_args()

    try:
        manifest_path = Path(args.manifest_path)
        html_path = Path(args.html_path)
        if args.write:
            return write(manifest_path, html_path)
        return check(manifest_path, html_path)
    except Exception as exc:
        print(f"Agent Portability Lab Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
