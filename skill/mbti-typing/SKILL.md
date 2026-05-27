---
name: mbti-typing
description: Rigorous MBTI and personality typing workflow for Chinese or English requests to determine, verify, disprove, or compare MBTI types; analyze exported conversations or personality reports; run multi-round forced-choice interviews; distinguish adjacent types such as ENTJ vs INTJ, INFP vs INFJ, INFP vs ENTJ, or ESTJ vs ENTJ; and produce evidence-based reports using cognitive functions, Big Five cross-checks, Bayesian evidence ledgers, differential diagnosis, and anti-overclaiming safeguards.
---

# MBTI Typing

## Core Stance

Use this skill to run a falsifiable personality-typing investigation, not a quick label assignment.

- Treat every type as a hypothesis with competing alternatives.
- Prefer "best-supported working formulation" over "this person is definitely X".
- Separate MBTI function-stack language, Big Five traits, Enneagram, attachment, culture, and development-stage explanations. Cross-check across frameworks, but do not pretend they are one theory.
- Do not use MBTI for clinical diagnosis, hiring, school admission, legal decisions, or any high-stakes gatekeeping.
- Let the subject correct the model. Corrections, contradictions, and "that wording is wrong" are high-value data, not noise.

## Mode Selector

Choose the mode before doing substantive work:

| User intent | Use | Required resources |
|---|---|---|
| "Type me", "Am I X?", "test until proven" | Live adaptive interview | `references/playbooks.md`, `references/question-bank.md`, `references/type-map.md` |
| "Analyze these chats/reports" | Transcript audit | `references/playbooks.md`, `references/evidence-ledger-template.md`, `references/type-map.md` |
| "X or Y?", "why not INFP?", "ENTJ vs INTJ" | Adjacent-type duel | `references/type-map.md`, `references/pair-duels.md`, `references/question-bank.md` |
| "Review this MBTI report" | Report quality review | `references/quality-gates.md`, `references/research-boundaries.md` |
| "Build a questionnaire/skill/process" | Protocol design | `references/methodology.md`, `references/research-boundaries.md` |

If the request is broad, start with a short mode declaration and then proceed. Do not ask the user to choose a mode unless the target is genuinely ambiguous.

## Workflow

1. **Intake the claim**
   - Capture the target question: "What type am I?", "Am I INFP?", "ENTJ or INTJ?", "analyze these logs", etc.
   - Record prior claims and their source: self-test, friend, expert, work feedback, old reports.
   - If files are provided, read summaries first, then sample original turns around contradictions, reversals, and user corrections.

2. **Build the candidate set**
   - Include the claimed type, the strongest nearby alternatives, and at least one surface-lookalike that could explain the same behavior through a different mechanism.
   - Keep the active set small enough to reason about, usually 3-6 candidates.
   - Track priors explicitly when a prior claim matters, but call them heuristic unless they come from a validated instrument.

3. **Create an evidence ledger**
   - For every answer or excerpt, write the observed behavior, candidate explanations, supporting candidates, contradicting candidates, alternative non-type explanations, and the next question needed.
   - Use `references/evidence-ledger-template.md` for the ledger and final report skeleton.
   - For long or multi-round work, maintain a structured state using `references/session-state.md` and validate it with `scripts/typing_session.py`.
   - For quantitative updates, optionally use `scripts/bayes_update.py`; never present its output as psychometric certainty.

4. **Interview adaptively**
   - Ask 4-6 questions per round. Use forced-choice, ranking, or concrete scenario questions.
   - Avoid abstract self-label questions such as "Are you empathetic?" Prefer scenes: "When your partner cries during a conflict, what happens in your body first?"
   - Design each round against the current top conflict, not against all 16 types at once.
   - Load `references/question-bank.md` when drafting questions.

5. **Run contradiction probes**
   - If one type looks obvious, attack it before concluding.
   - Ask: "If this person were the runner-up type, which evidence would be easiest and hardest to explain?"
   - Do not close while the top two candidates share the same evidence source, function set, or social presentation.

6. **Cross-check with modern trait evidence**
   - Use Big Five as an independent reality check, especially for E/I, J/P, F/T, and A/T-like stability claims.
   - Use attachment, culture, life history, role demands, and current environment as alternative explanations for emotional expression, dominance, conflict style, and achievement pressure.
   - Load `references/research-boundaries.md` before citing validity, reliability, A/T, or psychometric claims.

7. **Conclude with calibrated uncertainty**
   - Give the leading type, runner-up types, decisive evidence, unresolved ambiguities, and specific falsifiers.
   - Use descriptive confidence by default: low, medium, medium-high, high. Use numeric percentages only when the user explicitly wants heuristic Bayesian notation.
   - Include the strongest "this could still be wrong if..." section.

## Minimum Bar

A serious final typing must include:

- A candidate set with at least one plausible runner-up.
- At least two independent discriminators for the top-vs-runner-up distinction.
- One stress/recovery data point and one normal-state data point.
- One cross-framework check, usually Big Five; add attachment/culture/life-stage only when evidence warrants it.
- One section explaining what would falsify or revise the conclusion.
- One explicit boundary statement if the output could be mistaken for clinical, hiring, or deterministic advice.

## Accuracy Rules

- Require at least two independent discriminators before separating adjacent types.
- Down-weight correlated evidence. Four questions that all measure "likes planning" are not four independent proof points.
- Separate normal state, stress state, recovery state, relationship state, and public-performance state.
- Do not overread a single dramatic story; ask for repeated patterns and counterexamples.
- Mark non-standard concepts as "working observation" or "clinical-style observation", not MBTI theory.
- Treat A/T as a 16Personalities-style stability/neuroticism lens, not official MBTI.
- Prefer "the evidence supports Te-Ni over Fi-Ne" to "you are ENTJ because you are efficient".
- If the user wants something "addictive", make the experience compelling through precision, progressive revelation, contradiction handling, and personally useful insight. Do not use manipulative retention loops, false certainty, or flattery.

## Resource Guide

- `references/playbooks.md`: use to select the right operating mode and run live interviews, transcript audits, report reviews, type duels, or questionnaire design.
- `references/methodology.md`: use for the full multi-round protocol and lessons from deep exported-dialogue analysis.
- `references/type-map.md`: use for all 16 types, common adjacent confusions, function-stack caveats, and type-pair discriminators.
- `references/pair-duels.md`: use for high-frequency type-pair battles and killer discriminators.
- `references/question-bank.md`: use to generate discriminating questions by function, type pair, stress pattern, and cross-framework check.
- `references/session-state.md`: use to preserve long interviews and force candidate/evidence/contradiction tracking.
- `references/zh-output-style.md`: use when writing Chinese interview updates, final reports, and high-retention but ethical typing experiences.
- `references/quality-gates.md`: use before delivering a final report or when reviewing another report.
- `references/research-boundaries.md`: use for psychometric caveats, source links, and claims that must be qualified.
- `references/evidence-ledger-template.md`: use to structure evidence tracking and final reports.
- `scripts/bayes_update.py`: use when a transparent heuristic posterior calculation is useful.
- `scripts/typing_session.py`: use to initialize or validate structured typing state for long or serious sessions.
- `scripts/report_audit.py`: use to scan a draft report for missing sections and overclaiming risk.
- `scripts/skill_scorecard.py`: use after substantial edits to audit the skill package itself.
- `examples/benchmark-cases.json`, `examples/golden-reports.json`, and `scripts/benchmark_cases.py`: use to test outputs against synthetic differential-diagnosis cases and regression fixtures.

## Script Quick Start

Pass priors and likelihood ratios as JSON:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/bayes_update.py <<'JSON'
{
  "priors": {"ENTJ": 0.25, "INTJ": 0.25, "INFP": 0.25, "ESTJ": 0.25},
  "evidence": [
    {"id": "idle-default", "weight": 0.8, "lrs": {"ENTJ": 8, "INTJ": 2, "INFP": 0.3, "ESTJ": 1.5}},
    {"id": "stress-recovery", "weight": 0.5, "lrs": {"ENTJ": 2, "INTJ": 2, "INFP": 0.7, "ESTJ": 1}}
  ]
}
JSON
```

Interpret the output as an audit trail for reasoning, not as a validated MBTI score.

Audit a draft report:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/report_audit.py /path/to/report.md
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/report_audit.py --fail-on-findings /path/to/report.json
```

Create and validate a long-session state file:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/typing_session.py init --target "ENTJ vs INTJ" > case_state.json
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/typing_session.py validate case_state.json
```

Audit this skill package:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/skill_scorecard.py /Users/liuzaoqu/.codex/skills/mbti-typing
```

Validate benchmark cases:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/benchmark_cases.py validate /Users/liuzaoqu/.codex/skills/mbti-typing/examples/benchmark-cases.json
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/benchmark_cases.py regression /Users/liuzaoqu/.codex/skills/mbti-typing/examples/benchmark-cases.json /Users/liuzaoqu/.codex/skills/mbti-typing/examples/golden-reports.json
```
