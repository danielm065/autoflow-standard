# AutoFlow Standard

> **Documentation-as-code for AI-driven projects.** An 11-file convention + autonomous daemon + cross-agent CLI that keeps your Obsidian vault, AI agents (Claude/Codex/Hermes), and Discord in sync — automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hebrew + English](https://img.shields.io/badge/lang-Hebrew%20%2B%20English-blue.svg)](#)
[![Status: Production](https://img.shields.io/badge/status-production-green.svg)](#)

## What it is

A standardized 11-file structure for every project under `02-Projects/<Name>/`:

```
02-Projects/<Name>/
├── 📝 MANUAL (you write once, rarely change)
│   ├── CLAUDE.md           # routing card for AI agents
│   ├── VISION.md           # why + Out-of-Scope
│   ├── CONSTITUTION.md     # rules + Why per rule
│   └── ONBOARDING.md       # setup + credentials refs
│
├── 🤖 AUTO-GENERATED (daemon refreshes, do not edit)
│   ├── SYSTEM.md           # architecture (Arch-Hub linked)
│   ├── RUNBOOK.md          # incident response (buglog-aware)
│   └── PROCESS-MAP.md      # n8n / automation map
│
├── 📊 SESSION-DRIVEN (hook updates)
│   ├── STATUS.md           # current state
│   └── handoff.md          # next-session context
│
└── 📚 APPEND-ONLY (never deleted)
    ├── decisions.md        # why X was chosen
    └── mistakes.md         # what failed and why
```

## Why bother

| Problem | This solves |
|---|---|
| AI agents load 50KB of project docs every query → expensive | 11 files = load only what relevant. 5× cheaper context. |
| Multiple agents editing one mega-doc → merge hell | 11 files = 4 writers concurrently, 0 conflicts. |
| Manual + auto docs in same file → daemon overwrites human edits | Separated. AUTO-START/END markers protect manual sections. |
| Decisions get rewritten or lost | Append-only with INSERT markers. Never deleted. |
| New employee onboarding takes weeks of "where is...?" | ONBOARDING.md + CLAUDE.md routing → 30 min to productive. |
| Documentation goes stale | Daemon refreshes auto-sections every 5 min. PostToolUse hook triggers on edit. |
| Different agents (Claude/Codex/Hermes) need same context | Unified `vault` CLI + per-project CLAUDE.md routing card. |

## Features

- ✅ **11-file convention** with manual/auto/session/append-only separation
- ✅ **`vault` CLI** (Bash, stdlib-only Python) — agent-agnostic
- ✅ **3 auto-refresh skills** (Python): runbook, process-map, anatomy
- ✅ **macOS LaunchAgent daemon** — auto-refreshes every 5 min
- ✅ **PostToolUse hook** — refreshes immediately on file edit
- ✅ **Claude Code integration** — 7 slash commands (`/decision`, `/mistake`, `/note`, `/where-am-i`, `/refresh`, `/verify`, `/handoff`)
- ✅ **Hermes Discord integration** — bot skill for remote `!decision`, `!mistake`, `!note`
- ✅ **Obsidian Templater scaffolder** — 7 questions → 11 files
- ✅ **Obsidian Dataview dashboard** — compliance check across all projects
- ✅ **Token leak detection** — heuristic secrets scan in `vault verify`
- ✅ **Idempotent** — runs twice = no double writes
- ✅ **Hebrew + English** — UI Hebrew, code English

## Quick install

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/autoflow-standard.git
cd autoflow-standard

# 2. Set vault location
export AUTOFLOW_VAULT="$HOME/vault"

# 3. Run installer
./bin/install.sh

# 4. Verify
vault help
vault verify
```

## 5-minute walkthrough

### Scaffold a new project
```bash
# Option A: bash
mkdir -p "$AUTOFLOW_VAULT/02-Projects/MyProject"
cd "$AUTOFLOW_VAULT/02-Projects/MyProject"
# (manually copy templates/_ProjectStandard/*.md and fill placeholders)

# Option B: Obsidian Templater (interactive — recommended)
# Cmd+P → "Templater: Create new note from template" → "Project-Init"
# Answer 7 questions → 11 files created
```

### Log a decision
```bash
cd "$AUTOFLOW_VAULT/02-Projects/MyProject"
vault decision "Switched from REST to GraphQL — needed batched queries"
# Edits 02-Projects/MyProject/decisions.md (append-only, datestamped)
```

### Check compliance
```bash
vault verify              # all projects
vault verify MyProject    # just one + secrets scan
```

### From Claude Code
```
/decision Switched from REST to GraphQL
/mistake Tried polling instead of webhooks — too slow
/note Idea: weekly digest workflow
/where-am-i
```

### From Discord (via Hermes bot)
```
!decision Switched stack to Kubernetes
!note Bug idea — race condition in cache invalidation
!verify
```

### Auto-refresh
- LaunchAgent runs `vault-daemon` every 5 min
- PostToolUse hook triggers refresh on every Edit/Write inside `02-Projects/`
- Idempotent — runs only if source files changed

## Architecture

```
                 [files on disk: 02-Projects/<Name>/...]
                          ↑ ↓
                  [vault CLI: bash + python]
              ↑         ↑         ↑         ↑
        Claude Code   Codex    Hermes    macOS LaunchAgent
        (slash cmds  (AGENTS  (Discord    (daemon every
        + hooks)     .md)     skill)      5 min)
```

## Comparison to alternatives

| Approach | Pros | Cons |
|---|---|---|
| **Single big README** | Easy to read | Context expensive, drift, no autonomy |
| **OpenWolf (cerebrum/anatomy/memory)** | Daemon model | In practice 95% empty, single-codebase mindset |
| **Notion/Linear/Confluence** | Polished UI | Vendor lock-in, not Markdown, no AI context |
| **AutoFlow Standard** | Markdown, autonomous, multi-agent, cheap context | Setup effort: 30 min |

See [docs/comparison.md](docs/comparison.md) for detailed comparison.

## Documentation

- [Architecture: why 11 files?](docs/architecture.md)
- [Getting started](docs/getting-started.md)
- [Comparison to OpenWolf and single-file approaches](docs/comparison.md)
- [vault CLI reference](docs/concepts/vault-cli.md)
- [Daemon & autonomy](docs/concepts/daemon.md)
- [Claude Code integration](docs/concepts/claude-integration.md)
- [Hermes Discord integration](docs/concepts/hermes-integration.md)
- [Obsidian setup (Templater + Dataview)](integrations/obsidian/README.md)

## Status

Production. In use on 7+ active projects (WhatsApp automation, e-commerce pipelines, CRM, voice bots, lead gen).

## License

MIT — see [LICENSE](LICENSE).

## Credits

Created by [Daniel Moshe](https://autoflow.company) (AutoFlow). Inspired by the gaps in OpenWolf, Notion templates, and single-file READMEs.

## For AI agents working in this repo

See [AGENTS.md](AGENTS.md) — canonical instructions for Claude Code, Codex, Cursor, Aider, and any AI agent loading this repository.

## Reference example

[docs/examples/example-project/](docs/examples/example-project/) — a fully filled-out fictional project ("TaskTracker") showing what all 11 files look like when populated. Use this to learn the patterns before scaffolding your own.
