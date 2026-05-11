# Changelog

All notable changes to AutoFlow Standard.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) + [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-11

Initial public release.

### Added
- **11-file project standard** — CLAUDE, VISION, CONSTITUTION, ONBOARDING, SYSTEM, RUNBOOK, PROCESS-MAP, STATUS, handoff, decisions, mistakes
- **vault CLI** (Bash + Python) — 11 subcommands (decision/mistake/note/status/handoff/where-am-i/refresh/verify/list/inbox/active)
- **3 auto-refresh skills** (Python, stdlib-only):
  - `vault-runbook-refresh` — parses `.wolf/buglog.json` + `issues.md` → RUNBOOK auto-section
  - `vault-process-map` — parses `automations/*.json` + `n8n/*.json` → PROCESS-MAP auto-section
  - `vault-anatomy-refresh` — per-project file map with token estimates
- **vault-daemon** — Bash watcher with marker-based change detection, lock files, log rotation
- **macOS LaunchAgent** — runs daemon every 5 minutes
- **Claude Code integration** — 7 slash commands + 2 hooks (SessionStart, Stop, PostToolUse)
- **Hermes Discord integration** — `vault-cli` skill with INVOCATION PROTOCOL for reliable tool-use
- **Obsidian Templater scaffolder** — `Project-Init.md` trigger + `projectInit.js` (interactive 7-question scaffolder with rollback on partial failure)
- **Obsidian Dataview dashboard** — `Documentation-Health.md` (compliance check across all projects)
- **AUTO-START/END markers** — protect manual sections from daemon overwrites
- **INSERT NEW ABOVE THIS LINE** markers — append-only convention enforcement
- **Idempotent design** — running daemon twice = no double writes (md5 verified)
- **Heuristic secrets scan** — `vault verify` detects token leakage in `.md` files
- **Installer** (`bin/install.sh`) — one-shot setup with macOS + Linux detection
- **Documentation** — README, architecture.md, getting-started.md, comparison.md
- **MIT license**

### Design decisions
- Markdown-first (no proprietary formats)
- Per-project scope (not vault-wide like OpenWolf)
- Single Responsibility Principle applied to documentation
- Hebrew + English first-class (UI Hebrew, code English)
- Manual / Auto / Session / Append-only file categorization
- Stdlib Python only (no pip dependencies)
- Bash for CLI (portable to Linux with minor cron substitution)

### Borrowed from OpenWolf
- `anatomy.md` auto-scan concept (adapted to per-project)
- Daemon model

### Not yet implemented
- Linux cron template (placeholder in installer)
- Hermes auto-trigger on chat patterns (currently requires `!command` prefix)
- QuickAdd Obsidian setup guide
- `vault-vision-interview` interactive skill
- Web-based dashboard
- Mobile-first UI

### Known limitations
- `vault-daemon` macOS-only (LaunchAgent). Linux users add manual cron.
- `vault verify` secrets scan is heuristic only (catches obvious patterns).
- Token estimates are byte-based (rough). Accurate enough for context budgeting.
- No multi-vault support yet (one `AUTOFLOW_VAULT` per shell).
