# Cron report schema for Robert

Use this when normalizing Telegram-delivered cron messages.

## Goal

Make every recurring report scannable on mobile and immediately actionable.
The user should not need to infer the schema from prose.

## Canonical shape

1. **Status line**
   - exactly one bold line
   - format: `**<emoji> <job name> — <status>**`
   - statuses: `OK`, `ATTENTION`, `FAILED`

2. **Summary line**
   - one plain sentence
   - answer: what happened and whether action is needed

3. **Findings**
   - 1-5 bullets max
   - each bullet = one finding only
   - preferred bullet shape:
     - `<scope>: <fact>. <required action or 'No action needed.'>`

4. **Action block**
   - include only when action is needed
   - label: `**Action:**`
   - one bullet with the single recommended next move

5. **Meta block**
   - include only when useful
   - label: `**Meta:**`
   - short bullets such as `Delivered to`, `Checked window`, `Artifact path`

## Hard rules

- Do not dump raw script structure into Telegram.
- Do not explain the workflow when the user asked for the report result.
- Do not present multiple recommendations unless the user explicitly asked for options.
- Do not rely on section names like `Dependency notes`, `Problems`, `Fix`, `Next steps` unless they actually contain content.
- Empty sections are forbidden.
- If the user asks `what are you suggesting`, answer with a single recommended action sentence first.

## Good minimal example

**🔴 Weekly Docs Drift Detection — FAILED**
Found 5 user-facing doc gaps in upstream `NousResearch/hermes-agent`; action is needed.

- PR #54851: `tools/browser_tool.py` changed without `docs/reference/tools-reference.md` update. Follow up upstream.
- PR #54843: web extract/config behavior changed without docs update in 3 files. Follow up upstream.
- PR #54766: browser tool behavior changed without docs update. Follow up upstream.

**Action:**
- Sync the listed documentation files with upstream behavior and submit a PR or local patch set.

## Good no-action example

**🟢 Daily Hermes Backup — OK**
Backup finished successfully; no action needed.

- Backup repo: updated and pushed.
- Retention check: passed.
- Last run: 03:01 Asia/Jerusalem.

## Translation rule

If the collector emits JSON, tables, or verbose markdown, the cron prompt must translate it into this schema before delivery. Do not make the user reverse-engineer the structure from raw output.
