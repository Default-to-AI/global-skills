# Canonical Vault Ingestion Flow

1. Verify the selected input or queue item exists and is the intended source.
2. Read live vault source-of-truth files before structural decisions.
3. Determine the target domain from existing vault domains only.
4. Run existing-first checks across `_Inbox/`, target `raw/`, target `wiki/`, target `outputs/`, and related domains.
5. Validate source frontmatter against actual content.
6. Preserve the source in the target domain `raw/` location if it is source material.
7. Rewrite the title per vault standards: descriptive, non-clickbait, content-based.
8. Create or update durable `wiki/` notes and extracts as appropriate.
9. Separate extracted facts, inferred synthesis, and ambiguous or conflicting claims where useful.
10. Add wikilinks only to real existing targets, or create needed durable targets when justified by the source and live rules.
11. Update target domain `wiki/index.md` when the new material belongs in the domain map.
12. Append a target domain `wiki/log.md` entry.
13. Run `vault-audit-fix`.
14. Produce the post-ingestion report.
15. If Robert is present, continue into discussion and Q&A.
