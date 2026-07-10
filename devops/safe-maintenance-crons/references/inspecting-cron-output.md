# Inspecting Existing Cron Output

Use this when the task is not to design a cron, but to answer questions like:
- what cron jobs exist?
- what did maintenance last do?
- what was the latest output from a scheduled run?
- what exactly did the cron mean by a recommendation?

## Retrieval pattern

1. List jobs first to get the `job_id`, schedule, status, and next/last run metadata.
2. Read the latest markdown artifact under:
   - `~/.hermes/cron/output/<job_id>/` on standard Hermes installs
   - Example Windows host path: `C:/Users/Tiger/AppData/Local/hermes/cron/output/<job_id>/`
3. Use the newest timestamped `*.md` file there as the authoritative run output.
4. If the prompt or script behavior needs explanation, inspect the cron's injected prompt text and any referenced pre-run script.

## Important distinction

`cronjob list` tells you scheduler metadata.

It does **not** give the full human-facing run report. The actual delivered content is usually stored as a timestamped markdown artifact in the cron output directory.

## Explanation pattern

When explaining maintenance output:
- distinguish **what the script scanned** from **what the LLM was allowed to change**
- distinguish **archiving/moving** from **deleting**
- quote the exact rule when a recommendation refers to a cleanup policy
- state plainly when the cron identified issues implicitly rather than as a numbered top-3 list

## Common pitfall

Do not summarize a maintenance cron from `cronjob list` alone. That only shows status metadata. Read the latest output artifact before describing what the cron actually did.