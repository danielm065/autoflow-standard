# AI Usage Guide — How AI Agents Should Work in an AutoFlow Vault

> Extended companion to [AGENTS.md](../AGENTS.md). Covers concrete examples + edge cases.

## Session lifecycle

### 1. Session start (first prompt of a new conversation)

```python
# Pseudo-code for what AI should do at session start
if cwd.startswith(f"{AUTOFLOW_VAULT}/02-Projects/"):
    project = cwd.split("/02-Projects/")[1].split("/")[0]
    load(f"02-Projects/{project}/CLAUDE.md")     # routing
    load(f"02-Projects/{project}/VISION.md")     # why
    load(f"02-Projects/{project}/CONSTITUTION.md") # rules
    load(f"02-Projects/{project}/STATUS.md")     # state
    load(f"02-Projects/{project}/handoff.md")    # next step
    # ~15KB total. Sets context for rest of session.
elif cwd == AUTOFLOW_VAULT:
    load("CLAUDE.md")           # vault-level routing
    load("00-Dashboard/Documentation-Health.md")  # cross-project overview
else:
    # Outside vault — no AutoFlow Standard context
    pass
```

### 2. Mid-session (user makes a request)

Apply this decision tree:

```
User request
   │
   ├─ Asks for new feature?
   │     │
   │     ├─ Listed in VISION.md Out-of-Scope?
   │     │     ├─ YES → "Out of scope. Want to update VISION first?"
   │     │     └─ NO → Check CONSTITUTION for relevant rules
   │     │           ├─ Rule violated? → "Rule R<N> says X. Need to update CONSTITUTION first?"
   │     │           └─ No violation? → Proceed
   │     │
   │     └─ (implementing) → After done: `vault decision "..."` to log Why
   │
   ├─ Asks "Why was X chosen?"
   │     └─ `grep -i "X" decisions.md` → if found, cite. If not, ask user to fill gap.
   │
   ├─ Reports a bug?
   │     ├─ Check RUNBOOK.md scenarios
   │     ├─ Check `.wolf/buglog.json` if exists
   │     └─ Fix → `vault mistake "..."` if it was a new failure mode
   │
   └─ Asks for status?
         └─ `vault where-am-i` or read STATUS.md + handoff.md
```

### 3. Session end (user wraps up or context limit approaching)

```bash
# Suggest to user:
vault handoff "What you'd want the next session to know about state + next step."
```

The Stop hook (if installed) will also remind them.

## Concrete examples

### Example 1: User asks for a feature

**User:** "Can you add user authentication to the project?"

**AI (correct flow):**

```bash
# 1. Check VISION
cat "$AUTOFLOW_VAULT/02-Projects/CurrentProject/VISION.md" | grep -A 10 "Out of Scope"
```

If VISION says "❌ No user authentication — single-user only":

> Looking at VISION.md, user authentication is explicitly Out of Scope (project is single-user). If this requirement changed, we'd need to:
>
> 1. Update VISION.md to remove the Out-of-Scope item (with a dated entry in "שינויי VISION")
> 2. Log a decision: `vault decision "Scope expanded to multi-user — needed for X reason"`
> 3. Then implement
>
> Should I help update VISION first, or is this still out of scope?

**AI (wrong flow — DO NOT do this):**

> Sure! Adding authentication. I'll start by installing passport.js...

### Example 2: User reports a bug

**User:** "The API is returning 500 errors"

**AI (correct flow):**

```bash
# 1. Check RUNBOOK for this scenario
grep -A 15 "500\|API error\|server error" "$AUTOFLOW_VAULT/02-Projects/CurrentProject/RUNBOOK.md"

# 2. Check buglog (if Moshe-Asraf-style auto-collection enabled)
cat "$AUTOFLOW_VAULT/02-Projects/CurrentProject/.wolf/buglog.json" 2>/dev/null | head -50

# 3. Check recent mistakes
tail -50 "$AUTOFLOW_VAULT/02-Projects/CurrentProject/mistakes.md"
```

If RUNBOOK has a matching scenario → follow the documented recovery steps.
If new → debug → fix → then:

```bash
vault mistake "API 500s on /products endpoint — root cause: missing index on ON CONFLICT"
```

Help fill: **Tried:** "Restart didn't help" / **Result:** "Still 500" / **Why:** "Postgres locked rows" / **Better:** "Added composite index"

### Example 3: User asks "Why are we using X?"

**User:** "Why did we choose n8n over Make?"

**AI (correct flow):**

```bash
grep -B 1 -A 10 "n8n\|Make" "$AUTOFLOW_VAULT/02-Projects/CurrentProject/decisions.md"
```

If found: cite the decision date + Why + Alternatives considered.
If not found:

> I can't find a decision logged for this. Should I add one now via `vault decision`? You'd want to fill in the Why so the next agent knows.

### Example 4: User says "make changes"

**User:** "Refactor the auth middleware"

**AI (correct flow):**

```bash
# 1. Check CONSTITUTION for rules about auth
grep -i "auth\|middleware" "$AUTOFLOW_VAULT/02-Projects/CurrentProject/CONSTITUTION.md"

# 2. Check SYSTEM.md for current architecture context
cat "$AUTOFLOW_VAULT/02-Projects/CurrentProject/SYSTEM.md"

# 3. Make changes
# (edits)

# 4. Log decision
vault decision "Refactored auth middleware — extracted token validation to separate module for testability"
```

### Example 5: End of complex session

**User:** "Let's call it a night"

**AI (correct flow):**

> Before we close, let me write a handoff for the next session:
>
> ```bash
> vault handoff "Refactored auth middleware (commits at HEAD~3..HEAD). Token validation in src/auth/validator.ts. Next: add retry logic for transient failures + integration tests. Blocker: need test JWT signing keys from 1Password."
> ```
>
> Done. Next session will pick up from `handoff.md`. Good night.

## Token efficiency tips

| Strategy | Saves |
|---|---|
| Load only the 5 mandatory files at session start | ~80% vs loading everything |
| `grep` instead of `cat` for specific lookups | varies (10-50× depending on file size) |
| Read `.anatomy.md` for file map before opening any project file | avoids 5-10 unnecessary reads |
| Use `vault where-am-i` instead of reading STATUS + handoff separately | parses + summarizes |
| `vault list` instead of `ls 02-Projects/` | filters skip-list folders |

## Anti-patterns observed in real sessions

❌ **AI invents features without checking Out-of-Scope** — most common failure mode.
❌ **AI edits decisions.md directly** — bypasses CLI's date stamping + INSERT marker logic. Use `vault decision`.
❌ **AI overwrites AUTO-START/END content** — daemon will undo on next refresh. Edit manual sections only.
❌ **AI runs `vault decision` and claims success without verifying** — known bug pattern (we hit this in development). Always `tail -5 decisions.md` after to confirm.
❌ **AI loads all 11 files at session start "to be safe"** — wastes context. Load 5; load others on demand.

## When AI should suggest creating a new project

User says something like:
- "I'm starting work on X for client Y"
- "New automation idea: ..."
- "Let's track this separately"

→ Suggest:

> This sounds like a new project. AutoFlow Standard projects get 11 files scaffolded automatically. In Obsidian:
>
> 1. `Cmd+P` → "Templater: Create new note from template"
> 2. Choose `Project-Init`
> 3. Answer 7 questions (name, client, description, stack, why, success metric, out-of-scope)
>
> The scaffolder creates all 11 files atomically with rollback on failure. Want to do this now?

## Cross-agent handoff

If the user switches from Claude Code → Hermes Discord → Codex during a workflow:

- **Claude Code** typically reads CLAUDE.md per-project (its own session start)
- **Codex** reads AGENTS.md at repo root (looks for AGENTS.md by convention)
- **Hermes** loads the vault-cli skill on session start
- **All three** can `vault decision`, `vault mistake`, etc. — same write interface

The `handoff.md` is the **canonical cross-agent baton**. Whoever starts a session reads it. Whoever ends a session updates it.

## Edge cases

### Vault is on a sync mirror (GoogleDrive, Dropbox)
Master copy might be at `$AUTOFLOW_VAULT` (env var). Sync mirror is **read-only**. AI should detect:

```bash
case "$PWD" in
  *GoogleDrive*|*Dropbox*)
    echo "⚠️ You're in a sync mirror. Switch to: $AUTOFLOW_VAULT"
    exit 1
    ;;
esac
```

### Project has no CLAUDE.md (not migrated yet)
AI should:

> This project doesn't have AutoFlow Standard structure yet. Want me to scaffold the 11 files? I'll preserve existing files (README.md, etc.) as references in CLAUDE.md routing.

### User edits AUTO-section by accident
Detect:

```bash
grep -A 1 "AUTO-START" RUNBOOK.md  # check if content looks user-edited
```

If user inserted manual content between markers, warn:

> I see manual content in RUNBOOK.md's AUTO-START block. The daemon will overwrite this on next refresh. Move it to the section above the marker?

### Multiple agents editing same file simultaneously
The CLI uses Python file-write semantics (atomic write). If two `vault decision` calls fire at exactly the same moment, one wins, one loses. For now: serialize via flock (TODO future enhancement).

## Summary checklist for AI

At session start, ask yourself:

- [ ] Am I in a vault project? Load 5 files: CLAUDE/VISION/CONSTITUTION/STATUS/handoff.
- [ ] Do I understand what's Out-of-Scope?
- [ ] What rules apply (CONSTITUTION)?

When making changes:

- [ ] Does this violate VISION or CONSTITUTION?
- [ ] Should I log a `vault decision` after?
- [ ] Did anything fail? `vault mistake`.

At session end:

- [ ] `vault handoff "..."` for next session.

This is the contract.
