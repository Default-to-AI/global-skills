# Degraded Canonical Raw Repair

Use this pattern when the selected `_Inbox/` item is not a new subject, but the existing canonical raw file for that subject has degraded into a placeholder, stub, or otherwise incomplete capture.

## Trigger pattern

Apply this repair when **all** are true:

1. Existing-first search shows the subject already has a durable chain (`raw/` + `wiki/`/extract/log references).
2. The supposedly canonical raw file exists, but its body is materially incomplete relative to what downstream notes claim it contains.
3. The new `_Inbox/` capture is the same source/subject and is clearly richer than the degraded canonical raw.

Typical signs:
- the canonical raw says "placeholder" or contains only a stub;
- existing wiki notes describe capabilities, sections, or metadata that are missing from the canonical raw body;
- another older raw note explicitly says it was superseded by the degraded canonical raw.

## Repair procedure

1. **Create recovery copies first.** Save a recovery copy of the current canonical raw and the `_Inbox/` recapture before editing or clearing anything.
2. **Confirm subject identity.** Verify this is the same repository/article/video/source family, not a merely similar title.
3. **Promote the richer recapture into the canonical raw path.** Replace the degraded raw body with the richer recovered source while preserving or repairing frontmatter.
4. **Add a provenance note.** State that the canonical raw was restored from a later recapture because the prior canonical file had degraded.
5. **Refresh downstream wiki/extract notes only where the richer source adds durable value.** Do not create a second parallel raw note unless provenance genuinely requires separate preservation.
6. **Log the repair explicitly** in the domain `wiki/log.md` as duplicate-recapture resolution / canonical raw repair.
7. **Clear the `_Inbox/` item only after verification** that the repaired canonical raw, downstream notes, and log entry all exist.

## Reporting rule

Report this as **duplicate-recapture repair**, not as a brand-new ingestion and not as a simple duplicate discard. The key outcome is restoration of the canonical source-of-truth chain.

## Pitfalls

- Do not throw away the richer `_Inbox/` recapture just because a canonical filename already exists.
- Do not preserve the degraded canonical raw unchanged when downstream notes depend on it as the superseding source.
- Do not create a second durable raw file when the better move is to repair the existing canonical raw path.
- Do not delete the `_Inbox/` copy before creating a recovery handle and verifying the repaired chain.
