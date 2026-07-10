# Skill Audit Architecture

## Data Flow

```
shared-skills/ (canonical)
    |
    |-- external_dirs in config.yaml
    v
Profile skills/ (shadow copy via external_dirs)
    |
    |-- Profile local skills/ (overrides, additions)
    v
skills_list tool / hermes skills list
    |
    v
CLI / /skill-name dispatch
```

## Key Files

| File | Purpose |
|------|---------|
| `shared-skills/*/SKILL.md` | Canonical source of truth |
| `profiles/*/config.yaml` | `skills.external_dirs` points to shared-skills |
| `profiles/*/skills/` | Local overrides (same frontmatter name = override) |
| `scripts/skill-audit-collector.py` | Cron job - audits drift |

## Identity Resolution

1. **Discovery**: `skills_list` tool scans `SKILLS_DIR` + `external_dirs` via `_find_all_skills()`
2. **Deduplication**: First occurrence wins (local dir scanned first, then external dirs)
3. **Frontmatter `name:`**: Used as the canonical key for CLI, slash commands, tool dispatch
4. **Directory name**: Irrelevant to runtime; only matters for audit diffs

## Platform Filtering

`skill_matches_platform(frontmatter)` filters at discovery time:
- `platforms: [macos]` -> hidden on Windows/Linux
- `platforms: [linux, windows]` -> hidden on macOS
- No `platforms` field -> visible everywhere

This happens inside `_find_all_skills()` before `skills` list is returned. Platform-filtered skills are **not** in the CLI output - this is correct behavior, not a bug.

## Duplicate Handling

When two directories have the same frontmatter `name:`:
- First one scanned wins (local before external; alphabetical within dir)
- Second is silently skipped (see `seen_names` set in `_find_all_skills`)
- Audit script must detect this by comparing directory names for same frontmatter name

## Common Failure Modes

| Failure | Detection | Resolution |
|---------|-----------|------------|
| Dir name != frontmatter name | `name_mismatches` in audit | Rename directory |
| Duplicate frontmatter names | `len(skills) < len(dirs)` | Delete one directory |
| Missing from CLI but in shared | `shared_skills_missing_from_cli` | Check platform filter; fix audit parsing |
| Profile missing shared skill | `extra_in_cli` has shared skills | Verify `external_dirs` config |