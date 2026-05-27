#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    item_id: str
    likelihood_ratios: dict[str, float]
    weight: float
    note: str


def _positive_float(value: Any, label: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a number") from exc
    if not math.isfinite(parsed) or parsed <= 0:
        raise ValueError(f"{label} must be a positive finite number")
    return parsed


def _load_payload(path: str | None) -> dict[str, Any]:
    if path:
        text = Path(path).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise ValueError("expected JSON payload on stdin or via --input")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    return payload


def _parse_priors(raw: Any) -> dict[str, float]:
    if not isinstance(raw, dict) or not raw:
        raise ValueError("payload.priors must be a non-empty object")
    priors = {str(name): _positive_float(value, f"prior[{name}]") for name, value in raw.items()}
    total = sum(priors.values())
    return {name: value / total for name, value in priors.items()}


def _parse_evidence(raw: Any) -> list[EvidenceItem]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("payload.evidence must be a list")
    items: list[EvidenceItem] = []
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"evidence[{index}] must be an object")
        item_id = str(entry.get("id") or f"E{index}")
        raw_lrs = entry.get("lrs")
        if not isinstance(raw_lrs, dict) or not raw_lrs:
            raise ValueError(f"evidence[{item_id}].lrs must be a non-empty object")
        lrs = {str(name): _positive_float(value, f"LR[{item_id}][{name}]") for name, value in raw_lrs.items()}
        weight = float(entry.get("weight", 1.0))
        if not math.isfinite(weight) or weight < 0:
            raise ValueError(f"evidence[{item_id}].weight must be finite and >= 0")
        note = str(entry.get("note", ""))
        items.append(EvidenceItem(item_id=item_id, likelihood_ratios=lrs, weight=weight, note=note))
    return items


def update_posteriors(priors: dict[str, float], evidence: list[EvidenceItem]) -> tuple[dict[str, float], list[str]]:
    log_weights = {name: math.log(probability) for name, probability in priors.items()}
    warnings: list[str] = []

    for item in evidence:
        if item.weight == 0:
            continue
        unknown = sorted(set(item.likelihood_ratios) - set(priors))
        if unknown:
            warnings.append(f"{item.item_id}: ignored LR entries for unknown candidates: {', '.join(unknown)}")
        for name in priors:
            lr = item.likelihood_ratios.get(name, 1.0)
            log_weights[name] += math.log(lr) * item.weight

    max_log = max(log_weights.values())
    exp_weights = {name: math.exp(value - max_log) for name, value in log_weights.items()}
    total = sum(exp_weights.values())
    return {name: value / total for name, value in exp_weights.items()}, warnings


def _format_output(priors: dict[str, float], posteriors: dict[str, float], warnings: list[str]) -> dict[str, Any]:
    ranked = sorted(posteriors.items(), key=lambda item: item[1], reverse=True)
    return {
        "posteriors": [
            {
                "type": name,
                "probability": round(probability, 6),
                "prior": round(priors[name], 6),
                "odds_vs_rest": round(probability / (1 - probability), 6) if probability < 1 else None,
            }
            for name, probability in ranked
        ],
        "warnings": warnings,
        "interpretation_note": "Heuristic interview math only; do not treat as a validated psychometric score.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Update heuristic MBTI candidate posteriors from likelihood ratios.")
    parser.add_argument("--input", help="Path to a JSON payload. Defaults to stdin.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    try:
        payload = _load_payload(args.input)
        priors = _parse_priors(payload.get("priors"))
        evidence = _parse_evidence(payload.get("evidence", []))
        posteriors, warnings = update_posteriors(priors, evidence)
        output = _format_output(priors, posteriors, warnings)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    indent = 2 if args.pretty else None
    print(json.dumps(output, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
