---
type: skill
name: vault-cli
skill_key: vault-cli
description: Wraps AutoFlow `vault` CLI for Discord/chat-driven documentation. User logs decisions/mistakes/notes from phone via Discord, queries STATUS/compliance, triggers refresh. Uses terminal tool to invoke __SYSTEM_DIR__/bin/vault.
status: active
created: 2026-05-10
trigger: discord-command | direct-message | manual-invocation
when_to_use:
  - User asks via Discord/chat to log decision/mistake/note
  - User asks "where am I in <project>?" or "status of <project>?"
  - User asks to verify documentation compliance
  - User asks to refresh auto-generated docs (RUNBOOK, PROCESS-MAP, SYSTEM)
tools_required: [terminal]
allowlist: []
related_skills: [vault-operations, vault-health-check, vault-arch-refresh]
---

# vault-cli — AutoFlow Documentation Bridge

Hermes-side wrapper for `__SYSTEM_DIR__/bin/vault`. Lets user control vault documentation from Discord (mobile-aware).

---

## ⚠️ INVOCATION PROTOCOL (READ FIRST — MUST FOLLOW)

When user's Discord/chat message **starts with one of these prefixes**, IMMEDIATELY invoke the `terminal` tool with the corresponding shell command. **DO NOT reply with text first. DO NOT claim success without actually running the command.**

| Prefix | Command via terminal tool |
|---|---|
| `!note <text>` | `__SYSTEM_DIR__/bin/vault note "<text>"` |
| `!decision <text>` | `cd __AUTOFLOW_VAULT__/02-Projects/<active-project> && __SYSTEM_DIR__/bin/vault decision "<text>"` |
| `!mistake <text>` | `... vault mistake "<text>"` |
| `!status [project]` | `VAULT_PROJECT=<project> __SYSTEM_DIR__/bin/vault status` |
| `!where-am-i [project]` | `VAULT_PROJECT=<project> __SYSTEM_DIR__/bin/vault where-am-i` |
| `!verify [project]` | `__SYSTEM_DIR__/bin/vault verify [<project>]` |
| `!handoff [text]` | `... vault handoff "<text>"` |
| `!refresh` | `... vault refresh` |
| `!list` | `... vault list` |
| `!inbox` | `... vault inbox` |

### Verification step (MANDATORY for write commands)

After running write command (`note`, `decision`, `mistake`, `handoff`), verify:
1. Run terminal again: `tail -3 __AUTOFLOW_VAULT__/_system/inbox.md` (or relevant file)
2. Confirm new line appears
3. Reply with confirmation

### Active project resolution

If ambiguous → ask user: "Which project?" Do NOT guess.

---

## Discord channel mapping (recommended)

| Channel | Direction | Purpose |
|---|---|---|
| `#vault-commands` | in | slash commands |
| `#vault-activity` | out | session-end summaries |
| `#vault-decisions` | out | new decisions |
| `#vault-mistakes` | out | new mistakes |
| `#vault-alerts` | out | verify failures + secrets leaks |

## Setup checklist

- [ ] Add to `~/.zshrc`: `export PATH="__SYSTEM_DIR__/bin:$PATH"`
- [ ] Reload Hermes (restart LaunchAgent or `hermes reload`)
- [ ] Verify Hermes sees skill: `hermes skills list | grep vault-cli`
- [ ] Test from Discord: `!note testing vault-cli skill`
- [ ] Verify entry: `cat __AUTOFLOW_VAULT__/_system/inbox.md`
