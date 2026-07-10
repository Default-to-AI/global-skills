# Reference: Clone Profile with Vault Symlink (vault → librarian)

Session: 2026-06-19 — Created `librarian` profile from `vault` template with symlinked Vault folder and Agent-Skills.

## Source Profile
- Path: `C:\Users\Tiger\AppData\Local\hermes\profiles\vault`
- Key files: config.yaml (17KB), SOUL.md, hooks/ (3 Python guardrails), AGENTS.md, profile.yaml, README.md, .env, shell-hooks-allowlist.json
- State files SKIPPED: state.db (56MB), models_dev_cache.json, .skills_prompt_snapshot.json, audio_cache/, image_cache/, cost-snapshots/, logs/, sessions/, memories/, cron/, checkpoints/, pairing/, runtime/, webui_state/, templates/, scripts/, sandboxes/, lsp/

## Target Profile
- Path: `C:\Users\Tiger\AppData\Local\hermes\profiles\librarian`

## Commands Executed

```bash
# 1. Create profile directory
mkdir -p /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/hooks

# 2. Copy essential files (selective)
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/config.yaml      /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/SOUL.md         /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/hooks/*.py      /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/hooks/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/AGENTS.md       /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/profile.yaml    /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/README.md       /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/.env            /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/
cp /c/Users/Tiger/AppData/Local/hermes/profiles/vault/shell-hooks-allowlist.json /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/

# 3. Bulk path replacement in config.yaml
sed -i 's|C:\\\\\\\\Users\\\\\\\\Tiger\\\\\\\\AppData\\\\\\\\Local\\\\\\\\hermes\\\\\\\\profiles\\\\\\\\vault|C:\\\\\\\\Users\\\\\\\\Tiger\\\\\\\\AppData\\\\\\\\Local\\\\\\\\hermes\\\\\\\\profiles\\\\\\\\librarian|g' config.yaml
sed -i 's|profiles/vault/hooks|profiles/librarian/hooks|g' config.yaml

# 4. Update SOUL.md
sed -i 's/^# Profile: Vault$/# Profile: Librarian/' SOUL.md
sed -i 's/^\\\\- \\\\*\\\\*Role\\\\*\\\\*: Vault \\\\/ Librarian$/- **Role**: Librarian/' SOUL.md

# 5. Update profile.yaml description (replace "vault" with "librarian" in description)
sed -i 's/vault tasks/librarian tasks/' profile.yaml

# 6. Symlink Vault (Obsidian vault at C:\Users\Tiger\Vault)
rm -rf /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/vault   # auto-created dir
ln -sf /c/Users/Tiger/Vault /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/Vault

# 7. Symlink skills (shared Agent-Skills)
rmdir /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/skills   # auto-created dir
ln -sf /c/Users/Tiger/Agents/Agent-Skills /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/skills

# 8. Symlink obsidian vault skills (from vault profile's backup)
rm -rf /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/skills/obsidian
ln -sf /c/Users/Tiger/AppData/Local/hermes/profiles/vault/skills.bak/obsidian /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/skills/obsidian

# 9. Initialize empty cron jobs.json
echo '{"jobs": [], "updated_at": "'$(date -Iseconds)'"}' > /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/cron/jobs.json

# 10. Fix shell-hooks-allowlist.json hook paths
sed -i 's|profiles/vault/hooks|profiles/librarian/hooks|g' shell-hooks-allowlist.json

# 11. Verify
grep "cwd:" config.yaml                    # → librarian
grep "hooks" config.yaml                   # → librarian/hooks
readlink /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/Vault   # → /c/Users/Tiger/Vault
ls -la /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/skills   # → Agent-Skills contents
cat /c/Users/Tiger/AppData/Local/hermes/profiles/librarian/cron/jobs.json  # empty jobs
```

## Hook Files Copied
- `vault_never_do_guardrail.py` — blocks destructive ops
- `vault_ask_first_guardrail.py` — requires confirmation for vault writes
- `vault_guardrail_common.py` — shared utilities (not directly registered in config)

## Config Keys Updated
| Key | Before | After |
|-----|--------|-------|
| `terminal.cwd` | `...\\profiles\\vault` | `...\\profiles\\librarian` |
| `hooks.pre_tool_call[0].command` | `...\\profiles\\vault\\hooks\\...` | `...\\profiles\\librarian\\hooks\\...` |
| `hooks.pre_tool_call[1].command` | `...\\profiles\\vault\\hooks\\...` | `...\\profiles\\librarian\\hooks\\...` |

## Time Saved
- Full `cp -r` timed out at 180s (state.db 56MB)
- Selective copy + sed + symlinks: ~30s total

## Post-Creation Verification Checklist
- [ ] `config.yaml` cwd points to new profile
- [ ] `config.yaml` hook paths point to new profile hooks/
- [ ] `SOUL.md` has correct profile name and role
- [ ] `profile.yaml` description updated
- [ ] `shell-hooks-allowlist.json` hook paths updated
- [ ] `Vault/` symlink → `/c/Users/Tiger/Vault`
- [ ] `skills/` symlink → `/c/Users/Tiger/Agents/Agent-Skills`
- [ ] `skills/obsidian/` symlink → vault profile's skills.bak/obsidian (9 vault skills)
- [ ] `cron/jobs.json` exists and is empty
- [ ] No stale `profiles/vault` references in new profile files