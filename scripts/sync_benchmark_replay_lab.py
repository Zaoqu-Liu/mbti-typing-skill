#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


START_MARKER = "    // BEGIN GENERATED BENCHMARK REPLAY CASES"
END_MARKER = "    // END GENERATED BENCHMARK REPLAY CASES"

CASE_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

CASE_CONST_RE = re.compile(r"\s*const REPLAY_CASES = (?P<cases>\[.*\]);\s*$", re.DOTALL)


def load_cases(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise ValueError(f"{path} must contain an object with a cases list")
    return payload


def make_replay_cases(payload: dict[str, Any]) -> list[dict[str, Any]]:
    replay_cases: list[dict[str, Any]] = []
    for case in payload["cases"]:
        if not isinstance(case, dict):
            raise ValueError("each benchmark case must be an object")
        case_id = str(case["id"])
        prompt = str(case["prompt"])
        replay_cases.append(
            {
                "id": case_id,
                "cluster": str(case.get("cluster", "General")),
                "title": str(case.get("display_title", case_id)),
                "blindPrompt": prompt,
                "leading": str(case["expected_leading"]),
                "runnerUp": [str(item) for item in case["expected_runner_up"]],
                "trap": str(case["trap"]),
                "falsifier": str(case["required_falsifier_theme"]),
                "tags": [str(item) for item in case["required_evidence_tags"]],
            }
        )
    return replay_cases


def render_case_block(replay_cases: list[dict[str, Any]]) -> str:
    rendered = json.dumps(replay_cases, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const REPLAY_CASES = {rendered};\n{END_MARKER}"


def extract_embedded_cases(html: str) -> list[dict[str, Any]]:
    block_match = CASE_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("benchmark replay lab is missing generated benchmark replay case markers")
    const_match = CASE_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("benchmark replay lab generated block does not contain const REPLAY_CASES JSON")
    cases = json.loads(const_match.group("cases"))
    if not isinstance(cases, list):
        raise ValueError("benchmark replay lab REPLAY_CASES payload must be a list")
    return cases


def sync_html(html: str, replay_cases: list[dict[str, Any]]) -> str:
    replacement = render_case_block(replay_cases)
    if not CASE_BLOCK_RE.search(html):
        raise ValueError("benchmark replay lab is missing generated benchmark replay case markers")
    return CASE_BLOCK_RE.sub(replacement, html, count=1)


def check(cases_path: Path, html_path: Path) -> int:
    expected = make_replay_cases(load_cases(cases_path))
    actual = extract_embedded_cases(html_path.read_text(encoding="utf-8"))
    if actual == expected:
        print(f"Benchmark Replay Lab Source Sync: PASS ({len(expected)} cases match)")
        return 0

    expected_ids = [str(item["id"]) for item in expected]
    actual_ids = [str(item.get("id", "")) for item in actual if isinstance(item, dict)]
    print("Benchmark Replay Lab Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(cases_path: Path, html_path: Path) -> int:
    expected = make_replay_cases(load_cases(cases_path))
    html = html_path.read_text(encoding="utf-8")
    updated = sync_html(html, expected)
    if updated == html:
        print(f"Benchmark Replay Lab Source Sync: PASS ({len(expected)} cases already current)")
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Benchmark Replay Lab Source Sync: UPDATED ({len(expected)} cases written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/benchmark-replay-lab.html replay data from the canonical benchmark JSON cases.")
    parser.add_argument("cases_path", nargs="?", default="skill/mbti-typing/examples/benchmark-cases.json")
    parser.add_argument("html_path", nargs="?", default="docs/benchmark-replay-lab.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated REPLAY_CASES block.")
    args = parser.parse_args()

    cases_path = Path(args.cases_path)
    html_path = Path(args.html_path)
    try:
        if args.write:
            return write(cases_path, html_path)
        return check(cases_path, html_path)
    except Exception as exc:
        print(f"Benchmark Replay Lab Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
