#!/bin/bash
#
# AutoFlow Standard — installer
#
# Sets up:
#   1. $AUTOFLOW_VAULT/_system/{bin,Skills,Reports}/  → CLI + skills
#   2. $AUTOFLOW_VAULT/Templates/{_ProjectStandard,scripts}/  → scaffolder
#   3. $AUTOFLOW_VAULT/00-Dashboard/Documentation-Health.md  → compliance dashboard
#   4. ~/.claude/{commands,hooks}/ → Claude Code integration (optional)
#   5. ~/Library/LaunchAgents/com.autoflow.vault-daemon.plist (macOS) → daemon
#   6. ~/.hermes/skills/autoflow/vault-cli/ (if Hermes installed) → Discord integration
#
# Usage:
#   AUTOFLOW_VAULT=$HOME/vault ./bin/install.sh
#
# Idempotent. Re-run safely.

set -e

# ─── Config ──────────────────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AUTOFLOW_VAULT="${AUTOFLOW_VAULT:-$HOME/vault}"
SYSTEM_DIR="${AUTOFLOW_VAULT}/_system"

echo "═══════════════════════════════════════════════════════════"
echo "  AutoFlow Standard installer"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Vault location: $AUTOFLOW_VAULT"
echo "System dir:     $SYSTEM_DIR"
echo ""

# ─── 1. Vault directories ───────────────────────────────────────────
echo "→ Creating vault directories..."
mkdir -p "$AUTOFLOW_VAULT"/{02-Projects,00-Dashboard,Templates/_ProjectStandard,Templates/scripts,_system/{bin,Skills,Reports}}

# ─── 2. Copy bin/ ───────────────────────────────────────────────────
echo "→ Installing CLI to $SYSTEM_DIR/bin/"
cp "$REPO_DIR/bin/vault" "$SYSTEM_DIR/bin/vault"
cp "$REPO_DIR/bin/vault-daemon" "$SYSTEM_DIR/bin/vault-daemon"
chmod +x "$SYSTEM_DIR/bin/vault" "$SYSTEM_DIR/bin/vault-daemon"

# ─── 3. Copy skills/ ────────────────────────────────────────────────
echo "→ Installing skills to $SYSTEM_DIR/Skills/"
for skill in vault-anatomy-refresh vault-runbook-refresh vault-process-map; do
  mkdir -p "$SYSTEM_DIR/Skills/$skill"
  cp "$REPO_DIR/skills/$skill/run.py" "$SYSTEM_DIR/Skills/$skill/run.py"
  chmod +x "$SYSTEM_DIR/Skills/$skill/run.py"
done

# ─── 4. Copy templates ──────────────────────────────────────────────
echo "→ Installing templates to $AUTOFLOW_VAULT/Templates/"
cp "$REPO_DIR/templates/_ProjectStandard/"*.md "$AUTOFLOW_VAULT/Templates/_ProjectStandard/"
cp "$REPO_DIR/templates/Project-Init.md" "$AUTOFLOW_VAULT/Templates/Project-Init.md"
cp "$REPO_DIR/templates/scripts/projectInit.js" "$AUTOFLOW_VAULT/Templates/scripts/projectInit.js"

# ─── 5. Documentation-Health dashboard ──────────────────────────────
echo "→ Installing Documentation-Health.md dashboard"
cp "$REPO_DIR/integrations/obsidian/Documentation-Health.md" "$AUTOFLOW_VAULT/00-Dashboard/Documentation-Health.md"

# ─── 6. Claude Code integration (optional) ──────────────────────────
if [ -d "$HOME/.claude" ]; then
  echo "→ Detected Claude Code at $HOME/.claude — installing integration"
  mkdir -p "$HOME/.claude/commands" "$HOME/.claude/hooks"

  # Slash commands — substitute vault path
  for cmd in "$REPO_DIR/integrations/claude-code/commands/"*.md; do
    name=$(basename "$cmd")
    sed "s|__AUTOFLOW_VAULT__|$AUTOFLOW_VAULT|g; s|__SYSTEM_DIR__|$SYSTEM_DIR|g" "$cmd" > "$HOME/.claude/commands/$name"
  done

  # Hooks — substitute paths
  for hook in "$REPO_DIR/integrations/claude-code/hooks/"*.sh; do
    name=$(basename "$hook")
    sed "s|__AUTOFLOW_VAULT__|$AUTOFLOW_VAULT|g; s|__SYSTEM_DIR__|$SYSTEM_DIR|g" "$hook" > "$HOME/.claude/hooks/$name"
    chmod +x "$HOME/.claude/hooks/$name"
  done

  echo "  ⚠️  Hooks not wired yet. Add to ~/.claude/settings.json manually:"
  echo "      See $REPO_DIR/integrations/claude-code/settings.example.json"
else
  echo "→ Claude Code not detected. Skipping integration. Manual install:"
  echo "    cp $REPO_DIR/integrations/claude-code/commands/* ~/.claude/commands/"
fi

# ─── 7. macOS LaunchAgent (optional) ────────────────────────────────
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "→ macOS detected — installing LaunchAgent (daemon every 5 min)"
  PLIST_DEST="$HOME/Library/LaunchAgents/com.autoflow.vault-daemon.plist"
  sed "s|__VAULT_DAEMON_PATH__|$SYSTEM_DIR/bin/vault-daemon|g; s|__AUTOFLOW_VAULT__|$AUTOFLOW_VAULT|g; s|__REPORTS_DIR__|$SYSTEM_DIR/Reports|g" \
    "$REPO_DIR/integrations/launchd/com.autoflow.vault-daemon.plist.template" > "$PLIST_DEST"

  # Unload existing if loaded
  launchctl unload "$PLIST_DEST" 2>/dev/null || true
  launchctl load "$PLIST_DEST"
  echo "  ✓ LaunchAgent loaded. Verify: launchctl list | grep autoflow"
else
  echo "→ Linux/other detected. LaunchAgent skipped. Add cron manually:"
  echo "    */5 * * * * AUTOFLOW_VAULT=$AUTOFLOW_VAULT $SYSTEM_DIR/bin/vault-daemon"
fi

# ─── 8. Hermes integration (optional) ───────────────────────────────
if [ -d "$HOME/.hermes/skills" ]; then
  echo "→ Hermes detected — installing vault-cli skill"
  mkdir -p "$HOME/.hermes/skills/autoflow/vault-cli"
  sed "s|__AUTOFLOW_VAULT__|$AUTOFLOW_VAULT|g; s|__SYSTEM_DIR__|$SYSTEM_DIR|g" \
    "$REPO_DIR/integrations/hermes/skills/autoflow/vault-cli/SKILL.md" > "$HOME/.hermes/skills/autoflow/vault-cli/SKILL.md"
  echo "  ✓ Hermes skill installed. Reload Hermes to pick up: hermes reload (if exists)"
else
  echo "→ Hermes not detected. Skipping integration."
fi

# ─── 9. PATH check ──────────────────────────────────────────────────
echo ""
if echo "$PATH" | grep -q "$SYSTEM_DIR/bin"; then
  echo "✓ PATH already includes $SYSTEM_DIR/bin"
else
  echo "⚠️  PATH does NOT include $SYSTEM_DIR/bin"
  echo "   Add to ~/.zshrc (or ~/.bashrc):"
  echo ""
  echo "   export AUTOFLOW_VAULT=\"$AUTOFLOW_VAULT\""
  echo "   export PATH=\"\$AUTOFLOW_VAULT/_system/bin:\$PATH\""
fi

# ─── Done ───────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✓ Install complete"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Source your shell config: source ~/.zshrc"
echo "  2. Verify CLI:                vault help"
echo "  3. Check daemon:              launchctl list | grep autoflow"
echo "  4. Test:                      vault list && vault verify"
echo ""
echo "Create your first project:"
echo "  Open Obsidian → Cmd+P → 'Templater: Create new note from template' → 'Project-Init'"
echo ""
