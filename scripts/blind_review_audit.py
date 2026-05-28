#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_CONFIDENCE = {"low", "medium", "medium-high", "high"}
ALLOWED_SOURCES = {"synthetic", "consented-anonymized", "public-synthetic"}


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("blind review matrix must be a JSON object")
    return payload


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def metric_line(name: str, passed: int, total: int) -> str:
    ratio = 0 if total == 0 else passed / total
    return f"{name}: {passed}/{total} ({ratio:.2%})"


def run(path: Path) -> int:
    payload = read_json(path)
    root = path.parent.parent
    cases = as_list(payload.get("cases"))
    checks: list[Check] = [
        Check("schema:version", payload.get("schema_version") == "blind-review/v1", "schema version is blind-review/v1"),
        Check("schema:protocol", payload.get("protocol") == "docs/blind-review-protocol.md", "protocol path is declared"),
        Check("file:protocol", (root / "docs/blind-review-protocol.md").exists(), "blind review protocol file exists"),
        Check("cases:min_count", len(cases) >= 3, f"{len(cases)} blind review cases found"),
    ]

    top1_hits = 0
    top2_hits = 0
    runner_hits = 0
    boundary_hits = 0
    no_overclaim_hits = 0
    falsifier_hits = 0
    tag_hits = 0
    output_total = 0

    for case_index, case in enumerate(cases, start=1):
        prefix = f"case:{case.get('case_id', case_index)}"
        if not isinstance(case, dict):
            checks.append(Check(f"{prefix}:object", False, "case is an object"))
            continue

        case_id = str(case.get("case_id", ""))
        source = str(case.get("source", ""))
        privacy = str(case.get("privacy", ""))
        prompt = str(case.get("prompt", ""))
        candidate_set = [str(item) for item in as_list(case.get("candidate_set"))]
        hidden_reference = case.get("hidden_reference")
        reviewer_outputs = as_list(case.get("reviewer_outputs"))

        checks.extend(
            [
                Check(f"{prefix}:id", bool(case_id.startswith("blind-")), "case id starts with blind-"),
                Check(f"{prefix}:source", source in ALLOWED_SOURCES, f"source={source}"),
                Check(f"{prefix}:privacy", bool(privacy) and ("synthetic" in privacy or "sanitized" in privacy or "anonymized" in privacy), "privacy field proves synthetic/sanitized/anonymized status"),
                Check(f"{prefix}:prompt", len(prompt) >= 80, "reviewer-visible prompt is substantial"),
                Check(f"{prefix}:candidate_set", 3 <= len(candidate_set) <= 6, f"{len(candidate_set)} candidates"),
                Check(f"{prefix}:hidden_reference", isinstance(hidden_reference, dict), "hidden reference exists"),
                Check(f"{prefix}:reviewer_count", len(reviewer_outputs) >= 2, f"{len(reviewer_outputs)} reviewer outputs"),
            ]
        )

        if not isinstance(hidden_reference, dict):
            continue

        leading = str(hidden_reference.get("leading", ""))
        reference_runners = [str(item) for item in as_list(hidden_reference.get("runner_up"))]
        required_tags = [str(item) for item in as_list(hidden_reference.get("minimum_evidence_tags"))]
        reference_falsifier = str(hidden_reference.get("falsifier", ""))
        adjudication_notes = str(hidden_reference.get("adjudication_notes", ""))

        checks.extend(
            [
                Check(f"{prefix}:reference_leading", leading in candidate_set, "reference leading is in candidate set"),
                Check(f"{prefix}:reference_runner", bool(reference_runners) and all(item in candidate_set for item in reference_runners), "reference runner-up is in candidate set"),
                Check(f"{prefix}:reference_tags", len(required_tags) >= 2, f"{len(required_tags)} required evidence tags"),
                Check(f"{prefix}:reference_falsifier", bool(reference_falsifier), "reference falsifier is present"),
                Check(f"{prefix}:adjudication_notes", len(adjudication_notes) >= 60, "adjudication notes explain the decision"),
            ]
        )

        for output_index, output in enumerate(reviewer_outputs, start=1):
            out_prefix = f"{prefix}:output:{output_index}"
            if not isinstance(output, dict):
                checks.append(Check(f"{out_prefix}:object", False, "reviewer output is an object"))
                continue

            output_total += 1
            out_leading = str(output.get("leading", ""))
            out_runners = [str(item) for item in as_list(output.get("runner_up"))]
            out_confidence = str(output.get("confidence", ""))
            out_tags = [str(item) for item in as_list(output.get("evidence_tags"))]
            out_falsifier = str(output.get("falsifier", ""))
            boundary = output.get("boundary_included") is True
            overclaims = [str(item) for item in as_list(output.get("overclaim_flags"))]

            top1_hit = out_leading == leading
            top2_hit = top1_hit or leading in out_runners
            runner_hit = bool(set(reference_runners) & set(out_runners)) or out_leading in reference_runners
            tag_hit = bool(set(required_tags) & set(out_tags))
            falsifier_hit = bool(out_falsifier)
            no_overclaim = not overclaims

            top1_hits += int(top1_hit)
            top2_hits += int(top2_hit)
            runner_hits += int(runner_hit)
            tag_hits += int(tag_hit)
            falsifier_hits += int(falsifier_hit)
            boundary_hits += int(boundary)
            no_overclaim_hits += int(no_overclaim)

            checks.extend(
                [
                    Check(f"{out_prefix}:reviewer_id", bool(output.get("reviewer_id")), "reviewer id is present"),
                    Check(f"{out_prefix}:leading_in_candidates", out_leading in candidate_set, "leading is in candidate set"),
                    Check(f"{out_prefix}:runner_up", bool(out_runners) and all(item in candidate_set for item in out_runners), "runner-up is present and in candidate set"),
                    Check(f"{out_prefix}:confidence", out_confidence in ALLOWED_CONFIDENCE, f"confidence={out_confidence}"),
                    Check(f"{out_prefix}:evidence_tags", len(out_tags) >= 2, f"{len(out_tags)} evidence tags"),
                    Check(f"{out_prefix}:falsifier", falsifier_hit, "falsifier is present"),
                    Check(f"{out_prefix}:boundary", boundary, "boundary statement included"),
                    Check(f"{out_prefix}:overclaim", no_overclaim, "no overclaim flags"),
                ]
            )

    metrics = [
        metric_line("top1", top1_hits, output_total),
        metric_line("top2", top2_hits, output_total),
        metric_line("runner_up", runner_hits, output_total),
        metric_line("evidence_tag", tag_hits, output_total),
        metric_line("falsifier", falsifier_hits, output_total),
        metric_line("boundary", boundary_hits, output_total),
        metric_line("no_overclaim", no_overclaim_hits, output_total),
    ]

    checks.extend(
        [
            Check("metrics:output_total", output_total >= 6, f"{output_total} reviewer outputs"),
            Check("metrics:top2_visible", top2_hits >= top1_hits and output_total > 0, metrics[1]),
            Check("metrics:runner_up_visible", runner_hits > 0, metrics[2]),
            Check("metrics:boundary_visible", boundary_hits == output_total and output_total > 0, metrics[5]),
            Check("metrics:no_overclaim_visible", no_overclaim_hits == output_total and output_total > 0, metrics[6]),
        ]
    )

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Blind Review Audit: {passed}/{total} ({passed / total:.2%})")
    print("Blind Review Metrics: " + "; ".join(metrics))
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("examples/blind-review-matrix.json")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
