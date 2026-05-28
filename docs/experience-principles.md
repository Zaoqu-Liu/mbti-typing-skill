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
