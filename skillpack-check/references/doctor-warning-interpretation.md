# gbrain doctor warning interpretation (Windows / Supabase / cron-heavy setups)

Use this note when `gbrain doctor` reports a scary-looking mixed bag and you need to separate real breakage from routine maintenance.

## High-value interpretations

### `autopilot_lock_scope`
- Meaning: a lockfile exists outside GBRAIN_HOME or points at an old PID.
- Safe action: verify the owning PID is dead first; if dead, remove the stale lockfile.
- Do **not** delete a live lock just because the warning exists.

### `cycle_freshness`
- Meaning: one or more sources have not completed a recent dream/cycle.
- This is usually **staleness**, not core-system failure.
- Action: run `gbrain dream --source <id>` for the stale source or resume autopilot.
- Distinguish dormant auxiliary sources from the primary source the user actually cares about.

### `sync_freshness`
- Meaning: a source has not synced recently.
- Action: `gbrain sync --source <id>`.
- If the source is intentionally dormant, report it as low priority instead of treating it as an outage.

### `effective_date_health`
- Meaning: pages fell back to `updated_at` despite parseable frontmatter dates.
- Action: `gbrain reindex-frontmatter`.
- This is data hygiene, not emergency break/fix.

### `multi_source_drift`
- Meaning: same slug appears in `default` and should likely belong to a named source, OR the intended source never completed initial sync.
- Action: check `gbrain sources status` / source sync health **before** deleting anything.
- Do not treat drift as permission to blindly delete the `default` row.

### `graph_coverage` / `orphan_ratio` vacuous on markdown-only brains
- On brains with few/no typed entity pages, these checks can be technically `[OK]` but not informative.
- For graph-quality questions, use targeted backlink verification on real pages instead of over-reading the summary score.

## What doctor does NOT prove by itself
- A clean `doctor` run proves DB, embeddings, and general install health.
- It does **not** by itself prove the configured `chat_model` will successfully spend tokens on the next dream/extract/proposal step.
- To verify a chat-model change, do one of:
  1. a provider-native API smoke test with the exact endpoint/auth/model combo, or
  2. one real gbrain command that actually invokes the chat path (for example a dream/proposal-producing run).

## Practical reporting rule
When the user asks "is gbrain healthy?", separate findings into:
1. **Core healthy** — DB, embeddings, connection, schema, installed commands.
2. **Maintenance debt** — stale cycle/sync, date reindex, drift cleanup.
3. **User-facing risk** — stale lock blocking autopilot, broken chat model, blocked source, repeated sync failure.

Do not collapse maintenance warnings into a false "system broken" verdict.