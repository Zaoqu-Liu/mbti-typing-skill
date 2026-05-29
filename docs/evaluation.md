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

### 8. Response Quality Evaluation

Report audits catch final-output structure. Response evaluation catches the user-facing moment before that: whether a live answer earns the next round through sticky precision instead of fake certainty.

The response evaluation layer checks:

- Candidate set and serious runner-up are visible.
- Evidence movement is stated: what moved, what did not move, and why.
- Live and duel responses ask 4-6 concrete scene questions.
- Falsifiers and safety boundaries remain visible.
- Final reports include cross-framework boundaries when relevant.
- Anti-pattern responses with 100% certainty, flattery, no runner-up, no falsifier, or no next questions are blocked.

Checked by:

```bash
python3 -B scripts/response_eval_audit.py examples/response-eval-cases.json
python3 -B scripts/response_eval_lab_audit.py docs/response-eval-lab.html
```

Current target:

```text
Response Eval Audit: 45/45 (100.00%)
Response Eval Metrics: cases=4; positive_pass: 3/3 (100.00%); negative_blocked: 1/1 (100.00%); sticky_precision: 3/3 (100.00%); next_round: 3/3 (100.00%); no_overclaim: 3/3 (100.00%)
Response Eval Lab Audit: 69/69 (100.00%)
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

The scorecard also requires a demo layer: a visual tour, a short demo session, a sample report, a second journey-map image, a GitHub social preview crop, a GitHub product command-center bitmap, and a Response Eval command-center bitmap. This prevents the repository from becoming only a technical reference; visitors should be able to feel the typing loop quickly.

The visual blueprint gate checks that the README and visual tour expose twenty-two exact-label SVG assets:

- `docs/assets/experience-hub-route-map.svg` for the Pages root workflow selector to starter prompt to proof route.
- `docs/assets/github-ux-flywheel.svg` for the first-scan to local try-run to proof to Core Pack to return-evidence to safe-contribution repository flywheel.
- `docs/assets/repository-experience-map.svg` for the first-time GitHub visitor path.
- `docs/assets/typing-os-stack.svg` for the intake, hypothesis, question, evidence, duel, audit, distribution, and release-gate layering model.
- `docs/assets/typing-engine-blueprint.svg` for the evidence, duel, audit, and falsifier architecture.
- `docs/assets/evidence-retention-loop.svg` for the user-contradiction to ledger delta to runner-up pressure to next discriminator to benchmark repair retention loop.
- `docs/assets/trust-loop-dashboard.svg` for the feedback-to-benchmark-to-release trust loop.
- `docs/assets/benchmark-arena-pipeline.svg` for the benchmark JSON to case gallery source-of-truth sync.
- `docs/assets/benchmark-replay-loop.svg` for the benchmark JSON to blind replay to Replay Receipt to repair prompt feedback loop.
- `docs/assets/type-coverage-matrix.svg` for the all-16-leading-types benchmark coverage proof.
- `docs/assets/calibration-loop-map.svg` for the report paste to Calibration Receipt to repair prompt feedback loop.
- `docs/assets/blind-review-arena.svg` for the sanitized packet to independent reviewer to aggregate metrics evaluation loop.
- `docs/assets/consent-feedback-loop.svg` for the consented follow-up to redaction to repository-action loop.
- `docs/assets/adaptive-question-loop.svg` for the question-bank Markdown to Question Lab to audit-gate loop.
- `docs/assets/type-duel-decision-map.svg` for the pair-duels Markdown to Type Duel Lab to audit-gate loop.
- `docs/assets/agent-adapter-matrix.svg` for the canonical skill to Codex, Claude Code, Cursor, opencode, and audit-gate portability loop.
- `docs/assets/agent-compatibility-grid.svg` for the maintainable Core Pack surface across Codex, Claude Code, Cursor, and opencode, plus optional manifest recipes for teams that explicitly need another host.
- `docs/assets/agent-pack-export-flow.svg` for the manifest to exported pack to target repository copy path.
- `docs/assets/agent-adapter-lab-flow.svg` for the manifest to Agent Adapter Lab to pack command to target repository to `agent_adapter_improvement.yml` loop.
- `docs/assets/universal-agent-bridge-map.svg` for the known or unknown host to capability map to Agent Portability Lab to `agent_portability_request.yml` loop.
- `docs/assets/response-quality-radar.svg` for the answer-level candidate set, runner-up, evidence movement, next-question, falsifier, safety-boundary, Anti-Flattery, and response audit gates.
- `docs/assets/response-eval-lab-flow.svg` for the paste answer to mode-aware gates to quality radar to JSON receipt to repair prompt to `response_eval_improvement.yml` loop.

These SVGs are checked for accessibility metadata, expected product labels, and absence of script or remote dependencies. Bitmap visuals such as `docs/assets/social-preview.jpg`, `docs/assets/github-product-command-center.png`, and `docs/assets/response-eval-command-center.png` can create atmosphere; SVG blueprints carry precise workflow claims.

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

The Agent Adapter Audit validates that every supported agent entrypoint points back to one canonical protocol and preserves runner-up, falsifier, evidence-ledger, source-reference, and safety-boundary discipline:

```bash
python3 -B scripts/agent_adapter_audit.py .
```

The Agent Pack Export Audit validates that the compatibility layer can be exported into a portable directory without hand-copying drift. It checks the first-class Core Pack export, dry-run JSON, all-target export, selective export, required files, unknown-target failure, non-empty destination protection, and the generated `AGENT_PACK_MANIFEST.json` receipt:

```bash
python3 -B scripts/agent_pack_export_audit.py .
```

The Agent Adapter Lab Source Sync and Audit validate the public adoption surface: `docs/agent-adapter-lab.html` must embed the exact `agent-adapters/manifest.json` target set plus pack baseline paths, stay buildless, local-first, DOM-safe, copyable, and visibly bounded. It checks target selector, support filter, pack command, install checklist, adapter JSON receipt, issue seed, `agent_adapter_improvement.yml`, and `docs/assets/agent-adapter-lab-flow.svg` contribution path:

```bash
python3 -B scripts/sync_agent_adapter_lab.py agent-adapters/manifest.json docs/agent-adapter-lab.html
python3 -B scripts/agent_adapter_lab_audit.py docs/agent-adapter-lab.html agent-adapters/manifest.json
```

The Agent Portability Lab Source Sync and Audit validate the future-host bridge: `docs/agent-portability-lab.html` must embed the exact known targets from `agent-adapters/manifest.json` plus the capability axes used to support unknown hosts. It stays buildless, local-first, DOM-safe, copyable, and visibly bounded. It checks known target selection, unknown host intake, capability cards, Universal Agent Bridge plan, portable install recipe, `agent-portability-lab/v1` adapter draft, `agent_portability_request.yml` issue seed, `docs/assets/universal-agent-bridge-map.svg`, and safety-boundary language:

```bash
python3 -B scripts/sync_agent_portability_lab.py agent-adapters/manifest.json docs/agent-portability-lab.html
python3 -B scripts/agent_portability_lab_audit.py docs/agent-portability-lab.html agent-adapters/manifest.json .github/ISSUE_TEMPLATE/agent_portability_request.yml
```

The Index Hub Audit validates the Pages root: `docs/index.html` must be a real Experience Hub, not a redirect. It stays buildless, local-first, copyable, and visibly bounded. It checks workflow cards, direct links to every public lab, starter prompt copy, `docs/assets/experience-hub-route-map.svg`, safety-boundary language, and absence of unsafe rendering patterns:

```bash
python3 -B scripts/index_hub_audit.py docs/index.html docs/assets/experience-hub-route-map.svg
```

The Response Eval Audit validates that examples and future templates do not drift into shallow label assignment. It checks `examples/response-eval-cases.json` for positive live-round, type-duel, and final-report fixtures plus a blocked anti-pattern fixture, then reports `positive_pass`, `negative_blocked`, `sticky_precision`, `next_round`, and `no_overclaim` metrics:

```bash
python3 -B scripts/response_eval_audit.py examples/response-eval-cases.json
```

The Response Eval Lab Audit validates the public answer-quality surface: `docs/response-eval-lab.html` must stay buildless, local-first, DOM-safe, mode-aware, copyable, and visibly bounded as not psychometric ground truth. It also checks the repair prompt, Eval JSON, issue seed, radar, and `response_eval_improvement.yml` contribution path:

```bash
python3 -B scripts/response_eval_lab_audit.py docs/response-eval-lab.html
```

The repository UX scorecard also checks the Session Lab, Question Lab, Type Duel Lab, Benchmark Arena, Benchmark Replay Lab, Calibration Lab, static playground, and GitHub Pages workflow. The Session Lab must be buildless, local-first, shareable, importable, exportable, and free of external runtime dependencies so the first experience is fast, inspectable, and useful before installation.

The dedicated Session Lab audit validates the HTML interaction contract: visible share/import controls, all 16 type codes, URL-hash recovery, unicode-safe share links, JSON import/download, local persistence, DOM-safe rendering, safety boundaries, and focused candidate count.

The dedicated Case Gallery audit validates the public benchmark surface: all current benchmark cases, all 16 leading types, source-of-truth sync from `skill/mbti-typing/examples/benchmark-cases.json`, case filters, copied `Use $mbti-typing` prompts, benchmark issue seeds, visible runner-up/falsifier language, DOM-safe rendering, and no external runtime dependency.

The Benchmark Replay Lab Source Sync and Audit validate the active benchmark training surface: `docs/benchmark-replay-lab.html` must embed the exact canonical benchmark case set, preserve blind prompts before reference reveal, score leading type, runner-up, falsifier, and trap-awareness guesses, copy Replay Receipt JSON, repair prompts, and `benchmark_replay_improvement.yml` issue seeds, and keep local-first safety-boundary language visible.

```bash
python3 -B scripts/sync_benchmark_replay_lab.py skill/mbti-typing/examples/benchmark-cases.json docs/benchmark-replay-lab.html
python3 -B scripts/benchmark_replay_lab_audit.py docs/benchmark-replay-lab.html skill/mbti-typing/examples/benchmark-cases.json .github/ISSUE_TEMPLATE/benchmark_replay_improvement.yml
```

The dedicated Calibration Lab audit validates the public repair surface: all current benchmark cases, all 16 leading types, source-of-truth sync from `skill/mbti-typing/examples/benchmark-cases.json`, report paste, visible calibration gates, copied repair prompt, copied calibration JSON, copied failure issue seed, local persistence, DOM-safe rendering, and no external runtime dependency.

The dedicated Question Lab audit validates the public next-round surface: every current subsection in `skill/mbti-typing/references/question-bank.md`, Markdown source sync through `scripts/sync_question_lab.py`, search and category filters, concrete question goals, forced-choice options, copied 4-6 question round prompts, `question_improvement.yml` issue seeds, local persistence, DOM-safe rendering, and no external runtime dependency.

The dedicated Type Duel Lab audit validates the public adjacent-type surface: every current pair in `skill/mbti-typing/references/pair-duels.md`, all 16 type codes, Markdown source sync through `scripts/sync_type_duel_lab.py`, search and cluster filters, Killer Questions, Losing Conditions, copied duel prompts, `type_duel_improvement.yml` issue seeds, local persistence, DOM-safe rendering, and no external runtime dependency.

The dedicated Follow-Up Lab audit validates the public return surface: all 16 type codes, consent checkboxes, redaction placeholders, local privacy scanner, `consented-followup/v1` packet builder, copied issue seed, copied or downloaded JSON, local persistence, DOM-safe rendering, and no external runtime dependency.

The dedicated Agent Adapter audit validates the distribution surface: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CONVENTIONS.md`, `opencode.json`, `.aider.conf.yml`, `.gemini/settings.json`, `.claude/skills/mbti-typing/SKILL.md`, `.claude/commands/mbti-type.md`, `.cursor/rules/mbti-typing.mdc`, `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md`, `.windsurf/rules/mbti-typing.md`, `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md`, `.continue/rules/mbti-typing.md`, `agent-adapters/manifest.json`, `docs/agent-adapters.md`, `docs/agent-adapter-lab.html`, `docs/agent-portability-lab.html`, `docs/assets/agent-adapter-matrix.svg`, `docs/assets/agent-compatibility-grid.svg`, `docs/assets/agent-pack-export-flow.svg`, `docs/assets/agent-adapter-lab-flow.svg`, `docs/assets/universal-agent-bridge-map.svg`, `.github/ISSUE_TEMPLATE/agent_adapter_improvement.yml`, `.github/ISSUE_TEMPLATE/agent_portability_request.yml`, `scripts/export_agent_pack.py`, `scripts/agent_pack_export_audit.py`, `scripts/sync_agent_adapter_lab.py`, `scripts/agent_adapter_lab_audit.py`, `scripts/sync_agent_portability_lab.py`, and `scripts/agent_portability_lab_audit.py` must stay aligned with the canonical skill and the current tool conventions checked on 2026-05-29.

The dedicated Agent Pack Export audit validates the adoption path: `scripts/export_agent_pack.py` must export the canonical skill tree, baseline contracts, selected target entrypoints, adapter docs, prompt recipes, and an `AGENT_PACK_MANIFEST.json` receipt, while refusing unknown targets and non-empty destinations unless the user explicitly chooses `--force`.

The dedicated Agent Adapter Lab audit validates the adoption UX path: `docs/agent-adapter-lab.html`, `scripts/sync_agent_adapter_lab.py`, `scripts/agent_adapter_lab_audit.py`, `.github/ISSUE_TEMPLATE/agent_adapter_improvement.yml`, and `docs/assets/agent-adapter-lab-flow.svg` must stay aligned so visitors can select agent targets, copy the pack command, inspect the install checklist, export adapter JSON, and file adapter improvements without losing the candidate set, runner-up, evidence ledger, falsifier, or safety-boundary contract.

The dedicated Agent Portability Lab audit validates the generalization path: `docs/agent-portability-lab.html`, `scripts/sync_agent_portability_lab.py`, `scripts/agent_portability_lab_audit.py`, `.github/ISSUE_TEMPLATE/agent_portability_request.yml`, and `docs/assets/universal-agent-bridge-map.svg` must stay aligned so visitors can map a new or unknown host by capability, copy a bridge plan, copy a portable install recipe, export an adapter draft JSON, and file a portability request without losing the candidate set, runner-up, evidence ledger, falsifier, or safety-boundary contract.

The dedicated Index Hub audit validates the first-run product surface: `docs/index.html`, `docs/assets/experience-hub-route-map.svg`, and `scripts/index_hub_audit.py` must stay aligned so visitors can choose a task, copy a starter prompt, and reach every public workflow without a redirect or hidden network dependency.

The dedicated Response Eval audit validates the answer-level UX path: `examples/response-eval-cases.json`, `docs/assets/response-quality-radar.svg`, `docs/assets/response-eval-lab-flow.svg`, `docs/response-eval-lab.html`, `scripts/response_eval_audit.py`, and `scripts/response_eval_lab_audit.py` must stay aligned so examples and the public lab preserve candidate set, runner-up, evidence movement, next-round questions, falsifiers, safety boundaries, calibrated confidence, repair prompts, issue seeds, and Anti-Flattery discipline.

The public Pages link gate validates that README and prompt recipe buttons resolve to GitHub repository URLs. Local-first pages can link out to documentation; they just cannot depend on external scripts, remote assets, or network calls to render the core workflow.
