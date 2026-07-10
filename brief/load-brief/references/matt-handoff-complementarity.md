# Load Latest Handoff — Complementarity with Matt-Handoff

**Source Session:** northstar-2.0 statistics calculator (2026-06-17)
**Updated:** 2026-06-18 — phase-handoff removed; unified-handoff is the canonical handoff writer.

---

## Purpose

This skill (`load-latest-handoff`) and the `matt-handoff` skill serve complementary roles in the dual handoff pattern:

| Skill | Audience | Trigger | Output |
|-------|----------|---------|--------|
| `load-latest-handoff` | Machine/Subagent | Session start | Reads + deletes latest unified-handoff |
| `matt-handoff` | Human | Session end | Writes human-readable handoff to temp |

---

## Workflow Integration

### At Session Start (Machine → Human)
```bash
# Human loads the matt-handoff manually
cat C:/Users/Tiger/AppData/Local/Temp/statistics-handoff-p1-primitives-20260617-1846.md

# OR machine loads the unified-handoff
python C:/Users/Tiger/AppData/Local/hermes/skills/devops/load-latest-handoff/scripts/load_latest_handoff.py
```

### At Session End (Human → Machine)
```bash
# Human creates matt-handoff for next human
# (via matt-handoff skill)

# Machine creates unified-handoff for next machine
# (via unified-handoff skill + unified_handoff.py)
```

---

## Complementarity Rules

1. **Never both at once** — One session uses one or the other
2. **Unified-handoff is source of truth** — Validated, canonical, parseable
3. **Matt-handoff is human interface** — Scannable, skill-aware, actionable
4. **Unified-handoff consumed by this skill** — Deleted after load (exactly once)
5. **Matt-handoff persists** — Read by human, not auto-deleted

---

## Session Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ SESSION N                                                   │
│   ├─ Load: matt-handoff (human) OR load-latest-handoff (machine)   │
│   ├─ Work...                                                  │
│   ├─ End: Create matt-handoff (for human)                     │
│   └─ End: Create unified-handoff (for machine)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ SESSION N+1                                                 │
│   ├─ Load: matt-handoff (human) OR load-latest-handoff (machine)   │
│   └─ ...                                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Insight from Northstar-2.0 Session

The `load-latest-handoff` skill was tested and **worked correctly**:
- Found latest unified-handoff by mtime
- Displayed full content with metadata (session_id, trigger, phase)
- **Deleted the file after successful display**
- Output verification: `✅ Loaded and deleted: <path> (created <timestamp>) — internalized, no longer on disk.`

This confirms the "consume once" contract works.

---

## When to Use Which

| Scenario | Use |
|----------|-----|
| Subagent completion | Unified-handoff + `unified_handoff.py` |
| Cron job finish | Unified-handoff + `unified_handoff.py` |
| Phase gate (plan→work, etc.) | Unified-handoff + `unified_handoff.py` |
| Human session end | Matt-handoff skill |
| Human session start (manual) | Read matt-handoff from temp |
| Machine session start (auto) | `load-latest-handoff` skill |

---

## Implementation Notes

- **Unified-handoff directory:** `C:/Users/Tiger/AppData/Local/hermes/handoffs/` (canonical, hardcoded in unified_handoff.py)
- **Matt-handoff directory:** `%TEMP%` (ephemeral, human-only)
- **This skill's script:** `C:/Users/Tiger/AppData/Local/hermes/skills/devops/load-latest-handoff/scripts/load_latest_handoff.py`
- **Matt-handoff skill:** `matt-handoff` (built-in)

---

## Session Example: Northstar-2.0 (2026-06-17)

| Handoff | File | Consumer |
|---------|------|----------|
| Unified-handoff | `handoffs/handoff-default-statistics-northstar2-p0-remediation-to-p1-primitives-20260617-1809.md` | `load-latest-handoff` (deleted) |
| Matt-handoff | `%TEMP%/statistics-handoff-p1-primitives-20260617-1846.md` | Human at session start |