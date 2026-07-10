# gbrain link refresh and resolver behavior

Use this reference when vault graph work depends on gbrain's backlink/orphan metrics moving, not just Obsidian navigation improving.

## Durable findings from the 2026-07-10 vault graph session

### 1) Do not assume `gbrain sync` refreshes wikilink edges
In the tested flow, `gbrain sync` — even `gbrain sync --full` — did **not** reliably re-run wikilink extraction for an already-indexed source page.

Working repair path:
1. Soft-delete the source page slug: `gbrain delete <slug>`
2. Fresh-import the same page: `gbrain put <slug> < file.md`
3. Re-check the targets with `gbrain backlinks <target-slug>`

This mattered for `hermes/genuine-orphans-index`: normal syncs saw the content change, but backlink edges only appeared after delete+put.

### 2) Resolver matching favored basename/title-normalization, not full slug text
Working forms observed:
- `[[article]]` -> `types/article`
- `[[tradinglab]]` -> `finance/wiki/tradinglab`
- `[[13-06-2026-headroom-better-stack-ingestion-report]]` -> matching output page by basename
- `[[Eugene Fama]]` -> `finance/wiki/eugene-fama` (placeholder resolved via title-normalized text)

Non-working pattern to avoid as the default:
- `[[finance/wiki/eugene-fama]]`

Practical rule: start with slug basename links. If a placeholder/person page still fails, test the human title form.

### 3) Duplicate titles can block or confuse graph work
Three ingestion-report pages shared the same `title: Post-Ingestion Report`. Giving them unique titles reduced ambiguity before link-refresh verification.

### 4) Graph probes can return false negatives during transport trouble
Earlier empty `backlinks`/`graph` reads were partly explained by intermittent Supabase `CONNECT_TIMEOUT` behavior. Retry before concluding the graph is empty or that extraction failed globally.

## Recommended verification loop
1. Confirm the source page contains intended wikilinks.
2. Use basename-form links first.
3. Fresh-import the source page with `delete` + `put` if gbrain metrics matter.
4. Verify with `gbrain backlinks <target-slug>` on a representative sample across note types.
5. Only then claim orphan/backlink improvement.
