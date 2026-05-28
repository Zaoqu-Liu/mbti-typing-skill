#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_IDS = [
    "claimInput",
    "evidenceInput",
    "candidateGrid",
    "ledgerTable",
    "duelGrid",
    "questionStack",
    "reportOutput",
    "sessionStateOutput",
    "copyPrompt",
    "copyShareLink",
    "importJson",
    "downloadJson",
    "saveLocal",
]


REQUIRED_TYPES = [
    "INTJ",
    "INTP",
    "ENTJ",
    "ENTP",
    "INFJ",
    "INFP",
    "ENFJ",
    "ENFP",
    "ISTJ",
    "ISFJ",
    "ESTJ",
    "ESFJ",
    "ISTP",
    "ISFP",
    "ESTP",
    "ESFP",
]


REQUIRED_TERMS = [
    "not a clinical instrument",
    "not a psychometric result",
    "serious runner-up",
    "Strongest falsifier",
    "Use $mbti-typing",
    "Copy Share Link",
    "Import JSON",
    "share/v1",
    "mbti-typing-session-lab-state",
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


def script_text(html: str) -> str:
    match = re.search(r"<script>([\s\S]*)</script>", html)
    return match.group(1) if match else ""


def run(path: Path) -> int:
    html = read_text(path)
    script = script_text(html)
    checks: list[Check] = []

    checks.append(Check("html:title", "MBTI Typing Skill Session Lab" in html, "product title is visible"))
    checks.append(Check("html:single_script", html.count("<script>") == 1 and bool(script), "one inline script block is present"))
    checks.append(Check("html:share_controls", "Copy Share Link" in html and "Import JSON" in html, "share and import controls are visible"))
    checks.append(Check("html:proof_strip", "shareable URL hash plus JSON recovery" in html, "share/recovery proof is visible"))
    checks.append(Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"))
    checks.append(Check("html:repo_prompts_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill/blob/main/prompts/prompt-recipes.md" in html, "public page links to prompt recipes on GitHub"))

    for item_id in REQUIRED_IDS:
        checks.append(Check(f"id:{item_id}", f'id="{item_id}"' in html, "required interactive element id exists"))

    for type_code in REQUIRED_TYPES:
        checks.append(Check(f"type:{type_code}", type_code in html, "all 16 type codes remain discoverable"))

    for term in REQUIRED_TERMS:
        checks.append(Check(f"term:{term}", term in html, "required product/safety term exists"))

    for term in FORBIDDEN_TERMS:
        checks.append(Check(f"forbid:{term}", term not in html, "Session Lab stays local and avoids unsafe HTML injection"))

    checks.extend(
        [
            Check("js:text_encoder", "new TextEncoder()" in script and "new TextDecoder()" in script, "share links support unicode text safely"),
            Check("js:hash_restore", "window.location.hash" in script and "session=" in script and "loadSessionFromHash" in script, "URL hash session restore exists"),
            Check("js:hashchange_listener", 'window.addEventListener("hashchange", loadSessionFromHash)' in script, "same-tab share links can refresh the session"),
            Check("js:base64url", 'replace(/\\+/g, "-")' in script and 'replace(/\\//g, "_")' in script, "share payload uses URL-safe base64"),
            Check("js:json_import", "JSON.parse(sessionStateOutput.value)" in script and "applySessionPayload" in script, "editable JSON can restore a session"),
            Check("js:clipboard", "navigator.clipboard.writeText" in script, "copy actions use clipboard with fallback"),
            Check("js:download", "new Blob" in script and "application/json" in script and "URL.createObjectURL" in script, "JSON download is implemented"),
            Check("js:local_persistence", "localStorage.setItem" in script and "localStorage.getItem" in script, "local persistence is implemented"),
            Check("js:dom_safety", "textContent" in script and "replaceChildren" in script, "core renderers use text nodes instead of HTML injection"),
            Check("js:mode_guard", "allowedModes" in script and "setActiveMode" in script, "imported modes are constrained"),
            Check("js:candidate_count", ".slice(0, 5)" in script, "candidate board remains focused"),
        ]
    )

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Session Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/session-lab.html")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
