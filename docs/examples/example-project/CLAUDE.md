---
type: project-routing
project: TaskTracker
client: Internal — solo dev
created: 2026-02-01
---

# TaskTracker — Project Routing

> Reference example. This file shows what a filled-out `CLAUDE.md` looks like in practice.

## Load order — session start (required)
1. [VISION.md](VISION.md) — why this exists
2. [CONSTITUTION.md](CONSTITUTION.md) — rules
3. [STATUS.md](STATUS.md) — where we are
4. [handoff.md](handoff.md) — next step

## On demand
| Scenario | Read first | Support files |
|---|---|---|
| Architecture / how it works | [SYSTEM.md](SYSTEM.md) | — |
| Bug / production issue | [RUNBOOK.md](RUNBOOK.md) | — |
| Setup / credentials | [ONBOARDING.md](ONBOARDING.md) | `.env.example` |
| Workflow / automation | [PROCESS-MAP.md](PROCESS-MAP.md) | `cron/` |
| "Why did we choose X?" | [decisions.md](decisions.md) | — |
| "What's been tried + failed?" | [mistakes.md](mistakes.md) | — |

## Vault rules
- decisions/mistakes = **append-only**
- AUTO-START/END blocks in SYSTEM/RUNBOOK/PROCESS-MAP = daemon territory (don't edit)
- Master = `$AUTOFLOW_VAULT`. Sync mirrors = read-only.
