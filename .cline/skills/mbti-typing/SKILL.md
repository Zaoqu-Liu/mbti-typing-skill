---
name: mbti-typing
description: Rigorous MBTI typing workflow. Use for type-me requests, adjacent-type duels, transcript audits, report reviews, adaptive interviews, question-bank work, and adapter maintenance.
---

# MBTI Typing

Use `skill/mbti-typing/SKILL.md` as the canonical protocol when available.

Compact contract:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per round.
- Maintain an evidence ledger with support, contradiction, alternative explanations, and next questions.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive probes.
- Use `skill/mbti-typing/references/pair-duels.md` for adjacent-type duels.
- Name falsifiers and revision triggers before final closure.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

Repository verification:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```
