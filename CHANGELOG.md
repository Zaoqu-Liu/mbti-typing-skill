# Changelog

## 0.1.26 - 2026-05-29

- Added a low-typing question UX contract across the canonical skill, playbooks, question bank, Core Pack adapters, and agent docs: use native question UI only when present, otherwise ask compact `A/B/C/D/E` choices with a final `Other / none of these` escape hatch.
- Updated Cursor, Claude Code, Codex, opencode, Agent Adapter Lab, Agent Portability Lab, Question Lab, and Response Eval Lab so the low-friction choice path is visible, copyable, and source-synced instead of being a README-only recommendation.
- Added audit coverage for native-question gating and choice-first answers, raising Agent Adapter Audit to 339/339, Agent Adapter Lab Audit to 98/98, Agent Portability Lab Audit to 95/95, Response Eval Audit to 46/46, Response Eval Lab Audit to 71/71, Question Lab Audit to 74/74, and Repository UX Score to 678/678.

## 0.1.25 - 2026-05-29

- Added a maintainable first-class Core Pack for Codex, Claude Code, Cursor, and opencode, including the `--target core` export path, manifest `core_targets`, Agent Adapter Lab defaults, and stricter pack-export audits.
- Added the `imagegen` GitHub Product Command Center bitmap plus three precise SVG blueprints: GitHub UX Flywheel, MBTI Typing OS Stack, and Evidence Retention Loop, so the repository explains user retention, maintainable scope, and stateful evidence flow from a first-time visitor's perspective.
- Wired the new visual assets, Core Pack guidance, and audit expectations into README, Chinese README, Visual Tour, Evaluation, GitHub UX guidance, contribution rules, and repository gates, raising Agent Adapter Audit to 328/328, Agent Pack Export Audit to 28/28, Agent Adapter Lab Audit to 94/94, and Repository UX Score to 670/670.

## 0.1.24 - 2026-05-29

- Replaced the GitHub Pages root redirect with a buildless Experience Hub that routes first-time visitors by task: typing, answer review, benchmark replay, follow-up evidence, agent installation, future-host portability, and contribution.
- Added the Experience Hub Route Map SVG and direct starter-prompt UX so README, Pages, and the visual tour explain the full product loop before a user chooses a lab.
- Added `scripts/index_hub_audit.py` and wired it into `make test`, README, evaluation docs, contribution rules, and repository UX gates, raising Index Hub Audit to 82/82 and Repository UX Score to 641/641.

## 0.1.23 - 2026-05-29

- Added a buildless Agent Portability Lab for future or unknown agent hosts, with capability-first host intake, Universal Agent Bridge plans, portable install recipes, `agent-portability-lab/v1` adapter drafts, and `agent_portability_request.yml` issue seeds.
- Added `scripts/sync_agent_portability_lab.py`, `scripts/agent_portability_lab_audit.py`, and the Universal Agent Bridge Map SVG so new-host support is source-synced from `agent-adapters/manifest.json` and release-gated.
- Expanded the agent pack baseline and public navigation to include the portability lab, raising Agent Adapter Audit to 326/326, Agent Portability Lab Audit to 92/92, and Repository UX Score to 618/618.

## 0.1.22 - 2026-05-29

- Expanded the adapter surface from 11 to 18 targets: ChatGPT GPTs/Projects, Zed Agent Panel, Devin, JetBrains Junie, Amazon Q Developer CLI, Roo Code, and Kilo Code now join Codex, Claude Code, Cursor, opencode, Gemini CLI, GitHub Copilot, Windsurf, Cline, Continue, aider, and AGENTS.md-aware agents.
- Added native entrypoints for the new tools: `.rules`, `.roomodes`, `.roo/rules-mbti-typing/mbti-typing.md`, `kilo.jsonc`, `.kilo/rules/mbti-typing.md`, `.junie/AGENTS.md`, `.junie/commands/mbti-type.md`, `.amazonq/cli-agents/mbti-typing.json`, and `gpts/mbti-typing-gpt-instructions.md`.
- Added a buildless Benchmark Replay Lab that turns canonical benchmark cases into blind prompts, top-two guesses, reference reveal, Replay Receipt JSON, repair prompts, and `benchmark_replay_improvement.yml` issue seeds.
- Added `scripts/sync_benchmark_replay_lab.py`, `scripts/benchmark_replay_lab_audit.py`, and the Benchmark Replay Loop SVG so replay UX is source-synced and release-gated.
- Updated the manifest, Agent Adapter Lab, adapter docs, visual diagrams, export audit, and repository UX gates, raising Agent Adapter Audit to 313/313, Agent Adapter Lab Audit to 91/91, Benchmark Replay Lab Audit to 62/62, and Repository UX Score to 581/581.

## 0.1.21 - 2026-05-28

- Added a buildless Agent Adapter Lab so users can select Codex, Claude Code, Cursor, opencode, Gemini CLI, GitHub Copilot, Windsurf, Cline, Continue, aider, or AGENTS.md-aware targets and copy a pack command, install checklist, adapter JSON receipt, and `agent_adapter_improvement.yml` issue seed.
- Added `scripts/sync_agent_adapter_lab.py`, `scripts/agent_adapter_lab_audit.py`, the Agent Adapter Lab Flow SVG, and the adapter improvement issue template so public adoption UX is source-synced from `agent-adapters/manifest.json`.
- Expanded the agent pack baseline to carry the adoption lab and adapter audit scripts, and wired the new lab into `make test`, README, visual tour, evaluation docs, contribution rules, and repository UX gates, raising the Repository UX Score to 521/521.

## 0.1.20 - 2026-05-28

- Added a buildless Response Eval Lab so users can paste any MBTI answer, inspect mode-aware quality gates, copy a repair prompt, export Eval JSON, and create a `response_eval_improvement.yml` issue seed.
- Added `scripts/response_eval_lab_audit.py`, a GitHub social preview crop, the Response Eval Command Center bitmap, and the Response Eval Lab Flow SVG to make answer-quality UX visible and release-gated.
- Wired the lab, issue template, and new visual assets into `make test`, README, visual tour, evaluation docs, contribution rules, and repository UX gates, raising the Repository UX Score to 488/488.

## 0.1.19 - 2026-05-28

- Added `examples/response-eval-cases.json` and `scripts/response_eval_audit.py` so live-round, type-duel, final-report, and anti-pattern answers are release-gated for candidate set, runner-up, evidence movement, next questions, falsifiers, safety boundaries, and Anti-Flattery discipline.
- Added the Response Quality Radar SVG to make answer-level UX auditable for first-time GitHub visitors.
- Wired the response quality gate into `make test`, README, evaluation docs, visual tour, contribution rules, and repository UX gates, raising the Repository UX Score to 445/445.

## 0.1.18 - 2026-05-28

- Added `scripts/export_agent_pack.py` so `agent-adapters/manifest.json` can export a portable all-target or selective adapter pack instead of leaving users to hand-copy hidden agent files.
- Added `scripts/agent_pack_export_audit.py`, the Agent Pack Export Flow SVG, and manifest links for the pack exporter and pack audit.
- Wired the pack export path into `make test`, adapter docs, README, visual tour, evaluation docs, and repository UX gates, raising the Agent Adapter Audit to 201/201 and the Repository UX Score to 423/423.

## 0.1.17 - 2026-05-28

- Expanded the adapter layer from the four core targets to 11 entrypoints: Codex, generic AGENTS.md-aware agents, Claude Code, Cursor, opencode, Gemini CLI, GitHub Copilot, Windsurf, Cline, Continue, and aider.
- Added `CLAUDE.md`, `GEMINI.md`, `CONVENTIONS.md`, `.gemini/settings.json`, `.aider.conf.yml`, `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md`, `.windsurf/rules/mbti-typing.md`, `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md`, `.continue/rules/mbti-typing.md`, and the Agent Compatibility Grid SVG.
- Expanded `scripts/agent_adapter_audit.py` to 189 checks and wired the broader compatibility surface into repository UX gates, raising the Repository UX Score to 405/405.

## 0.1.16 - 2026-05-28

- Added a cross-agent adapter layer for Codex, Claude Code, Cursor, opencode, and AGENTS.md-aware agents without forking the canonical MBTI typing protocol.
- Added `AGENTS.md`, `opencode.json`, `.claude/skills/mbti-typing/SKILL.md`, `.claude/commands/mbti-type.md`, `.cursor/rules/mbti-typing.mdc`, `agent-adapters/manifest.json`, `docs/agent-adapters.md`, and the Agent Adapter Matrix SVG.
- Added `scripts/agent_adapter_audit.py` and wired it into `make test` and repository UX gates, raising the Repository UX Score to 361/361.

## 0.1.15 - 2026-05-28

- Added a buildless Question Lab that turns `question-bank.md` into a searchable Round Builder with concrete probes, forced-choice options, 4-6 question templates, copyable `$mbti-typing` round prompts, and `question_improvement.yml` issue seeds.
- Added `scripts/sync_question_lab.py`, `scripts/question_lab_audit.py`, and the Adaptive Question Loop SVG so question-bank source drift, page safety, and GitHub UX claims are release-gated.
- Expanded the public product loop with a next-question precision layer between Session Lab and Type Duel Lab, raising the Repository UX Score to 325/325.

## 0.1.14 - 2026-05-28

- Added a buildless Type Duel Lab that turns `pair-duels.md` into a searchable adjacent-type matrix with Killer Questions, Losing Conditions, copyable `$mbti-typing` duel prompts, and `type_duel_improvement.yml` issue seeds.
- Added `scripts/sync_type_duel_lab.py`, `scripts/type_duel_lab_audit.py`, and the Type Duel Decision Map SVG so pair-duel source drift, page safety, and GitHub UX claims are release-gated.
- Expanded the public product loop with a precision layer for close forks such as ENTJ vs INTJ, INFP vs INFJ, ENTP vs ESTP, and all current source duels, raising the Repository UX Score to 294/294.

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
