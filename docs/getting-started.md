# Getting Started

## 1. Prerequisites

| Tool | Required | Used for |
|---|---|---|
| **bash 4+** or **zsh** | ✅ | CLI |
| **python 3.10+** | ✅ | Auto-refresh skills |
| **git** | ✅ | Version control vault |
| **Obsidian** | ✅ | Edit + view vault |
| **Templater plugin** | ✅ | New project scaffolder |
| **Dataview plugin** | ✅ | Documentation-Health dashboard |
| **macOS** | 🟡 | LaunchAgent daemon (Linux: use cron) |
| **Claude Code** | 🟢 | Slash commands integration |
| **Hermes Agent** | 🟢 | Discord integration |

## 2. Install

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/autoflow-standard.git
cd autoflow-standard

# Set your vault path (where you want the AutoFlow vault to live)
export AUTOFLOW_VAULT="$HOME/vault"

# Run installer
./bin/install.sh
```

The installer:
1. Creates `$AUTOFLOW_VAULT/{02-Projects,00-Dashboard,Templates,_system}` structure
2. Installs CLI to `$AUTOFLOW_VAULT/_system/bin/vault`
3. Copies 3 Python skills to `$AUTOFLOW_VAULT/_system/Skills/`
4. Copies 11 templates to `$AUTOFLOW_VAULT/Templates/_ProjectStandard/`
5. Wires Claude Code commands (if `~/.claude/` exists)
6. Loads macOS LaunchAgent (if macOS)
7. Wires Hermes skill (if `~/.hermes/skills/` exists)

## 3. Add to PATH

```bash
# Add to ~/.zshrc (or ~/.bashrc):
export AUTOFLOW_VAULT="$HOME/vault"
export PATH="$AUTOFLOW_VAULT/_system/bin:$PATH"

# Reload
source ~/.zshrc

# Verify
which vault
vault help
```

## 4. Configure Obsidian

Open Obsidian and:

1. **Install Templater**: Settings → Community Plugins → Browse → "Templater" → Install + Enable
2. **Install Dataview**: Same path, search "Dataview"
3. **Templater settings:**
   - Template folder: `Templates`
   - User scripts folder: `Templates/scripts`
   - Enable JavaScript Queries: ON (for Documentation-Health.md)
4. **Dataview settings:** Enable JavaScript Queries

## 5. Create your first project

### Option A: Templater interactive (recommended)

In Obsidian:
1. `Cmd+P` → "Templater: Create new note from template"
2. Choose `Project-Init`
3. Answer 7 questions:
   - Project name (English, no spaces — e.g., `MyApp`)
   - Client display name (Hebrew/English OK)
   - One-line description
   - Stack (e.g., `Node.js + Postgres + n8n`)
   - Why does this project exist? (1-2 sentences)
   - Success metric
   - What's OUT of scope? (comma separated)

**Result:** 11 files at `02-Projects/MyApp/` ready to use.

### Option B: Manual

```bash
mkdir -p "$AUTOFLOW_VAULT/02-Projects/MyApp"
cd "$AUTOFLOW_VAULT/02-Projects/MyApp"
cp "$AUTOFLOW_VAULT/Templates/_ProjectStandard/"*.md .

# Replace {{project_name}}, {{client_name}}, {{date}} placeholders
# in each file using your text editor
```

## 6. Use the CLI

```bash
cd "$AUTOFLOW_VAULT/02-Projects/MyApp"

# Log a decision
vault decision "Switched from REST to GraphQL — needed batched queries"

# Log a mistake
vault mistake "Tried Redis for sessions — overkill, switched to JWT"

# Quick note (global inbox)
vault note "Idea: weekly digest workflow"

# Where am I in this project?
vault where-am-i

# Refresh auto-generated docs
vault refresh

# Check 11-file compliance + secrets scan
vault verify MyApp

# List all projects
vault list
```

## 7. Verify autonomy

The daemon runs every 5 minutes via LaunchAgent. Check it:

```bash
# Is it loaded?
launchctl list | grep autoflow

# Check log
tail -20 "$AUTOFLOW_VAULT/_system/Reports/daemon-log.md"

# Force a run (manually)
"$AUTOFLOW_VAULT/_system/bin/vault-daemon"
```

If you edit a file in `02-Projects/MyApp/issues.md`, then within 5 minutes the daemon should detect it and refresh the RUNBOOK auto-section.

## 8. Verify Claude Code integration

If you installed Claude Code:

1. Start a new Claude Code session inside a project folder:
   ```bash
   cd "$AUTOFLOW_VAULT/02-Projects/MyApp"
   claude  # or `claude code` depending on install
   ```
2. Try a slash command:
   - `/decision Decided to use Postgres over MySQL`
   - `/where-am-i`
   - `/verify`

These wrap the `vault` CLI — same behavior, different surface.

## 9. Verify Hermes Discord integration (optional)

If you have Hermes installed:

```bash
# Restart Hermes to load skill
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.hermes.gateway.plist

# Send via Discord (any allowlisted channel):
!note Testing Hermes integration

# Verify
cat "$AUTOFLOW_VAULT/_system/inbox.md"
# Should see the new entry
```

## 10. Open the dashboard

In Obsidian, open `00-Dashboard/Documentation-Health.md`. You should see:
- Table of active projects
- 11-file coverage matrix
- Recent decisions list
- Stale STATUS warnings

If empty or errored, ensure Dataview JavaScript Queries are enabled.

## Next steps

- [Migrate existing projects to AutoFlow Standard](examples/migration-walkthrough.md) (TODO)
- [Architecture deep-dive](architecture.md)
- [vault CLI reference](concepts/vault-cli.md)
- [Comparison to alternatives](comparison.md)
