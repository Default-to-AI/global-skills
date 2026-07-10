---
name: create-brief
description: Use when ending a session or at a phase boundary to create a brief document that is both machine-parseable and human-readable. Compacts the session into grounded truths, verifies critical assumptions, suggests 3 follow-ups with one recommended.
---
# Create Brief Skill

## Overview
Creates one brief document that serves both humans (quick-read, actionable) and machines (schema-validated, parseable). Written to the canonical briefs directory. Includes verification checklist, 3 follow-up options with recommendation, and integrates with `load-brief` for session resumption.
**Note:** The term "handoff" is now referred to as "brief" in this skill and related skills.

## When to Use
- Ending a session (manual or context limit)
- Phase transition (plan→work, work→review, review→compound)
- Subagent completion
- Any point where a fresh agent/session needs to continue from exactly here
- **When to use session-brief instead**: If the session was primarily discussion, planning, or decision-making without implementation work, use the session-brief skill for a lighter-weight, conversation-focused brief.

## Core Pattern

```
1. Collect session facts (git, artifacts, decisions, blockers)
2. Verify critical assumptions (build, lint, tests, key invariants)
3. Generate brief with:
   - Machine frontmatter (schema, session_id, phase, timestamps)
   - Human sections (context, done, blockers, risks, quick-start)
   - Verification checklist (what next agent MUST verify)
   - 3 follow-up options + recommendation
4. Write to canonical briefs dir
5. Output verification message with file path
```

## Brief Document Structure

### Frontmatter (Machine)
```yaml
---
session_id: "uuid-short"
created: "ISO8601"
phase_from: "p0-remediation"
phase_to: "p1-primitives"
profile: "default"
project: "statistics"
branch: "fix/design-system-p0-remediation"
base_commit: "abf8de8"
schema_version: "1.0"
---
```

### Human Sections
1. **Project Context** — repo, branch, three-layer alignment table
2. **What Was Done** — commits, verification results, key files
3. **Current State** — objective, missing pieces, existing assets
4. **Blocking Decisions** — table with decision, context, blocking flag
5. **Risks** — table with impact/likelihood/mitigation
6. **Verification Checklist** — what next agent MUST run/verify
7. **Quick Start** — copy-paste commands
8. **Follow-ups (3 options + 1 recommended)** — structured choices

---

## Verification Checklist (Required in Every Brief)

Next agent MUST verify before proceeding:
- [ ] `npm run build` succeeds
- [ ] `npm run lint:colors` passes (0 violations)
- [ ] Git status clean on expected branch
- [ ] Key invariants hold (no hardcoded sizes, no raw slate/gray/zinc, signature elements exist)

---

## Follow-Up Format (Exactly 3 Options)

```markdown
## Follow-Up Options

### Option A (Recommended): [Title]
**Scope:** [one-line scope]
**Why:** [one-line rationale]
**First Step:** [exact command]

### Option B: [Title]
**Scope:** [one-line scope]
**Why:** [one-line rationale]
**First Step:** [exact command]

### Option C: [Title]
**Scope:** [one-line scope]
**Why:** [one-line rationale]
**First Step:** [exact command]
```

---

## Integration with load-brief

- Briefs written to `C:/Users/Tiger/AppData/Local/hermes/briefs/`
- Filename: `brief-{profile}-{project}-{phase_from}-to-{phase_to}-{timestamp}.md`
- `load-brief` reads most recent, displays, deletes, outputs verification
- This skill ensures briefs are compatible (frontmatter + markdown body)

## Usage

```bash
# From terminal or slash command
python C:/Users/Tiger/AppData/Local/hermes/skills/devops/create-brief/scripts/create_brief.py \
  --phase-from p0-remediation \
  --phase-to p1-primitives \
  --session-id stats-p0-complete-20260617
```

## Output Verification Message

```
✅ Brief created: C:/Users/Tiger/AppData/Local/hermes/briefs/brief-default-statistics-p0-remediation-to-p1-primitives-20260617-1846.md
📋 Session: stats-p0-complete-20260617 | Phase: p0-remediation → p1-primitives
🔍 Next agent must verify: npm run build && npm run lint:colors
🎯 Recommended follow-up: Option A — Build Button + Badge primitives
```

## Script Implementation

### `scripts/create_brief.py`

Collects data from:
- `git status`, `git log -1 --format`, `git branch --show-current`
- `package.json` (project name)
- Existing artifacts in project (`DESIGN.md`, `design-system-audit.md`, `ux-evaluation.md`)
- Runs verification commands (`npm run build`, `npm run lint:colors`)

Generates the complete brief document, writes to canonical dir, outputs verification message.

## Phase Transition Triggers (Absorbed 2026-06-18 from phase-handoff)

The previous `phase-handoff` skill has been consolidated into this skill. Its four
trigger conditions map directly onto `create-brief`'s existing `When to Use`:

| phase-handoff trigger | create-brief coverage |
|---|---|
| `phase-transition`     | "Phase transition (plan→work, work→review, review→compound)" — handled by `generate_brief(phase_from, phase_to, ...)` |
| `subagent-complete`    | "Subagent completion" — use this skill with `--profile` of the originating subagent |
| `cron-complete`        | Use this skill at cron job finish with a session_id like `<job>-complete-<date>` |
| `session-end`          | "Ending a session (manual or context limit)" — call this skill before closeout |

**Written brief filename pattern (unchanged):**

```
brief-{profile}-{project}-{phase_from}-to-{phase_to}-{YYYYMMDD-HHMM}.md
```

**Canonical directory:** `C:/Users/Tiger/AppData/Local/hermes/briefs/`
(loaded-and-deleted by `load-brief`, hidden from next session if absent).

For the structured-context JSON schema (`decisions_locked`, `files_changed`,
`test_results`, `open_questions`, `next_steps`, `risks`) that phase-handoff used to
require, supply it via `--context-file path/to/context.json` (extend `create_brief.py`
to consume it; until then, write the structured facts into the markdown body directly).