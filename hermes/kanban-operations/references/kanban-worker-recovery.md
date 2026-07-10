# Kanban Worker Recovery Reference

Session-specific patterns and recipes for recovering from common kanban worker failure modes observed in practice.

## Artifact Not Registered

### Detection
```bash
hermes kanban runs <task-id>
# Shows completed but artifacts array empty or missing
hermes kanban show <task-id>
# No workspace directory exists
```

### Recovery Recipe
```bash
# 1. Create workspace if missing
mkdir -p "C:/Users/Tiger/AppData/Local/hermes/kanban/workspaces/<task-id>"

# 2. Regenerate from parent task output (if available)
hermes kanban show <parent-task-id>  # get artifact path
# Read parent artifact, generate output, write to workspace

# 3. Register via comment
hermes kanban comment <task-id> "Artifact recovered: <filename> — generated from parent <parent-task-id>"
```

### Example (this session)
- Task: `t_8e76480d` (engineer — Build HTML summary page)
- Parent: `t_dd2a94a7` (strategist — spacex-ipo-trading-plan.md)
- Worker completed at 15:41 but no workspace created, no artifact registered
- Recovery: Created workspace, built HTML from parent markdown, saved to workspace, delivered via Telegram, commented on task

## Workspace Conventions

| Platform | Workspace Root |
|----------|----------------|
| Windows (native) | `C:\Users\<user>\AppData\Local\hermes\kanban\workspaces\` |
| WSL | `/mnt/c/Users/<user>/AppData/Local/hermes/kanban/workspaces/` |

**Always use absolute paths.** The `kanban_show` output shows the workspace path but it may not exist yet.

## Stale Running State

### Detection
```bash
hermes kanban show <task-id>
# status: running, but:
ps aux | grep <task-id>  # no process
hermes kanban reclaim <task-id>  # "not running or unknown id"
hermes kanban promote <task-id>  # "task is 'done'"
```

### Resolution
```bash
hermes kanban show <task-id>
# If completed timestamp exists → task is done, state is stale
# Just proceed with downstream tasks
```

## Log Inspection Patterns

```bash
# Full worker log (includes agent reasoning)
hermes kanban log <task-id>

# Key things to look for:
# - "Now I have all the source material" → worker read parent artifacts
# - "Let me create..." → worker starting output generation
# - Completion summary in final event
```

## Prevention Checklist (for worker prompts)

When spawning workers via kanban, ensure the task body includes:
- [ ] Explicit instruction: "Write output to the workspace path (`$KANBAN_WORKSPACE` or the path shown in `kanban_show`), NOT the current working directory."
- [ ] Expected artifact filename(s)
- [ ] Verification step: "Confirm file exists at workspace path before completing."

## Quick Commands

```bash
# List all tasks with status
hermes kanban list --status ALL

# Show task with full context (parent results + comments)
hermes kanban context <task-id>

# View attempt history
hermes kanban runs <task-id>

# Follow live events
hermes kanban watch
```