---
applyTo: "**/*"
---

# MBTI Typing Skill

When working in this repository, keep all MBTI typing behavior aligned with `skill/mbti-typing/SKILL.md`.

Required protocol:

- Candidate set with serious runner-up.
- Evidence ledger for observations, support, contradiction, alternative explanation, and next question.
- 4-6 concrete questions per interview round.
- Pair-duel discipline through `skill/mbti-typing/references/pair-duels.md`.
- Question-bank discipline through `skill/mbti-typing/references/question-bank.md`.
- Falsifier and revision trigger before final closure.
- Boundary statement: not clinical, hiring, legal, medical, financial, or deterministic advice.

For compatibility work, update `agent-adapters/manifest.json`, `docs/agent-adapters.md`, and `scripts/agent_adapter_audit.py` together.

Before release, run `make test` and `python3 -B scripts/agent_adapter_audit.py .`.
