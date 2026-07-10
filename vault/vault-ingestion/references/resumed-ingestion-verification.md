# Resumed Ingestion Verification

Use this when an ingestion session is resumed after an empty assistant reply, interrupted closeout, or uncertain mid-stream state.

## Goal
Recover from partial progress by trusting live vault artifacts, not the missing narrative.

## Recovery Pattern
1. Reconstruct the intended artifact chain from live files:
   - domain `raw/` capture
   - durable `wiki/` page(s) and/or extract
   - target `wiki/index.md` entry
   - target `wiki/log.md` entry
   - original `_Inbox/` item state
2. Verify each artifact exists and points to the others correctly.
3. Read back the exact touched ranges of `wiki/index.md` and `wiki/log.md` rather than assuming append/patch operations were clean.
4. Look specifically for reader-visible corruption that audits may miss:
   - malformed Markdown list markers (`|-`, `||-`, doubled bullets)
   - duplicated adjacent entries from repeated patch attempts
   - stale titles/slugs after renames
   - mismatched source-capture links
5. If artifacts already exist, continue by repairing/finishing them instead of restarting the ingest from `_Inbox/`.
6. Only remove the inbox original after the canonical chain and log/index updates are verified.
7. Then produce the normal post-ingestion report.

## Why
Ingestion work often spans many tool calls. If a turn drops the visible reply, the vault may still contain most of the durable work. Restarting from scratch risks duplicate captures and unnecessary churn; resuming from live state preserves provenance and graph integrity.
