# Blind Review Protocol

This protocol turns MBTI typing quality into a blinded review loop. It is for improving reasoning, not for proving a person's objective type.

## Purpose

The project already has synthetic benchmark cases, golden fixtures, Session Lab, Benchmark Arena, and Calibration Lab. Blind review adds a harder layer:

1. A case packet is sanitized and stripped of the expected answer.
2. Reviewers or models independently produce a leading type, runner-up, evidence tags, falsifier, confidence, and boundary statement.
3. An adjudicator compares outputs against a hidden reference formulation or consensus result.
4. Aggregate metrics reveal where the skill is strong, brittle, overconfident, or under-specified.
5. Repeated failures become benchmark cases, golden fixtures, question-bank improvements, or report-audit rules.

## Non-Negotiable Boundaries

- Do not use blind review for hiring, clinical diagnosis, school admission, legal decisions, or any selection process.
- Do not publish identifiable user material.
- Do not treat adjudicated type as permanent truth.
- Do not reward confidence without evidence.
- Do not collapse runner-up types just to improve top-1 accuracy.

## Source-Anchored Guardrails

The protocol follows the same research boundary as the skill:

- Official MBTI guidance frames type work as development and self-awareness, with voluntary use, confidentiality, and the respondent as the final judge of type.
- Official reliability discussion supports caution around exact whole-type certainty even when preference-scale reliability is discussed more positively.
- Five-Factor Model comparison work supports using Big Five as an independent cross-check while avoiding a claim that MBTI categories are clean psychometric classes.
- Forced-choice and Bayesian tools are used as reasoning aids, not as standardized psychometric scoring.

Useful source anchors:

- The Myers-Briggs Company MBTI facts: https://www.themyersbriggs.com/en-us/support/mbti-facts
- The Myers-Briggs Company ethical principles: https://www.themyersbriggs.com/en-US/Support/Ethical-Principles-for-MBTI-Practitioners
- MBTI Online recruitment boundary: https://support.mbtionline.com/hc/en-us/articles/360036487832-Why-should-the-MBTI-not-be-used-for-Recruitment-Employee-Selection
- McCrae & Costa, MBTI from the Five-Factor Model perspective: https://doi.org/10.1111/j.1467-6494.1989.tb00759.x
- Brown & Maydeu-Olivares, forced-choice item response modeling: https://doi.org/10.1177/0013164410375112

## Case Packet Requirements

Each blind case packet must include:

- `case_id`: stable identifier.
- `source`: `synthetic`, `consented-anonymized`, or `public-synthetic`.
- `privacy`: evidence that the packet is synthetic or sanitized.
- `prompt`: what reviewers see.
- `candidate_set`: 3-6 plausible candidates.
- `hidden_reference`: kept out of reviewer view during judging.
- `minimum_evidence_tags`: evidence tags expected in strong reports.
- `adjudication_notes`: why the reference formulation wins over the runner-up.

The reviewer should not see:

- Expected leading type.
- Expected runner-up.
- Falsifier target.
- Prior model outputs.
- Other reviewers' answers.

## Reviewer Output Requirements

Each reviewer output must include:

- `reviewer_id`: anonymized reviewer or model id.
- `leading`: leading hypothesis.
- `runner_up`: one or more serious alternatives.
- `confidence`: `low`, `medium`, `medium-high`, or `high`.
- `evidence_tags`: concrete evidence tags, not adjectives.
- `falsifier`: what would change the conclusion.
- `boundary_included`: whether the output says this is not clinical, hiring, psychometric, or deterministic.
- `overclaim_flags`: any absolute-certainty wording.

## Metrics

Blind review tracks:

- **Top-1 hit**: leading type equals the adjudicated leading formulation.
- **Top-2 hit**: adjudicated leading appears as leading or runner-up.
- **Runner-up preservation**: the serious runner-up is present.
- **Evidence tag coverage**: expected evidence tags appear in the output.
- **Falsifier coverage**: the output includes a revision trigger.
- **Boundary rate**: the output includes safety boundaries.
- **Overclaim rate**: the output avoids "definitely", "100%", "must be", or equivalent certainty language.

Top-1 accuracy without runner-up preservation is not considered a good result.

## Adjudication Procedure

1. Build or select a case packet.
2. Remove labels and expected answers from the reviewer-visible prompt.
3. Collect independent reviewer outputs.
4. Run `scripts/blind_review_audit.py examples/blind-review-matrix.json`.
5. Inspect aggregate metrics and per-case failures.
6. Convert repeated failures into benchmark cases, golden fixtures, pair-duel rules, or Calibration Lab gates.

## Acceptance Threshold

A blind review pack is publishable when:

- Every case is synthetic or explicitly sanitized.
- Every case has at least three candidates.
- Every case has at least two reviewer outputs.
- Every reviewer output names a runner-up and falsifier.
- Aggregate top-2 hit rate is visible.
- Boundary and overclaim metrics are visible.

The threshold is not "perfect accuracy." The threshold is inspectable uncertainty.
