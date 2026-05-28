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
    "subjectConsent",
    "publicIssueOk",
    "dataMinimized",
    "withdrawalOk",
    "noHighStakes",
    "candidateSetInput",
    "leadingInput",
    "runnerInput",
    "confidenceSelect",
    "falsifierInput",
    "obsNormal",
    "obsStress",
    "obsRecovery",
    "obsReflection",
    "feltRightInput",
    "feltWrongInput",
    "nextPromptInput",
    "runAudit",
    "privacyScore",
    "scoreMirror",
    "gateSummary",
    "safetyGrid",
    "packetOutput",
    "issueSeedOutput",
    "copyPacket",
    "downloadPacket",
    "copyIssueSeed",
]


REQUIRED_TERMS = [
    "MBTI Typing Skill Follow-Up Lab",
    "Consent Packet Builder",
    "Privacy Gate",
    "Copy Follow-Up JSON",
    "Copy Issue Seed",
    "Download JSON",
    "consented_followup.yml",
    "Use $mbti-typing",
    "not a clinical instrument",
    "local-first",
    "redaction",
    "withdrawal",
    "public-safe",
]


FORBIDDEN_TERMS = [
    "<script src",
    " src=",
    "innerHTML",
    "insertAdjacentHTML",
    "document.write",
    "eval(",
]


TYPE_CODES = [
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run(path: Path) -> int:
    html = read_text(path)
    checks: list[Check] = [
        Check("html:title", "<title>MBTI Typing Skill Follow-Up Lab</title>" in html, "product title is present"),
        Check("html:single_script", len(re.findall(r"<script>", html)) == 1, "one inline script block is present"),
        Check("html:no_external_runtime", all(term not in html for term in FORBIDDEN_TERMS), "page stays local and avoids unsafe HTML injection"),
        Check("html:repo_readme_link", "https://github.com/Zaoqu-Liu/mbti-typing-skill#readme" in html, "public page links to the GitHub README"),
        Check("html:issue_template_link", "issues/new?template=consented_followup.yml" in html, "page links to the consented follow-up issue template"),
        Check("js:all_16_types", all(type_code in html for type_code in TYPE_CODES), "all 16 type codes remain visible"),
        Check("js:dom_safety", "textContent" in html and "replaceChildren" in html and "document.createElement" in html, "rendering uses DOM nodes"),
        Check("js:clipboard", "navigator.clipboard.writeText" in html, "copy actions use clipboard with fallback"),
        Check("js:download_json", "new Blob" in html and "application/json" in html, "JSON download is implemented"),
        Check("js:local_persistence", "localStorage.setItem" in html and "mbti-typing-follow-up-lab-state" in html, "follow-up drafts persist locally"),
        Check("js:privacy_scanner", "scanForSensitiveText" in html and "HIGH_RISK_TERMS" in html, "privacy scanner exists"),
        Check("js:packet_builder", "buildFollowUpPacket" in html and "consented-followup/v1" in html, "packet builder emits the consented follow-up schema"),
        Check("js:issue_seed", "buildIssueSeed" in html and "consented_followup.yml" in html, "issue seed builder exists"),
        Check("js:placeholder_gate", "hasPlaceholder" in html and "[DATE_RANGE]" in html and "[RELATIONSHIP_CONTEXT]" in html, "redaction placeholder gate exists"),
        Check("js:gate_count", html.count("[\"") >= 9 and "auditPacket" in html, "privacy gate checks are present"),
    ]

    checks.extend(Check(f"id:{item}", f'id="{item}"' in html, "required interactive element id exists") for item in REQUIRED_IDS)
    checks.extend(Check(f"term:{term}", term in html, "required product/safety term exists") for term in REQUIRED_TERMS)
    checks.extend(Check(f"forbid:{term}", term not in html, "page avoids external runtime or unsafe HTML injection") for term in FORBIDDEN_TERMS)

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Follow-Up Lab Audit: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/follow-up-lab.html")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
