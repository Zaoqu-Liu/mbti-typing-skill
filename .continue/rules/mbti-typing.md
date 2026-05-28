# MBTI Typing Skill Rule

Apply this rule when a task involves MBTI typing, adjacent-type duels, transcript audits, report reviews, adaptive interview design, question-bank work, or cross-agent adapter maintenance.

Canonical source: `skill/mbti-typing/SKILL.md`.

Required behavior:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per interview round.
- Maintain an evidence ledger.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive probes.
- Use `skill/mbti-typing/references/pair-duels.md` for close type pairs.
- Name falsifiers and revision triggers.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

Verification:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```
