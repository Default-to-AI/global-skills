# Hermes Vault Memory Layer (RETIRED DESIGN — 2026-07-10)

This documents a vault-first 3-tier memory pattern Robert evaluated. **It was not adopted as a live system** — the manual `Vault/Hermes/memory/` folder was flattened because gbrain already indexes the Vault (`vault-tiger`, 1091 pages) and Hermes hot memory + `session_search` cover the rest. Kept as a historical design reference only.

## Recommended architecture

### Tier 1 — Hermes built-in hot memory
Keep only:
- stable user preferences
- stable environment facts
- critical corrections
- small, high-signal conventions

Why:
- always loaded
- strict char budget
- wrong place for timelines, logs, or bulky project state

### Tier 2 — Vault durable semantic memory
Store in a dedicated vault area such as `Vault/Hermes/memory/`:
- reusable workflows
- durable decisions
- operating conventions
- environment notes worth re-checking later
- project memory that should remain human-readable

Recommended starter files:
- `index.md`
- `preferences.md`
- `environment.md`
- `workflows.md`
- `decisions.md`
- `retrieval-playbook.md`
- `projects/README.md`
- `projects/memory-backend-evaluation.md`

Rule: keep this layer **role-based**, not date-based.

### Tier 3 — Recall layer
Use Hermes `session_search` / session DB for:
- verbatim prior exchanges
- timelines
- exact wording from old sessions
- temporary work history not worth durable promotion

## Default implementation path

**Vault-first beats OSB-first** when the user wants a practical upgrade now and there is no proven need yet for graph/temporal memory.

Default sequence:
1. Create the vault durable-memory schema first.
2. Add a retrieval playbook so future sessions know which layer to query first.
3. Use direct vault file retrieval plus `session_search`.
4. Add OSB/MCP later only if mediated recall or richer automation is actually needed.

## Important boundary

Do **not** pollute the existing domain `wiki/` area with durable operating memory notes.
Use a separate `memory/` area under the relevant domain, e.g. `Vault/Hermes/memory/`.

## Promotion rules

Promote into vault durable memory only when the information is:
- stable
- reusable
- specific enough to help future work
- better as a maintained note than as a transcript snippet

Do **not** mirror ordinary chat, temporary task progress, or every intermediate thought.

## Verification pattern

Before calling the architecture wired up, verify all of:
1. The memory files exist on disk.
2. A seeded fact is retrievable by search/read from the vault layer.
3. The routing playbook exists and clearly separates hot memory vs vault memory vs `session_search`.
4. Hermes still uses built-in hot memory only unless an external backend was intentionally added.
5. The recall path remains separate (`session_search`, not vault transcript dumping).

## Seeded-fact example

A good verification fact:

> Robert's winning Hermes memory architecture is: Hermes hot memory + Vault durable semantic memory + `session_search` raw recall.

## Current proven implementation

**Retired 2026-07-10.** This vault-first `Hermes/memory/` markdown layer was flattened: it duplicated Hermes hot memory + gbrain's `vault-tiger` source (which already indexes the whole Vault, 1091 pages) and nothing auto-read it. A backup copy remains at `~/AppData/Local/hermes/backups/vault-hermes-memory-20260710-205645/`.

Current decision: **use gbrain (vault-tiger + gstack-code) + Hermes hot memory + session_search as the active memory system.** Mnemosyne remains the most promising later-stage backend only if that proves insufficient for temporal/graph memory.
