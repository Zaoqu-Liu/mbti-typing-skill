#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_SOURCES = {"synthetic", "consented-anonymized", "public-synthetic"}
ALLOWED_REDACTION = {"public-safe-synthetic", "public-safe-anonymized"}
ALLOWED_CONFIDENCE = {"low", "medium", "medium-high", "high"}
REQUIRED_STATES = {"normal", "stress", "conflict", "recovery", "reflection", "public_performance", "relationship"}

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?\d[\s().-]*){9,}")
URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
HANDLE_RE = re.compile(r"(?<!\w)@[A-Za-z0-9_]{3,}")
EXACT_DATE_RE = re.compile(r"\b(?:20\d{2}|19\d{2})[-/](?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12]\d|3[01])\b")
FORBIDDEN_CONTEXT_TERMS = {
    "hospital",
    "medical",
    "diagnosis",
    "lawsuit",
    "lawyer",
    "court",
    "salary",
    "school",
    "admission",
    "hiring",
    "address",
    "passport",
    "身份证",
    "医院",
    "医疗",
    "诊断",
    "诉讼",
    "律师",
    "法院",
    "工资",
    "学校",
    "升学",
    "招聘",
    "地址",
    "护照",
}


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("consented follow-up packet must be a JSON object")
    return payload


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def collect_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(collect_text(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(collect_text(item) for item in value.values())
    return ""


def has_obvious_identifier(text: str) -> tuple[bool, str]:
    scanners = [
        ("email", EMAIL_RE),
        ("phone", PHONE_RE),
        ("url", URL_RE),
        ("handle", HANDLE_RE),
        ("exact_date", EXACT_DATE_RE),
    ]
    for label, scanner in scanners:
        if scanner.search(text):
            return True, label
    lowered = text.lower()
    for term in FORBIDDEN_CONTEXT_TERMS:
        if term.lower() in lowered:
            return True, f"forbidden_context:{term}"
    return False, ""


def run(path: Path) -> int:
    payload = read_json(path)
    root = path.parent.parent
    packets = as_list(payload.get("packets"))
    checks: list[Check] = [
        Check("schema:version", payload.get("schema_version") == "consented-followup/v1", "schema version is consented-followup/v1"),
        Check("schema:protocol", payload.get("protocol") == "docs/consent-redaction-protocol.md", "protocol path is declared"),
        Check("file:protocol", (root / "docs/consent-redaction-protocol.md").exists(), "consent redaction protocol file exists"),
        Check("packets:min_count", len(packets) >= 2, f"{len(packets)} packets found"),
    ]

    observation_total = 0
    state_coverage: set[str] = set()
    privacy_passes = 0
    feedback_passes = 0

    for packet_index, packet in enumerate(packets, start=1):
        prefix = f"packet:{packet.get('packet_id', packet_index)}"
        if not isinstance(packet, dict):
            checks.append(Check(f"{prefix}:object", False, "packet is an object"))
            continue

        packet_id = str(packet.get("packet_id", ""))
        source = str(packet.get("source", ""))
        consent = packet.get("consent") if isinstance(packet.get("consent"), dict) else {}
        privacy = packet.get("privacy") if isinstance(packet.get("privacy"), dict) else {}
        candidate_set = [str(item) for item in as_list(packet.get("candidate_set"))]
        formulation = packet.get("current_formulation") if isinstance(packet.get("current_formulation"), dict) else {}
        observations = [item for item in as_list(packet.get("follow_up_observations")) if isinstance(item, dict)]
        feedback = packet.get("user_feedback") if isinstance(packet.get("user_feedback"), dict) else {}
        packet_text = collect_text(packet)
        identifier_found, identifier_label = has_obvious_identifier(packet_text)

        consent_ok = (
            consent.get("subject_consent") is True
            and consent.get("public_issue_ok") is True
            and bool(consent.get("withdrawal_note"))
        )
        privacy_ok = (
            privacy.get("direct_identifiers_removed") is True
            and privacy.get("third_party_details_removed") is True
            and privacy.get("data_minimized") is True
            and privacy.get("contains_private_chat") is False
            and privacy.get("redaction_level") in ALLOWED_REDACTION
            and not identifier_found
        )
        privacy_passes += int(privacy_ok)

        leading = str(formulation.get("leading", ""))
        runners = [str(item) for item in as_list(formulation.get("runner_up"))]
        confidence = str(formulation.get("confidence", ""))
        falsifier = str(formulation.get("falsifier", ""))
        feedback_ok = bool(as_list(feedback.get("felt_right"))) and bool(as_list(feedback.get("felt_wrong"))) and bool(feedback.get("next_observation_prompt"))
        feedback_passes += int(feedback_ok)

        checks.extend(
            [
                Check(f"{prefix}:id", packet_id.startswith("consent-"), "packet id starts with consent-"),
                Check(f"{prefix}:source", source in ALLOWED_SOURCES, f"source={source}"),
                Check(f"{prefix}:consent", consent_ok, "subject consent, public issue permission, and withdrawal note are present"),
                Check(f"{prefix}:privacy_flags", privacy_ok, identifier_label or "privacy flags and identifier scan pass"),
                Check(f"{prefix}:candidate_set", 3 <= len(candidate_set) <= 6, f"{len(candidate_set)} candidates"),
                Check(f"{prefix}:leading", leading in candidate_set, "leading type is in candidate set"),
                Check(f"{prefix}:runner_up", bool(runners) and all(item in candidate_set for item in runners), "runner-up exists and is in candidate set"),
                Check(f"{prefix}:confidence", confidence in ALLOWED_CONFIDENCE, f"confidence={confidence}"),
                Check(f"{prefix}:falsifier", len(falsifier) >= 30, "falsifier is specific"),
                Check(f"{prefix}:observations", len(observations) >= 3, f"{len(observations)} follow-up observations"),
                Check(f"{prefix}:feedback", feedback_ok, "felt-right, felt-wrong, and next observation prompt are present"),
            ]
        )

        for observation_index, observation in enumerate(observations, start=1):
            observation_total += 1
            obs_prefix = f"{prefix}:observation:{observation_index}"
            state = str(observation.get("state", ""))
            state_coverage.add(state)
            summary = str(observation.get("summary", ""))
            tags = [str(item) for item in as_list(observation.get("evidence_tags"))]
            supports = [str(item) for item in as_list(observation.get("supports"))]
            weakens = [str(item) for item in as_list(observation.get("weakens"))]
            privacy_note = str(observation.get("privacy_note", ""))
            obs_identifier_found, obs_identifier_label = has_obvious_identifier(summary)
            checks.extend(
                [
                    Check(f"{obs_prefix}:state", state in REQUIRED_STATES, f"state={state}"),
                    Check(f"{obs_prefix}:summary", len(summary) >= 60, "summary is behavior-rich"),
                    Check(f"{obs_prefix}:redaction_placeholders", "[" in summary and "]" in summary, "summary uses redaction placeholders"),
                    Check(f"{obs_prefix}:identifier_scan", not obs_identifier_found, obs_identifier_label or "no obvious identifiers in summary"),
                    Check(f"{obs_prefix}:evidence_tags", len(tags) >= 2, f"{len(tags)} evidence tags"),
                    Check(f"{obs_prefix}:supports", bool(supports) and all(item in candidate_set for item in supports), "supports points to candidate types"),
                    Check(f"{obs_prefix}:weakens", bool(weakens) and all(item in candidate_set for item in weakens), "weakens points to candidate types"),
                    Check(f"{obs_prefix}:privacy_note", len(privacy_note) >= 25, "privacy note explains redaction"),
                ]
            )

    state_metric = len(state_coverage & REQUIRED_STATES)
    checks.extend(
        [
            Check("metrics:observation_total", observation_total >= 6, f"{observation_total} follow-up observations"),
            Check("metrics:state_coverage", state_metric >= 4, f"{state_metric} states represented"),
            Check("metrics:privacy_passes", privacy_passes == len(packets) and len(packets) > 0, f"{privacy_passes}/{len(packets)} packets privacy-safe"),
            Check("metrics:feedback_passes", feedback_passes == len(packets) and len(packets) > 0, f"{feedback_passes}/{len(packets)} packets include user feedback"),
        ]
    )

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Consent Redaction Audit: {passed}/{total} ({passed / total:.2%})")
    print(f"Consent Redaction Metrics: packets={len(packets)}; observations={observation_total}; states={state_metric}; privacy_safe={privacy_passes}/{len(packets)}; feedback={feedback_passes}/{len(packets)}")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("examples/consented-followup-packet.json")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
