#!/usr/bin/env bash
# cron_flash_guard_check.sh — re-deploy guard for the Windows silent-cron patch.
#
# WHY: `hermes update` or a venv rebuild wipes
#   HERMES_HOME/hermes-agent/venv/Lib/site-packages/usercustomize.py
# silently bringing back the console-window flash on cron jobs.
#
# Run this after any `hermes update` (or wire it as a no_agent cron watchdog).
# - If the venv guard is present: exit 0 (ok).
# - If missing but a source copy exists in user site-packages: re-deploy + exit 0.
# - If BOTH are missing: print an alert to stderr and exit 1 (real failure).
set -u
HERMES_HOME="${HERMES_HOME:-$HOME/AppData/Local/hermes}"
VENV_UC="$HERMES_HOME/hermes-agent/venv/Lib/site-packages/usercustomize.py"
SRC_UC="$HOME/AppData/Roaming/Python/Python312/site-packages/usercustomize.py"

if [ -f "$VENV_UC" ]; then
  echo "OK: venv usercustomize.py present - cron flash-guard active."
  exit 0
fi

if [ -f "$SRC_UC" ]; then
  cp "$SRC_UC" "$VENV_UC" \
    && echo "FIXED: re-deployed venv usercustomize.py (was wiped by update)." \
    && exit 0
fi

echo "ALERT: venv AND source usercustomize.py both missing - paste Layer 1 from the windows-silent-cron skill." >&2
exit 1
