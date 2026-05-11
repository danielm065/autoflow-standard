#!/bin/bash
#
# post-edit-vault-refresh.sh — Claude Code PostToolUse hook
#
# After Edit/Write inside 02-Projects/<N>/, signal daemon to refresh.
# Lightweight — touches markers, spawns daemon in bg. Doesn't block.

set +e

AUTOFLOW_VAULT="${AUTOFLOW_VAULT:-__AUTOFLOW_VAULT__}"
STATE_DIR="__SYSTEM_DIR__/Reports/daemon-state"
DAEMON="__SYSTEM_DIR__/bin/vault-daemon"

INPUT=$(cat)
FILE=$(echo "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed -E 's/.*"file_path"[[:space:]]*:[[:space:]]*"([^"]+)"/\1/')

[ -z "$FILE" ] && exit 0

case "$FILE" in
  "${AUTOFLOW_VAULT}"/02-Projects/*) ;;
  *) exit 0 ;;
esac

project=$(echo "$FILE" | sed -E "s|.*/02-Projects/([^/]+).*|\1|")
[ -z "$project" ] && exit 0

case "$project" in
  Tasks|Meetings|Processes|Personal-Life|_legacy|_unassigned|_archive) exit 0 ;;
esac

[ ! -f "${AUTOFLOW_VAULT}/02-Projects/${project}/CLAUDE.md" ] && exit 0

mkdir -p "$STATE_DIR"
rm -f "${STATE_DIR}/${project}.anatomy.marker"

case "$FILE" in
  *.json)        rm -f "${STATE_DIR}/${project}.process-map.marker" ;;
  */issues.md)   rm -f "${STATE_DIR}/${project}.runbook.marker" ;;
  */buglog.json) rm -f "${STATE_DIR}/${project}.runbook.marker" ;;
esac

nohup bash "$DAEMON" >/dev/null 2>&1 &

exit 0
