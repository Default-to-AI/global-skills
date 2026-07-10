# Slash Command Collision — Reproduction & Fix (2026-06-18)

## Symptom
`/requesting-code-review` failed with "not a quick/plugin/skill command" in Hermes Desktop (gateway), despite skill being installed and enabled (`hermes skills list` shows it).

## Root Cause
Three skills had identical frontmatter `name: requesting-code-review`:

| Directory | Frontmatter `name:` |
|-----------|---------------------|
| `skills/software-development/requesting-code-review/` | `requesting-code-review` |
| `skills/software-development/superpowers-requesting-code-review/` | `requesting-code-review` |
| `shared-skills/software-development/requesting-code-review/` | `requesting-code-review` |

The scanner in `agent/skill_commands.py:scan_skill_commands()` deduplicates by `seen_names` set, but **filesystem iteration order is non-deterministic**. CLI and gateway processes saw different orders → registered different skills for the same `/requesting-code-review` command.

## Diagnosis
```bash
# Find duplicate frontmatter names
grep -r "^name:" shared-skills/*/SKILL.md skills/*/SKILL.md | \
  sed 's/.*name: *//' | sort | uniq -d
```

## Fix Applied
1. **Renamed** `superpowers-requesting-code-review` skill's frontmatter name to match its directory:
   ```yaml
   name: superpowers-requesting-code-review
   ```
2. **Removed** the local duplicate (`skills/software-development/requesting-code-review/`), keeping `shared-skills/` as canonical
3. **Restarted gateway** (`hermes gateway restart`) — required because gateway caches skill commands at startup
4. **Fresh session in Desktop** (`/new`) — fetches updated command map from gateway

## Verification
After fix, `/requesting-code-review` in Desktop works, and CLI chat also resolves correctly.

## Prevention
- Run audit script regularly (detects duplicate frontmatter names)
- Ensure directory name == frontmatter `name:` for all skills
- When adding `superpowers-*` skills, always rename frontmatter `name:` to include the prefix