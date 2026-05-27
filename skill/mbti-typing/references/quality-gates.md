# Quality Gates

## Table of Contents

- Gate summary
- Scoring rubric
- Red flags
- Final report checklist
- Review output format

## Gate Summary

Use these gates before delivering a final typing or when reviewing a report.

| Gate | Pass condition |
|---|---|
| Candidate discipline | At least 3 candidates were considered, or a narrower pair was justified |
| Differential diagnosis | The report explains why the runner-up loses |
| Evidence independence | The decisive evidence comes from at least two independent contexts |
| Normal vs stress split | Normal default behavior is not confused with stress or recovery behavior |
| Framework hygiene | MBTI, Big Five, A/T, Enneagram, attachment, culture, and development are separated |
| Psychometric humility | Numeric certainty and function scores are marked as heuristic or removed |
| User correction | Any user rejection of wording is incorporated |
| Safety | No clinical, hiring, school, legal, or deterministic use |
| Utility | The final answer gives practical implications tied to the user's goal |

## Scoring Rubric

Score each gate:

- `2`: clearly satisfied.
- `1`: partially satisfied; mention caveat.
- `0`: missing or failed.

Interpretation:

- `16-18`: strong report.
- `12-15`: usable with caveats.
- `8-11`: needs revision before being trusted.
- `<8`: do not present as a serious typing.

## Red Flags

Immediate revision required if the report contains:

- "Scientifically proven", "100% certain", "world's most accurate", or similar certainty language.
- A single final type with no runner-up.
- Type used to diagnose mental illness, predict job success, or justify excluding someone.
- Function scores presented as measured data without an instrument.
- A/T treated as official MBTI.
- "All X types..." or "X types never..." claims.
- A loop where behavior infers type and the inferred type explains the same behavior.
- A dramatic anecdote treated as stronger than repeated mundane behavior.

## Final Report Checklist

Before final answer, verify:

- The opening answer is short enough to understand.
- The type label is paired with process language, for example `ENTJ-like Te-Ni formulation`.
- The runner-up is steelmanned, not dismissed.
- There is a table of decisive evidence.
- There is a table or paragraph of evidence against the leading type.
- Big Five is used as cross-check if enough data exists.
- A/T is marked as 16Personalities-style if used.
- Non-standard ideas are labeled as observations.
- The final section says what would change the conclusion.
- The user's own corrections or objections are explicitly reflected.

## Review Output Format

When reviewing a report, use:

```markdown
Findings:
1. [P1] Issue title - file/section if available
   Why it matters:
   Fix:

2. [P2] Issue title
   Why it matters:
   Fix:

Score:
- Candidate discipline: 0/1/2
- Differential diagnosis: 0/1/2
- Evidence independence: 0/1/2
- Normal vs stress split: 0/1/2
- Framework hygiene: 0/1/2
- Psychometric humility: 0/1/2
- User correction: 0/1/2
- Safety: 0/1/2
- Utility: 0/1/2

Verdict:
```

Keep praise secondary. Findings first.

For Markdown or structured JSON reports, run:

```bash
python3 /Users/liuzaoqu/.codex/skills/mbti-typing/scripts/report_audit.py --fail-on-findings /path/to/report.md
```
