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

The current benchmark target is stricter than raw case count: every one of the 16 MBTI type codes must appear as `expected_leading` at least once, and each benchmark case must have a matching golden fixture.

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

### 6. Blind Review

Blind review checks whether the workflow still behaves well when expected answers are hidden from reviewers or model variants.

The blind review layer evaluates:

- Top-1 hit rate.
- Top-2 hit rate.
- Runner-up preservation.
- Evidence-tag coverage.
- Falsifier coverage.
- Boundary statement rate.
- No-overclaim rate.

Checked by:

```bash
python3 -B scripts/blind_review_audit.py examples/blind-review-matrix.json
```

Top-1 alone is not enough. A report that guesses the leading type while dropping the serious runner-up or falsifier is not considered high quality.

### 7. Consent, Redaction, and Follow-Up

Real user feedback is useful only when it can enter the project without exposing private material. This layer checks that public follow-up packets are consented, redacted, minimized, withdrawable, and structured around delayed observations rather than raw chat logs.

The consent and redaction layer evaluates:

- Subject consent and public issue permission.
- Absence of raw private chat, direct identifiers, third-party details, and high-stakes private contexts.
- Redacted observations across normal, stress, conflict, recovery, reflection, or relationship states.
- Candidate set, leading hypothesis, serious runner-up, confidence, and falsifier.
- User feedback about what felt right, what felt wrong, and what should be observed next.

Checked by:

```bash
python3 -B scripts/consent_redaction_audit.py examples/consented-followup-packet.json
```

The interactive product surface for this layer is checked separately:

```bash
python3 -B scripts/follow_up_lab_audit.py docs/follow-up-lab.html
```

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

The visual blueprint gate checks that the README and visual tour expose eight exact-label SVG assets:

- `docs/assets/repository-experience-map.svg` for the first-time GitHub visitor path.
- `docs/assets/typing-engine-blueprint.svg` for the evidence, duel, audit, and falsifier architecture.
- `docs/assets/trust-loop-dashboard.svg` for the feedback-to-benchmark-to-release trust loop.
- `docs/assets/benchmark-arena-pipeline.svg` for the benchmark JSON to case gallery source-of-truth sync.
- `docs/assets/type-coverage-matrix.svg` for the all-16-leading-types benchmark coverage proof.
- `docs/assets/calibration-loop-map.svg` for the report paste to Calibration Receipt to repair prompt feedback loop.
- `docs/assets/blind-review-arena.svg` for the sanitized packet to independent reviewer to aggregate metrics evaluation loop.
- `docs/assets/consent-feedback-loop.svg` for the consented follow-up to redaction to repository-action loop.

These SVGs are checked for accessibility metadata, expected product labels, and absence of script or remote dependencies. Bitmap visuals can create atmosphere; SVG blueprints carry precise workflow claims.

The activation gate validates that the sample session state can pass final-state checks and that the sample report passes the report audit:

```bash
make activation
```

The blind review gate validates that `examples/blind-review-matrix.json` follows the public protocol, includes at least three synthetic or sanitized cases, preserves hidden references, includes at least two reviewer outputs per case, and reports top-1, top-2, runner-up, falsifier, boundary, and overclaim metrics:

```bash
make blind-review-audit
```

The consent redaction gate validates that `examples/consented-followup-packet.json` follows the public protocol, includes consent and withdrawal language, removes private identifiers, uses redaction placeholders, preserves delayed observations across multiple states, and records user feedback:

```bash
make consent-redaction-audit
```

The repository UX scorecard also checks the Session Lab, Benchmark Arena, Calibration Lab, static playground, and GitHub Pages workflow. The Session Lab must be buildless, local-first, shareable, importable, exportable, and free of external runtime dependencies so the first experience is fast, inspectable, and useful before installation.

The dedicated Session Lab audit validates the HTML interaction contract: visible share/import controls, all 16 type codes, URL-hash recovery, unicode-safe share links, JSON import/download, local persistence, DOM-safe rendering, safety boundaries, and focused candidate count.

The dedicated Case Gallery audit validates the public benchmark surface: all current benchmark cases, all 16 leading types, source-of-truth sync from `skill/mbti-typing/examples/benchmark-cases.json`, case filters, copied `Use $mbti-typing` prompts, benchmark issue seeds, visible runner-up/falsifier language, DOM-safe rendering, and no external runtime dependency.

The dedicated Calibration Lab audit validates the public repair surface: all current benchmark cases, all 16 leading types, source-of-truth sync from `skill/mbti-typing/examples/benchmark-cases.json`, report paste, visible calibration gates, copied repair prompt, copied calibration JSON, copied failure issue seed, local persistence, DOM-safe rendering, and no external runtime dependency.

The dedicated Follow-Up Lab audit validates the public return surface: all 16 type codes, consent checkboxes, redaction placeholders, local privacy scanner, `consented-followup/v1` packet builder, copied issue seed, copied or downloaded JSON, local persistence, DOM-safe rendering, and no external runtime dependency.

The public Pages link gate validates that README and prompt recipe buttons resolve to GitHub repository URLs. Local-first pages can link out to documentation; they just cannot depend on external scripts, remote assets, or network calls to render the core workflow.
