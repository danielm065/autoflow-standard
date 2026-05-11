#!/bin/bash
#
# session-end-vault.sh — Claude Code Stop hook
#
# Runs at end of session. If CWD inside vault project:
#   1. Suggest writing handoff (if missing for today)
#   2. Run quick verify
# Non-blocking. Prints info, never fails session.

set +e

AUTOFLOW_VAULT="${AUTOFLOW_VAULT:-__AUTOFLOW_VAULT__}"
VAULT_BIN="__SYSTEM_DIR__/bin/vault"

case "$PWD" in
  "${AUTOFLOW_VAULT}"/02-Projects/*) ;;
  *) exit 0 ;;
esac

[ -x "$VAULT_BIN" ] || exit 0

project=$(echo "$PWD" | sed -E "s|${AUTOFLOW_VAULT}/02-Projects/([^/]+).*|\1|")
[ -z "$project" ] && exit 0

echo ""
echo "═══════════════════════════════════════════════"
echo "🏁 Session ending — vault summary for ${project}"
echo "═══════════════════════════════════════════════"

"$VAULT_BIN" verify "$project" 2>&1 | head -8

handoff_file="${AUTOFLOW_VAULT}/02-Projects/${project}/handoff.md"
if [ -f "$handoff_file" ]; then
  today=$(date +%Y-%m-%d)
  if ! grep -q "$today" "$handoff_file" 2>/dev/null; then
    echo ""
    echo "💡 No handoff entry for today (${today})."
    echo "   Run: vault handoff \"<what's next>\""
  fi
fi

echo ""
exit 0
