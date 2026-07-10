# Supabase direct migrations + dirty-tree refusal

Use this reference when a gbrain brain on Supabase looks half-broken: doctor is slow, `apply-migrations` wedges on heavyweight versions, or the last migration keeps failing with no obvious detail.

## Durable pattern

### 1) Separate pooled-vs-direct Postgres behavior

A Supabase transaction/session pooler URL can be acceptable for light reads and short writes, yet become pathological on heavyweight gbrain migration phases (graph extraction, takes backfills, facts writeback).

Symptoms:
- `gbrain doctor --fast` is slow or intermittently wedged.
- `gbrain apply-migrations --yes` repeatedly stalls or times out on the same heavy migration.
- Re-running progresses farther only after long waits, then wedges again.

Winning move:
- Verify the existing brain's project ref first.
- Test the direct URL `postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres` independently.
- Back up config.
- Patch gbrain to the direct `5432` URL.
- Re-run doctor and migrations.

Do **not** switch to a different project ref just because a fresh password exists there. Confirm which project already contains the brain's pages/sources.

## 2) Treat heavyweight migrations as idempotent backfills

Some gbrain migrations do real work over thousands of pages. A timeout does not automatically mean the migration is stuck forever.

Observed pattern:
- A migration can spend minutes on link extraction or frontmatter/takes/facts backfill.
- Partial durable work may already have landed in the DB before the wrapper timeout kills the outer process.
- Re-running after the heavy sub-phase has finished is often the correct move.

Practical rule:
- If the DB shows the expected new rows landing and the heavy phase is idempotent, let it finish once and then re-run the full chain with a longer timeout.
- Distinguish "still writing" from "idle forever" before deciding it is hung.

## 3) Final writeback migrations may be blocked by Git cleanliness, not the DB

When the last migration writes facts back into markdown pages, the failure mode can shift from database throughput to repository policy.

Key check:
- Run `git -C <source-local-path> status --porcelain`.
- If non-empty, a writeback migration may refuse to proceed until the source tree is clean.

Interpretation:
- Repeated `status=failed` with sparse logs can still be deterministic and healthy from the DB's perspective.
- The correct conclusion is "source worktree dirty" — not "Supabase still broken".

## 4) User decision boundary

If the source is the user's vault or another content repo with real work in progress, do not auto-commit just to satisfy the migration.

Escalate explicitly:
- Commit current changes, then retry.
- Stash current changes, then retry.
- Skip the writeback migration and leave facts in the DB.

The skill should present that as an informed tradeoff, not as a mysterious migration failure.

## 5) Key-free model path can still work

If the user lacks Anthropic/OpenRouter credentials, gbrain cleanup and dream flows can still run when the live engine is pointed at a working local or other configured model provider. Verify the live engine override, not just stale file-level defaults.

Meaning:
- "No Anthropic key" is not automatically blocking.
- Distinguish chat/takes provider needs from the database/migration problem.
