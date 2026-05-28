---
name: mbti-typing
description: Rigorous MBTI typing workflow for type-me requests, adjacent-type duels, transcript audits, report reviews, question-bank work, and cross-agent adapter maintenance.
---

# MBTI Typing

Use `skill/mbti-typing/SKILL.md` as the canonical protocol.

If only this adapter is visible, preserve this compact contract:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per live interview round.
- Maintain an evidence ledger.
- Use `question-bank.md` for adaptive probes.
- Use `pair-duels.md` for adjacent-type discriminators.
- Name falsifiers and revision triggers before closing.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

Before release or adapter changes, run `make test` and `python3 -B scripts/agent_adapter_audit.py .`.
