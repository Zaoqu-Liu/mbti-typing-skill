# Evidence Ledger Template

## Intake

- Target question:
- Claimed type(s):
- Source of claim:
- Current context:
- Files or conversations reviewed:
- Sensitive material handling notes:

## Candidate Set

| Candidate | Why included | Prior or starting weight | What would support it | What would weaken it |
|---|---|---:|---|---|
| | | | | |

## Evidence Ledger

| ID | Evidence / answer | Context | Supports | Contradicts | Alternative explanations | Weight | Follow-up needed |
|---|---|---|---|---|---|---:|---|
| E1 | | | | | | | |

Weight guide:

- `3`: repeated real behavior; high diagnostic value; low social desirability.
- `2`: clear answer but possible role/culture/self-image contamination.
- `1`: weak clue or correlated with other evidence.
- `0`: record only; do not use diagnostically.

## Bayesian Scratchpad

Use this only if numeric transparency helps.

```json
{
  "priors": {
    "TYPE_A": 0.5,
    "TYPE_B": 0.5
  },
  "evidence": [
    {
      "id": "E1",
      "weight": 0.7,
      "lrs": {
        "TYPE_A": 3,
        "TYPE_B": 0.7
      },
      "note": "Why this evidence matters"
    }
  ]
}
```

## Contradiction Gate

Before final answer:

- Best evidence for leading type:
- Best evidence against leading type:
- Best evidence for runner-up:
- Evidence runner-up cannot explain well:
- Role/culture/stress alternatives:
- User corrections incorporated:
- Non-standard terms labeled:

## Final Report Skeleton

### Short Answer

Best-supported formulation:

Runner-up:

Confidence level:

### Why This Beats The Alternatives

| Type | Evidence for | Evidence against | Current status |
|---|---|---|---|
| | | | |

### Function / Process Evidence

| Process | Evidence | Strength | Caveat |
|---|---|---:|---|
| | | | |

### Big Five Cross-Check

| Trait | Likely level | Evidence | Caveat |
|---|---|---|---|
| Openness | | | |
| Conscientiousness | | | |
| Extraversion | | | |
| Agreeableness | | | |
| Neuroticism | | | |

### Uncertainty And Falsifiers

This conclusion would change if:

- 
- 
- 

### Practical Implications

Keep this section grounded in the user's goals. Do not give therapy-like advice unless asked, and do not pathologize type traits.

## Structured Report JSON

Use this when the report needs auditability or when generating a reusable artifact. `scripts/report_audit.py` can audit this structure directly.

```json
{
  "short_answer": "Best-supported formulation in one paragraph.",
  "leading_formulation": {
    "type": "ENTJ",
    "process": "Te-Ni working formulation",
    "confidence": "medium-high"
  },
  "runner_up": {
    "type": "INTJ",
    "steelman": "Why this remains plausible",
    "why_it_loses": "What evidence it struggles to explain"
  },
  "claims": [
    {
      "claim": "Te appears more default than emergency-use.",
      "evidence_ids": ["E1", "E3"],
      "caveat": "Work role may amplify Te."
    }
  ],
  "evidence": [
    {
      "id": "E1",
      "observation": "Concrete answer or excerpt",
      "context": "normal",
      "supports": ["ENTJ", "Te-Ni"],
      "contradicts": ["INFP"],
      "alternatives": ["role training"]
    }
  ],
  "alternatives": [
    {
      "type": "INTJ",
      "best_case": "Private Ni model evidence",
      "hardest_problem": "Repeated external command energy"
    }
  ],
  "cross_framework_check": {
    "big_five": "Trait-level check or reason skipped",
    "other": "Attachment/culture/life-stage only if evidence warrants"
  },
  "uncertainty": "What remains unresolved",
  "falsifiers": [
    "Evidence that would change the conclusion"
  ],
  "framework_boundaries": [
    "A/T is 16Personalities-style, not official MBTI."
  ]
}
```
