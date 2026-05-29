# Experience Principles

The product goal is not "ask a long personality quiz." The goal is an adaptive reasoning experience that makes users feel the system is genuinely tracking them.

## Core Loop

1. State the current candidate set.
2. Ask a small number of high-yield questions.
3. Explain which answers moved which hypotheses.
4. Surface the strongest contradiction.
5. Choose the next discriminator.

This loop should feel progressive. Every round should narrow, split, or revise the model.

## What Makes It Addictive Without Being Manipulative

Use:

- Precision: name the exact behavior pattern, not a generic type slogan.
- Progressive revelation: show the user what became clearer this round.
- Contradiction handling: treat "that is not me" as valuable evidence.
- Personal utility: explain how the pattern affects work, conflict, recovery, and decision-making.
- Calibrated surprise: mention a non-obvious alternative when it is genuinely supported.

Do not use:

- Fake certainty.
- Flattery.
- Fear of missing out.
- Endless questioning with no state update.
- Barnum statements that fit almost anyone.
- Personality labels as identity locks.

## Allowed Retention Loop

The sticky loop should be evidence repair:

1. A user runs a typing session or report.
2. Calibration Lab checks the output against a benchmark case.
3. Failed gates become a repair prompt, JSON receipt, or calibration issue seed.
4. Repeated failures become benchmark cases, golden fixtures, or audit rules.

This keeps people returning because the system becomes more inspectable and harder to fool, not because it withholds answers or inflates certainty.

## Benchmark Replay Loop

The most game-like retention loop should still be falsifiable. Users should be able to replay hard benchmark cases without seeing the expected answer first.

The allowed loop is:

1. Benchmark Replay Lab loads the same canonical `benchmark-cases.json` cases as the public gallery.
2. The user copies a blind prompt before the reference leading type, runner-up, trap, and falsifier are visible.
3. The user records a leading type guess, runner-up guess, and falsifier or trap note.
4. Reveal Reference exposes the expected answer and turns the miss into a Replay Receipt, repair prompt, or `benchmark_replay_improvement.yml` issue seed.
5. Repeated replay misses become question-bank updates, pair-duel rules, benchmark edits, response-eval fixtures, or audit wording.

This creates an ethical challenge loop: people return because hard cases are replayable and mistakes become sharper prompts, not because the tool hides uncertainty or makes identity promises.

## Response Quality Loop

The most visible product moment is the answer between rounds. It has to make the user feel tracked without using identity hooks.

The allowed loop is:

1. A response states the current candidate set and serious runner-up before any label lock.
2. It shows evidence movement: what got stronger, what stayed weak, and what would reverse the order.
3. It asks 4-6 concrete scene questions only when those questions target the current fork.
4. It keeps falsifiers, safety boundaries, and calibrated confidence visible.
5. `examples/response-eval-cases.json` stores positive live-round, type-duel, and final-report fixtures plus a blocked anti-pattern.
6. `Response Eval Audit` checks sticky precision, next-round relevance, no-overclaim, negative blocking, and Anti-Flattery before release.

This creates stickiness through answer quality. The user returns because the response remembered the uncertainty and selected the next fork, not because it used 100% certainty, flattery, superiority language, or a permanent identity lock.

## Adaptive Question Loop

The highest-frequency retention moment is the next question. A user often knows the previous answer was not enough, but they do not know which fork should be tested next.

The allowed loop is:

1. The user reaches an unresolved uncertainty such as leader vs runner-up, normal vs stress state, public role vs private recovery, or Big Five cross-check.
2. Question Lab exposes source-synced probes from `question-bank.md`, including concrete questions, forced-choice options, contradiction follow-ups, and 4-6 question round templates.
3. The user copies a focused `$mbti-typing` round prompt that names the current uncertainty, required evidence state, runner-up, and falsifier target.
4. If a prompt feels repetitive or generic, the user copies a `question_improvement.yml` issue seed with the weak question, desired discriminator, sanitized context, and safety boundary.
5. Maintainers turn repeated weak-question patterns into question-bank updates, pair-duel rules, benchmark cases, golden fixtures, or report-audit checks.

This creates stickiness through adaptive precision: the tool earns another round by showing exactly why that round should exist.

## Adjacent-Type Precision Loop

The highest-value moment for many users is not the first label. It is the point where two nearby explanations both sound plausible.

The allowed loop is:

1. The user reaches a close fork such as ENTJ vs INTJ, INFP vs INFJ, or ENTP vs ESTP.
2. Type Duel Lab exposes the shared surface, Killer Questions, Losing Conditions, runner-up discipline, and falsifier focus from `pair-duels.md`.
3. The user copies a focused `$mbti-typing` duel prompt instead of restarting a generic quiz.
4. If a discriminator is weak, the user copies a `type_duel_improvement.yml` issue seed with the pair, limitation, proposed question, losing conditions, and sanitized evidence context.
5. Maintainers turn repeated pair misses into reference updates, benchmark cases, golden fixtures, or audit checks.

This creates stickiness through precision: the user sees exactly which fork is being tested and exactly what would make each side lose.

## Blind Improvement Loop

The strongest retention loop is public falsifiability:

1. Convert a confusing session into a sanitized blind packet.
2. Hide the reference answer from reviewers or model variants.
3. Compare top-1, top-2, runner-up, evidence tags, falsifiers, boundaries, and overclaim flags.
4. Turn aggregate misses into benchmark cases, golden fixtures, pair-duel prompts, or audit checks.

This gives advanced users a reason to return after the first report: they can watch the system become harder to fool.

## Consent-Based Return Loop

The highest-risk source of improvement is real user follow-up. It is valuable because people notice what felt wrong only after living with a report, but it is unsafe if the repository accepts raw private logs.

The allowed loop is:

1. The user shares only consented, redacted, public-safe observations.
2. Follow-Up Lab checks consent, redaction placeholders, sensitive markers, candidate set, runner-up, confidence, and falsifier before any public issue exists.
3. The packet preserves state labels, candidate set, runner-up, confidence, and falsifier.
4. The user states what felt right, what felt wrong, and what should be observed next.
5. The audit blocks direct identifiers, raw private chat, third-party details, missing consent, and missing withdrawal language.
6. Maintainers turn repeated feedback into benchmark cases, pair-duel questions, report-audit rules, or documentation changes.

This lets users come back with corrections without turning personal material into repository content.

## Cross-Agent Portability Loop

The workflow should survive tool switching. A user may start in Codex, share a repository with a Claude Code user, continue in Cursor, and later run opencode in a terminal. That should not create four subtly different typing protocols.

The allowed loop is:

1. `skill/mbti-typing/SKILL.md` remains the canonical reasoning source.
2. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `CONVENTIONS.md` keep concise project-level contracts for agents that read repository instructions.
3. Claude Code, Cursor, opencode, Gemini CLI, GitHub Copilot, Windsurf, Cline, Continue, aider, and generic AGENTS.md-aware adapters only describe discovery, invocation, and install shape.
4. `agent-adapters/manifest.json` records the supported entrypoints.
5. `scripts/export_agent_pack.py` exports all or selected adapter entrypoints into a portable pack with an `AGENT_PACK_MANIFEST.json` receipt.
6. `scripts/agent_adapter_audit.py` checks that adapters preserve candidate set, runner-up, evidence ledger, falsifier, source references, and safety boundaries.
7. `scripts/agent_pack_export_audit.py` checks that the manifest can become a copyable pack without omitting the canonical skill or selected target files.

This creates distribution stickiness: people can keep using the same MBTI Typing Skill even when their preferred agent runtime changes.

## Universal Agent Bridge Loop

The adapter layer must not depend on guessing the exact next platform. New agent hosts appear faster than repository maintainers can write bespoke adapters, so the durable loop is capability-first.

The allowed loop is:

1. A visitor opens Agent Portability Lab with either a known target or an unknown host.
2. The visitor checks only the capabilities the host can actually load: project instruction file, native `SKILL.md` directory, project rule or mode file, custom agent JSON/profile, slash command, chat project instructions, or config instruction array.
3. The lab generates a Universal Agent Bridge plan, portable install recipe, `agent-portability-lab/v1` adapter draft, and `agent_portability_request.yml` issue seed.
4. Maintainers turn repeated portability requests into new manifest targets only after source evidence confirms the host's instruction surface.
5. `scripts/sync_agent_portability_lab.py` and `scripts/agent_portability_lab_audit.py` keep the public page source-synced, local-first, copyable, and visibly bounded.

This creates generality without hand-waving: users can bring the skill to future tools because the bridge is based on instruction capabilities, while the project avoids claiming native support before a host proves it can load the canonical protocol.

## Experience Hub Loop

The Pages root should reduce choice paralysis instead of hiding the product behind a redirect. A visitor who lands on `docs/index.html` should see the main jobs immediately: start typing, validate an answer, study failures, install in an agent, map an unknown host, or contribute evidence.

The allowed loop is:

1. The visitor opens the Experience Hub and chooses a task card.
2. The page keeps a copyable starter prompt visible for agents that can already read `$mbti-typing`.
3. The Experience Hub Route Map shows how each route preserves candidate set, serious runner-up, evidence ledger, falsifier, and safety boundary.
4. The page links directly to Session Lab, Question Lab, Type Duel Lab, Response Eval Lab, Calibration Lab, Benchmark Replay Lab, Benchmark Arena, Follow-Up Lab, Agent Adapter Lab, and Agent Portability Lab.
5. `scripts/index_hub_audit.py` and the Index Hub Audit keep the root page local-first, non-redirecting, link-complete, copyable, and visually grounded before release.

This creates first-run stickiness without dark patterns: users return because the root page remembers the real jobs they came to do and sends them to the shortest useful workflow.

## Interview Rhythm

Each live round should usually contain 4-6 questions:

- 1 normal-state question.
- 1 stress or conflict question.
- 1 forced-choice tradeoff.
- 1 counterexample question.
- 1 pair-specific discriminator.
- Optional: 1 Big Five or life-context cross-check.

After each round, the system should briefly update:

- Current leader.
- Serious runner-up.
- Evidence that moved.
- Evidence that did not move.
- The next fork.

## Chinese Output Style

For Chinese users, the style should be direct, sharp, and evidence-led:

- Use short sections.
- Avoid therapy-like filler.
- Avoid horoscope-like prose.
- Say "目前证据更支持" instead of "你就是".
- Keep the strongest doubt visible.
- Make the next question feel like it was chosen for this person.

## Ending Well

A final report is successful when the user can answer these questions:

- Why this type over the runner-up?
- Which evidence mattered most?
- Which evidence was weak or ambiguous?
- What would make the result change?
- How should the user keep observing themselves?

The report should end with a working formulation, not a permanent verdict.
