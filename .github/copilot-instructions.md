# MBTI Typing Skill Instructions

Use this repository as a rigorous cross-agent MBTI Typing Skill, not a quick label generator.

- Read `AGENTS.md` first for the concise project contract.
- Treat `skill/mbti-typing/SKILL.md` as the canonical protocol.
- Use `skill/mbti-typing/references/question-bank.md` for adaptive interview questions.
- Use `skill/mbti-typing/references/pair-duels.md` for close type-pair discriminators.
- Preserve candidate set, serious runner-up, evidence ledger, falsifier, revision trigger, and safety boundary language.
- Keep Big Five, Enneagram, attachment, culture, role demands, and life-stage explanations separate from MBTI.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.
- After adapter, documentation, scorecard, or public UX changes, run `make test` and `python3 -B scripts/agent_adapter_audit.py .`.
