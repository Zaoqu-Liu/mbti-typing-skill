# MBTI Typing Skill Kilo Code Rule

Use this rule when Kilo Code is asked to determine, compare, audit, or improve MBTI typing work.

Canonical source: `skill/mbti-typing/SKILL.md`.

Required behavior:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per round.
- Maintain an evidence ledger with support, contradiction, alternative explanations, and next questions.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive probes.
- Use `skill/mbti-typing/references/pair-duels.md` for adjacent-type duels.
- Name falsifiers and revision triggers.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

Verification:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```
