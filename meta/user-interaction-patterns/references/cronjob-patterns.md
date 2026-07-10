# Cronjob Patterns

## The `deliver` default trap

**The `cronjob` tool's `deliver` parameter silently defaults to `"local"`** (save only, no delivery to the user). Every cron creation requires explicit `deliver="origin"` to function.

**Always do:**
```python
cronjob(action="create", ..., deliver="origin")
```

**Always verify after creation:**
```python
cronjob(action="list")  # Check deliver field in output
```

If `deliver` shows `"local"`, fix immediately:
```python
cronjob(action="update", job_id="...", deliver="origin")
```

## Watchdog patterns

### `no_agent=True` (preferred for notification-only crons)
- Runs a script every N minutes
- Script compares current state to cached state
- **Silent when nothing changed**, outputs notification text when it detects a change
- Output is delivered verbatim to the user
- Zero LLM cost per tick
- Good for: kanban board monitoring, file change detection, price thresholds

### `no_agent=False` (LLM-driven cron — requires strict guardrails)
- Runs a prompt every N minutes, agent checks state and decides actions
- High token cost per tick (even when nothing changes)
- Prone to hallucination unless the prompt has extremely strict rules:
  - Never create cards with `--parent` links (causes circular dependencies)
  - Never ask the user to do something — just act
  - Output max 2 lines per tick
  - Track created card IDs to avoid duplicates
- Only use when the cron needs to take autonomous actions (not just notify)