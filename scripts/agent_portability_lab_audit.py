#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from sync_agent_portability_lab import build_portability_manifest, extract_embedded_manifest, load_manifest


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "metricTargets",
    "metricCapabilities",
    "checkedOn",
    "targetSelect",
    "hostNameInput",
    "capabilityList",
    "chosenCapabilityCount",
    "targetSummary",
    "bridgePlanOutput",
    "portableInstallOutput",
    "adapterDraftOutput",
    "portabilityIssueOutput",
    "copyBridgePlan",
    "copyPortableInstall",
    "copyAdapterDraft",
    "downloadPortabilityJson",
    "copyPortabilityIssue",
]

REQUIRED_TERMS = [
    "MBTI Typing Skill Agent Portability Lab",
    "Universal Agent Bridge Lab",
    "Agent Portability Lab",
    "agent-portability-lab/v1",
    "agent_portability_request.yml",
    "canonical protocol",
    "unknown host",
    "capability-first",
    "Native question UI",
    "native_question_ui",
    "candidate set",
    "serious runner-up",
    "evidence ledger",
    "falsifier",
    "safety boundary",
    "AGENTS.md",
    "SKILL.md",
    "Codex",
    "Claude Code",
    "Cursor",
    "opencode",
    "GitHub Copilot",
    "Windsurf",
    "Cline",
    "Continue",
    "Amazon Q",
    "Roo Code",
    "Kilo Code",
    "local-first",
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


def run(html_path: Path, manifest_path: Path, issue_template_path: Path) -> int:
    html = read_text(html_path)
    issue_template = read_text(issue_template_path)
    manifest = load_manifest(manifest_path)
    expected = build_portability_manifest(manifest)
    try:
        embedded = extract_embedded_manifest(html)
    except Exception as exc:
        embedded = {}
        embedded_error = str(exc)
    else:
        embedded_error = ""

    target_ids = [target.get("id") for target in expected.get("targets", []) if isinstance(target, dict)]
    capability_ids = [axis.get("id") for axis in expected.get("capability_axes", []) if isinstance(axis, dict)]

    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Agent Portability Lab</title>" in html, "product title is present"),
        Check("html:single_script", html.count("<script>") == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("html:issue_template_link", "agent_portability_request.yml" in html, "page names the portability issue template"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:download_json", "new Blob" in html and "application/json" in html, "JSON download is implemented"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-agent-portability-lab-state" in html, "capability choices persist locally"),
        Check("js:bridge_plan", "buildBridgePlan" in html and "capability-first" in html, "bridge plan builder exists"),
        Check("js:adapter_draft", "buildAdapterDraft" in html and "agent-portability-lab/v1" in html, "adapter draft builder exists"),
        Check("js:issue_seed", "buildIssueSeed" in html and "agent_portability_request.yml" in html, "portability issue seed exists"),
        Check("sync:embedded_manifest_parse", not embedded_error, f"embedded manifest parses: {embedded_error}"),
        Check("sync:embedded_manifest_exact", embedded == expected, "embedded manifest matches agent-adapters/manifest.json plus capability axes"),
        Check("sync:target_count", len(embedded.get("targets", [])) >= 18, "embedded manifest covers at least eighteen targets"),
        Check("sync:capability_count", len(embedded.get("capability_axes", [])) >= 8, "embedded manifest covers capability-first portability axes"),
        Check("issue_template:contract", all(term in issue_template for term in ("Agent portability request", "unknown host", "candidate set", "serious runner-up", "evidence ledger", "falsifier", "safety boundary")), "portability issue template preserves protocol terms"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"target:{target_id}", str(target_id) in html, "manifest target appears in generated page") for target_id in target_ids)
    checks.extend(Check(f"capability:{capability_id}", str(capability_id) in html, "capability axis appears in generated page") for capability_id in capability_ids)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Agent Portability Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    html_path = Path(argv[1]) if len(argv) > 1 else Path("docs/agent-portability-lab.html")
    manifest_path = Path(argv[2]) if len(argv) > 2 else Path("agent-adapters/manifest.json")
    issue_template_path = Path(argv[3]) if len(argv) > 3 else Path(".github/ISSUE_TEMPLATE/agent_portability_request.yml")
    return run(html_path, manifest_path, issue_template_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
