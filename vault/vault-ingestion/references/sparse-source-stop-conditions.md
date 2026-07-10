# Sparse / Invalid Source Stop Conditions

Use this when the selected inbox file exists but the body is too thin, malformed, or misleading to support a real ingest.

## Trigger

Apply this check when any of the following is true:
- the file body is only a fragment, stub, or one-line note;
- the title/frontmatter implies a rich source, but the body does not contain that source;
- searches only find loosely related material that shares a keyword from the title;
- continuing would require guessing the intended source from adjacent vault context.

## Required handling

1. **Trust the body over the filename.** A descriptive filename is not evidence that the source payload is present.
2. **Stop ingestion before domain-wide speculative search.** Do not fan out into broad searches just because a title fragment matches existing notes.
3. **Classify the blocker explicitly** in the report: truncated capture, wrong file, placeholder note, or insufficient source payload.
4. **Do not create raw/wiki/log artifacts** from the sparse file alone.
5. **Offer the next safe move**: inspect the next inbox item, ask Robert for the intended source, or wait for a fuller capture.

## Anti-pattern

Bad recovery pattern:
- selected file body is a single sentence;
- agent searches the vault for title words like "daily Hermes";
- agent starts reasoning from neighboring notes/videos as if they were the selected source.

Correct pattern:
- verify the selected file really lacks the source;
- record that the ingest is blocked on source quality;
- stop cleanly instead of manufacturing provenance from nearby materials.
