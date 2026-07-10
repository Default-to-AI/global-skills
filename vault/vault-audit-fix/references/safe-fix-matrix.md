# Vault Audit Safe-Fix Matrix

## Safe to fix without approval

- Broken wikilink casing/path when exactly one intended target exists.
- Example wikilinks in prose that should be code/plain text and have no real target.
- Malformed frontmatter syntax where the correct value is obvious from file location or content.
- Missing canonical domain frontmatter when file location determines the domain.
- Stale generated index when the live script supports deterministic regeneration.
- Missing log entry for an operation the current agent just performed.
- Audit issues introduced by the current agent's own edits.

## Report for Robert approval

- Delete durable notes or raw captures.
- Merge duplicate notes.
- Rename durable wiki pages.
- Change `Types/`.
- Create new domains or change domain taxonomy.
- Bulk rewrite many files.
- Modify source/raw body content beyond metadata or format repair.
- Resolve ambiguous domain placement.
- Resolve duplicate candidates with materially different source evidence.

## Report as blocked / needs investigation

- Audit script missing or failing due to environment/toolchain issues.
- Conflicting standards between live files.
- Broken link target cannot be inferred.
- File appears intentionally experimental or temporary.
