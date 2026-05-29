#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


EXPECTED_TARGETS = (
    "aider",
    "amazon-q",
    "chatgpt-gpts",
    "claude-code",
    "cline",
    "codex",
    "continue",
    "cursor",
    "devin",
    "gemini-cli",
    "generic-agents-md",
    "github-copilot",
    "jetbrains-junie",
    "kilo-code",
    "opencode",
    "roo-code",
    "windsurf",
    "zed",
)

REQUIRED_ALL_EXPORT_FILES = (
    "AGENT_PACK_MANIFEST.json",
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
    "agent-adapters/README.md",
    "agent-adapters/manifest.json",
    "docs/agent-adapters.md",
    "docs/agent-adapter-lab.html",
    "docs/agent-portability-lab.html",
    "docs/assets/agent-compatibility-grid.svg",
    "docs/assets/agent-pack-export-flow.svg",
    "docs/assets/agent-adapter-lab-flow.svg",
    "docs/assets/universal-agent-bridge-map.svg",
    ".github/ISSUE_TEMPLATE/agent_adapter_improvement.yml",
    ".github/ISSUE_TEMPLATE/agent_portability_request.yml",
    "scripts/export_agent_pack.py",
    "scripts/agent_adapter_audit.py",
    "scripts/agent_pack_export_audit.py",
    "scripts/sync_agent_adapter_lab.py",
    "scripts/agent_adapter_lab_audit.py",
    "scripts/sync_agent_portability_lab.py",
    "scripts/agent_portability_lab_audit.py",
    "prompts/prompt-recipes.md",
    "skill/mbti-typing/SKILL.md",
    "skill/mbti-typing/scripts/typing_session.py",
    "skill/mbti-typing/references/question-bank.md",
    "skill/mbti-typing/references/pair-duels.md",
)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def run_command(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", "scripts/export_agent_pack.py", "--root", str(root), *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def audit(root: Path) -> list[Check]:
    checks: list[Check] = []
    exporter = root / "scripts/export_agent_pack.py"
    checks.append(Check("file:exporter", exporter.exists(), "exporter script exists"))

    list_run = run_command(root, ["--list-targets"])
    listed_targets = tuple(sorted(line.strip() for line in list_run.stdout.splitlines() if line.strip()))
    checks.append(Check("list_targets:exit", list_run.returncode == 0, "target listing exits successfully"))
    checks.append(Check("list_targets:coverage", listed_targets == EXPECTED_TARGETS, f"targets={listed_targets}"))

    dry_run = run_command(root, ["--dry-run", "--target", "cursor", "--target", "cline"])
    checks.append(Check("dry_run:exit", dry_run.returncode == 0, "dry run exits successfully"))
    try:
        dry_payload = json.loads(dry_run.stdout)
    except Exception as exc:
        dry_payload = {}
        checks.append(Check("dry_run:json", False, f"dry run emits JSON: {exc}"))
    else:
        checks.append(Check("dry_run:json", isinstance(dry_payload, dict), "dry run emits a JSON object"))
        checks.append(Check("dry_run:schema", dry_payload.get("schema") == "mbti-typing-agent-pack/v1", "dry run schema is pinned"))
        checks.append(Check("dry_run:targets", dry_payload.get("selected_targets") == ["cursor", "cline"], "dry run keeps requested target order"))
        dry_files = {item.get("source") for item in dry_payload.get("files", []) if isinstance(item, dict)}
        checks.append(Check("dry_run:baseline_skill", "skill/mbti-typing" in dry_files, "dry run includes canonical skill directory"))
        checks.append(Check("dry_run:target_entrypoints", {".cursor/rules/mbti-typing.mdc", ".cline/skills/mbti-typing/SKILL.md"} <= dry_files, "dry run includes selected entrypoints"))

    with tempfile.TemporaryDirectory(prefix="mbti-agent-pack-audit-") as tmp:
        tmp_root = Path(tmp)
        all_dest = tmp_root / "all"
        all_run = run_command(root, ["--dest", str(all_dest), "--target", "all"])
        checks.append(Check("all_export:exit", all_run.returncode == 0, "all-target export exits successfully"))
        pack_manifest_path = all_dest / "AGENT_PACK_MANIFEST.json"
        checks.append(Check("all_export:manifest_file", pack_manifest_path.exists(), "export writes AGENT_PACK_MANIFEST.json"))
        if pack_manifest_path.exists():
            pack_manifest = read_json(pack_manifest_path)
            selected = tuple(sorted(pack_manifest.get("selected_targets", [])))
            planned_files = [
                item
                for item in pack_manifest.get("files", [])
                if isinstance(item, dict) and isinstance(item.get("destination"), str)
            ]
            checks.append(Check("all_export:schema", pack_manifest.get("schema") == "mbti-typing-agent-pack/v1", "export manifest schema is pinned"))
            checks.append(Check("all_export:target_coverage", selected == EXPECTED_TARGETS, f"targets={selected}"))
            checks.append(Check("all_export:file_plan", len(planned_files) >= 20, f"file groups={len(planned_files)}"))
            checks.append(Check("all_export:safety_contract", "falsifier and revision trigger" in pack_manifest.get("safety_contract", []), "pack manifest preserves safety contract"))
            missing = [rel for rel in REQUIRED_ALL_EXPORT_FILES if not (all_dest / rel).exists()]
            checks.append(Check("all_export:required_files", not missing, f"missing={missing}"))
            missing_planned = [
                item.get("destination", "")
                for item in planned_files
                if not (all_dest / str(item.get("destination"))).exists()
            ]
            checks.append(Check("all_export:planned_files_exist", not missing_planned, f"missing planned={missing_planned}"))

        selective_dest = tmp_root / "selective"
        selective_run = run_command(root, ["--dest", str(selective_dest), "--target", "cursor", "--target", "continue"])
        checks.append(Check("selective_export:exit", selective_run.returncode == 0, "selective export exits successfully"))
        if (selective_dest / "AGENT_PACK_MANIFEST.json").exists():
            selective_manifest = read_json(selective_dest / "AGENT_PACK_MANIFEST.json")
            checks.append(Check("selective_export:targets", selective_manifest.get("selected_targets") == ["cursor", "continue"], "selective export records requested targets"))
            checks.append(Check("selective_export:cursor", (selective_dest / ".cursor/rules/mbti-typing.mdc").exists(), "selective export includes Cursor rule"))
            checks.append(Check("selective_export:continue", (selective_dest / ".continue/rules/mbti-typing.md").exists(), "selective export includes Continue rule"))
            checks.append(Check("selective_export:no_copilot", not (selective_dest / ".github/copilot-instructions.md").exists(), "selective export omits unrequested Copilot adapter"))

        blocked_dest = tmp_root / "blocked"
        blocked_dest.mkdir()
        marker = blocked_dest / "keep.txt"
        marker.write_text("do not remove\n", encoding="utf-8")
        blocked_run = run_command(root, ["--dest", str(blocked_dest), "--target", "cursor"])
        checks.append(Check("safety:non_empty_dest_blocked", blocked_run.returncode != 0 and marker.exists(), "non-empty destination is blocked without --force"))

    unknown_run = run_command(root, ["--dry-run", "--target", "unknown-agent"])
    checks.append(Check("safety:unknown_target", unknown_run.returncode != 0 and "unknown target" in unknown_run.stderr, "unknown target fails clearly"))
    return checks


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    checks = audit(root.resolve())
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Agent Pack Export Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
