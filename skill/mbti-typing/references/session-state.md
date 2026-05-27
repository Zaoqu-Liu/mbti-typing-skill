# Session State

## Table of Contents

- Purpose
- Required state fields
- Evidence item fields
- Round fields
- Validation gates
- State update rhythm

## Purpose

Use a state file for serious or long MBTI typing sessions. The goal is to prevent drift: early contradictions, runner-up types, and user corrections should remain visible after many rounds.

Use `scripts/typing_session.py init --target "..."` to create a template and `scripts/typing_session.py validate case_state.json` before major conclusions.

## Required State Fields

```json
{
  "target_question": "Am I ENTJ or INTJ?",
  "mode": "live_interview",
  "candidate_set": [
    {
      "type": "ENTJ",
      "status": "leading",
      "why_included": "Prior self-test and Te/Ni evidence",
      "support": [],
      "against": []
    }
  ],
  "rounds": [],
  "evidence": [],
  "contradictions": [],
  "user_corrections": [],
  "framework_boundaries": [],
  "current_board": {
    "leading": [],
    "runner_up": [],
    "dropped": []
  },
  "next_round_target": "",
  "falsifiers": [],
  "final_formulation": null
}
```

## Evidence Item Fields

Each evidence item should include:

- `id`: stable identifier, such as `E07`.
- `round`: integer round number or transcript section.
- `observation`: what the subject actually said or did.
- `context`: normal, stress, recovery, relationship, work, social, long-term pattern, or external observer.
- `supports`: list of candidate types or process hypotheses.
- `contradicts`: list of candidate types or process hypotheses.
- `alternatives`: role, culture, attachment, health, life stage, incentive, self-image, or one-off story.
- `weight`: 0-5.
- `independence_group`: label for correlated evidence; repeated planning answers should share one group.
- `follow_up`: next question if unresolved.

Weight caps:

| Evidence source | Max weight |
|---|---:|
| Repeated real behavior across settings | 5 |
| User correction that invalidates an interpretation | 5 |
| Stress/recovery pattern repeated over time | 4 |
| External observer report | 4 |
| Concrete example from one setting | 3 |
| Self-description or identity claim | 2 |
| Single dramatic anecdote | 2 |
| Online test or third-party label | 1 |

## Round Fields

Each round should include:

- `round`: number.
- `target`: the uncertainty attacked in this round.
- `questions`: prompts asked.
- `answers`: compressed answers.
- `movement`: what changed in the candidate board.
- `new_contradictions`: contradictions discovered.
- `next_target`: next uncertainty.

## Validation Gates

Before a final answer, state should prove:

- At least 3 candidates were initially considered unless the user requested a narrow duel.
- At least one runner-up remains or was explicitly defeated.
- At least one normal-state evidence item exists.
- At least one stress/recovery/conflict evidence item exists.
- At least one contradiction was checked or explicitly absent.
- At least one framework boundary is recorded.
- At least one falsifier is recorded.
- Each leading claim has at least one supporting evidence item and one caveat.

## State Update Rhythm

After every round:

1. Add new evidence.
2. Update candidate support/against lists.
3. Move candidates between leading, runner-up, and dropped.
4. Add or resolve contradictions.
5. Write the next round target.
6. Ask whether the subject rejects any interpretation.

For transcript audits, update after each major conversation file rather than each message.
