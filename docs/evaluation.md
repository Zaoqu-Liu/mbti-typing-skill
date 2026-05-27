# Evaluation

This project treats MBTI typing quality as an engineering problem: outputs should be inspectable, falsifiable, and regression-tested.

It does not claim clinical validity, psychometric certification, or deterministic personality truth. The goal is narrower and more useful: make an AI typing workflow harder to fool, easier to audit, and more honest about uncertainty.

## Evaluation Layers

### 1. Package Integrity

The repository must contain the core skill, references, examples, and scripts needed to run the workflow without hidden state.

Checked by:

```bash
python3 -B skill/mbti-typing/scripts/skill_scorecard.py skill/mbti-typing
```

Current target:

```text
Score: 35/35 (100.00%)
```

### 2. Benchmark Case Validity

Benchmark cases are synthetic but intentionally adversarial. Each case should contain:

- A plausible surface type.
- At least one serious runner-up.
- A trap that a shallow system would overfit.
- Expected discriminators or falsifiers.

Checked by:

```bash
python3 -B skill/mbti-typing/scripts/benchmark_cases.py validate skill/mbti-typing/examples/benchmark-cases.json
```

### 3. Golden Report Regression

Golden reports include good and bad fixtures. Regression checks make sure the auditor keeps catching high-risk failures such as:

- Missing runner-up.
- Unsupported certainty.
- No falsifiers.
- Framework mixing.
- Single-anecdote overfitting.
- Vague type stereotypes.

Checked by:

```bash
python3 -B skill/mbti-typing/scripts/benchmark_cases.py regression skill/mbti-typing/examples/benchmark-cases.json skill/mbti-typing/examples/golden-reports.json
```

### 4. Human Transcript Review

For real exported conversations, evaluation should look at reasoning behavior, not whether the model says a popular type name.

Useful review questions:

- Did the system preserve a candidate set for long enough?
- Did it separate normal state, stress state, recovery state, and public-performance state?
- Did it attack the leading hypothesis before concluding?
- Did the final report state what would change the conclusion?
- Did it avoid using MBTI as clinical, hiring, or deterministic advice?

### 5. User Experience Quality

A compelling typing system should be sticky because the reasoning feels unusually precise, not because it manipulates the user.

Good signs:

- The next question feels personally relevant and non-generic.
- The user can see why each answer changes the candidate set.
- Runner-up types are treated seriously.
- The system can say "not enough evidence" without sounding broken.
- Corrections from the user visibly update the model.

Bad signs:

- The system flatters the user into accepting a label.
- It hides uncertainty to sound confident.
- It keeps asking repetitive questions to prolong the session.
- It mixes MBTI, Big Five, Enneagram, attachment, and diagnosis without labels.

## Release Gate

Before release:

```bash
make test
find . -name '__pycache__' -print
```

The first command must pass. The second command must print nothing.

`make test` also runs the repository UX scorecard:

```bash
python3 -B scripts/repository_scorecard.py .
```

This verifies that the GitHub-facing project experience has the expected hero image, visual diagrams, bilingual README path, evaluation docs, and repository trust artifacts.

The scorecard also requires a demo layer: a visual tour, a short demo session, a sample report, and a second journey-map image. This prevents the repository from becoming only a technical reference; visitors should be able to feel the typing loop quickly.

The activation gate validates that the sample session state can pass final-state checks and that the sample report passes the report audit:

```bash
make activation
```

The repository UX scorecard also checks the Session Lab, static playground, and GitHub Pages workflow. The Session Lab must be buildless, local-first, exportable, and free of external runtime dependencies so the first experience is fast, inspectable, and useful before installation.
