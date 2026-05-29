# Agent Conventions

This repository packages one MBTI Typing Skill protocol for many agent tools.

Always follow these conventions when editing or using this repository:

- Keep `skill/mbti-typing/SKILL.md` as the canonical protocol.
- Keep `AGENTS.md` as the concise cross-agent contract.
- Preserve candidate set, serious runner-up, evidence ledger, falsifiers, revision triggers, and safety boundary language.
- Prefer concrete scenes, forced choices, rankings, and counterexamples over generic personality quiz wording.
- Prefer low-typing question UX: native question UI when present, compact `A/B/C/D/E` choices when not, and a final "Other / none of these - I will explain" escape hatch.
- Use `skill/mbti-typing/references/question-bank.md` for next-round probes.
- Use `skill/mbti-typing/references/pair-duels.md` for adjacent-type duels.
- Do not use MBTI for clinical, hiring, school admission, legal, medical, financial, or deterministic decisions.
- Run `make test` and `python3 -B scripts/agent_adapter_audit.py .` after protocol, adapter, documentation, or public UX changes.
