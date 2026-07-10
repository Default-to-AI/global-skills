# Duplicate Re-capture Resolution

Use this when an `_Inbox/` item appears to be a fresh addition but the vault already contains a canonical raw + wiki + extract chain for the same source.

## Decision rule

Treat the new inbox item as a duplicate when all are true:
- same underlying URL / repository / video / article;
- same subject, not a companion source;
- no materially richer durable content than the existing canonical chain.

## Canonical workflow

1. Create a recovery copy outside the vault before removing the inbox file.
2. Check for the existing canonical chain across:
   - `_Inbox/`
   - target domain `raw/`
   - target domain `wiki/`
   - related domains when routing may have changed since the first ingest
3. Compare for meaningful deltas:
   - new facts or sections;
   - corrected metadata;
   - stronger title/description;
   - useful related-link opportunity.
4. If delta is trivial, do **not** create a second raw note.
5. Patch the existing durable note only if the duplicate reveals a worthwhile connection, clarification, or cross-domain relationship.
6. Append a log entry that explicitly says duplicate-resolution, names the canonical raw note, and states why no second raw note was kept.
7. Remove the inbox duplicate only after the canonical chain and log update are verified.

## Example from session

- New inbox file: `AutoAgent - Autonomously optimizes AI agent harnesses through benchmark-driven iteration.md`
- Existing canonical chain: `AI Sphere/raw/01-06-2026-autoagent.md` + `AI Sphere/wiki/autoagent.md` + `AI Sphere/wiki/extract-autoagent.md`
- Resolution: keep the existing chain, add the cross-link to `[[agent-skills-for-context-engineering]]`, log the duplicate-resolution, then clear `_Inbox/`.
