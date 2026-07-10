# Windows no_agent Delivery Quirk

## Symptom
A cron job with `no_agent: true` and a Python `script:` under `~/.hermes/scripts/` shows **`Status: silent (empty output)`** in the cron output artifact, even though running the same script directly (`python script.py`) prints the expected report to stdout.

## Environment
- Hermes on Windows (MSYS/bash)
- Python script in `~/.hermes/scripts/`
- Cron job using `no_agent: true` + `script: script_name.py`
- Delivery target: Telegram

## Root Cause (Hypothesis)
The scheduler's stdout capture for `no_agent` jobs on this Windows host appears to lose or discard output before delivery. The script works correctly in direct invocation, suggesting the issue is in the subprocess pipe handling or encoding when the scheduler captures stdout.

## Workaround: Agent-Mode Relay Pattern
Instead of `no_agent: true`, use:
1. `no_agent: false` (default)
2. Keep the same `script:` — its stdout is injected into the agent prompt
3. Use a minimal agent prompt that reads the injected output and echoes it verbatim:

```yaml
prompt: |
  Scheduled Hermes cleanup relay.

  Read the injected stdout from the pre-run script first.
  - If the injected script output is empty or whitespace, respond with exactly `[SILENT]`.
  - Otherwise, return the injected cleanup report verbatim.
  - Do not run tools.
  - Do not add commentary, markdown wrappers, or extra lines.
```

This pattern reliably delivers the script's output because the agent acts as a pass-through and Hermes delivers the agent's final response.

## When to Still Use no_agent
- Watchdog-style jobs where **empty output = healthy** (e.g., disk space check that only alerts on threshold breach)
- Jobs that must run without any LLM overhead
- Jobs where you explicitly want silent-if-nothing-to-report behavior

## Lesson
On this Windows host, **verify end-to-end delivery** of a `no_agent` script job before relying on it for user-visible reports. If delivery fails, switch to the agent-mode relay pattern.