# Deterministic Cleanup Script Pattern

## Problem
The original `hermes-cleanup-daily` cron used a massive LLM prompt with ~50 explicit shell commands. When executed, the combined stdout exceeded the response length limit, causing:
```
RuntimeError: Response truncated due to output length limit
```

## Solution
Move all filesystem logic into a **deterministic Python script** that:
1. Enforces a hard max-deletion quota (e.g., 10 items per run)
2. Emits a concise, structured summary report
3. Never produces unbounded output

## Script Structure
```python
#!/usr/bin/env python3
"""Deterministic cleanup with quota and concise report."""
from dataclasses import dataclass
from pathlib import Path
# ... imports

MAX_DELETIONS = 25  # Hard quota — prevents output explosion

# Kanban workspace cleanup constants
KANABAN_WORKSPACES_ROOT = HERMES_ROOT / "kanban" / "workspaces"
KANABAN_WORKSPACE_MAX_AGE_DAYS = 7
KANABAN_WORKSPACE_KEEP_COUNT = 3  # keep 3 most recent regardless of age

def main():
    actions: list[Action] = []
    skips: list[Skip] = []
    
    # Ordered by priority / safety
    maybe_delete_request_dumps(actions, now)
    maybe_delete_state_snapshots(actions, now)
    maybe_delete_temp_artifacts(actions, now)
    maybe_delete_kanban_workspaces(actions, now)  # NEW: completed kanban task workspaces
    maybe_archive_old_plans(actions, skips, now)
    maybe_delete_pycache(actions, skips, now)
    maybe_delete_bootstrap(actions, now)
    maybe_delete_config_backups(actions, now)
    maybe_delete_cache_terminal(actions, now)
    maybe_delete_screenshots(actions, now)
    maybe_delete_logs(actions, now)
    maybe_delete_profile_artifacts(actions, now)
    
    # Emit concise Telegram-ready report
    print(TEMPLATE.format(...))
```

```python
def maybe_delete_kanban_workspaces(actions: list[Action], now: datetime) -> None:
    """Delete completed kanban task workspaces older than the threshold,
    keeping the newest few as recovery handles."""
    if not KANABAN_WORKSPACES_ROOT.exists():
        return
    workspaces = sorted(
        (p for p in KANABAN_WORKSPACES_ROOT.iterdir() if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for workspace in workspaces[KANABAN_WORKSPACE_KEEP_COUNT:]:
        if old_enough(workspace, KANABAN_WORKSPACE_MAX_AGE_DAYS, now):
            if not delete_path(workspace, "kanban-workspaces", actions):
                return
```

## Key Principles
- **Quota-first**: Stop after N deletions regardless of candidates remaining (currently `MAX_DELETIONS = 25`)
- **Report skipped items**: Important review items (backups, old plans) are reported but not deleted
- **No LLM judgment**: The script decides what's deletable; the cron only relays
- **Deterministic output**: Same input filesystem state → same output report
- **Safe by default**: Denylist paths are hardcoded, not inferred
- **Ordered by priority**: Request dumps → state snapshots → temp artifacts → **kanban workspaces** → plan archival → pycache → bootstrap → config backups → terminal cache → screenshots → logs → profile artifacts
- **Recovery handles preserved**: Each category keeps a small number of recent items (e.g., 3 newest plans, 3 newest kanban workspaces, 2 newest state snapshots) regardless of age

## Cron Job Config
```yaml
script: hermes-cleanup-daily.py
no_agent: false  # Use agent-mode relay on Windows (see windows-no-agent-quirk.md)
prompt: |
  Scheduled Hermes cleanup relay.
  Read the injected stdout from the pre-run script first.
  - If empty, respond with exactly `[SILENT]`.
  - Otherwise, return the injected report verbatim.
  - No tools, no commentary.
```

## Result
- Zero truncation failures
- Sub-second execution
- Predictable, auditable deletions
- Clean Telegram report every run

## Kanban Workspace Cleanup (Added 2026-06-12)
The daily cleanup now includes `maybe_delete_kanban_workspaces()` which removes completed kanban task workspaces from `C:/Users/Tiger/AppData/Local/hermes/kanban/workspaces/` that are:
- Older than 7 days (`KANABAN_WORKSPACE_MAX_AGE_DAYS`)
- Not among the 3 most recent workspaces (`KANABAN_WORKSPACE_KEEP_COUNT = 3`)

This prevents the side menu/TUI session list from accumulating stale completed-task directories while preserving a small recovery window. The cleanup runs after temp artifacts and before plan archival in the priority order.