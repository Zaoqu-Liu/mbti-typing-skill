# MBTI Typing Skill Agent Contract

This repository packages one MBTI typing protocol for multiple agent tools. Keep this file concise because Codex, Cursor, opencode, and other agents may load it as project-level context.

## When To Apply

Use the MBTI typing protocol when the user asks to:

- determine, verify, disprove, or compare MBTI types
- analyze exported conversations, personality reports, or long self-descriptions
- run an adaptive interview, adjacent-type duel, transcript audit, or report review
- improve this repository's typing workflow, question bank, pair duels, audits, or agent adapters

Do not use this protocol for clinical diagnosis, hiring, school admission, legal decisions, medical decisions, financial decisions, or deterministic claims about a person's worth or future.

## Canonical Source

When available, read `skill/mbti-typing/SKILL.md` first. Load deeper references only when needed:

- `skill/mbti-typing/references/playbooks.md`
- `skill/mbti-typing/references/question-bank.md`
- `skill/mbti-typing/references/pair-duels.md`
- `skill/mbti-typing/references/type-map.md`
- `skill/mbti-typing/references/research-boundaries.md`
- `skill/mbti-typing/references/evidence-ledger-template.md`
- `skill/mbti-typing/references/quality-gates.md`

## Required Behavior

- Treat every type as a hypothesis, not a label to guess.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete, high-yield questions per round.
- Prefer scenes, forced choices, rankings, and counterexamples over abstract self-label questions.
- Maintain an evidence ledger: observation, candidate explanations, support, contradiction, alternative non-type explanation, and next question.
- Separate normal state, stress state, recovery state, relationship state, public-performance state, role demands, culture, and life stage.
- Use Big Five or other frameworks only as cross-checks, clearly labeled as separate from MBTI.
- Before concluding, attack the leading type with falsifiers and explain what would change the result.
- Make the experience compelling through precision, progressive revelation, contradiction handling, and useful insight. Do not use fake certainty, flattery, fear, or endless questioning.

## Output Contract

A serious typing output must include:

- leading formulation and serious runner-up
- decisive evidence and weak evidence
- at least two independent discriminators for the top pair
- normal-state and stress/recovery/conflict evidence
- falsifiers or revision triggers
- boundary statement: not clinical, hiring, legal, medical, financial, or deterministic advice

## Verification

Before release or adapter changes, run:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```

No public agent adapter should drift from the canonical protocol, omit runner-up/falsifier discipline, or remove the safety boundary.
