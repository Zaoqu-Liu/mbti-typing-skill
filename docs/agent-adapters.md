# Agent Adapters

The MBTI Typing Skill should be portable across mainstream agent tools without becoming four separate protocols.

## Design Rule

One canonical protocol, many thin adapters:

- `skill/mbti-typing/SKILL.md` remains the deepest source of truth.
- `AGENTS.md` is the short repository-level contract for tools that read project instructions.
- Tool-specific files only explain discovery and invocation.
- `scripts/agent_adapter_audit.py` blocks drift.

## Supported Tools

![Agent Adapter Matrix](assets/agent-adapter-matrix.svg)

| Tool | Files | Why this shape |
|---|---|---|
| Codex | `skill/mbti-typing/SKILL.md`, `skill/mbti-typing/agents/openai.yaml`, `AGENTS.md` | Codex already consumes a local skill package and project-level agent instructions. |
| Claude Code | `.claude/skills/mbti-typing/SKILL.md`, `.claude/commands/mbti-type.md` | Claude Code skills are directory-based `SKILL.md` files; command files remain compatible. |
| Cursor | `.cursor/rules/mbti-typing.mdc`, `AGENTS.md` | Cursor project rules live in `.cursor/rules` as MDC files and can also use `AGENTS.md`. |
| opencode | `AGENTS.md`, `opencode.json` | opencode reads `AGENTS.md`; `opencode.json` can aggregate instruction files. |

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

## Release Gate

```bash
python3 -B scripts/agent_adapter_audit.py .
make test
```

The adapter audit checks file presence, manifest targets, install commands, invocation strings, safety boundaries, and source references.
