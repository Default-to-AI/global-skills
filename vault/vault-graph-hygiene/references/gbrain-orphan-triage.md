# gbrain orphan triage on Robert's vault

Use this when a cron report or audit proposes "fix orphans" at large scale.

## Triage order

1. **Classify the orphan population before editing anything.**
   Split into:
   - genuine human vault notes
   - indexed source-repo code/config pages
   - auto-generated skill/wiki/artifact outputs
   - ghost entries with no backing `.md`

2. **Do not trust the top-line orphan count.**
   In practice a four-digit count can be mostly source-repo/code pages, not vault-note hygiene work.

3. **Verify what gbrain is actually measuring.**
   Check whether graph/backlinks are populated and whether `extract` is ingesting links at all. If `graph` returns empty `links: []` broadly or `extract` reports `0 link(s)`, Obsidian `[[wikilinks]]` may still be useful for the vault but will not move gbrain's internal orphan metric.

4. **Scope fixes to genuine human notes first.**
   Safe high-value fixes:
   - add missing frontmatter (`type`, `created`) using real git/file evidence
   - create an Obsidian MOC for real note navigation
   - ignore generated/code artifacts unless the user explicitly wants those normalized

5. **Windows case-path pitfall.**
   Do not delete apparent case-only duplicates like `Types/` vs `types/` until you verify tracked path + filesystem behavior. On Windows these may be the same canonical file.

## Durable lessons from the 2026-07-10 session

- Large gbrain orphan counts can be massively inflated by non-vault material.
- MOCs can still be worthwhile for Obsidian navigation even when gbrain does not ingest those links into its own graph.
- Frontmatter backfills on real notes are the highest-confidence, lowest-risk hygiene fix.
