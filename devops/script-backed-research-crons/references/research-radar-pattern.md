# Research Radar Pattern

## Use Case

Recurring research jobs that scan several sources, rank them, preserve the evidence, and then deliver a short Telegram brief.

## Minimal collector schema

Each candidate item should normalize to:
- `title`
- `url`
- `source`
- `published_at`
- `summary`
- `score`
- `matched_topics`
- `why_it_matters`

This makes ranking, dedupe, artifact writing, and prompt summarization straightforward.

## Artifact layout

Use a date-partitioned directory under a stable root, for example:

```text
C:/Users/Tiger/AppData/Local/hermes/research-radar/
  YYYY-MM-DD/
    ranked-signals.json
    ranked-signals.md
    unified-feed.md
```

Recommended semantics:
- `ranked-signals.json` — canonical machine-readable source of truth
- `ranked-signals.md` — quick human-readable ranked list
- `unified-feed.md` — broader evidence log across all scored items

## Stdout pattern for cron injection

The script should print only a compact digest, for example:
- artifact path
- files written
- sources checked
- total scored item count
- top 3 items with one-line relevance notes

The cron prompt should then treat that stdout and the artifacts as the primary evidence layer.

## Ranking hygiene

Useful deterministic safeguards:
- source weighting
- topic keyword scoring
- explicit noise filters for junk release tags / backup artifacts / merge markers
- light source-diversity selection so the top 3 are not all from one feed
- dedupe before final ranking

## Verification pattern

1. Run the script directly.
2. Inspect the artifact directory.
3. Open at least one `.md` and one `.json` artifact.
4. Create a one-shot local cron with the same script.
5. Trigger it and run a tick if needed.
6. Read `cron/output/<job_id>/...md` to verify the final rendered brief.
7. Only after that trust the production Telegram delivery path.

## Skill-path rule for cron jobs

If a scheduled job uses skills, prefer the fully qualified skill path when there is any chance of name collision.

Why: ambiguous short names can be tolerated in interactive work but skipped in scheduled runs, which creates misleading partial success.

## Tone rule

For Telegram briefs:
- keep sections short
- use `**bold**` section labels
- use light emojis
- avoid long paragraphs
- avoid underline-dependent formatting
