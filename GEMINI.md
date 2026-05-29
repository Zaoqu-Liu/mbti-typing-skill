# Gemini CLI Context

@./AGENTS.md
@./skill/mbti-typing/SKILL.md

## MBTI Typing Skill

Use this repository as a rigorous MBTI typing protocol, not a personality-label shortcut.

- Keep `skill/mbti-typing/SKILL.md` as the canonical protocol.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive 4-6 question rounds.
- Use `skill/mbti-typing/references/pair-duels.md` for close type pairs.
- Preserve candidate set, serious runner-up, evidence ledger, falsifiers, revision triggers, and safety boundaries.
- Keep live interviews low-typing: use native question UI only if available; otherwise ask compact `A/B/C/D/E` choices with the final option for "Other / none of these - I will explain".
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.
- Before release or adapter changes, run `make test` and `python3 -B scripts/agent_adapter_audit.py .`.
