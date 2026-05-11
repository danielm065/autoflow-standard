# AGENTS.md — Canonical AI Agent Instructions

> Loaded automatically by Claude Code, Codex, Cursor, and Aider when they open this repo.
> Treat this as the **system prompt** for any AI agent working in an AutoFlow Standard vault.

## TL;DR for any AI agent

1. **Vault location:** `$AUTOFLOW_VAULT` (env var). Default: `$HOME/vault`.
2. **Projects live at:** `$AUTOFLOW_VAULT/02-Projects/<Name>/`.
3. **Every project has 11 standardized files** — see structure below.
4. **`vault` CLI is the official write interface** — never edit `decisions.md` / `mistakes.md` directly; use `vault decision "..."` or `vault mistake "..."`.
5. **Auto-generated sections** (between `<!-- AUTO-START -->` and `<!-- AUTO-END -->` markers in RUNBOOK.md, PROCESS-MAP.md) — **never edit manually**. They're rewritten by the daemon.
6. **Documentation is the contract.** Before suggesting changes, read VISION.md and CONSTITUTION.md.

## When you're inside a project folder

Read these in order at the start of every session:

```
1. ./CLAUDE.md          # routing card — tells you what else to load
2. ./VISION.md          # why this project exists + Out-of-Scope (do NOT propose features here)
3. ./CONSTITUTION.md    # rules — each with "Why" — do NOT violate
4. ./STATUS.md          # current state, blockers, open tasks
5. ./handoff.md         # what the last session said about "next step"
```

Load on demand:
- **Architecture question?** → `./SYSTEM.md`
- **Bug or production incident?** → `./RUNBOOK.md`
- **Need credentials or to set up environment?** → `./ONBOARDING.md`
- **Automation / workflow question?** → `./PROCESS-MAP.md`
- **"Why was X chosen?"** → `./decisions.md`
- **"What's been tried and failed?"** → `./mistakes.md`

## How to write changes

### Logging a decision (when you decide something with the user)
```bash
vault decision "Switched from REST to GraphQL — needed batched queries"
```
Then help the user fill in `**Why:**` and `**Alternatives considered:**` (the CLI leaves TODO placeholders).

### Logging a mistake (when something didn't work)
```bash
vault mistake "Tried Redis for sessions — overkill; switched back to JWT"
```
Fill `**Tried/Result/Why-it-failed/Better-approach**` from conversation context if obvious.

### Saving a quick thought / future idea
```bash
vault note "Idea: weekly digest workflow for clients"
```
Goes to `$AUTOFLOW_VAULT/_system/inbox.md` (processed weekly by user).

### End of session
```bash
vault handoff "Tomorrow: finish auth refactor. Token validator at line 42 needs retry logic."
```
Writes timestamped entry to `./handoff.md`.

## Rules you MUST follow

### R1. Out-of-Scope is sacred
Before proposing a new feature, check `VISION.md → ⚠️ Out of Scope`. If listed there, **do not propose it**. Tell the user: "This is marked out-of-scope. Want me to update VISION.md first?"

### R2. CONSTITUTION rules with "Why" are not negotiable
Each rule has a documented reason. If you think a rule should change, **propose updating CONSTITUTION.md first**, don't just violate it.

### R3. Append-only logs
`decisions.md` and `mistakes.md` are append-only. Never delete entries. Use `vault decision` / `vault mistake` — they append above the `<!-- INSERT NEW ... -->` marker.

### R4. Auto-sections are off-limits
Content between `<!-- AUTO-START: vault-runbook-refresh -->` and `<!-- AUTO-END: vault-runbook-refresh -->` (and similar for `vault-process-map`) is rewritten by the daemon every refresh. Your manual edits will be **lost on next refresh**. Edit the manual section above/below the markers instead.

### R5. Read CLAUDE.md before suggesting file moves
The project's `CLAUDE.md` is the routing manifest. If you move/rename files, update CLAUDE.md too.

### R6. No secrets in markdown
Never paste tokens, API keys, passwords into any `.md` file. The CLI has a heuristic secrets scanner — `vault verify <project>` flags leaks.

### R7. Vault writes only on master path
If your CWD shows you're inside a sync mirror (e.g., `GoogleDrive/...vault/...`), **stop**. Edits there cause drift. Move to `$AUTOFLOW_VAULT` (master path).

## When you're NOT inside a project (e.g., at vault root)

You're likely doing meta-work. Useful files:
- `00-Dashboard/Documentation-Health.md` — which projects are compliant?
- `_system/inbox.md` — captured ideas
- `_system/Reports/daemon-log.md` — what the daemon refreshed recently
- `Templates/_ProjectStandard/` — skeletons for new projects

## Creating a new project

User says "make a new project for X":

1. Tell them: open Obsidian → `Cmd+P` → "Templater: Create new note from template" → choose `Project-Init`.
2. They'll answer 7 questions interactively.
3. **You** don't create projects manually — Templater scaffolder does it (interactive prompts, atomic creation with rollback on failure).

If user insists on CLI:
```bash
mkdir -p "$AUTOFLOW_VAULT/02-Projects/$NEW_NAME"
cd "$AUTOFLOW_VAULT/02-Projects/$NEW_NAME"
cp "$AUTOFLOW_VAULT/Templates/_ProjectStandard/"*.md .
# Then help user fill {{project_name}}, {{client_name}}, {{date}} placeholders
```

## Verifying compliance

Always-safe read-only commands:
```bash
vault verify                  # all projects compliance check
vault verify <project>        # one project + secrets scan
vault where-am-i              # active project STATUS + handoff
vault list                    # all projects
vault status                  # active project STATUS.md
```

## Common user requests — how to handle

| User says | You do |
|---|---|
| "Add feature X" | Read VISION Out-of-Scope first. If listed → push back. If not → check CONSTITUTION for relevant rules. |
| "Why did we choose X?" | `cat decisions.md` and search. If not found, ask user to fill the gap. |
| "Something is broken" | Read RUNBOOK.md scenarios first. If new, log to `vault mistake` after fixing + propose adding to RUNBOOK. |
| "How does this project work?" | Load CLAUDE.md → SYSTEM.md → ask if they need PROCESS-MAP.md too. |
| "I'm new here, where do I start?" | ONBOARDING.md → then VISION.md → then STATUS.md. |
| "What was decided yesterday?" | `tail -50 decisions.md`. |
| "Refresh docs" | `vault refresh` (calls all 3 auto-doc skills). |
| "What's the next step?" | `cat handoff.md`. |

## Anti-patterns (do NOT do these)

❌ **Don't** write a 50KB monolithic README and call it documentation.
❌ **Don't** edit `decisions.md` or `mistakes.md` directly — use the CLI (append-only enforcement).
❌ **Don't** edit content between AUTO-START/AUTO-END markers (daemon overwrites).
❌ **Don't** silently violate a CONSTITUTION rule. If you must violate, propose updating the rule first.
❌ **Don't** propose features listed in VISION Out-of-Scope without asking the user to update VISION first.
❌ **Don't** paste secrets into markdown.
❌ **Don't** create projects manually with CLI when Templater scaffolder exists (it has rollback).

## Hermes / Discord users

If the user is talking to you via Discord (Hermes context), they may use prefixes:
- `!decision <text>` → invoke `vault decision`
- `!mistake <text>` → invoke `vault mistake`
- `!note <text>` → invoke `vault note`
- `!where-am-i [project]` → invoke `vault where-am-i`
- `!verify [project]` → invoke `vault verify`
- `!handoff [text]` → invoke `vault handoff`
- `!refresh` → invoke `vault refresh`

**MUST USE terminal tool for these — never claim success without actually running the command.**

## More documentation

- [README.md](README.md) — public elevator pitch
- [docs/architecture.md](docs/architecture.md) — why 11 files (deep)
- [docs/getting-started.md](docs/getting-started.md) — 10-step setup
- [docs/comparison.md](docs/comparison.md) — vs OpenWolf / Notion / single-README
- [docs/ai-usage.md](docs/ai-usage.md) — extended AI agent guide
- [docs/examples/example-project/](docs/examples/example-project/) — fully filled-out reference project

## Single source of truth

**This file.** When in doubt, re-read it. It's intentionally short and direct.

---

_Last updated: 2026-05-11. Maintainer: Daniel Moshe (AutoFlow)._
