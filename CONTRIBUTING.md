# Contributing

Thank you for improving MBTI Typing Skill.

This repository values rigor over personality-label theater. Contributions should make the system more falsifiable, safer, more useful, or easier to validate.

## Contribution Principles

- Preserve uncertainty and runner-up types.
- Prefer concrete behavior over self-labels.
- Separate MBTI, Big Five, A/T, Enneagram, attachment, culture, and life-stage claims.
- Do not add deterministic claims about people.
- Do not add hiring, clinical, legal, or selection use cases.
- Add tests or fixtures when changing behavior.

## Good First Contributions

- Add benchmark cases for under-covered type pairs.
- Improve pair-duel discriminators.
- Add realistic bad reports that should fail audit.
- Share Calibration Lab failures through the `calibration_result.yml` issue template.
- Tighten Chinese or English output templates.
- Improve safety wording in reports.

## Development

Run:

```bash
make test
```

Expected:

```text
Score: 35/35 (100.00%)
Regression passed for 16 golden fixtures.
Calibration Lab Audit: 53/53 (100.00%)
```

## Benchmark Case Guidelines

Each benchmark case must include:

- `id`
- `prompt`
- `expected_leading`
- `expected_runner_up`
- `required_evidence_tags`
- `trap`
- `required_falsifier_theme`

Each case should test a real differential-diagnosis problem, not a stereotype.

## Calibration Result Guidelines

Calibration reports are useful when a model output looks plausible but fails a specific benchmark gate.

Before opening a calibration issue:

- Remove private or identifiable text.
- Include the benchmark case id.
- Include the Calibration Lab score.
- Include failed gates such as missing runner-up, missing falsifier, weak evidence tags, missing boundary, or overclaim trigger.
- Explain the expected repair in one or two concrete sentences.

## Pull Request Checklist

- [ ] `make test` passes.
- [ ] Any new claim has a caveat or evidence standard.
- [ ] Any new type-pair guidance includes losing conditions for both sides.
- [ ] Any new benchmark case includes a trap and falsifier theme.
- [ ] Any new calibration result is sanitized and points to a specific failed gate.
- [ ] No clinical, hiring, or deterministic use case has been added.
