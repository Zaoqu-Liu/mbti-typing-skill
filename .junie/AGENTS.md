# MBTI Typing Skill Junie Guidelines

Use these JetBrains Junie guidelines for MBTI type-me requests, adjacent-type duels, transcript audits, report reviews, adaptive interview design, question-bank work, benchmark repair, and cross-agent adapter maintenance.

Canonical source: `skill/mbti-typing/SKILL.md`.

Required behavior:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per round.
- Maintain an evidence ledger.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive probes.
- Use `skill/mbti-typing/references/pair-duels.md` for close type pairs.
- Name falsifiers and revision triggers before final closure.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

Verification:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```
