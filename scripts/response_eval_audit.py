#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_MODES = {"live_round", "type_duel", "final_report", "anti_pattern"}
ALLOWED_SOURCES = {"synthetic", "public-synthetic", "consented-anonymized"}

OVERCLAIM_RE = re.compile(
    r"100%|百分百|绝对|一定是|不用怀疑|无需再问|唯一答案|世界上最准|不可能|必然|永远|"
    r"\bdefinitely\b|\balways\b|\bnever\b|\bguaranteed\b",
    re.IGNORECASE,
)
FLATTERY_RE = re.compile(
    r"天生|比别人高级|最强人格|最强类型|完美人格|上等人|注定|无敌|神判|领导者命|"
    r"\bsuperior\b|\bdestined\b|\bborn leader\b",
    re.IGNORECASE,
)
TYPE_RE = re.compile(r"\b(?:I|E)(?:N|S)(?:T|F)(?:J|P)\b")
QUESTION_RE = re.compile(r"(?:^|\n)\s*(?:[-*]|\d+[.)、])\s*[^。\n]*(?:\?|？)", re.MULTILINE)
OPTION_RE = re.compile(r"(?:^|\n)\s*(?:[A-EＡ-Ｅ][.)、:]|[-*]\s*(?:A|B|C|D|E)\b)", re.MULTILINE | re.IGNORECASE)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("response evaluation cases must be a JSON object")
    return payload


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def question_count(text: str) -> int:
    return len(QUESTION_RE.findall(text))


def feature_map(text: str) -> dict[str, bool]:
    types = set(TYPE_RE.findall(text))
    q_count = question_count(text)
    option_count = len(OPTION_RE.findall(text))
    no_overclaim = OVERCLAIM_RE.search(text) is None
    no_flattery = FLATTERY_RE.search(text) is None
    has_escape = contains_any(text, ("Other / none of these", "以上都不是", "都不是", "我补充", "自由补充", "let me explain", "none of these"))
    return {
        "candidate_set": len(types) >= 2 and contains_any(text, ("候选集", "候选榜", "candidate set", "hypotheses")),
        "runner_up": contains_any(text, ("runner-up", "serious runner-up", "第二候选", "备选", "仍然是", "仍然很强")),
        "evidence_movement": contains_any(text, ("证据移动", "真正移动", "支持", "削弱", "weakens", "moved", "弱证据", "强证据")),
        "next_questions": 4 <= q_count <= 6,
        "scene_questions": contains_any(text, ("最近一次", "具体场景", "发生的例子", "举一个", "复盘", "压力", "冲突", "恢复", "正常状态")),
        "choice_first_questions": option_count >= 10 and has_escape and contains_any(text, ("直接选", "少打字", "低打字", "choice", "选项", "A/B/C/D/E")),
        "falsifier": contains_any(text, ("反证", "改判", "反超", "falsifier", "would change", "降低", "提高")),
        "safety_boundary": contains_any(text, ("不是临床", "不是诊断", "不是心理测量", "not clinical", "not psychometric", "招聘", "hiring", "人格真值")),
        "calibrated_confidence": contains_any(text, ("目前证据", "confidence", "暂时", "不是确定", "not high", "medium", "可修正")),
        "cross_framework_boundary": contains_any(text, ("big five", "a/t", "九型", "依恋", "框架", "不能替代")),
        "duel_losing_conditions": contains_any(text, ("loses if", "失去领先", "反超", "降低", "提高")),
        "final_report_shape": contains_any(text, ("短结论", "为什么", "强证据", "弱证据", "继续观察", "working formulation")),
        "no_overclaim": no_overclaim,
        "no_flattery": no_flattery,
    }


def failure_codes(features: dict[str, bool], mode: str) -> set[str]:
    required_by_mode = {
        "live_round": {
            "candidate_set",
            "runner_up",
            "evidence_movement",
            "next_questions",
            "scene_questions",
            "choice_first_questions",
            "falsifier",
            "safety_boundary",
            "calibrated_confidence",
        },
        "type_duel": {
            "candidate_set",
            "runner_up",
            "evidence_movement",
            "next_questions",
            "scene_questions",
            "choice_first_questions",
            "falsifier",
            "safety_boundary",
            "duel_losing_conditions",
        },
        "final_report": {
            "candidate_set",
            "runner_up",
            "evidence_movement",
            "falsifier",
            "safety_boundary",
            "cross_framework_boundary",
            "final_report_shape",
        },
        "anti_pattern": {
            "candidate_set",
            "runner_up",
            "evidence_movement",
            "next_questions",
            "falsifier",
            "safety_boundary",
        },
    }
    failures = {f"missing_{name}" for name in required_by_mode.get(mode, set()) if not features.get(name, False)}
    if not features["no_overclaim"]:
        failures.add("overclaim")
    if not features["no_flattery"]:
        failures.add("flattery")
    return failures


def metric_line(name: str, passed: int, total: int) -> str:
    ratio = 0 if total == 0 else passed / total
    return f"{name}: {passed}/{total} ({ratio:.2%})"


def run(path: Path) -> int:
    payload = read_json(path)
    cases = as_list(payload.get("cases"))
    checks: list[Check] = [
        Check("schema:version", payload.get("schema_version") == "response-eval/v1", "schema version is response-eval/v1"),
        Check("schema:purpose", "sticky precision" in str(payload.get("purpose", "")).lower(), "purpose names sticky precision"),
        Check("cases:min_count", len(cases) >= 4, f"{len(cases)} response eval cases found"),
    ]

    mode_set = {str(case.get("mode", "")) for case in cases if isinstance(case, dict)}
    checks.append(Check("cases:mode_coverage", {"live_round", "type_duel", "final_report", "anti_pattern"} <= mode_set, f"modes={sorted(mode_set)}"))

    positive_total = 0
    positive_passes = 0
    negative_total = 0
    negative_blocked = 0
    sticky_precision_hits = 0
    next_round_hits = 0
    choice_first_hits = 0
    no_overclaim_hits = 0

    for case_index, case in enumerate(cases, start=1):
        prefix = f"case:{case.get('case_id', case_index)}"
        if not isinstance(case, dict):
            checks.append(Check(f"{prefix}:object", False, "case is an object"))
            continue

        case_id = str(case.get("case_id", ""))
        mode = str(case.get("mode", ""))
        source = str(case.get("source", ""))
        prompt = str(case.get("prompt", ""))
        response = str(case.get("response", ""))
        expected = case.get("expected") if isinstance(case.get("expected"), dict) else {}
        should_pass = expected.get("should_pass") is True
        features = feature_map(response)
        failures = failure_codes(features, mode)

        checks.extend(
            [
                Check(f"{prefix}:id", case_id.startswith("response-"), "case id starts with response-"),
                Check(f"{prefix}:mode", mode in ALLOWED_MODES, f"mode={mode}"),
                Check(f"{prefix}:source", source in ALLOWED_SOURCES, f"source={source}"),
                Check(f"{prefix}:prompt", len(prompt) >= 60, "prompt is substantial enough for response evaluation"),
                Check(f"{prefix}:response", len(response) >= 120, "response is substantial enough to audit"),
            ]
        )

        if should_pass:
            positive_total += 1
            required_features = [str(item) for item in as_list(expected.get("required_features"))]
            missing = [feature for feature in required_features if not features.get(feature, False)]
            passed_case = not missing and features["no_overclaim"] and features["no_flattery"]
            positive_passes += int(passed_case)
            sticky_precision = all(
                features.get(name, False)
                for name in ("candidate_set", "runner_up", "evidence_movement", "falsifier", "safety_boundary")
            )
            sticky_precision_hits += int(sticky_precision)
            next_round_needed = mode in {"live_round", "type_duel"}
            next_round_ok = (not next_round_needed) or (features["next_questions"] and features["scene_questions"])
            next_round_hits += int(next_round_ok)
            choice_first_ok = (not next_round_needed) or features["choice_first_questions"]
            choice_first_hits += int(choice_first_ok)
            no_overclaim_hits += int(features["no_overclaim"] and features["no_flattery"])
            checks.extend(
                [
                    Check(f"{prefix}:required_features", not missing, "required features present" if not missing else f"missing={missing}"),
                    Check(f"{prefix}:no_overclaim", features["no_overclaim"], "response avoids fake certainty"),
                    Check(f"{prefix}:no_flattery", features["no_flattery"], "response avoids manipulative flattery"),
                    Check(f"{prefix}:expected_pass", passed_case, "positive fixture passes response quality gate"),
                ]
            )
        else:
            negative_total += 1
            expected_failures = {str(item) for item in as_list(expected.get("expected_failure_codes"))}
            blocked = bool(failures) and expected_failures <= failures
            negative_blocked += int(blocked)
            checks.extend(
                [
                    Check(f"{prefix}:expected_failures", bool(expected_failures), "negative fixture declares expected failure codes"),
                    Check(f"{prefix}:detected_failures", expected_failures <= failures, f"detected={sorted(failures)}"),
                    Check(f"{prefix}:negative_blocked", blocked, "anti-pattern fixture is blocked by the audit"),
                ]
            )

    checks.extend(
        [
            Check("metrics:positive_total", positive_total >= 3, f"{positive_total} positive response fixtures"),
            Check("metrics:positive_passes", positive_passes == positive_total and positive_total > 0, metric_line("positive_pass", positive_passes, positive_total)),
            Check("metrics:negative_blocked", negative_blocked == negative_total and negative_total > 0, metric_line("negative_blocked", negative_blocked, negative_total)),
            Check("metrics:sticky_precision", sticky_precision_hits == positive_total and positive_total > 0, metric_line("sticky_precision", sticky_precision_hits, positive_total)),
            Check("metrics:next_round", next_round_hits == positive_total and positive_total > 0, metric_line("next_round", next_round_hits, positive_total)),
            Check("metrics:choice_first", choice_first_hits == positive_total and positive_total > 0, metric_line("choice_first", choice_first_hits, positive_total)),
            Check("metrics:no_overclaim", no_overclaim_hits == positive_total and positive_total > 0, metric_line("no_overclaim", no_overclaim_hits, positive_total)),
        ]
    )

    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    print(f"Response Eval Audit: {passed}/{total} ({passed / total:.2%})")
    print(
        "Response Eval Metrics: "
        + "; ".join(
            [
                f"cases={len(cases)}",
                metric_line("positive_pass", positive_passes, positive_total),
                metric_line("negative_blocked", negative_blocked, negative_total),
                metric_line("sticky_precision", sticky_precision_hits, positive_total),
                metric_line("next_round", next_round_hits, positive_total),
                metric_line("choice_first", choice_first_hits, positive_total),
                metric_line("no_overclaim", no_overclaim_hits, positive_total),
            ]
        )
    )
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")

    return 0 if passed == total else 2


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("examples/response-eval-cases.json")
    return run(path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
