# Agent Adapter Layer

This directory documents how the same MBTI Typing Skill is exposed to multiple agent tools without changing the underlying reasoning protocol.

## Source Of Truth

- Canonical protocol: `skill/mbti-typing/SKILL.md`
- Shared project contract: `AGENTS.md`
- Adapter manifest: `agent-adapters/manifest.json`
- Drift gate: `scripts/agent_adapter_audit.py`

## Adapter Matrix

![Agent Adapter Matrix](../docs/assets/agent-adapter-matrix.svg)

![Agent Compatibility Grid](../docs/assets/agent-compatibility-grid.svg)

| Tool | Primary entrypoint | Invocation | Notes |
|---|---|---|---|
| Codex | `skill/mbti-typing/SKILL.md` | `Use $mbti-typing ...` | Existing Codex skill package and `agents/openai.yaml`. |
| Generic AGENTS.md-aware agents | `AGENTS.md`, `CONVENTIONS.md` | Ask the agent to follow `AGENTS.md` | Lowest-common-denominator project contract. |
| Claude Code | `.claude/skills/mbti-typing/SKILL.md` | `/mbti-typing` | Includes `.claude/commands/mbti-type.md` as a slash-command fallback. |
| Cursor | `.cursor/rules/mbti-typing.mdc` | Ask Cursor to use the MBTI Typing Skill rule or mention `@mbti-typing` | Project rule uses MDC frontmatter and points back to the canonical skill. |
| opencode | `AGENTS.md` and `opencode.json` | `opencode run "Use the MBTI Typing Skill ..."` | `opencode.json` aggregates `AGENTS.md`, this adapter README, and the canonical skill. |
| Gemini CLI | `GEMINI.md`, `.gemini/settings.json` | `gemini "Use the MBTI Typing Skill ..."` | `GEMINI.md` imports `AGENTS.md` and the canonical skill. |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md` | Ask Copilot to use the MBTI Typing Skill | Repository instructions and project skill route back to the same protocol. |
| Windsurf | `.windsurf/rules/mbti-typing.md` | Ask Windsurf to apply the MBTI Typing Skill rule | Workspace rule uses model-decision activation. |
| Cline | `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md` | Ask Cline to use the MBTI Typing Skill | Skill and rule both point back to the canonical source. |
| Continue | `.continue/rules/mbti-typing.md` | Ask Continue to apply the MBTI Typing Skill rule | Local rule preserves the same evidence-led workflow. |
| aider | `CONVENTIONS.md`, `.aider.conf.yml` | `aider --read CONVENTIONS.md --read AGENTS.md` | Conventions file keeps the protocol visible during coding sessions. |

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

Gemini CLI:

```bash
cp AGENTS.md GEMINI.md <target-repo>/
mkdir -p <target-repo>/.gemini
cp .gemini/settings.json <target-repo>/.gemini/settings.json
```

GitHub Copilot:

```bash
mkdir -p <target-repo>/.github/instructions <target-repo>/.github/skills/mbti-typing
cp .github/copilot-instructions.md <target-repo>/.github/copilot-instructions.md
cp .github/instructions/mbti-typing.instructions.md <target-repo>/.github/instructions/
cp .github/skills/mbti-typing/SKILL.md <target-repo>/.github/skills/mbti-typing/
```

Windsurf:

```bash
mkdir -p <target-repo>/.windsurf/rules
cp .windsurf/rules/mbti-typing.md <target-repo>/.windsurf/rules/
```

Cline:

```bash
mkdir -p <target-repo>/.cline/skills/mbti-typing <target-repo>/.clinerules
cp .cline/skills/mbti-typing/SKILL.md <target-repo>/.cline/skills/mbti-typing/
cp .clinerules/mbti-typing.md <target-repo>/.clinerules/
```

Continue:

```bash
mkdir -p <target-repo>/.continue/rules
cp .continue/rules/mbti-typing.md <target-repo>/.continue/rules/
```

aider:

```bash
cp AGENTS.md CONVENTIONS.md .aider.conf.yml <target-repo>/
```

## Verification

Run:

```bash
python3 -B scripts/agent_adapter_audit.py .
make test
```

If a tool-specific adapter omits runner-up discipline, falsifier language, evidence-led workflow, or safety boundaries, the audit should fail.
