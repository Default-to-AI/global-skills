# Channel Digest Formatting

Use this reference when a recurring research cron is delivered directly into a chat channel and the user cares more about legibility than analysis.

## Rule of thumb

The channel message is a product surface, not an operator console.

Keep these out of the delivered message unless explicitly requested:
- scheduler status
- engine version notes
- artifact paths
- internal planner commentary
- debug warnings that do not change the visible output

Put that material in saved artifacts instead.

## Minimal watchlist schema

When the user asks for a simple monitoring feed, treat the requested fields as a fixed schema.

Example: YouTube trending videos
- title as the clickable link
- creator / channel
- views
- likes if available
- no prose summary unless requested

Example layout:

```md
📺 **YouTube — Hermes Agent (last 72h)** · 4 videos

**1. [Video title](https://youtube.com/watch?v=...)**
   👤 Channel Name · 👁 12.4K · 👍 850

**2. [Another title](https://youtube.com/watch?v=...)**
   👤 Another Channel · 👁 8.1K · 👍 420
```

## Field discipline

If the user says "only give me the links, creator, views, likes" then do not add:
- source commentary
- ranking rationale
- long explanation of why an item matters
- cross-source synthesis
- action recommendations

## Delivery split

Use a two-layer output model:
1. durable artifact for operators and debugging
2. compact channel digest for the human reader

Do not collapse both layers into one noisy post.
