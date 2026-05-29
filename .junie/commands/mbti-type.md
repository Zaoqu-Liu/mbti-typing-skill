---
description: Run a rigorous MBTI typing investigation with candidate set, runner-up, evidence ledger, and falsifier discipline.
---

Use `skill/mbti-typing/SKILL.md` as the canonical protocol for this task.
Use `skill/mbti-typing/references/question-bank.md` for adaptive probes and `skill/mbti-typing/references/pair-duels.md` for close type-pair discriminators.

Task: `$input`

Return:

- leading formulation and serious runner-up
- decisive evidence and weak evidence
- at least two discriminators for the top pair
- normal-state and stress/recovery/conflict evidence
- falsifiers or revision triggers
- boundary statement: not clinical, hiring, legal, medical, financial, or deterministic advice

For repository, adapter, benchmark, or public UX changes, run:

```bash
make test
python3 -B scripts/agent_adapter_audit.py .
```
