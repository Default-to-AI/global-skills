# Git-backed Hermes backup cron timeouts

Use this when a Hermes backup cron reports `Script timed out after 120s` or similar while running a local backup/sync script.

## Diagnostic pattern

1. Inspect the cron output artifact first to distinguish script timeout from agent/reporting failure.
2. Inspect the backing script and identify expensive phases: copy/mirror, compression, `git add`, `git status`, `git commit`, `git push`, network sync.
3. Run the same phases manually with timers and short output summaries. Do not rely on absence of errors; record return code and elapsed seconds per phase.
4. For Git-backed backups, check destination repo state:
   - `git status --short | wc -l`
   - `git status -sb`
   - `git log -1 --oneline --date=iso --format='%h %ad %s'`
   - `GIT_TERMINAL_PROMPT=0 timeout 30 git ls-remote --heads origin main`
5. If a manual commit was created only for diagnostics and push fails/times out, reset the destination repo back to `origin/main` before patching the script, unless the user explicitly wants that diagnostic commit retained.

## Durable fix pattern

Runtime and generated artifacts can dominate the diff and make `git add`/`commit`/`push` exceed the scheduler budget even when copy/mirror is fast. Keep the backup focused on durable configuration and knowledge state.

Recommended exclusions for Hermes-local backups unless the user says otherwise:

- directories: `cache`, `logs`, `lsp`, `cron/output`, `audio_cache`, `screenshots`, `checkpoints`, `node_modules`, `bin`, `.git`, `__pycache__`, `.pytest_cache`, local repo checkouts such as `hermes-agent`, profile-retirement backup folders.
- files/patterns: `*.log`, `*.pyc`, `*.sqlite`, `*.sqlite-shm`, `*.sqlite-wal`, `*.db`, `*.db-shm`, `*.db-wal`, `*.pid`, `*.lock`, `.env.local`, large binaries like `uv.exe`.

If a mirror destination already contains newly excluded directories, delete those directories from the destination before the next mirror. Mirror tools may prevent future copies of excluded dirs but not remove already-present excluded content.

For unattended git commands, set `GIT_TERMINAL_PROMPT=0` so a missing credential path fails quickly instead of hanging until the scheduler times out.

## Verification

A repaired backup cron path should have positive evidence:

- backing script compiles or passes a syntax check;
- direct script run exits `0` within the scheduler budget;
- logs show elapsed times for copy, git stage/status/commit/push;
- destination repo is clean against `origin/main` after push;
- `git ls-remote` confirms the remote branch points to the pushed commit;
- cron config still has the expected `script` binding and next run time.
