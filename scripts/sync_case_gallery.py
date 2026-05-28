#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


START_MARKER = "    // BEGIN GENERATED BENCHMARK CASES"
END_MARKER = "    // END GENERATED BENCHMARK CASES"

CASE_BLOCK_RE = re.compile(
    rf"{re.escape(START_MARKER)}\n(?P<body>.*?)\n{re.escape(END_MARKER)}",
    re.DOTALL,
)

CASE_CONST_RE = re.compile(r"\s*const CASES = (?P<cases>\[.*\]);\s*$", re.DOTALL)


def load_cases(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise ValueError(f"{path} must contain an object with a cases list")
    return payload


def make_gallery_cases(payload: dict[str, Any]) -> list[dict[str, Any]]:
    gallery_cases: list[dict[str, Any]] = []
    for case in payload["cases"]:
        if not isinstance(case, dict):
            raise ValueError("each benchmark case must be an object")
        case_id = str(case["id"])
        gallery_cases.append(
            {
                "id": case_id,
                "cluster": str(case.get("cluster", "General")),
                "title": str(case.get("display_title", case_id)),
                "leading": str(case["expected_leading"]),
                "runnerUp": [str(item) for item in case["expected_runner_up"]],
                "prompt": str(case["prompt"]),
                "trap": str(case["trap"]),
                "falsifier": str(case["required_falsifier_theme"]),
                "tags": [str(item) for item in case["required_evidence_tags"]],
            }
        )
    return gallery_cases


def render_case_block(gallery_cases: list[dict[str, Any]]) -> str:
    rendered = json.dumps(gallery_cases, ensure_ascii=False, indent=6)
    rendered = rendered.replace("\n", "\n    ")
    return f"{START_MARKER}\n    const CASES = {rendered};\n{END_MARKER}"


def extract_embedded_cases(html: str) -> list[dict[str, Any]]:
    block_match = CASE_BLOCK_RE.search(html)
    if not block_match:
        raise ValueError("case gallery is missing generated benchmark case markers")
    const_match = CASE_CONST_RE.match(block_match.group("body"))
    if not const_match:
        raise ValueError("case gallery generated block does not contain const CASES JSON")
    cases = json.loads(const_match.group("cases"))
    if not isinstance(cases, list):
        raise ValueError("case gallery CASES payload must be a list")
    return cases


def sync_html(html: str, gallery_cases: list[dict[str, Any]]) -> str:
    replacement = render_case_block(gallery_cases)
    if not CASE_BLOCK_RE.search(html):
        raise ValueError("case gallery is missing generated benchmark case markers")
    return CASE_BLOCK_RE.sub(replacement, html, count=1)


def check(cases_path: Path, html_path: Path) -> int:
    expected = make_gallery_cases(load_cases(cases_path))
    actual = extract_embedded_cases(html_path.read_text(encoding="utf-8"))
    if actual == expected:
        print(f"Case Gallery Source Sync: PASS ({len(expected)} cases match)")
        return 0

    expected_ids = [str(item["id"]) for item in expected]
    actual_ids = [str(item.get("id", "")) for item in actual if isinstance(item, dict)]
    print("Case Gallery Source Sync: FAIL")
    print(f"- expected ids: {', '.join(expected_ids)}")
    print(f"- actual ids: {', '.join(actual_ids)}")
    return 2


def write(cases_path: Path, html_path: Path) -> int:
    expected = make_gallery_cases(load_cases(cases_path))
    html = html_path.read_text(encoding="utf-8")
    updated = sync_html(html, expected)
    if updated == html:
        print(f"Case Gallery Source Sync: PASS ({len(expected)} cases already current)")
        return 0
    html_path.write_text(updated, encoding="utf-8")
    print(f"Case Gallery Source Sync: UPDATED ({len(expected)} cases written)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/case-gallery.html benchmark data from the canonical JSON cases.")
    parser.add_argument("cases_path", nargs="?", default="skill/mbti-typing/examples/benchmark-cases.json")
    parser.add_argument("html_path", nargs="?", default="docs/case-gallery.html")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated CASES block.")
    args = parser.parse_args()

    cases_path = Path(args.cases_path)
    html_path = Path(args.html_path)
    try:
        if args.write:
            return write(cases_path, html_path)
        return check(cases_path, html_path)
    except Exception as exc:
        print(f"Case Gallery Source Sync: ERROR ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
