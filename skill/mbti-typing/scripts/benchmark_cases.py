#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from report_audit import audit_structured_report


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def validate_cases(payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        return [Finding("high", "cases_missing", "Benchmark payload needs a non-empty cases list.")]

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            findings.append(Finding("high", "case_type", f"cases[{index}] must be an object."))
            continue
        case_id = str(case.get("id", ""))
        if not case_id:
            findings.append(Finding("high", "case_id", f"cases[{index}] missing id."))
        elif case_id in seen_ids:
            findings.append(Finding("high", "case_id_duplicate", f"Duplicate case id: {case_id}."))
        seen_ids.add(case_id)
        for key in ("prompt", "expected_leading", "expected_runner_up", "required_evidence_tags", "trap", "required_falsifier_theme"):
            if key not in case:
                findings.append(Finding("medium", "case_incomplete", f"{case_id or index} missing {key}."))
        if not isinstance(case.get("expected_runner_up", []), list) or not case.get("expected_runner_up"):
            findings.append(Finding("medium", "case_runner_up", f"{case_id or index} needs at least one expected runner-up."))
        if not isinstance(case.get("required_evidence_tags", []), list) or len(case.get("required_evidence_tags", [])) < 2:
            findings.append(Finding("medium", "case_evidence_tags", f"{case_id or index} needs at least two required evidence tags."))

    if len(cases) < 8:
        findings.append(Finding("medium", "case_count", "Benchmark should include at least 8 cases."))

    if not findings:
        findings.append(Finding("info", "pass", f"Benchmark case set is valid with {len(cases)} cases."))
    return findings


def _extract_evidence_tags(report: dict[str, Any]) -> set[str]:
    tags: set[str] = set()
    for item in report.get("evidence", []):
        if not isinstance(item, dict):
            continue
        for key in ("tags", "evidence_tags"):
            raw_tags = item.get(key, [])
            if isinstance(raw_tags, list):
                tags.update(str(tag) for tag in raw_tags)
    raw_tags = report.get("evidence_tags", [])
    if isinstance(raw_tags, list):
        tags.update(str(tag) for tag in raw_tags)
    return tags


def grade_report(case: dict[str, Any], report: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    case_id = str(case.get("id", "case"))
    leading = report.get("leading_formulation", {})
    if isinstance(leading, dict):
        leading_type = leading.get("type")
    else:
        leading_type = None
    if leading_type != case.get("expected_leading"):
        findings.append(Finding("high", "wrong_leading", f"{case_id}: expected leading {case.get('expected_leading')}, got {leading_type}."))

    runner_up = report.get("runner_up", {})
    runner_type = runner_up.get("type") if isinstance(runner_up, dict) else runner_up
    expected_runners = set(str(item) for item in case.get("expected_runner_up", []))
    if runner_type not in expected_runners:
        findings.append(Finding("medium", "runner_up_mismatch", f"{case_id}: expected runner-up in {sorted(expected_runners)}, got {runner_type}."))

    report_tags = _extract_evidence_tags(report)
    missing_tags = sorted(set(str(tag) for tag in case.get("required_evidence_tags", [])) - report_tags)
    if missing_tags:
        findings.append(Finding("medium", "missing_evidence_tags", f"{case_id}: missing evidence tags: {', '.join(missing_tags)}."))

    falsifiers = " ".join(str(item) for item in report.get("falsifiers", []))
    theme = str(case.get("required_falsifier_theme", "")).lower()
    if theme and theme not in falsifiers.lower():
        findings.append(Finding("medium", "missing_falsifier_theme", f"{case_id}: falsifiers should cover theme '{theme}'."))

    if not findings:
        findings.append(Finding("info", "pass", f"{case_id}: report matches benchmark expectations."))
    return findings


def validate_fixtures(cases_payload: dict[str, Any], fixtures_payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    cases = {str(case.get("id")): case for case in cases_payload.get("cases", []) if isinstance(case, dict)}
    fixtures = fixtures_payload.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        return [Finding("high", "fixtures_missing", "Golden fixtures payload needs a non-empty fixtures list.")]

    seen: set[str] = set()
    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            findings.append(Finding("high", "fixture_type", f"fixtures[{index}] must be an object."))
            continue
        case_id = str(fixture.get("case_id", ""))
        if case_id not in cases:
            findings.append(Finding("high", "fixture_case", f"fixtures[{index}] references unknown case_id: {case_id}."))
            continue
        if case_id in seen:
            findings.append(Finding("high", "fixture_duplicate", f"Duplicate fixture for case_id: {case_id}."))
        seen.add(case_id)
        if "good_report" not in fixture:
            findings.append(Finding("high", "fixture_good_missing", f"{case_id} missing good_report."))
        if "bad_report" not in fixture:
            findings.append(Finding("high", "fixture_bad_missing", f"{case_id} missing bad_report."))

    missing = sorted(set(cases) - seen)
    for case_id in missing:
        findings.append(Finding("medium", "fixture_missing_case", f"Missing fixture for case_id: {case_id}."))

    if not findings:
        findings.append(Finding("info", "pass", f"Golden fixtures cover {len(fixtures)} benchmark cases."))
    return findings


def run_regression(cases_payload: dict[str, Any], fixtures_payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    case_findings = validate_cases(cases_payload)
    findings.extend(finding for finding in case_findings if finding.severity != "info")
    fixture_findings = validate_fixtures(cases_payload, fixtures_payload)
    findings.extend(finding for finding in fixture_findings if finding.severity != "info")
    if findings:
        return findings

    cases = {str(case.get("id")): case for case in cases_payload.get("cases", []) if isinstance(case, dict)}
    for fixture in fixtures_payload["fixtures"]:
        case_id = str(fixture["case_id"])
        case = cases[case_id]
        good_report = fixture["good_report"]
        bad_report = fixture["bad_report"]

        good_grade = grade_report(case, good_report)
        findings.extend(Finding(finding.severity, f"good_{finding.code}", finding.message) for finding in good_grade if finding.severity != "info")

        good_audit = audit_structured_report(good_report)
        findings.extend(Finding(finding.severity, f"good_audit_{finding.code}", f"{case_id}: {finding.message}") for finding in good_audit if finding.severity != "info")

        bad_grade = grade_report(case, bad_report)
        if all(finding.severity == "info" for finding in bad_grade):
            findings.append(Finding("high", "bad_report_passed", f"{case_id}: bad_report unexpectedly passed benchmark grading."))

    if not findings:
        findings.append(Finding("info", "pass", f"Regression passed for {len(fixtures_payload['fixtures'])} golden fixtures."))
    return findings


def print_findings(findings: list[Finding], as_json: bool) -> None:
    if as_json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
        return
    for finding in findings:
        print(f"[{finding.severity}] {finding.code}: {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MBTI benchmark cases or grade a structured report against one case.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a benchmark case JSON file.")
    validate_parser.add_argument("cases_path")
    validate_parser.add_argument("--json", action="store_true")

    show_parser = subparsers.add_parser("show", help="Print one benchmark case prompt by id.")
    show_parser.add_argument("cases_path")
    show_parser.add_argument("case_id")

    grade_parser = subparsers.add_parser("grade", help="Grade a structured report JSON against a benchmark case.")
    grade_parser.add_argument("cases_path")
    grade_parser.add_argument("case_id")
    grade_parser.add_argument("report_path")
    grade_parser.add_argument("--json", action="store_true")

    regression_parser = subparsers.add_parser("regression", help="Run all golden fixture regression tests.")
    regression_parser.add_argument("cases_path")
    regression_parser.add_argument("fixtures_path")
    regression_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        cases_payload = load_json(Path(args.cases_path))
        if args.command == "validate":
            findings = validate_cases(cases_payload)
            print_findings(findings, args.json)
            return 0 if all(finding.severity == "info" for finding in findings) else 2
        if args.command == "regression":
            fixtures_payload = load_json(Path(args.fixtures_path))
            findings = run_regression(cases_payload, fixtures_payload)
            print_findings(findings, args.json)
            return 0 if all(finding.severity == "info" for finding in findings) else 2
        cases = {str(case.get("id")): case for case in cases_payload.get("cases", []) if isinstance(case, dict)}
        if args.case_id not in cases:
            raise ValueError(f"unknown case id: {args.case_id}")
        if args.command == "show":
            print(cases[args.case_id]["prompt"])
            return 0
        if args.command == "grade":
            report = load_json(Path(args.report_path))
            findings = grade_report(cases[args.case_id], report)
            print_findings(findings, args.json)
            return 0 if all(finding.severity == "info" for finding in findings) else 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
