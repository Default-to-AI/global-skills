# Shared Skills Setup — Session Transcript & Verification

## Session Context
**Date:** June 6, 2026
**Profile:** vault
**Trigger:** User reported friction — updating a skill in vault profile didn't sync to engineer/reviewer/strategist/writer profiles.

## Architecture Discovered
- Each profile: `~/.hermes/profiles/<name>/skills/`
- Global: `~/.hermes/skills/` (symlink → `/c/Users/Tiger/AI Hub/Global Skills/`)
- Discovery order (skill_commands.py:278-282): local dir → `external_dirs`
- No auto-sync mechanism exists in Hermes core

## Solution Implemented
1. Created canonical: `/c/Users/Tiger/AppData/Local/hermes/shared-skills/`
2. Populated from global skills
3. Configured each profile's `skills.external_dirs: ["shared-skills"]`
4. Verified all profiles list identical skills

## Commands Run (Reproducible)
```bash
# 1. Create canonical shared skills directory
mkdir -p /c/Users/Tiger/AppData/Local/hermes/shared-skills
cp -r "/c/Users/Tiger/AI Hub/Global Skills/"* /c/Users/Tiger/AppData/Local/hermes/shared-skills/

# 2. Configure each profile (run from any profile or default)
hermes config set skills.external_dirs '["shared-skills"]' --profile vault
hermes config set skills.external_dirs '["shared-skills"]' --profile engineer
hermes config set skills.external_dirs '["shared-skills"]' --profile reviewer
hermes config set skills.external_dirs '["shared-skills"]' --profile strategist
hermes config set skills.external_dirs '["shared-skills"]' --profile writer

# 3. Verify
for p in vault engineer reviewer strategist writer; do
  echo "=== $p ==="
  hermes skills list --profile $p | head -20
done
```

## Verification Results
All 5 profiles now show identical skill lists sourced from `shared-skills/`.

## Profile Config Locations Updated
- `~/.hermes/profiles/vault/config.yaml`
- `~/.hermes/profiles/engineer/config.yaml`
- `~/.hermes/profiles/reviewer/config.yaml`
- `~/.hermes/profiles/strategist/config.yaml`
- `~/.hermes/profiles/writer/config.yaml`

Each now contains:
```yaml
skills:
  external_dirs:
    - "shared-skills"
```

## Ongoing Maintenance
- **Add new skill:** `hermes skills install <id> --profile default` (writes to global, then copy to shared-skills) OR write directly to `shared-skills/`
- **Update skill:** Edit in `shared-skills/`, all profiles see it on next `/reload-skills`
- **Profile-specific override:** Place in `profiles/<name>/skills/` — takes precedence
- **Disable in one profile:** `hermes skills config disable <skill> --profile <name>`