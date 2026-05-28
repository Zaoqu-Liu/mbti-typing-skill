# Agent Adapter Layer

This directory documents how the same MBTI Typing Skill is exposed to multiple agent tools without changing the underlying reasoning protocol.

## Source Of Truth

- Canonical protocol: `skill/mbti-typing/SKILL.md`
- Shared project contract: `AGENTS.md`
- Adapter manifest: `agent-adapters/manifest.json`
- Drift gate: `scripts/agent_adapter_audit.py`

## Adapter Matrix

![Agent Adapter Matrix](../docs/assets/agent-adapter-matrix.svg)

| Tool | Primary entrypoint | Invocation | Notes |
|---|---|---|---|
| Codex | `skill/mbti-typing/SKILL.md` | `Use $mbti-typing ...` | Existing Codex skill package and `agents/openai.yaml`. |
| Claude Code | `.claude/skills/mbti-typing/SKILL.md` | `/mbti-typing` | Includes `.claude/commands/mbti-type.md` as a slash-command fallback. |
| Cursor | `.cursor/rules/mbti-typing.mdc` | Ask Cursor to use the MBTI Typing Skill rule or mention `@mbti-typing` | Project rule uses MDC frontmatter and points back to the canonical skill. |
| opencode | `AGENTS.md` and `opencode.json` | `opencode run "Use the MBTI Typing Skill ..."` | `opencode.json` aggregates `AGENTS.md`, this adapter README, and the canonical skill. |

## Universal Contract

Every adapter must preserve the same behavior:

- candidate set with serious runner-up
- evidence ledger
- 4-6 concrete questions per round
- adjacent-type duel when the top two are close
- Big Five or framework cross-checks only when labeled separately
- falsifier and revision trigger before final closure
- explicit safety boundary: not clinical, hiring, legal, medical, financial, or deterministic advice

## Installation Notes

Codex:

```bash
cp -R skill/mbti-typing ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R .claude/skills/mbti-typing ~/.claude/skills/
```

Cursor:

```bash
mkdir -p .cursor/rules
cp .cursor/rules/mbti-typing.mdc <target-repo>/.cursor/rules/
```

opencode:

```bash
cp AGENTS.md opencode.json <target-repo>/
```

## Verification

Run:

```bash
python3 -B scripts/agent_adapter_audit.py .
make test
```

If a tool-specific adapter omits runner-up discipline, falsifier language, evidence-led workflow, or safety boundaries, the audit should fail.
