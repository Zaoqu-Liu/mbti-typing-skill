#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "Makefile",
    ".github/workflows/ci.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/benchmark_case.yml",
    "docs/assets/mbti-typing-hero.png",
    "docs/evaluation.md",
    "docs/experience-principles.md",
    "docs/github-ux.md",
    "skill/mbti-typing/SKILL.md",
]


README_REQUIRED_TERMS = [
    "docs/assets/mbti-typing-hero.png",
    "Visual System Map",
    "Adaptive Typing Loop",
    "Evidence Ledger Flow",
    "Quality Gate Pipeline",
    "Trust Architecture",
    "make test",
    "Score: 35/35",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    return int(width), int(height)


def check_required_files(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        checks.append(Check(f"file:{rel}", path.exists(), "required repository file exists"))
    return checks


def check_hero(root: Path) -> list[Check]:
    path = root / "docs/assets/mbti-typing-hero.png"
    checks: list[Check] = []
    try:
        width, height = png_size(path)
    except Exception as exc:
        return [Check("hero:png", False, f"hero image is readable PNG: {exc}")]

    ratio = width / height
    checks.append(Check("hero:min_width", width >= 1200, f"width={width}"))
    checks.append(Check("hero:min_height", height >= 650, f"height={height}"))
    checks.append(Check("hero:wide_ratio", 1.55 <= ratio <= 1.95, f"ratio={ratio:.2f}"))
    return checks


def check_readme(root: Path) -> list[Check]:
    readme = read_text(root / "README.md")
    zh_readme = read_text(root / "README.zh-CN.md")
    mermaid_count = len(re.findall(r"```mermaid", readme))
    checks = [
        Check("readme:hero_image", "![MBTI Typing Skill hero]" in readme, "English README displays hero image"),
        Check("readme:mermaid_count", mermaid_count >= 4, f"{mermaid_count} Mermaid diagrams found"),
        Check("readme:zh_hero", "docs/assets/mbti-typing-hero.png" in zh_readme, "Chinese README references hero image"),
    ]
    for term in README_REQUIRED_TERMS:
        checks.append(Check(f"readme:term:{term}", term in readme, "English README contains required UX/proof term"))
    return checks


def check_docs(root: Path) -> list[Check]:
    ux = read_text(root / "docs/github-ux.md")
    evaluation = read_text(root / "docs/evaluation.md")
    experience = read_text(root / "docs/experience-principles.md")
    return [
        Check("docs:ux_mermaid", "```mermaid" in ux, "GitHub UX document contains a visitor journey diagram"),
        Check("docs:evaluation_repo_gate", "repository_scorecard.py" in evaluation, "Evaluation docs mention repository scorecard"),
        Check("docs:experience_no_fake_certainty", "Fake certainty" in experience, "Experience docs reject manipulative certainty"),
    ]


def run(root: Path) -> int:
    checks: list[Check] = []
    checks.extend(check_required_files(root))
    checks.extend(check_hero(root))
    checks.extend(check_readme(root))
    checks.extend(check_docs(root))

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Repository UX Score: {passed}/{total} ({passed / total:.2%})")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    return run(root.resolve())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
