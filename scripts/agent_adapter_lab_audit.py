#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from sync_agent_adapter_lab import build_lab_manifest, extract_embedded_manifest, load_manifest


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "metricTargets",
    "metricEntrypoints",
    "metricBaseline",
    "checkedOn",
    "targetSearch",
    "supportFilter",
    "targetList",
    "visibleTargetCount",
    "selectAllTargets",
    "selectCoreTargets",
    "clearTargets",
    "selectedTargetCount",
    "fileGroupCount",
    "packCommandOutput",
    "installChecklistOutput",
    "adapterReceiptOutput",
    "issueSeedOutput",
    "selectedTargetSummary",
    "copyPackCommand",
    "copyInstallChecklist",
    "copyAdapterJson",
    "downloadAdapterJson",
    "copyIssueSeed",
]

REQUIRED_TERMS = [
    "MBTI Typing Skill Agent Adapter Lab",
    "Agent Adoption Lab",
    "Codex",
    "Claude Code",
    "Cursor",
    "opencode",
    "Gemini CLI",
    "GitHub Copilot",
    "Windsurf",
    "Cline",
    "Continue",
    "aider",
    "AGENTS.md",
    "AGENT_PACK_MANIFEST.json",
    "scripts/export_agent_pack.py",
    "scripts/agent_adapter_audit.py",
    "scripts/agent_pack_export_audit.py",
    "scripts/agent_adapter_lab_audit.py",
    "agent_adapter_improvement.yml",
    "candidate set",
    "serious runner-up",
    "evidence ledger",
    "falsifier",
    "safety boundary",
    "source-of-truth sync",
    "local-first",
    "agent-adapter-lab/v1",
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


def run(html_path: Path, manifest_path: Path) -> int:
    html = read_text(html_path)
    manifest = load_manifest(manifest_path)
    expected = build_lab_manifest(manifest)
    try:
        embedded = extract_embedded_manifest(html)
    except Exception as exc:
        embedded = {}
        embedded_error = str(exc)
    else:
        embedded_error = ""

    target_ids = [target.get("id") for target in expected.get("targets", []) if isinstance(target, dict)]
    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Agent Adapter Lab</title>" in html, "product title is present"),
        Check("html:single_script", html.count("<script>") == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("html:issue_template_link", "agent_adapter_improvement.yml" in html, "page names the agent adapter issue template"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:download_json", "new Blob" in html and "application/json" in html, "JSON download is implemented"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-agent-adapter-lab-state" in html, "adapter selection persists locally"),
        Check("js:pack_command", "buildPackCommand" in html and "--target" in html and "--dest" in html, "pack command builder exists"),
        Check("js:install_checklist", "buildInstallChecklist" in html and "Install checklist" in html, "install checklist builder exists"),
        Check("js:receipt", "buildReceipt" in html and "schema_version" in html and "agent-adapter-lab/v1" in html, "adapter receipt builder exists"),
        Check("js:issue_seed", "buildIssueSeed" in html and "agent_adapter_improvement.yml" in html, "agent adapter issue seed exists"),
        Check("sync:embedded_manifest_parse", not embedded_error, f"embedded manifest parses: {embedded_error}"),
        Check("sync:embedded_manifest_exact", embedded == expected, "embedded manifest matches agent-adapters/manifest.json plus export baseline"),
        Check("sync:target_count", len(embedded.get("targets", [])) >= 18, "embedded manifest covers at least eighteen targets"),
        Check("sync:baseline_paths", "docs/agent-adapter-lab.html" in embedded.get("baseline_paths", []), "baseline exports the public Agent Adapter Lab"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"target:{target_id}", str(target_id) in html, "manifest target appears in generated page") for target_id in target_ids)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Agent Adapter Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    html_path = Path(argv[1]) if len(argv) > 1 else Path("docs/agent-adapter-lab.html")
    manifest_path = Path(argv[2]) if len(argv) > 2 else Path("agent-adapters/manifest.json")
    return run(html_path, manifest_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
