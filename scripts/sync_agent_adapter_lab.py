#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from export_agent_pack import BASELINE_PATHS


START_MARKER = "    // BEGIN GENERATED AGENT ADAPTER MANIFEST"
END_MARKER = "    // END GENERATED AGENT ADAPTER MANIFEST"

MANIFEST_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

MANIFEST_CONST_RE = re.compile(r"\s*const AGENT_ADAPTER_MANIFEST = (?P<payload>\{.*\});\s*$", re.DOTALL)


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


def normalize_target(target: dict[str, Any]) -> dict[str, Any]:
    entrypoints = target.get("entrypoints")
    if not isinstance(entrypoints, list):
        entrypoints = []
    return {
        "id": str(target.get("id", "")),
        "display": str(target.get("display", "")),
        "support_level": str(target.get("support_level", "")),
        "source_url": str(target.get("source_url", "")),
        "entrypoints": [str(item) for item in entrypoints],
        "invoke": str(target.get("invoke", "")),
        "install": str(target.get("install", "")),
        "contract": str(target.get("contract", "")),
    }


def build_lab_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    shared_references = manifest.get("shared_references")
    if not isinstance(shared_references, list):
        shared_references = []
    return {
        "schema": manifest.get("schema"),
        "canonical_skill": manifest.get("canonical_skill"),
        "canonical_contract": manifest.get("canonical_contract"),
        "adapter_audit": manifest.get("adapter_audit"),
        "pack_exporter": manifest.get("pack_exporter"),
        "pack_audit": manifest.get("pack_audit"),
        "checked_on": manifest.get("checked_on"),
        "baseline_paths": list(BASELINE_PATHS),
        "shared_references": [str(item) for item in shared_references],
        "targets": [normalize_target(target) for target in manifest.get("targets", []) if isinstance(target, dict)],
    }


def render_manifest_block(payload: dict[str, Any]) -> str:
    rendered = json.dumps(payload, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const AGENT_ADAPTER_MANIFEST = {rendered};\n{END_MARKER}"


def extract_embedded_manifest(html: str) -> dict[str, Any]:
    block_match = MANIFEST_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("agent adapter lab is missing generated manifest markers")
    const_match = MANIFEST_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("agent adapter lab generated block does not contain AGENT_ADAPTER_MANIFEST JSON")
    payload = json.loads(const_match.group("payload"))
    if not isinstance(payload, dict):
        raise ValueError("agent adapter lab manifest payload must be an object")
    return payload


def sync_html(html: str, payload: dict[str, Any]) -> str:
    if not MANIFEST_BLOCK_RE.search(html):
        raise ValueError("agent adapter lab is missing generated manifest markers")
    updated = MANIFEST_BLOCK_RE.sub(render_manifest_block(payload), html, count=1)
    target_count = len(payload.get("targets", []))
    entrypoint_count = len(
        {
            entrypoint
            for target in payload.get("targets", [])
            if isinstance(target, dict)
            for entrypoint in target.get("entrypoints", [])
            if isinstance(entrypoint, str)
        }
    )
    replacements = {
        r'(<strong id="metricTargets">).*?(</strong>)': str(target_count),
        r'(<strong id="metricEntrypoints">).*?(</strong>)': str(entrypoint_count),
        r'(<strong id="metricBaseline">).*?(</strong>)': str(len(payload.get("baseline_paths", []))),
        r'(<span id="checkedOn">).*?(</span>)': str(payload.get("checked_on", "")),
    }
    for pattern, value in replacements.items():
        updated = re.sub(pattern, rf"\g<1>{value}\2", updated, count=1)
    return updated


def check(manifest_path: Path, html_path: Path) -> int:
    expected = build_lab_manifest(load_manifest(manifest_path))
    actual = extract_embedded_manifest(read_text(html_path))
    if actual == expected:
        print(f"Agent Adapter Lab Source Sync: PASS ({len(expected['targets'])} targets match)")
        return 0

    expected_ids = [str(item.get("id", "")) for item in expected.get("targets", []) if isinstance(item, dict)]
    actual_ids = [str(item.get("id", "")) for item in actual.get("targets", []) if isinstance(item, dict)]
    print("Agent Adapter Lab Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(manifest_path: Path, html_path: Path) -> int:
    expected = build_lab_manifest(load_manifest(manifest_path))
    html = read_text(html_path)
    updated = sync_html(html, expected)
    if updated == html:
        print(f"Agent Adapter Lab Source Sync: PASS ({len(expected['targets'])} targets already current)")
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Agent Adapter Lab Source Sync: UPDATED ({len(expected['targets'])} targets written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/agent-adapter-lab.html from agent-adapters/manifest.json.")
    parser.add_argument("manifest_path", nargs="?", default="agent-adapters/manifest.json")
    parser.add_argument("html_path", nargs="?", default="docs/agent-adapter-lab.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated AGENT_ADAPTER_MANIFEST block.")
    args = parser.parse_args()

    try:
        manifest_path = Path(args.manifest_path)
        html_path = Path(args.html_path)
        if args.write:
            return write(manifest_path, html_path)
        return check(manifest_path, html_path)
    except Exception as exc:
        print(f"Agent Adapter Lab Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
