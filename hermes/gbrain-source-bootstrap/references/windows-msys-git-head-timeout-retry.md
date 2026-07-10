# Windows/MSYS git HEAD timeout retry

## Trigger pattern

Use this note when gbrain records sync failures with all of:

- `path: <head>`
- `error: git HEAD verification failed: spawnSync git ETIMEDOUT`
- `code: UNKNOWN`

Common places it surfaces:
- `gbrain sync`
- `gbrain doctor --fast`
- queued source-sync retries

## What it usually means

On Windows hosts running Git via MSYS/bash, a cold or flaky `execFileSync('git', ['rev-parse', 'HEAD'])` can time out even when the repo is fine. This is a **retry-class spawn fault**, not automatically a broken repo, parse error, or DB issue.

## Fast diagnosis

1. Verify the repo itself responds normally:
   - `git rev-parse HEAD`
   - `git status --porcelain`
2. Read the sync implementation and confirm the failing path is the HEAD-verification wrapper around git, not markdown import or embedding code.
3. Check whether the failure ledger entry is stale or still reappearing on fresh syncs.

## Durable local fix pattern

Patch the sync helper that shells out to git so timeout-class failures retry with short backoff before surfacing a hard failure.

Desired behavior:
- keep the normal per-call timeout cap (for example 30s)
- retry only timeout-like failures (`ETIMEDOUT`, timed-out `SIGTERM`, equivalent spawn timeout markers)
- log the retry so later diagnosis has positive evidence
- stop after a small bounded number of attempts

## Positive verification standard

A valid fix is not "no errors on the second run". Look for all of:

1. a logged retry on `rev-parse HEAD`
2. the same sync finishing `EXIT=0`
3. no fresh open `<head>` sentinel recorded in the sync-failure ledger afterward

Example positive signal shape:

```text
[git retry 1/2] rev-parse HEAD in /c/Users/Tiger/Vault timed out; retrying in 500ms
Text imported. Run 'gbrain embed --stale' to generate embeddings.
Synced <old>..<new>:
  +1 added, ~10 modified, -0 deleted
EXIT=0
```

## Cleaning up historical failures

If old `<head>` timeout entries remain in the ledger after the retry fix proves itself:

- preserve the records
- mark them acknowledged with a reason
- do not delete audit history just to make the dashboard look clean

This distinguishes **historical environmental noise** from active unresolved sync failures.

## Non-lessons

Do **not** save either of these as durable rules:
- "gbrain sync is broken on Windows"
- "browser/tools/git do not work here"

The durable lesson is the retry-and-verify pattern around flaky MSYS git spawn timeouts.
