# Delegation Timeout Pattern — Vault Profile

## Observation (2026-06-07)

When a file is added to the vault with proper frontmatter (including `Ingested: true`) and the vault's automatic ingestion workflow has completed:
- Wiki pages exist in the target domain (`wiki/agentic-coding-workflows-2026-guide.md`, `wiki/extract-agentic-coding-workflows-2026.md`, etc.)
- Domain `wiki/index.md` is updated
- `Ingested: true` appears in raw file frontmatter

Delegating to the `vault` profile via `delegate_task` for ingestion **times out after 600s** (40 API calls) because the profile attempts redundant processing on already-complete work.

## Root Cause

The vault profile's ingestion logic does not short-circuit when it detects `Ingested: true` + existing wiki chain. It proceeds through the full canonical flow, consuming tokens and time.

## Mitigation

Before delegating to vault profile for ingestion:
1. Check `Ingested: true` in raw file frontmatter
2. Verify corresponding wiki pages exist in target domain
3. Verify domain `wiki/index.md` includes the new material
4. If all true → ingestion complete, do not delegate

## Session Evidence

- Raw file: `Agent Skills/raw/07-06-2026-agentic-coding-workflows-2026.md` (line 11: `Ingested: true`)
- Wiki pages created: guide, extract, author, platform
- Domain index updated: `Agent Skills/wiki/index.md` (updated 06-06-2026)
- Delegation timed out at 600s with 40 API calls
- Manual verification confirmed ingestion complete

## Applies To

- Any vault ingestion request where user says "I added a file to vault — ingest it now"
- Cron/background ingestion jobs that might re-process
- Handoffs to vault profile that include already-ingested material