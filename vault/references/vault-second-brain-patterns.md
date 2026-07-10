# Vault second-brain patterns

Condensed pattern extracted from live review of `C:\Users\Tiger\Vault`.

## What this vault is

- An **agent-readable knowledge graph**, not a loose markdown archive.
- Root operating docs define behavior; domain `wiki/AGENTS.md` files refine local conventions.
- `vault-index.md` is the safe top-level map.

## Default traversal

1. `AGENTS.md`
2. `vault-guide.md`
3. `vault-index.md`
4. target `domain/wiki/index.md`
5. target `domain/wiki/log.md`
6. target `domain/wiki/AGENTS.md` if present

## High-value operating rules

- `_Inbox/` is transient intake, not durable knowledge.
- Frontmatter is evidence, not truth; read the body before trusting routing metadata.
- `type` / `platform` / `author` values must be looked up live before writing links.
- Never write a wikilink to a target that does not exist.
- `Types/` is read-only infrastructure in this vault.
- `outputs/` may already contain reusable agent syntheses; check there before re-deriving work.
- `wiki/log.md` is operational memory; read it before meaningful domain changes.

## Practical implication for Hermes

For this vault, broad filesystem search is a fallback, not the default. Start from the operating docs and domain maps, then follow linked durable notes. Use raw/inbox material mainly for provenance, verification, or ingestion work.
