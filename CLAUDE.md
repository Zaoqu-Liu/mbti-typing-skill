# Claude Project Instructions

Read `AGENTS.md` first, then use `skill/mbti-typing/SKILL.md` as the canonical MBTI Typing Skill protocol.

Use this repository for rigorous MBTI typing, adjacent-type duels, transcript audits, report reviews, question-bank work, and adapter maintenance.

Required behavior:

- Treat each type as a falsifiable hypothesis.
- Keep a candidate set with a serious runner-up.
- Ask 4-6 concrete questions per live interview round.
- Use `AskUserQuestion` for low-typing choice questions only when it is available; otherwise use compact `A/B/C/D/E` choices with the final option for "Other / none of these - I will explain".
- Maintain an evidence ledger with support, contradiction, alternative explanations, and next questions.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive probes.
- Use `skill/mbti-typing/references/pair-duels.md` for close forks.
- Name falsifiers and revision triggers before closing.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.

For repository work, run `make test` and `python3 -B scripts/agent_adapter_audit.py .` before claiming adapter or protocol changes are ready.
