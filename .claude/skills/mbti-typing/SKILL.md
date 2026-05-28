---
name: mbti-typing
description: Rigorous MBTI and personality typing workflow. Use for type-me requests, adjacent-type duels, transcript audits, report reviews, adaptive interviews, question-bank work, and personality typing protocol design.
when_to_use: Use when the user asks to determine, verify, disprove, compare, audit, or improve MBTI typing. Also use for ENTJ vs INTJ, INFP vs INFJ, INFP vs ENTJ, ESTJ vs ENTJ, exported conversations, personality reports, and multi-round interviews.
argument-hint: "[claim, transcript, report, or type pair]"
---

# MBTI Typing

Use the repository's canonical protocol when available: `skill/mbti-typing/SKILL.md`.

If the canonical file is not available after this adapter is copied elsewhere, follow this compact contract.

## Core Stance

- Treat every type as a falsifiable hypothesis.
- Keep a candidate set with at least one serious runner-up.
- Ask 4-6 concrete questions per round.
- Prefer scenes, forced choices, rankings, and counterexamples over abstract self-label questions.
- Maintain an evidence ledger with support, contradiction, alternative explanations, and next questions.
- Separate MBTI function-stack language from Big Five, Enneagram, attachment, culture, role demand, and life-stage explanations.
- Do not use MBTI for clinical diagnosis, hiring, school admission, legal decisions, medical decisions, financial decisions, or deterministic claims.

## Operating Modes

- Live adaptive interview: use `question-bank.md`, 4-6 questions per round, and update the candidate board after every answer.
- Adjacent-type duel: use `pair-duels.md`, killer discriminators, losing conditions, and falsifiers.
- Transcript audit: preserve excerpts, source context, contradictions, and evidence tags.
- Report review: check runner-up, falsifier, evidence quality, overclaiming, and framework mixing.
- Protocol improvement: update references, examples, audits, and public labs together.

## Final Answer Minimum Bar

Every serious typing result must include:

- leading formulation and serious runner-up
- two independent discriminators for the top pair
- normal-state evidence and stress/recovery/conflict evidence
- Big Five or other cross-framework check when useful
- what would falsify or revise the conclusion
- safety boundary: not clinical, hiring, legal, medical, financial, or deterministic advice

## Claude Code Invocation

Use `/mbti-typing` directly, or ask naturally:

```text
Use /mbti-typing to distinguish ENTJ vs INTJ from these notes.
```

For repository work, run `make test` and `python3 -B scripts/agent_adapter_audit.py .` before claiming an adapter change is ready.
