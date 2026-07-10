# Existing-First Search Patterns

Use this when the canonical ingestion flow says to run existing-first checks before creating any durable vault material.

## Goal
Prove whether the source or subject already exists in `_Inbox/`, target `raw/`, target `wiki/`, target `outputs/`, or a related domain **without** getting trapped in bad search syntax or duplicate no-progress loops.

## Tool Rules

- `search_files(target="files")` → filename search using glob-like patterns such as `*last*30*days*`.
- `search_files(target="content")` → regex search inside files such as `r8jAMxz7Zlg` or `Last 30 Days`.
- Do **not** pass shell wildcards like `*foo*` into content search.
- If using `terminal` for fallback search, use a valid command shape such as:
  - `grep -r 'term' '/c/Users/Tiger/Vault/Agent Skills' 2>/dev/null`
- Do **not** invent malformed shell snippets like `grep>command`.

## Search Order

1. Search by the strongest stable identifier first:
   - video ID
   - repository name
   - URL slug
   - exact title fragment
2. If that fails, pivot to filename search in likely folders:
   - `_Inbox/`
   - target domain `raw/`
   - target domain `wiki/`
   - related domains when the topic might already live elsewhere
3. If still cold, inspect the directory listing and derive filename tokens from real nearby files before issuing another query.
4. Only then fall back to validated recursive grep/content search.

## No-Progress Guard

If the same query returns zero results twice, change strategy. Good pivots:
- switch content search ↔ filename search
- shorten the query to stable title tokens
- search the whole domain root instead of only one subfolder
- inspect actual filenames before issuing another search

Repeated identical zero-result searches are evidence of operator error, not new information.

## Ingestion-Specific Reminder

Existing-first is a **decision gate**, not a ritual. The purpose is to decide whether to create new raw/wiki material, update an existing chain, or resolve a duplicate re-capture. Use the cheapest correct search that answers that question and move on.
