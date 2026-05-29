# Agent Adapter Layer

This directory documents how the same MBTI Typing Skill is exposed to a small first-class agent surface without changing the underlying reasoning protocol. The maintained Core Pack is Codex, Claude Code, Cursor, and opencode; the rest of the manifest is an optional recipe catalog for teams that need a specific host.

## Source Of Truth

- Canonical protocol: `skill/mbti-typing/SKILL.md`
- Shared project contract: `AGENTS.md`
- Adapter manifest: `agent-adapters/manifest.json`
- Drift gate: `scripts/agent_adapter_audit.py`
- Adoption lab sync: `scripts/sync_agent_adapter_lab.py`
- Adoption lab audit: `scripts/agent_adapter_lab_audit.py`
- Portability lab sync: `scripts/sync_agent_portability_lab.py`
- Portability lab audit: `scripts/agent_portability_lab_audit.py`

## Adapter Matrix

Maintenance rule:

- First-class Core Pack: Codex, Claude Code, Cursor, opencode.
- Portable baseline: `AGENTS.md` and `CONVENTIONS.md` for AGENTS.md-aware agents.
- Optional manifest recipes: additional host-specific files can be exported when needed, but they are not allowed to fork the protocol.

![Agent Adapter Matrix](../docs/assets/agent-adapter-matrix.svg)

![Agent Compatibility Grid](../docs/assets/agent-compatibility-grid.svg)

| Tool | Primary entrypoint | Invocation | Notes |
|---|---|---|---|
| Codex | `skill/mbti-typing/SKILL.md` | `Use $mbti-typing ...` | Existing Codex skill package and `agents/openai.yaml`. |
| Generic AGENTS.md-aware agents | `AGENTS.md`, `CONVENTIONS.md` | Ask the agent to follow `AGENTS.md` | Lowest-common-denominator project contract. |
| ChatGPT GPTs and Projects | `gpts/mbti-typing-gpt-instructions.md` | Create a GPT or Project from the instructions file | GPT instructions and knowledge-file guidance preserve the protocol outside coding IDEs. |
| Zed Agent Panel | `.rules`, `AGENTS.md` | Ask Zed Agent Panel to use the MBTI Typing Skill rule | Root `.rules` file and AGENTS fallback keep Zed aligned. |
| Devin and Devin CLI | `AGENTS.md` | Ask Devin to follow `AGENTS.md` | Devin uses the same portable project instruction contract. |
| Claude Code | `.claude/skills/mbti-typing/SKILL.md` | `/mbti-typing` | Includes `.claude/commands/mbti-type.md` as a slash-command fallback. |
| Cursor | `.cursor/rules/mbti-typing.mdc` | Ask Cursor to use the MBTI Typing Skill rule or mention `@mbti-typing` | Project rule uses MDC frontmatter and points back to the canonical skill. |
| opencode | `AGENTS.md` and `opencode.json` | `opencode run "Use the MBTI Typing Skill ..."` | `opencode.json` aggregates `AGENTS.md`, this adapter README, and the canonical skill. |
| Gemini CLI | `GEMINI.md`, `.gemini/settings.json` | `gemini "Use the MBTI Typing Skill ..."` | `GEMINI.md` imports `AGENTS.md` and the canonical skill. |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/mbti-typing.instructions.md`, `.github/skills/mbti-typing/SKILL.md` | Ask Copilot to use the MBTI Typing Skill | Repository instructions and project skill route back to the same protocol. |
| Windsurf | `.windsurf/rules/mbti-typing.md` | Ask Windsurf to apply the MBTI Typing Skill rule | Workspace rule uses model-decision activation. |
| Cline | `.cline/skills/mbti-typing/SKILL.md`, `.clinerules/mbti-typing.md` | Ask Cline to use the MBTI Typing Skill | Skill and rule both point back to the canonical source. |
| Continue | `.continue/rules/mbti-typing.md` | Ask Continue to apply the MBTI Typing Skill rule | Local rule preserves the same evidence-led workflow. |
| aider | `CONVENTIONS.md`, `.aider.conf.yml` | `aider --read CONVENTIONS.md --read AGENTS.md` | Conventions file keeps the protocol visible during coding sessions. |
| JetBrains Junie | `.junie/AGENTS.md`, `.junie/commands/mbti-type.md` | Ask Junie to use the guidelines or run `/mbti-type` | Guidelines and slash command make the workflow reusable in JetBrains IDEs. |
| Amazon Q Developer CLI | `.amazonq/cli-agents/mbti-typing.json` | `q chat --agent mbti-typing` | Custom agent loads the canonical skill and read-only resources. |
| Roo Code | `.roomodes`, `.roo/rules-mbti-typing/mbti-typing.md` | Switch to the MBTI Typing mode | Project mode and rules keep Roo focused on the protocol. |
| Kilo Code | `kilo.jsonc`, `.kilo/rules/mbti-typing.md` | Ask Kilo to apply the MBTI Typing Skill rule | Project instructions load the same evidence-led workflow. |

## Universal Contract

Every adapter must preserve the same behavior:

- candidate set with serious runner-up
- evidence ledger
- 4-6 concrete questions per round
- low-typing native question UI strategy: use `request_user_input`, `AskUserQuestion`, `AskQuestion`, or another host question tool only when it is actually available
- compact `A/B/C/D/E` fallback when no native question UI is present
- final `Other / none of these - I will explain` escape hatch unless the host automatically provides free-form input
- adjacent-type duel when the top two are close
- Big Five or framework cross-checks only when labeled separately
- falsifier and revision trigger before final closure
- explicit safety boundary: not clinical, hiring, legal, medical, financial, or deterministic advice

Typing answers are not product preferences, so adapters must not mark one answer option as recommended and must not reveal option-to-type mappings before the subject answers.

## Installation Notes

The safest way to move the adapter layer into another repository is to export a pack from the manifest instead of hand-copying files:

```bash
python3 -B scripts/export_agent_pack.py --dest /tmp/mbti-agent-pack --target core
```

Selective exports keep the pack lean, and `--target all` is reserved for teams that deliberately want every optional manifest recipe:

```bash
python3 -B scripts/export_agent_pack.py --dest /tmp/mbti-cursor-continue-pack --target cursor --target continue
```

The export includes the canonical `skill/mbti-typing/` directory, baseline project contracts, selected adapter entrypoints, prompt recipes, adapter docs, and an `AGENT_PACK_MANIFEST.json` receipt with selected targets, entrypoints, invocation examples, install notes, file groups, and safety contract. The exporter refuses to write into a non-empty destination unless `--force` is explicit.

![Agent Pack Export Flow](../docs/assets/agent-pack-export-flow.svg)

For first-run adoption, use the [Agent Adapter Lab](../docs/agent-adapter-lab.html). It reads the same manifest, lets a user choose Core Pack or Select All, copies the export command, shows the install checklist, emits an adapter JSON receipt, and prepares an `agent_adapter_improvement.yml` issue seed when an adapter is missing or stale.

The lab also exposes the low-typing question UX contract from `agent-adapters/manifest.json`, so users can see whether a selected host should use native question UI or compact choices.

![Agent Adapter Lab Flow](../docs/assets/agent-adapter-lab-flow.svg)

For future or unknown hosts, use the [Agent Portability Lab](../docs/agent-portability-lab.html). It maps a host by capability before inventing an adapter: project instruction file, native `SKILL.md` directory, project rule or mode file, custom agent JSON/profile, slash command, native question UI, chat project instructions, or config instruction array. It emits a Universal Agent Bridge plan, portable install recipe, `agent-portability-lab/v1` adapter draft, and `agent_portability_request.yml` issue seed while preserving the candidate set, serious runner-up, evidence ledger, falsifier, and safety boundary.

![Universal Agent Bridge Map](../docs/assets/universal-agent-bridge-map.svg)

Run the dedicated Agent Pack Export Audit before publishing adapter changes:

```bash
python3 -B scripts/agent_pack_export_audit.py .
python3 -B scripts/sync_agent_adapter_lab.py agent-adapters/manifest.json docs/agent-adapter-lab.html
python3 -B scripts/agent_adapter_lab_audit.py docs/agent-adapter-lab.html agent-adapters/manifest.json
python3 -B scripts/sync_agent_portability_lab.py agent-adapters/manifest.json docs/agent-portability-lab.html
python3 -B scripts/agent_portability_lab_audit.py docs/agent-portability-lab.html agent-adapters/manifest.json .github/ISSUE_TEMPLATE/agent_portability_request.yml
```

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

ChatGPT GPTs and Projects:

```bash
cp gpts/mbti-typing-gpt-instructions.md <target-repo>/
```

Zed Agent Panel:

```bash
cp .rules AGENTS.md <target-repo>/
```

Devin:

```bash
cp AGENTS.md <target-repo>/
```

JetBrains Junie:

```bash
mkdir -p <target-repo>/.junie/commands
cp .junie/AGENTS.md <target-repo>/.junie/AGENTS.md
cp .junie/commands/mbti-type.md <target-repo>/.junie/commands/
```

Amazon Q Developer CLI:

```bash
mkdir -p <target-repo>/.amazonq/cli-agents
cp .amazonq/cli-agents/mbti-typing.json <target-repo>/.amazonq/cli-agents/
```

Roo Code:

```bash
mkdir -p <target-repo>/.roo/rules-mbti-typing
cp .roomodes <target-repo>/.roomodes
cp .roo/rules-mbti-typing/mbti-typing.md <target-repo>/.roo/rules-mbti-typing/
```

Kilo Code:

```bash
mkdir -p <target-repo>/.kilo/rules
cp kilo.jsonc <target-repo>/kilo.jsonc
cp .kilo/rules/mbti-typing.md <target-repo>/.kilo/rules/
```

## Verification

Run:

```bash
python3 -B scripts/agent_adapter_audit.py .
python3 -B scripts/agent_pack_export_audit.py .
python3 -B scripts/sync_agent_adapter_lab.py agent-adapters/manifest.json docs/agent-adapter-lab.html
python3 -B scripts/agent_adapter_lab_audit.py docs/agent-adapter-lab.html agent-adapters/manifest.json
python3 -B scripts/sync_agent_portability_lab.py agent-adapters/manifest.json docs/agent-portability-lab.html
python3 -B scripts/agent_portability_lab_audit.py docs/agent-portability-lab.html agent-adapters/manifest.json .github/ISSUE_TEMPLATE/agent_portability_request.yml
make test
```

If a tool-specific adapter omits runner-up discipline, falsifier language, evidence-led workflow, or safety boundaries, the audit should fail.
