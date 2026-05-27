#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


OVERCLAIM_PATTERNS: list[tuple[str, str]] = [
    (r"\b100\s*%\b|百分之百", "Avoid absolute certainty."),
    (r"99\.\d+\s*%|99\s*%", "High-precision percentages need explicit heuristic framing."),
    (r"scientifically proven|科学证明|科学证实", "Do not frame interview typing as scientifically proven."),
    (r"world'?s most accurate|世界上最准|最准确", "Avoid unverifiable superiority claims."),
    (r"definitely|必然是|一定是|绝对是", "Use calibrated type language."),
    (r"临床诊断|诊断为|病理", "Do not turn MBTI typing into clinical diagnosis."),
    (r"招聘|录用|筛选候选人|岗位筛选", "MBTI should not be used for hiring or selection."),
]

SECTION_PATTERNS: list[tuple[str, str, str]] = [
    ("short_answer", r"短.{0,4}结论|short answer|best-supported|最佳", "Missing short answer / best-supported formulation section."),
    ("runner_up", r"runner.?up|备选|候选|alternative|为什么不是|排除", "Missing runner-up or alternatives section."),
    ("evidence", r"证据|evidence|依据|观察", "Missing evidence section."),
    ("cross_check", r"big five|五因素|大五|attachment|依恋|culture|文化|enneagram|九型", "Missing cross-framework check or explicit reason to skip it."),
    ("uncertainty", r"不确定|uncertainty|局限|caveat|限制", "Missing uncertainty/caveat section."),
    ("falsifier", r"证伪|falsif|如果.*错|would change|改变结论", "Missing falsifier / what would change the conclusion section."),
]

STRUCTURED_REQUIRED_KEYS = {
    "short_answer": "Structured report missing short_answer.",
    "leading_formulation": "Structured report missing leading_formulation.",
    "runner_up": "Structured report missing runner_up.",
    "evidence": "Structured report missing evidence list.",
    "alternatives": "Structured report missing alternatives / differential diagnosis.",
    "cross_framework_check": "Structured report missing cross_framework_check.",
    "uncertainty": "Structured report missing uncertainty.",
    "falsifiers": "Structured report missing falsifiers.",
    "framework_boundaries": "Structured report missing framework_boundaries.",
}


def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_dir():
        raise IsADirectoryError(path)
    return path.read_text(encoding="utf-8")


def audit_text(text: str, include_sections: bool = True) -> list[Finding]:
    findings: list[Finding] = []
    lower_text = text.lower()

    for pattern, message in OVERCLAIM_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            findings.append(Finding("high", "overclaim", message))

    if include_sections:
        for code, pattern, message in SECTION_PATTERNS:
            if not re.search(pattern, lower_text, flags=re.IGNORECASE):
                findings.append(Finding("medium", f"missing_{code}", message))

    if re.search(r"\b[EI][NS][TF][JP]-[AT]\b", text) and not re.search(r"16Personalities|A/T|Assertive|Turbulent|官方|not official", text, flags=re.IGNORECASE):
        findings.append(Finding("medium", "at_boundary", "A/T appears without a 16Personalities-style boundary note."))

    if re.search(r"\b(Te|Ti|Fe|Fi|Ne|Ni|Se|Si)\s*[:：]?\s*\d{2,3}\b", text) and not re.search(r"heuristic|启发式|非测量|not.*measured", text, flags=re.IGNORECASE):
        findings.append(Finding("medium", "function_scores", "Function scores appear without a non-measured/heuristic caveat."))

    if not findings:
        findings.append(Finding("info", "pass", "No obvious structural or overclaiming issues found by heuristic audit."))

    return findings


def _maybe_json(text: str) -> Any | None:
    stripped = text.lstrip()
    if not stripped.startswith("{"):
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def audit_structured_report(payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    for key, message in STRUCTURED_REQUIRED_KEYS.items():
        if key not in payload:
            findings.append(Finding("high", "structured_missing", message))

    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list) or not evidence:
        findings.append(Finding("high", "structured_evidence", "Structured report needs a non-empty evidence list."))
        evidence = []

    evidence_ids = set()
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            findings.append(Finding("high", "structured_evidence_item", f"evidence[{index}] must be an object."))
            continue
        item_id = str(item.get("id", ""))
        if item_id:
            evidence_ids.add(item_id)
        for key in ("id", "observation", "supports", "contradicts", "context"):
            if key not in item:
                findings.append(Finding("medium", "structured_evidence_item", f"evidence[{index}] missing {key}."))

    claims = payload.get("claims", [])
    if claims is not None and not isinstance(claims, list):
        findings.append(Finding("high", "structured_claims", "claims must be a list when provided."))
        claims = []

    if isinstance(claims, list):
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                findings.append(Finding("high", "structured_claim", f"claims[{index}] must be an object."))
                continue
            claim_text = str(claim.get("claim", "")).strip()
            linked = claim.get("evidence_ids", [])
            if not claim_text:
                findings.append(Finding("medium", "structured_claim", f"claims[{index}] missing claim text."))
            if not isinstance(linked, list) or not linked:
                findings.append(Finding("high", "claim_without_evidence", f"claims[{index}] has no evidence_ids."))
            else:
                unknown = sorted(str(item) for item in linked if str(item) not in evidence_ids)
                if unknown:
                    findings.append(Finding("high", "claim_unknown_evidence", f"claims[{index}] references unknown evidence ids: {', '.join(unknown)}."))
            if "caveat" not in claim:
                findings.append(Finding("medium", "claim_without_caveat", f"claims[{index}] missing caveat."))

    if not payload.get("runner_up"):
        findings.append(Finding("high", "structured_runner_up", "Structured report needs a serious runner_up."))
    if not payload.get("falsifiers"):
        findings.append(Finding("high", "structured_falsifiers", "Structured report needs falsifiers."))
    if not payload.get("framework_boundaries"):
        findings.append(Finding("high", "structured_boundaries", "Structured report needs framework boundary notes."))

    serialized = json.dumps(payload, ensure_ascii=False)
    findings.extend(finding for finding in audit_text(serialized, include_sections=False) if finding.code != "pass")

    if not findings:
        findings.append(Finding("info", "pass", "Structured report passed heuristic audit."))
    return findings


def _format_markdown(findings: list[Finding]) -> str:
    lines = ["# MBTI Report Audit", ""]
    for finding in findings:
        lines.append(f"- [{finding.severity}] {finding.code}: {finding.message}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristically audit an MBTI report for missing safeguards and overclaiming.")
    parser.add_argument("path", help="Markdown or text report to audit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--fail-on-findings", action="store_true", help="Exit with code 2 when medium/high findings are present.")
    args = parser.parse_args()

    try:
        text = _read_text(Path(args.path))
        payload = _maybe_json(text)
        findings = audit_structured_report(payload) if isinstance(payload, dict) else audit_text(text)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
    else:
        print(_format_markdown(findings))
    if args.fail_on_findings and any(finding.severity in {"medium", "high"} for finding in findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
