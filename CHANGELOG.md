# Changelog

## 0.1.13 - 2026-05-28

- Added a buildless Follow-Up Lab that turns delayed observations into consented, redacted, public-safe JSON packets and `consented_followup.yml` issue seeds.
- Added `scripts/follow_up_lab_audit.py` and wired the Follow-Up Lab into `make test`, navigation, README, evaluation docs, and repository UX gates.
- Expanded the public product loop from Session Lab, Benchmark Arena, and Calibration Lab into a full return path for users who come back with new evidence, raising the Repository UX Score to 262/262.

## 0.1.12 - 2026-05-28

- Added a Consent Redaction Protocol so real-world follow-up can enter the project only through consented, redacted, withdrawable, public-safe packets.
- Added `examples/consented-followup-packet.json`, `scripts/consent_redaction_audit.py`, and a `consented_followup.yml` issue template to check privacy flags, redaction placeholders, delayed observations, user feedback, and withdrawal wording.
- Added the Consent Feedback Loop SVG and expanded repository gates so consented follow-up claims are checked by `make test`, raising the Repository UX Score to 245/245.

## 0.1.11 - 2026-05-28

- Added a Blind Review Protocol for sanitized multi-reviewer or multi-model evaluation without exposing the expected answer to reviewers.
- Added `examples/blind-review-matrix.json`, `scripts/blind_review_audit.py`, and a `blind_review.yml` issue template to track top-1, top-2, runner-up, evidence-tag, falsifier, boundary, and overclaim metrics.
- Added the Blind Review Arena SVG and expanded repository gates so blind-review claims are checked by `make test`, raising the Repository UX Score to 222/222.

## 0.1.10 - 2026-05-28

- Added a local-first Calibration Lab that checks pasted typing reports against benchmark leading type, runner-up, evidence tags, falsifier theme, safety boundary, and overclaim gates.
- Added source-of-truth sync and audit scripts for `docs/calibration-lab.html`, plus a `calibration_result.yml` issue template so failed reports can become reusable contribution artifacts.
- Added the Calibration Loop Map SVG and expanded repository UX gates to verify the new repair loop, Calibration Lab Audit 53/53, and Repository UX Score 200/200.

## 0.1.9 - 2026-05-28

- Expanded the benchmark suite from 8 to 16 adversarial cases so every MBTI type appears as an expected leading hypothesis at least once.
- Added matching golden good/bad fixtures for all 16 cases and tightened benchmark validation to require all-16 leading-type coverage.
- Added the Benchmark Type Coverage Matrix SVG and expanded repository UX gates to verify the new coverage proof, Case Gallery Audit 48/48, and Repository UX Score 171/171.

## 0.1.8 - 2026-05-28

- Fixed GitHub Pages navigation so README and prompt recipe buttons resolve to the public GitHub repository instead of parent-directory paths that 404 after deploy.
- Tightened repository UX gates to distinguish external links from external runtime dependencies and verify public README/prompt links.
- Raised Session Lab audit coverage to 61/61, Case Gallery audit coverage to 39/39, and repository UX scorecard coverage to 161/161.

## 0.1.7 - 2026-05-28

- Added a Benchmark Arena Pipeline SVG to make the benchmark JSON, sync script, public case gallery, audit gate, and issue feedback loop visible to first-time visitors.
- Added `scripts/sync_case_gallery.py` so `docs/case-gallery.html` is checked against the canonical benchmark JSON before release.
- Expanded Case Gallery audit coverage to verify JSON parity and raised the repository UX scorecard to 158/158.

## 0.1.6 - 2026-05-28

- Added a buildless Benchmark Arena case gallery with filters, trap inspection, runner-up/falsifier visibility, copied benchmark prompts, and benchmark issue seeds.
- Added a dedicated Case Gallery audit and wired it into `make test`.
- Expanded repository UX gates to verify the public benchmark surface and raised the scorecard to 144/144.

## 0.1.5 - 2026-05-28

- Added Session Lab share links, URL-hash recovery, editable JSON import, and a dedicated Session Lab audit gate.
- Added three precise SVG product blueprints for GitHub visitor routing, the typing engine, and the trust loop.
- Expanded `make test` and the repository UX scorecard to verify share/import/recovery behavior plus blueprint accessibility, labels, and dependency hygiene.

## 0.1.4 - 2026-05-28

- Added a local-first Session Lab that converts user notes into candidate triage, evidence ledger items, focused duels, next-round questions, report drafts, Codex prompts, and exportable session state.
- Updated GitHub Pages to open the Session Lab by default and expanded the repository UX scorecard.

## 0.1.3 - 2026-05-28

- Added a buildless interactive playground and GitHub Pages deployment workflow.

## 0.1.2 - 2026-05-28

- Added copy-paste prompt recipes, evidence-ledger example, final-session-state example, and activation validation.

## 0.1.1 - 2026-05-28

- Added a one-minute demo path, visual tour, sample live session, sample final report, and second journey-map image.

## 0.1.0 - 2026-05-28

- Initial open-source release.
- Added Codex skill for rigorous MBTI typing.
- Added evidence ledger, session state, pair duels, Chinese output style, and quality gates.
- Added benchmark cases and golden regression fixtures.
- Added local scorecard and CI workflow.
- Added GitHub README hero image, Mermaid system diagrams, GitHub UX documentation, and repository UX scorecard.
