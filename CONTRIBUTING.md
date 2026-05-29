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
- Share blind benchmark replay misses through `docs/benchmark-replay-lab.html` and the `benchmark_replay_improvement.yml` issue template.
- Improve next-round probes through `docs/question-lab.html` and the `question_improvement.yml` issue template.
- Improve pair-duel discriminators.
- Share weak adjacent-type forks through `docs/type-duel-lab.html` and the `type_duel_improvement.yml` issue template.
- Add realistic bad reports that should fail audit.
- Share Calibration Lab failures through the `calibration_result.yml` issue template.
- Share sanitized blind review findings through the `blind_review.yml` issue template.
- Share consented follow-up observations through `docs/follow-up-lab.html` and the `consented_followup.yml` issue template.
- Improve agent adapters for Codex, Claude Code, Cursor, opencode, Gemini CLI, GitHub Copilot, Windsurf, Cline, Continue, aider, or AGENTS.md-aware tools without forking the protocol.
- Improve `scripts/export_agent_pack.py` so cross-agent adoption is easier to copy into another repository.
- Improve adapter adoption through `docs/agent-adapter-lab.html` and the `agent_adapter_improvement.yml` issue template.
- Add or repair future-host support through `docs/agent-portability-lab.html` and the `agent_portability_request.yml` issue template before committing a bespoke adapter.
- Improve the first-run GitHub Pages route through `docs/index.html`, `docs/assets/experience-hub-route-map.svg`, and `scripts/index_hub_audit.py` so new visitors can pick a task before reading internals.
- Add response-eval fixtures that catch shallow live-round, type-duel, final-report, or anti-pattern answers.
- Share weak answers through `docs/response-eval-lab.html` and the `response_eval_improvement.yml` issue template.
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
Blind Review Audit: 93/93 (100.00%)
Consent Redaction Audit: 78/78 (100.00%)
Agent Adapter Audit: 326/326 (100.00%)
Agent Pack Export Audit: 24/24 (100.00%)
Agent Adapter Lab Audit: 91/91 (100.00%)
Agent Portability Lab Audit: 92/92 (100.00%)
Index Hub Audit: 82/82 (100.00%)
Response Eval Audit: 45/45 (100.00%)
Response Eval Lab Audit: 69/69 (100.00%)
Question Lab Audit: 71/71 (100.00%)
Type Duel Lab Audit: 68/68 (100.00%)
Benchmark Replay Lab Audit: 62/62 (100.00%)
Follow-Up Lab Audit: 61/61 (100.00%)
Calibration Lab Audit: 53/53 (100.00%)
Repository UX Score: 641/641 (100.00%)
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

## Benchmark Replay Guidelines

Benchmark replay contributions are useful when a benchmark prompt exposes a repeatable miss in leading type, runner-up preservation, falsifier recognition, or trap awareness.

Before opening a replay issue:

- Start with `docs/benchmark-replay-lab.html` when possible.
- Record the blind prompt replay before revealing the reference.
- Include the Replay Receipt score, leading guess, runner-up guess, and falsifier or trap note.
- Use `benchmark_replay_improvement.yml` for public-safe replay summaries.
- Explain whether the repair should update the benchmark prompt, question bank, pair duel, response eval fixture, or audit wording.
- Do not include private transcripts, direct identifiers, third-party details, clinical claims, hiring use cases, or deterministic claims about people.

## Question Improvement Guidelines

Question improvements are useful when the next round feels generic, repetitive, or unable to separate the leading type from a serious runner-up.

Before opening a question issue:

- Start with `docs/question-lab.html` when possible.
- Identify the target uncertainty, such as leader vs runner-up, normal vs stress, public role vs private recovery, contradiction follow-up, or Big Five cross-check.
- Propose a concrete scene-based question, not an abstract self-label question.
- Include the intended evidence state and what answer would weaken the current leading hypothesis.
- Include forced-choice options only when each side has a real losing condition.
- Preserve runner-up, falsifier, and safety-boundary language.
- Do not include private transcripts, direct identifiers, third-party details, clinical claims, hiring use cases, or deterministic claims about people.

## Calibration Result Guidelines

Calibration reports are useful when a model output looks plausible but fails a specific benchmark gate.

Before opening a calibration issue:

- Remove private or identifiable text.
- Include the benchmark case id.
- Include the Calibration Lab score.
- Include failed gates such as missing runner-up, missing falsifier, weak evidence tags, missing boundary, or overclaim trigger.
- Explain the expected repair in one or two concrete sentences.

## Type Duel Improvement Guidelines

Type duel improvements are useful when two adjacent types remain plausible after a normal interview round.

Before opening a type-duel issue:

- Start with `docs/type-duel-lab.html` when possible.
- Identify one pair, not a broad type family.
- Explain the current limitation with a synthetic or sanitized example.
- Propose one focused discriminator, not a generic self-label question.
- Include losing conditions for both sides.
- Preserve runner-up, falsifier, and safety-boundary language.
- Do not include private transcripts, direct identifiers, third-party details, clinical claims, hiring use cases, or deterministic claims about people.

## Blind Review Guidelines

Blind review contributions are useful when a typing output looks good only because the expected answer was visible.

Before opening a blind review issue:

- Remove private or identifiable text.
- Keep the expected answer hidden from reviewer outputs.
- Include at least two independent reviewer outputs.
- Include leading type, runner-up, confidence, evidence tags, falsifier, boundary statement, and overclaim flags.
- Include aggregate top-1, top-2, runner-up preservation, falsifier, boundary, and no-overclaim metrics.
- Explain whether the result should become a benchmark case, golden fixture, pair-duel rule, question-bank item, or report-audit rule.

## Consented Follow-Up Guidelines

Consented follow-up contributions are useful when a person has lived with a typing report long enough to notice what held up and what did not.

Before opening a consented follow-up issue:

- Start with `docs/follow-up-lab.html` when possible.
- Read `docs/consent-redaction-protocol.md`.
- Confirm subject consent and public issue permission.
- Do not include raw private chat logs, screenshots, names, handles, emails, phone numbers, exact dates, workplaces, schools, family identifiers, medical details, legal details, salary details, or identifiable third-party behavior.
- Use redaction placeholders such as `[PERSON_A]`, `[RELATIONSHIP_CONTEXT]`, `[DATE_RANGE]`, `[PROJECT]`, or `[WORKPLACE]`.
- Include a candidate set, leading type, runner-up, confidence, and falsifier.
- Include delayed observations across at least three states such as normal, stress, conflict, recovery, reflection, or relationship.
- Include what felt right, what felt wrong, and what should be observed next.
- Expect maintainers to turn useful patterns into benchmark cases, golden fixtures, pair-duel discriminators, report-audit checks, or documentation updates.

## Response Evaluation Guidelines

Response evaluation contributions are useful when an answer looks polished but fails the actual user experience.

Before opening a response-eval change:

- Start with `docs/response-eval-lab.html` when possible, so the failed gate, repair prompt, Eval JSON, and `response_eval_improvement.yml` issue seed are visible before editing fixtures.
- Add or edit `examples/response-eval-cases.json`.
- Cover one concrete mode: live round, type duel, final report, or anti-pattern.
- Positive examples must preserve candidate set, runner-up, evidence movement, falsifier, safety boundary, and calibrated confidence.
- Live-round and type-duel examples should ask 4-6 concrete scene questions selected for the current uncertainty.
- Anti-pattern examples should make the failure explicit: 100% certainty, flattery, label lock, missing runner-up, missing falsifier, missing safety boundary, or missing next questions.
- Run `python3 -B scripts/response_eval_audit.py examples/response-eval-cases.json`.
- Run `python3 -B scripts/response_eval_lab_audit.py docs/response-eval-lab.html` if the public lab, copy outputs, radar, issue seed, or gate wording changed.

## Agent Adapter Guidelines

Agent adapter contributions are useful when a mainstream agent tool changes discovery rules, install shape, or project-instruction conventions.

Before opening an adapter change:

- Keep `skill/mbti-typing/SKILL.md` as the canonical protocol.
- Update `AGENTS.md` only for concise cross-agent behavior, not tool-specific detail.
- Keep `CLAUDE.md`, `GEMINI.md`, `CONVENTIONS.md`, `.claude/skills/mbti-typing/SKILL.md`, `.claude/commands/mbti-type.md`, `.cursor/rules/mbti-typing.mdc`, `opencode.json`, `.gemini/settings.json`, `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md`, `.windsurf/rules/mbti-typing.md`, `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md`, `.continue/rules/mbti-typing.md`, `.aider.conf.yml`, and tool-specific files thin.
- Update `agent-adapters/manifest.json` if a target, entrypoint, install command, or invocation changes.
- Update `docs/agent-adapters.md` with source links and the date checked when tool conventions change.
- Start with `docs/agent-adapter-lab.html` when possible, so the target set, generated pack command, install checklist, adapter JSON receipt, and `agent_adapter_improvement.yml` issue seed are visible before editing files.
- Run `python3 -B scripts/agent_adapter_audit.py .` before claiming compatibility.
- Run `python3 -B scripts/agent_pack_export_audit.py .` if a manifest target, adapter file, pack exporter, install command, or portability claim changes.
- Run `python3 -B scripts/sync_agent_adapter_lab.py agent-adapters/manifest.json docs/agent-adapter-lab.html`.
- Run `python3 -B scripts/agent_adapter_lab_audit.py docs/agent-adapter-lab.html agent-adapters/manifest.json` if the manifest, pack baseline, public adoption lab, issue seed, or adapter UX wording changed.
- Preserve runner-up, falsifier, evidence-ledger, source-reference, and safety-boundary language in every adapter.

## Agent Portability Guidelines

Agent portability contributions are useful when a new or unknown host is likely to become a mainstream workflow, but its exact adapter shape is not proven yet.

Before opening a portability change:

- Start with `docs/agent-portability-lab.html` when possible.
- Map real host capabilities before proposing files: project instruction file, native `SKILL.md` directory, project rule or mode file, custom agent JSON/profile, slash command, chat project instructions, or config instruction array.
- Use `agent_portability_request.yml` for public-safe portability requests.
- Do not claim native skill support unless the host documentation or a real host run proves it.
- Keep the bridge thin: unknown hosts should route to `skill/mbti-typing/SKILL.md`, `AGENTS.md`, and the existing adapter manifest instead of duplicating the whole protocol.
- Update `agent-adapters/manifest.json` only after the target has stable entrypoints, invocation guidance, installation guidance, and a source URL.
- Run `python3 -B scripts/sync_agent_portability_lab.py agent-adapters/manifest.json docs/agent-portability-lab.html`.
- Run `python3 -B scripts/agent_portability_lab_audit.py docs/agent-portability-lab.html agent-adapters/manifest.json .github/ISSUE_TEMPLATE/agent_portability_request.yml`.
- Run `python3 -B scripts/agent_adapter_audit.py .` and `python3 -B scripts/agent_pack_export_audit.py .` if the change touches export packaging or named adapter targets.
- Preserve candidate set, serious runner-up, evidence ledger, falsifier, revision trigger, and safety-boundary language in every bridge.

## Experience Hub Guidelines

Experience Hub contributions are useful when the first GitHub Pages visit is unclear, too linear, or missing a path for a major user intent.

Before opening an Experience Hub change:

- Start with `docs/index.html` and choose the user job first: typing, validation, benchmark replay, follow-up evidence, agent installation, future-host portability, or contribution.
- Keep `docs/assets/experience-hub-route-map.svg` text-accurate and readable in README, visual tour, and Pages contexts.
- Preserve the starter prompt, candidate set, serious runner-up, evidence ledger, falsifier, and safety-boundary language.
- Link public Pages routes directly and use GitHub blob links for repository files that are outside `docs/`.
- Run `python3 -B scripts/index_hub_audit.py docs/index.html docs/assets/experience-hub-route-map.svg`.

## Pull Request Checklist

- [ ] `make test` passes.
- [ ] Any agent adapter change passes `scripts/agent_adapter_audit.py` and keeps `agent-adapters/manifest.json` aligned.
- [ ] Any adapter packaging or manifest change passes `scripts/agent_pack_export_audit.py`.
- [ ] Any Agent Portability Lab, future-host bridge, or portability issue-template change passes `scripts/sync_agent_portability_lab.py` and `scripts/agent_portability_lab_audit.py`.
- [ ] Any Experience Hub, first-run route, Pages root, or route-map change passes `scripts/index_hub_audit.py`.
- [ ] Any response example or output-template change passes `scripts/response_eval_audit.py`.
- [ ] Any Response Eval Lab, answer-quality gate, repair prompt, or issue seed change passes `scripts/response_eval_lab_audit.py`.
- [ ] Any new claim has a caveat or evidence standard.
- [ ] Any new question-bank improvement is source-synced through `scripts/sync_question_lab.py` and passes `scripts/question_lab_audit.py`.
- [ ] Any new type-pair guidance includes losing conditions for both sides.
- [ ] Any new type-duel improvement is source-synced through `scripts/sync_type_duel_lab.py` and passes `scripts/type_duel_lab_audit.py`.
- [ ] Any new benchmark case includes a trap and falsifier theme.
- [ ] Any Benchmark Replay Lab, replay issue seed, or replay gate change passes `scripts/sync_benchmark_replay_lab.py` and `scripts/benchmark_replay_lab_audit.py`.
- [ ] Any new calibration result is sanitized and points to a specific failed gate.
- [ ] Any new blind review result preserves blinding and includes aggregate metrics.
- [ ] Any new follow-up packet is consented, redacted, withdrawable, and passes `scripts/consent_redaction_audit.py`.
- [ ] No clinical, hiring, or deterministic use case has been added.
