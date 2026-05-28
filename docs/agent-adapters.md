# Agent Adapters

The MBTI Typing Skill should be portable across mainstream agent tools without becoming eleven separate protocols.

## Design Rule

One canonical protocol, many thin adapters:

- `skill/mbti-typing/SKILL.md` remains the deepest source of truth.
- `AGENTS.md` is the short repository-level contract for tools that read project instructions.
- Tool-specific files only explain discovery and invocation.
- `scripts/agent_adapter_audit.py` blocks drift.

## Supported Tools

![Agent Adapter Matrix](assets/agent-adapter-matrix.svg)

![Agent Compatibility Grid](assets/agent-compatibility-grid.svg)

| Tool | Files | Why this shape |
|---|---|---|
| Codex | `skill/mbti-typing/SKILL.md`, `skill/mbti-typing/agents/openai.yaml`, `AGENTS.md` | Codex already consumes a local skill package and project-level agent instructions. |
| Generic AGENTS.md-aware agents | `AGENTS.md`, `CONVENTIONS.md` | Keeps a lowest-common-denominator contract for agents that read project instruction files. |
| Claude Code | `.claude/skills/mbti-typing/SKILL.md`, `.claude/commands/mbti-type.md` | Claude Code skills are directory-based `SKILL.md` files; command files remain compatible. |
| Cursor | `.cursor/rules/mbti-typing.mdc`, `AGENTS.md` | Cursor project rules live in `.cursor/rules` as MDC files and can also use `AGENTS.md`. |
| opencode | `AGENTS.md`, `opencode.json` | opencode reads `AGENTS.md`; `opencode.json` can aggregate instruction files. |
| Gemini CLI | `GEMINI.md`, `.gemini/settings.json`, `AGENTS.md` | Gemini CLI context files can load project memory; this adapter routes context back to the same protocol. |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md` | Repository instructions and project skill entrypoints keep Copilot aligned with the canonical skill. |
| Windsurf | `.windsurf/rules/mbti-typing.md`, `AGENTS.md` | Workspace rules keep the typing protocol available during Cascade-style coding sessions. |
| Cline | `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md`, `AGENTS.md` | Project skill and rule both point back to the canonical source. |
| Continue | `.continue/rules/mbti-typing.md`, `AGENTS.md` | Local rule file preserves the evidence-led workflow in Continue sessions. |
| aider | `CONVENTIONS.md`, `.aider.conf.yml`, `AGENTS.md` | Conventions file and read config keep the protocol visible during pair-programming sessions. |

## What Must Never Drift

Every adapter must preserve:

- candidate set and serious runner-up
- evidence ledger
- 4-6 question rhythm
- adjacent-type duel discipline
- source references to `question-bank.md` and `pair-duels.md`
- falsifiers and revision triggers
- safety boundary against clinical, hiring, legal, medical, financial, or deterministic use

## Current Source Notes

These conventions were checked on 2026-05-28:

- [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills) documents skills as `SKILL.md` files and says project skills live under `.claude/skills/<skill-name>/SKILL.md`; [Claude Code slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) also states legacy `.claude/commands/` files keep working.
- [Cursor rules](https://docs.cursor.com/en/context/rules) documents project rules under `.cursor/rules` using MDC files with frontmatter such as `description`, `globs`, and `alwaysApply`, and lists `AGENTS.md` as a simple alternative.
- [opencode rules](https://opencode.ai/docs/rules/) documents `AGENTS.md` as its project instruction file, and [opencode config](https://opencode.ai/docs/config/) supports `opencode.json` with an `instructions` array for additional instruction files.
- The [OpenAI Codex repository](https://github.com/openai/codex) itself uses a root `AGENTS.md`, and this project keeps Codex's existing local skill package as the primary entrypoint.
- The [Gemini CLI configuration docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md) document context file loading and configurable context file names.
- [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) document `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, root instruction files such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`, and project skill locations.
- [Windsurf rules](https://docs.windsurf.com/windsurf/cascade/rules) document workspace rule files and activation metadata.
- [Cline skills](https://docs.cline.bot/features/skills) and Cline rules document project skills and repository rules for reusable agent behavior.
- [Continue rules](https://docs.continue.dev/customize/deep-dives/rules) document repository-local rule files under `.continue/rules`.
- [aider conventions](https://aider.chat/docs/usage/conventions.html) document `CONVENTIONS.md` as a project convention file that can be loaded into coding sessions.

## Release Gate

```bash
python3 -B scripts/agent_adapter_audit.py .
make test
```

The adapter audit checks file presence, manifest targets, install commands, invocation strings, safety boundaries, and source references.
