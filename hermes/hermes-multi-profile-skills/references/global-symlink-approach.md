# Global Symlink Approach for Shared Skills

## Session Context
**Date:** June 21, 2026  
**Trigger:** User requested consolidating shared-skills into Agent-Skills as the single global skills directory for all agents (Hermes, Codex, Gemini, etc.)  
**Problem:** Previous configuration used both a symlink (`skills -> Agent-Skills`) AND `external_dirs: shared-skills`, causing skill loading ambiguity and duplication.

## Architecture Discovered
- Global skills directory: `~/.hermes/skills/` (symlink → `/c/Users/Tiger/Agents/Agent-Skills/`)
- Profile skills: `~/.hermes/profiles/<name>/skills/` (for overrides)
- Discovery order: local dir → global dir → `external_dirs` (when configured)
- `external_dirs` was configured to point to `shared-skills` (now removed)

## Solution Implemented
1. Established canonical skills directory: `/c/Users/Tiger/Agents/Agent-Skills/`
2. Set global skills symlink: `~/.hermes/skills/` → `/c/Users/Tiger/Agents/Agent-Skills/`
3. Removed `shared-skills` directory (content merged into Agent-Skills)
4. Cleared `skills.external_dirs` in config.yaml (set to empty array)
5. Preserved profile-specific override capability

## Commands Executed
```bash
# 1. Ensure Agent-Skills exists as canonical directory
mkdir -p /c/Users/Tiger/Agents/Agent-Skills

# 2. Set up global skills symlink (if not already present)
ln -sf /c/Users/Tiger/Agents/Agent-Skills /c/Users/Tiger/AppData/Local/hermes/skills

# 3. Merge shared-skills content into Agent-Skills (preserving existing files)
#    (Done via file copy operations - see session history for details)

# 4. Remove obsolete shared-skills directory
rm -rf /c/Users/Tiger/AppData/Local/hermes/shared-skills

# 5. Update config.yaml to clear external_dirs
#    (Changed external_dirs: [\"C:/Users/Tiger/AppData/Local/hermes/shared-skills\"] to external_dirs: [])

# 6. Verify configuration
hermes config get skills.external_dirs  # Should show []
ls -la /c/Users/Tiger/AppData/Local/hermes/skills  # Should show symlink to Agent-Skills
```

## Verification Results
- All Hermes profiles (vault, engineer, reviewer, strategist, writer) see identical skill sets
- Skill loading is unambiguous (no duplicate skill names)
- Profile-specific overrides still work (skills in `profiles/<name>/skills/` take precedence)
- Hermes slash commands (like `/skills`) display correct, deduplicated skill lists

## Profile Config Locations Updated
- `~/.hermes/profiles/<name>/config.yaml` for all profiles
- Each now contains: `skills.external_dirs: []` (empty array)

## Ongoing Maintenance
- **Add new skill:** Use `hermes skills install/update` from any profile (writes to global skills dir)
- **Update skill:** Modify in `/c/Users/Tiger/Agents/Agent-Skills/` (the canonical location)
- **Profile-specific override:** Place skill in `profiles/<name>/skills/` — takes precedence over global
- **Verify symlink:** `ls -la ~/.hermes/skills` should point to `/c/Users/Tiger/Agents/Agent-Skills`

## Advantages Over Previous Approach
- Eliminates skill loading ambiguity (no duplicate skill sources)
- Simpler configuration (no per-profile external_dirs to manage)
- Works consistently across all agents that use the same skills directory format
- Preserves ability for profile-specific customizations
- Single point of truth for global skills

## Related Reference
- See `shared-skills-setup.md` for the previous `external_dirs`-based approach