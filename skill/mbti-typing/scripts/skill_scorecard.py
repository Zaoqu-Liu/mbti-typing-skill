#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/playbooks.md",
    "references/methodology.md",
    "references/type-map.md",
    "references/pair-duels.md",
    "references/question-bank.md",
    "references/session-state.md",
    "references/zh-output-style.md",
    "references/quality-gates.md",
    "references/research-boundaries.md",
    "references/evidence-ledger-template.md",
    "examples/benchmark-cases.json",
    "examples/golden-reports.json",
    "scripts/bayes_update.py",
    "scripts/typing_session.py",
    "scripts/report_audit.py",
    "scripts/benchmark_cases.py",
]

REQUIRED_SKILL_TERMS = [
    "Mode Selector",
    "Minimum Bar",
    "references/pair-duels.md",
    "references/session-state.md",
    "references/zh-output-style.md",
    "scripts/typing_session.py",
    "scripts/report_audit.py",
    "scripts/benchmark_cases.py",
    "examples/benchmark-cases.json",
    "examples/golden-reports.json",
]


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    for rel in REQUIRED_FILES:
        checks.append(Check(f"file:{rel}", (root / rel).exists(), "required file exists"))

    skill_path = root / "SKILL.md"
    skill_text = _read(skill_path) if skill_path.exists() else ""
    for term in REQUIRED_SKILL_TERMS:
        checks.append(Check(f"skill_term:{term}", term in skill_text, "SKILL.md references core capability"))

    all_text = "\n".join(_read(path) for path in root.rglob("*") if path.is_file() and path.suffix in {".md", ".py", ".yaml"})
    todo_marker = "TO" + "DO"
    bracketed_todo = "[TO" + "DO]"
    checks.append(Check("no_todo", todo_marker not in all_text and bracketed_todo not in all_text, "no template placeholders"))
    type_map = _read(root / "references/type-map.md") if (root / "references/type-map.md").exists() else ""
    types = {"ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP", "INTJ", "INFJ", "ENTJ", "ENFJ", "INTP", "INFP", "ENTP", "ENFP"}
    missing_types = sorted(type_name for type_name in types if not re.search(rf"\|\s*{type_name}\s*\|", type_map))
    checks.append(Check("all_16_types", not missing_types, f"missing types: {', '.join(missing_types)}" if missing_types else "all 16 types present"))

    pair_duels = _read(root / "references/pair-duels.md") if (root / "references/pair-duels.md").exists() else ""
    duel_count = len(re.findall(r"^###\s+", pair_duels, flags=re.MULTILINE))
    checks.append(Check("pair_duel_count", duel_count >= 18, f"{duel_count} duel sections found"))

    benchmark_path = root / "examples/benchmark-cases.json"
    if benchmark_path.exists():
        try:
            benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
            cases = benchmark.get("cases", [])
            valid_cases = isinstance(cases, list) and len(cases) >= 8
        except json.JSONDecodeError as exc:
            checks.append(Check("benchmark_cases", False, f"invalid JSON: {exc}"))
        else:
            checks.append(Check("benchmark_cases", valid_cases, f"{len(cases) if isinstance(cases, list) else 0} benchmark cases found"))
    else:
        checks.append(Check("benchmark_cases", False, "benchmark-cases.json missing"))

    golden_path = root / "examples/golden-reports.json"
    if benchmark_path.exists() and golden_path.exists():
        script_path = root / "scripts/benchmark_cases.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script_path), "regression", str(benchmark_path), str(golden_path)],
            capture_output=True,
            text=True,
        )
        detail = (result.stdout or result.stderr).strip()
        checks.append(Check("golden_regression", result.returncode == 0, detail or "golden regression passed"))
    else:
        checks.append(Check("golden_regression", False, "benchmark or golden fixture file missing"))

    scripts = sorted(str(path) for path in (root / "scripts").glob("*.py"))
    if scripts:
        try:
            for script in scripts:
                source = Path(script).read_text(encoding="utf-8")
                compile(source, script, "exec")
        except SyntaxError as exc:
            checks.append(Check("scripts_compile", False, f"{exc.filename}:{exc.lineno}: {exc.msg}"))
        else:
            checks.append(Check("scripts_compile", True, "scripts compile in memory"))
    else:
        checks.append(Check("scripts_compile", False, "no scripts found"))

    checks.append(Check("no_pycache", not any("__pycache__" in str(path) for path in root.rglob("*")), "no Python cache artifacts"))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the MBTI typing skill package itself.")
    parser.add_argument("path", help="Path to the skill directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    root = Path(args.path)
    checks = run_checks(root)
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    result = {
        "score": round(passed / total, 4) if total else 0,
        "passed": passed,
        "total": total,
        "checks": [check.__dict__ for check in checks],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Score: {passed}/{total} ({result['score']:.2%})")
        for check in checks:
            status = "PASS" if check.passed else "FAIL"
            print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


if __name__ == "__main__":
    raise SystemExit(main())
