#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VALID_MODES = {"live_interview", "transcript_audit", "adjacent_duel", "report_review", "protocol_design"}
VALID_TYPES = {
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
    "INTJ", "INFJ", "ENTJ", "ENFJ",
    "INTP", "INFP", "ENTP", "ENFP",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


def make_template(target: str, mode: str) -> dict[str, Any]:
    return {
        "target_question": target,
        "mode": mode,
        "candidate_set": [],
        "rounds": [],
        "evidence": [],
        "contradictions": [],
        "user_corrections": [],
        "framework_boundaries": [
            "MBTI interview typing is a working formulation, not clinical diagnosis or hiring selection."
        ],
        "current_board": {
            "leading": [],
            "runner_up": [],
            "dropped": []
        },
        "next_round_target": "",
        "falsifiers": [],
        "final_formulation": None
    }


def load_state(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("state must be a JSON object")
    return payload


def _is_list(value: Any) -> bool:
    return isinstance(value, list)


def validate_state(state: dict[str, Any], final: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    required = [
        "target_question", "mode", "candidate_set", "rounds", "evidence",
        "contradictions", "user_corrections", "framework_boundaries",
        "current_board", "next_round_target", "falsifiers", "final_formulation",
    ]
    for key in required:
        if key not in state:
            findings.append(Finding("high", "missing_field", f"Missing required field: {key}"))

    mode = state.get("mode")
    if mode is not None and mode not in VALID_MODES:
        findings.append(Finding("medium", "unknown_mode", f"Unknown mode: {mode}"))

    candidates = state.get("candidate_set", [])
    if not _is_list(candidates):
        findings.append(Finding("high", "candidate_set_type", "candidate_set must be a list"))
        candidates = []

    candidate_types: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            findings.append(Finding("high", "candidate_type", f"candidate_set[{index}] must be an object"))
            continue
        type_name = str(candidate.get("type", ""))
        if type_name and type_name not in VALID_TYPES:
            findings.append(Finding("medium", "unknown_type", f"Unknown MBTI type: {type_name}"))
        if type_name:
            candidate_types.add(type_name)
        for key in ("why_included", "support", "against"):
            if key not in candidate:
                findings.append(Finding("medium", "candidate_incomplete", f"{type_name or index} missing {key}"))

    evidence = state.get("evidence", [])
    if not _is_list(evidence):
        findings.append(Finding("high", "evidence_type", "evidence must be a list"))
        evidence = []

    context_values: set[str] = set()
    independence_groups: set[str] = set()
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            findings.append(Finding("high", "evidence_item_type", f"evidence[{index}] must be an object"))
            continue
        item_id = item.get("id", f"evidence[{index}]")
        for key in ("observation", "context", "supports", "contradicts", "alternatives", "weight", "independence_group"):
            if key not in item:
                findings.append(Finding("medium", "evidence_incomplete", f"{item_id} missing {key}"))
        if "context" in item:
            context_values.add(str(item["context"]).lower())
        if "independence_group" in item:
            independence_groups.add(str(item["independence_group"]))
        weight = item.get("weight")
        if weight is not None:
            try:
                parsed = float(weight)
            except (TypeError, ValueError):
                findings.append(Finding("medium", "weight_invalid", f"{item_id} weight must be numeric"))
            else:
                if parsed < 0 or parsed > 5:
                    findings.append(Finding("medium", "weight_range", f"{item_id} weight should be between 0 and 5"))

    board = state.get("current_board", {})
    if not isinstance(board, dict):
        findings.append(Finding("high", "board_type", "current_board must be an object"))
        board = {}
    for key in ("leading", "runner_up", "dropped"):
        if key not in board or not isinstance(board.get(key), list):
            findings.append(Finding("medium", "board_incomplete", f"current_board.{key} must be a list"))

    if final:
        if len(candidates) < 2:
            findings.append(Finding("high", "final_candidates", "Final state needs at least a leading type and a runner-up or explicit defeated alternative."))
        if not board.get("leading"):
            findings.append(Finding("high", "final_no_leading", "Final state needs current_board.leading."))
        if not board.get("runner_up") and not board.get("dropped"):
            findings.append(Finding("high", "final_no_alternative", "Final state needs runner-up or dropped alternatives with reasons."))
        normal_contexts = {"normal", "idle", "work", "social", "relationship", "long-term pattern", "long_term"}
        stress_contexts = {"stress", "recovery", "conflict", "pressure", "burnout"}
        if not (context_values & normal_contexts):
            findings.append(Finding("high", "final_no_normal_evidence", "Final state needs normal-state evidence."))
        if not (context_values & stress_contexts):
            findings.append(Finding("high", "final_no_stress_evidence", "Final state needs stress/recovery/conflict evidence."))
        if len(independence_groups) < 2:
            findings.append(Finding("medium", "final_low_independence", "Final state should have at least two independent evidence groups."))
        if not state.get("framework_boundaries"):
            findings.append(Finding("high", "final_no_boundaries", "Final state needs framework boundary notes."))
        if not state.get("falsifiers"):
            findings.append(Finding("high", "final_no_falsifiers", "Final state needs falsifiers."))

    if not findings:
        findings.append(Finding("info", "pass", "Session state passed heuristic validation."))
    return findings


def summarize_state(state: dict[str, Any]) -> str:
    board = state.get("current_board", {})
    lines = [
        "# Typing Session Summary",
        "",
        f"Target: {state.get('target_question', '')}",
        f"Mode: {state.get('mode', '')}",
        f"Leading: {', '.join(board.get('leading', [])) if isinstance(board, dict) else ''}",
        f"Runner-up: {', '.join(board.get('runner_up', [])) if isinstance(board, dict) else ''}",
        f"Evidence items: {len(state.get('evidence', [])) if isinstance(state.get('evidence'), list) else 'invalid'}",
        f"Contradictions: {len(state.get('contradictions', [])) if isinstance(state.get('contradictions'), list) else 'invalid'}",
        f"Next target: {state.get('next_round_target', '')}",
    ]
    return "\n".join(lines)


def print_findings(findings: list[Finding], as_json: bool = False) -> None:
    if as_json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
        return
    for finding in findings:
        print(f"[{finding.severity}] {finding.code}: {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create and validate structured MBTI typing session state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Print a blank session state JSON template.")
    init_parser.add_argument("--target", required=True, help="Typing target question.")
    init_parser.add_argument("--mode", default="live_interview", choices=sorted(VALID_MODES))

    validate_parser = subparsers.add_parser("validate", help="Validate a session state JSON file.")
    validate_parser.add_argument("path")
    validate_parser.add_argument("--final", action="store_true", help="Apply final-answer gates.")
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON findings.")

    summary_parser = subparsers.add_parser("summary", help="Summarize a session state JSON file.")
    summary_parser.add_argument("path")

    args = parser.parse_args()

    try:
        if args.command == "init":
            print(json.dumps(make_template(args.target, args.mode), ensure_ascii=False, indent=2))
            return 0
        if args.command == "validate":
            findings = validate_state(load_state(Path(args.path)), final=args.final)
            print_findings(findings, as_json=args.json)
            return 0 if all(finding.severity in {"info"} for finding in findings) else 2
        if args.command == "summary":
            print(summarize_state(load_state(Path(args.path))))
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
