#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PACK_SCHEMA = "mbti-typing-agent-pack/v1"
BASELINE_PATHS = (
    "skill/mbti-typing",
    "AGENTS.md",
    "CONVENTIONS.md",
    "agent-adapters/README.md",
    "agent-adapters/manifest.json",
    "docs/agent-adapters.md",
    "docs/agent-adapter-lab.html",
    "docs/assets/agent-compatibility-grid.svg",
    "docs/assets/agent-pack-export-flow.svg",
    "docs/assets/agent-adapter-lab-flow.svg",
    "prompts/prompt-recipes.md",
    ".github/ISSUE_TEMPLATE/agent_adapter_improvement.yml",
    "scripts/export_agent_pack.py",
    "scripts/agent_adapter_audit.py",
    "scripts/agent_pack_export_audit.py",
    "scripts/sync_agent_adapter_lab.py",
    "scripts/agent_adapter_lab_audit.py",
)
IGNORE_NAMES = {"__pycache__", ".DS_Store"}


@dataclass(frozen=True)
class FilePlan:
    source: str
    destination: str
    kind: str
    reason: str


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def resolve_under(root: Path, rel: str) -> Path:
    root_resolved = root.resolve()
    path = (root_resolved / rel).resolve()
    try:
        path.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {rel}") from exc
    return path


def load_manifest(root: Path) -> dict[str, Any]:
    manifest = read_json(root / "agent-adapters/manifest.json")
    if manifest.get("schema") != "mbti-typing-agent-adapters/v1":
        raise ValueError("unsupported adapter manifest schema")
    targets = manifest.get("targets", [])
    if not isinstance(targets, list) or not targets:
        raise ValueError("adapter manifest has no targets")
    return manifest


def target_by_id(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    targets: dict[str, dict[str, Any]] = {}
    for target in manifest.get("targets", []):
        if not isinstance(target, dict):
            raise ValueError("every manifest target must be an object")
        target_id = target.get("id")
        if not isinstance(target_id, str) or not target_id:
            raise ValueError("every manifest target needs an id")
        targets[target_id] = target
    return targets


def select_targets(manifest: dict[str, Any], requested: list[str]) -> list[dict[str, Any]]:
    targets = target_by_id(manifest)
    requested_ids = requested or ["all"]
    if "all" in requested_ids:
        return [target for target in manifest["targets"] if isinstance(target, dict)]

    unknown = sorted(set(requested_ids) - set(targets))
    if unknown:
        known = ", ".join(sorted(targets))
        raise ValueError(f"unknown target(s): {', '.join(unknown)}; known targets: {known}")
    return [targets[target_id] for target_id in requested_ids]


def make_file_plan(root: Path, manifest: dict[str, Any], selected: list[dict[str, Any]]) -> list[FilePlan]:
    plans: list[FilePlan] = []
    seen: set[str] = set()
    seen_dirs: set[str] = set()

    def add(rel: str, reason: str) -> None:
        if rel in seen:
            return
        if any(rel.startswith(f"{directory}/") for directory in seen_dirs):
            return
        source = resolve_under(root, rel)
        if not source.exists():
            raise FileNotFoundError(f"missing required export source: {rel}")
        kind = "dir" if source.is_dir() else "file"
        plans.append(FilePlan(source=rel, destination=rel, kind=kind, reason=reason))
        seen.add(rel)
        if kind == "dir":
            seen_dirs.add(rel)

    for rel in BASELINE_PATHS:
        add(rel, "baseline portable protocol and docs")

    for target in selected:
        target_id = str(target["id"])
        for rel in target.get("entrypoints", []):
            if not isinstance(rel, str):
                raise ValueError(f"target {target_id} contains a non-string entrypoint")
            add(rel, f"{target_id} entrypoint")

    return plans


def copy_plan(root: Path, dest: Path, plans: list[FilePlan], force: bool) -> None:
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(f"destination is not empty: {dest}; pass --force to merge into it")
    dest.mkdir(parents=True, exist_ok=True)

    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in IGNORE_NAMES}

    for plan in plans:
        source = resolve_under(root, plan.source)
        target = dest / plan.destination
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=force, ignore=ignore)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not force:
                raise FileExistsError(f"destination file already exists: {target}")
            shutil.copy2(source, target)


def build_pack_manifest(manifest: dict[str, Any], selected: list[dict[str, Any]], plans: list[FilePlan]) -> dict[str, Any]:
    return {
        "schema": PACK_SCHEMA,
        "source_manifest_schema": manifest.get("schema"),
        "source_checked_on": manifest.get("checked_on"),
        "canonical_skill": manifest.get("canonical_skill"),
        "canonical_contract": manifest.get("canonical_contract"),
        "selected_targets": [target["id"] for target in selected],
        "entrypoints": {
            target["id"]: target.get("entrypoints", [])
            for target in selected
        },
        "invoke": {
            target["id"]: target.get("invoke", "")
            for target in selected
        },
        "install": {
            target["id"]: target.get("install", "")
            for target in selected
        },
        "files": [asdict(plan) for plan in plans],
        "safety_contract": [
            "candidate set with serious runner-up",
            "evidence ledger",
            "falsifier and revision trigger",
            "no clinical, hiring, legal, medical, financial, or deterministic use",
        ],
    }


def export_pack(root: Path, dest: Path, requested_targets: list[str], force: bool, dry_run: bool) -> dict[str, Any]:
    manifest = load_manifest(root)
    selected = select_targets(manifest, requested_targets)
    plans = make_file_plan(root, manifest, selected)
    pack_manifest = build_pack_manifest(manifest, selected, plans)
    if dry_run:
        return pack_manifest
    copy_plan(root, dest, plans, force)
    (dest / "AGENT_PACK_MANIFEST.json").write_text(
        json.dumps(pack_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return pack_manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a portable MBTI Typing Skill agent pack.")
    parser.add_argument("--root", default=".", help="Repository root containing agent-adapters/manifest.json.")
    parser.add_argument("--dest", default="agent-pack", help="Destination directory for the exported pack.")
    parser.add_argument("--target", action="append", default=[], help="Target id to export; repeatable. Use all for every target.")
    parser.add_argument("--force", action="store_true", help="Merge into a non-empty destination.")
    parser.add_argument("--dry-run", action="store_true", help="Print the export plan JSON without writing files.")
    parser.add_argument("--list-targets", action="store_true", help="Print known target ids and exit.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    try:
        manifest = load_manifest(root)
        if args.list_targets:
            print("\n".join(target_by_id(manifest).keys()))
            return 0
        pack_manifest = export_pack(
            root=root,
            dest=Path(args.dest).resolve(),
            requested_targets=args.target,
            force=bool(args.force),
            dry_run=bool(args.dry_run),
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps(pack_manifest, indent=2, ensure_ascii=False))
    else:
        print(
            f"Exported {len(pack_manifest['files'])} file groups for "
            f"{len(pack_manifest['selected_targets'])} target(s) to {Path(args.dest).resolve()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
