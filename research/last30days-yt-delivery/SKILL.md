---
name: last30days-yt-delivery
version: "2.0.0"
description: "Format /last30days YouTube results (trending videos, use-case roundups) into a clean, skimmable Discord/Telegram-ready block. Use when the last30days run surfaces a ranked YouTube video list and the user wants a polished deliverable instead of the raw 'Ranked Evidence Clusters' / 'What I learned' shape."
user-invocable: false
---

# last30days YouTube Delivery Formatter

Turns a last30days YouTube result set (the ranked video list with score + publisher + subs + views + likes + published date + URL) into a tight, scannable message. This is the DURABLE mirror of the `YOUTUBE DELIVERY MODE` addendum baked into the `last30days` SKILL.md — kept here so upstream last30days syncs (which overwrite SKILL.md) do not lose the contract.

## When to use
- User ran `/last30days <topic>` and the output is a ranked YouTube video list (e.g. "Trending Hermes Use Cases YouTube Videos").
- User says "format it", "make it clean", "deliver as a message", or pastes raw last30days text wanting a cleaned version.
- Do NOT use for GENERAL/NEWS/COMPARISON query types that need the `What I learned:` prose synthesis. This is specifically for the YouTube-videos deliverable.

## Layout contract (verified against user feedback 2026-07-10, baked into last30days SKILL.md)
1. **Intro line** — one emoji + bold summary sentence. NO `What I learned:` section. NO `Status:` section. Ever.
2. **Videos** — each as a flush-left `#` heading (NO numbering, NO indentation on the title line). Title includes a relevant emoji prefix for skimming.
3. **Under each title**, a 2-space-indented bulleted list with exactly:
   - 🏆 `Score: {final_score} (matched {m}/{n} subqueries)` — score STAYS VISIBLE as a bullet so order is self-evident WITHOUT a 1–5 counter.
   - 📺 `{Publisher} · {subs} subs · {views} views`
   - 💡 `{description / why-it-matters, trimmed}`
   - 🔗 `{url}`
4. **Drop** likes and published date (user explicitly removed them).
5. **Source files** at the end:
   - 📂 **Source Files**
   - list the engine outputs from `LAST30DAYS_MEMORY_DIR`:
     - `{slug}-raw-vN.md` — the actual file the engine writes (e.g. `hermes-agent-use-cases-raw-v3.md`). `N` increments per suffix/date collision.
     - `latest.md` — NOT written by the engine. It is Robert's separate archival step (copy of the newest raw). Do NOT claim the engine created it.

## Save path — FINAL (Robert, 2026-07-10)
Authoritative save dir for this topic:
`C:\Users\Tiger\Agents\Docs-and-Research\Last30Days\yt-hermes-use-cases`
Raw file: `hermes-agent-use-cases-raw-v3.md` (already exists in that dir).
The engine default `~/Documents/Last30Days` is WRONG for this user. Invoke with:
`LAST30DAYS_MEMORY_DIR="C:/Users/Tiger/Agents/Docs-and-Research/Last30Days/yt-hermes-use-cases" python3 scripts/last30days.py "<topic>" --emit compact …`
The directory exists and already holds `hermes-agent-use-cases-raw-v3.md`. Always verify the path exists before claiming files were saved.
`latest.md` does NOT exist yet — it will be created after the FIRST run (copy of the newest raw). Before that first run, do NOT reference `latest.md`.

## Execution Mode block (ADD TO END OF EVERY OUTPUT)
After the Source Files section, append an `## Execution Mode` block:
- If the run was driven by the **Agent** (a reasoning model generated the plan via `--plan` and the rerank):
  `⚙️ **Execution Mode:** Agent — planned + reranked by {model}` (model = the active reasoning model, e.g. `tencent/hy3:free`).
- If **Script Only** (no LLM/API key; engine used its deterministic fallback planner + ranker):
  `⚙️ **Execution Mode:** Script Only — LLM planner/rerank unavailable.`
  and append the failure detail:
  `⚠️ Attempted provider: {LAST30DAYS_REASONING_PROVIDER or 'default internal'} — {exact stderr/error from engine, e.g. "No --plan and no LLM provider configured. Using deterministic fallback..."}`

This tells the user at a glance whether the ranking came from a reasoning model or the script's deterministic floor.

## Platform delivery (CRITICAL — do this, don't just link)
- **Discord / Telegram: ATTACH the files, do NOT emit `file://` links.** `file://` links are blocked inside the Discord app and Telegram — they will NOT open File Explorer. When the deliverable lands in a Discord channel, attach `latest.md` + the raw file as message attachments via the discord tool (or the Hermes attachment path). On Telegram, send the files as document attachments.
- **Markdown viewers (Obsidian / Notebooks / LM Studio):** `file://` links ARE clickable there. For those hosts only, you may render `📄 [latest.md](file://{LAST30DAYS_MEMORY_DIR}/latest.md)`.
- **If the source files do not exist on disk:** say so honestly. Do NOT fabricate clickable links or attachments to nonexistent paths.

## Example output (exact shape)
```
🎬 **Top 5 Trending Hermes Agent YouTube Videos** — Last 30 Days

Quick read on what's climbing for Hermes use cases. Five made the cut, ranked by traction score.

# 🖥️ Hermes Agent Desktop: Full Setup + Real Use Cases
  - 🏆 Score: 64 (matched 1/3 subqueries)
  - 📺 Greg Isenberg · 666,000 subs · 124,213 views
  - 💡 Desktop app just dropped — how to actually make money & get productive with Hermes desktop + agents.
  - 🔗 https://www.youtube.com/watch?v=EJm8Ka-gVOc

# ⏱️ Hermes Agent Use Cases That Actually SAVE You Time
  - 🏆 Score: 46 (matched 1/3 subqueries)
  - 📺 Hostinger Academy · 367,000 subs · 3,871 views
  - 💡 3 use cases no other AI agent can pull off. Code APP10 for 10% off.
  - 🔗 https://www.youtube.com/watch?v=YZAPEx5aqsc

# 💪 5 POWERFUL Hermes Agent Use Cases!
  - 🏆 Score: 45 (matched 1/3 subqueries)
  - 📺 Julian Goldie SEO · 406,000 subs · 2,945 views
  - 💡 Five high-impact Hermes agent workflows.
  - 🔗 https://www.youtube.com/watch?v=XRLjaIUNj9Q

# 🔥 6 Insane Hermes Agent Use Cases That You Need Right Now
  - 🏆 Score: 43 (matched 1/3 subqueries)
  - 📺 AI LABS · 139,000 subs · 32,224 views
  - 💡 What Hermes can really do — the ones most people miss.
  - 🔗 https://www.youtube.com/watch?v=qMEm1bgxnUM

# 🤯 7 Mind-Blowing Use Cases for Hermes Agent
  - 🏆 Score: 42 (matched 1/3 subqueries)
  - 📺 Rick Mulready · 115,000 subs · 37,153 views
  - 💡 Build a human-first, AI-powered operating system for your business.
  - 🔗 https://www.youtube.com/watch?v=JZWJzSSHYqU

📂 **Source Files**
- 📄 latest.md
- 📄 hermes-agent-use-cases-raw-v3.md
```
(In Discord/Telegram: attach those two files instead of listing them as links.)

## How the last30days score works (so you can explain it)
The `score N` in the raw output is `final_score`, produced by `scripts/lib/rerank.py`. It is NOT a simple view/like count.
- **Pipeline:** each source (YouTube, Reddit, X, etc.) emits candidates with a per-source `relevance` in [0,1] (blend of result-rank position, token overlap with the query, and an engagement boost via `log1p(likes+views)/40`, capped at 0.2). `fusion.py` does weighted reciprocal-rank fusion across the run's paraphrased subqueries. `cluster.py` groups candidates by entity overlap; a cluster's score = the max `final_score` of its members.
- **Rerank (`rerank.py`):** an LLM scores each candidate's relevance on a ~0–100 scale, then penalties/floors apply:
  - `ENTITY_MISS_PENALTY = 25` — off-topic (doesn't name the entity) gets demoted hard.
  - `FIRST_PARTY_AUTHOR_CREDIT = 5` — a resolved handle's own post gets a small lift.
  - `RESCUE_FLOOR_MAX = 40` — high-engagement on-topic posts can't be fully zeroed.
  - `INTERACTION_FLOOR = 35` — first-party replies/@mentions survive into the visible band.
  - `FIRST_PARTY_FLOOR = 25` — first-party posts clear the zero band.
- **The `(m/n)` after the score** = query-coverage indicator: this cluster's representative matched `m` of the `n` paraphrased subqueries the planner generated for the topic (planner fans out into 2–5 subqueries depending on intent; `use cases` style topics get ~3–5). Higher fraction = broader match across the topic's paraphrase fanout.
- **Bottom line:** score rewards on-topic, high-engagement, multi-source evidence. A 64 (Greg Isenberg) beat a 42 (Rick Mulready) because of combined relevance + engagement + broader subquery coverage, not raw view count alone.

## Pitfalls
- Never re-introduce "What I learned:" or "Status:" sections — user deleted them.
- Never number the titles (`# 1. ...` is wrong; use bare `# Title`).
- Never put the title on an indented line — flush-left `#`.
- Never drop the score bullet — keep order self-evident without a visible counter.
- Don't invent file paths. If `~/Documents/Last30Days` doesn't exist, say the links are illustrative and the files must be generated by an actual run.
- In Discord/Telegram: ATTACH source files, never `file://` link them.
