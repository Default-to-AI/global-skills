# Vault Cron Ingestion Design

## Purpose

Autonomously process pending `_Inbox/` items using the same canonical ingestion process used in foreground sessions.

## Required Skills

- `vault-ingestion`
- `vault-audit-fix`

## Recommended Prompt Shape

Process pending files in `C:\Users\Tiger\Vault\_Inbox` using the canonical Vault ingestion workflow. Preserve sources, create or update wiki material, create links, update domain logs, run audit-fix, and generate a background ingestion report. Do not delete, merge, rename, change Types, create domains, or perform ambiguous destructive changes without Robert approval. Leave ambiguous items in `_Inbox/` and report the needed decision.

## Bounded Input Rules

- Process only `_Inbox/` unless Robert configures another queue.
- Limit items per run if needed to avoid huge autonomous batches.
- Skip files that cannot be classified safely.
- Never invent new domains.
