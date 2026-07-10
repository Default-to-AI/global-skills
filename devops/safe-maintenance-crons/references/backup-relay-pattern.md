# Backup Relay Pattern for Scheduled Jobs

Use this pattern when a cron job's main work is a deterministic backup/sync script and the human-facing requirement is a short Telegram update.

## Core shape

1. Compute the current local time in the job's required timezone.
2. Send a **start** message before launching the backup script.
3. Run the script and capture both stdout/stderr plus exit code.
4. Compute a fresh local timestamp for completion.
5. Send either:
   - a short **success** message when exit code is 0, or
   - a short **failure** message that includes the useful script output when exit code is non-zero.
6. Clean up one-off plan artifacts created only for the run.

## Message design

For mobile chat transports, favor:
- one bold main status line
- optional short italic label like `*Time:*`
- simple language and light emoji
- no underline dependence
- success copy that summarizes outcome instead of dumping logs
- raw script output only on failure, where it actually helps debugging

## Why this matters

A backup job is usually judged on two things:
- did the backup actually finish?
- did the human get a quick trustworthy status update?

Short start/finish markers reduce ambiguity when the script hangs or fails mid-run.

## Verification checklist

- start notification send returned success
- backup script exit code recorded
- completion notification send returned success
- failure path preserves stdout/stderr for debugging
- temporary plan files removed after the run

## Time handling

Do not reuse a stale timestamp across the whole workflow. Generate the start timestamp before the script, and the completion timestamp after the script, both in the required local timezone.
