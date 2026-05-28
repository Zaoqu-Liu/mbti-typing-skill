# Consent Redaction Protocol

This protocol defines how real or realistic user material can become useful project evidence without becoming a privacy leak.

It is a repository safety protocol, not a legal compliance certification.

## Why This Exists

The project can improve from synthetic benchmarks, Calibration Lab results, and blind review. It still needs a safe path for real-world ambiguity:

- A user returns after two weeks with new observations.
- A prior report felt partly right and partly wrong.
- A conflict, recovery period, or work pattern clarified a candidate pair.
- A contributor wants to turn a failure into a benchmark without exposing private logs.

Without consent and redaction rules, accuracy work becomes unsafe. With strict packet rules, useful patterns can become tests while private life stays out of the repository.

## Contribution Boundary

Public contributions may include:

- Synthetic examples.
- Consented and anonymized summaries.
- Redacted observation patterns.
- Aggregated follow-up findings.

Public contributions must not include:

- Raw private chat logs.
- Medical, legal, school, hiring, or selection details.
- Names, handles, email addresses, phone numbers, addresses, workplace names, school names, family identifiers, or exact dates.
- Identifiable third-party behavior.
- Screenshots of private conversations.

## Packet Requirements

Each consented follow-up packet must include:

- `packet_id`: stable id starting with `consent-`.
- `source`: `synthetic`, `consented-anonymized`, or `public-synthetic`.
- `consent.subject_consent`: true.
- `consent.public_issue_ok`: true for anything intended for a public issue.
- `consent.withdrawal_note`: clear statement that the contributor can ask maintainers to remove or further redact the packet.
- `privacy.direct_identifiers_removed`: true.
- `privacy.third_party_details_removed`: true.
- `privacy.data_minimized`: true.
- `privacy.redaction_level`: `public-safe-synthetic` or `public-safe-anonymized`.
- `candidate_set`: 3-6 plausible types.
- `current_formulation`: leading type, runner-up, confidence, and falsifier.
- `follow_up_observations`: at least three observations across normal, stress/conflict, and recovery or reflection states.
- `user_feedback`: what felt right, what felt wrong, and what the next observation prompt should be.

## Redaction Rules

Use placeholders instead of personal details:

- `[PERSON_A]`, `[PERSON_B]`
- `[WORKPLACE]`
- `[CITY]`
- `[DATE_RANGE]`
- `[PROJECT]`
- `[RELATIONSHIP_CONTEXT]`

Prefer behavior summaries over raw quotes:

```text
Good: During [PROJECT], the subject took energy from making the execution path concrete.
Bad: On March 4 at Acme Corp, Alice told Bob that...
```

## Follow-Up Quality

Useful delayed evidence should separate:

- Normal state.
- Stress or conflict state.
- Recovery state.
- Public performance state.
- Relationship or team state.

The goal is not to keep a user in an endless loop. The goal is to make revision triggers observable.

## Acceptance Threshold

A packet is publishable when:

- It passes `scripts/consent_redaction_audit.py`.
- It contains no obvious direct identifiers.
- It has a specific candidate set and runner-up.
- It includes at least one falsifier.
- It includes delayed observations across at least three states.
- It explains what the system got right and wrong.

If a packet fails privacy checks, do not open a public issue. Redact further or keep it private.
