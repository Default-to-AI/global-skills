# gbrain runtime and ghost-slug notes

Session-derived operational notes for vault graph work.

## 1. Soft-deleted slugs are not a safe link-refresh primitive

If you `gbrain delete <slug>` to force a fresh import, do **not** assume `gbrain put` or `gbrain capture --slug <slug>` will revive that same slug immediately.

Observed durable pattern:
- the slug can remain soft-deleted;
- `put` / `capture` may report success while the page stays non-live (`page_not_found_after_write`-style write-through result);
- backlinks can temporarily continue to show the deleted slug as a source until purge catches up.

Safer recovery pattern:
1. Prefer non-destructive refresh methods first.
2. If a slug is already soft-deleted and will not revive cleanly, create a **fresh slug** for the rebuilt source note instead of looping on `delete` + `put`.
3. Re-verify backlinks against the **live** slug, not just aggregate orphan counts.
4. Treat old deleted-slug edges as purge-lag, not proof the new source note is wrong.

## 2. Resolver form matters more than pretty links

For gbrain backlink/orphan work, verify the resolver's preferred form before bulk editing.

Observed working forms:
- slug basename links like `[[article]]` for `types/article`;
- normalized title links for some notes;
- full slug-path links were less reliable in the tested flow.

Practice:
- test a few representative targets first;
- once one form proves live in backlinks, standardize the batch to that form.

## 3. Verify source-page edge creation, not just target existence

When a MOC/index page is supposed to de-orphan targets:
- verify the target receives inbound backlinks from the intended source page;
- sample multiple target types, not just one note;
- do not close from a headline orphan-count delta alone.

## 4. Dream/model validation can silently skip instead of failing hard

When using `gbrain dream` to validate chat-model availability:
- an unreachable chat model may yield JSON with `"status": "skipped"` and `"phases": []`;
- this can still exit successfully instead of raising a hard error.

Implication:
- a shell wrapper that only falls back on non-zero exit codes will **not** catch this case;
- for model-health checks, inspect dream output content, not exit code alone.

Use this when validating whether a cloud model is truly active before relying on dream/autopilot for proposal generation.
