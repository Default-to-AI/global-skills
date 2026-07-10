# Cron smoke + Telegram formatting verification

Use this when cron health is uncertain **or** when you changed the wording/formatting of scheduled Telegram updates.

## Goal
Separate three different questions:
1. Does the cron executor actually run jobs?
2. Does the job produce the intended output shape?
3. Does Telegram delivery/rendering behave as expected?

## Minimal executor smoke test
1. Create a tiny one-shot local job (`deliver: local`) with a deterministic script that prints one short line.
2. Trigger it immediately.
3. Run a tick if needed.
4. Verify a fresh artifact exists under `C:/Users/Tiger/AppData/Local/hermes/cron/output/<job_id>/`.
5. If the job still exists in `jobs.json`, also verify `last_run_at` moved.

If the artifact exists, the executor path is healthy enough to stop blaming the scheduler globally.

## Formatting smoke test
Use a one-shot local cron job whose prompt requires the exact intended output shape.

Recommended Telegram-safe formatting:
- `**bold**` for section labels and key status words
- `*italic*` only for short qualifiers like time or notes
- light emojis for scanability
- no underline dependence

Example shape:
- `🧪 **Formatting smoke**:` one-line summary
- `📦 **Details**:` 1-2 bullets
- `➡️ **Next look**:` one short bullet

Verify the rendered text first in the saved cron output artifact. Then allow the next real scheduled Telegram run to confirm the live transport rendering.

## Cleanup
Remove the temporary smoke script, temporary output dirs, and any one-off plan artifact once the check is complete.
