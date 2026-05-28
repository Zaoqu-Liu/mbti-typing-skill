---
trigger: model_decision
description: Use for rigorous MBTI typing, adjacent-type duels, transcript audits, report reviews, question-bank work, and adapter maintenance.
---

# MBTI Typing Skill Rule

Use `AGENTS.md` and `skill/mbti-typing/SKILL.md` as the shared protocol.

- Keep every type as a falsifiable hypothesis.
- Preserve candidate set, serious runner-up, evidence ledger, falsifier, revision trigger, and safety boundary language.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive 4-6 question rounds.
- Use `skill/mbti-typing/references/pair-duels.md` for adjacent-type discriminators.
- Separate MBTI from Big Five, Enneagram, attachment, culture, role demand, and life-stage explanations.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.
- Run `make test` and `python3 -B scripts/agent_adapter_audit.py .` after changing protocol or adapters.
