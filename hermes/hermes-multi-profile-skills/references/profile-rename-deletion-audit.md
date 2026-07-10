# Profile Rename / Deletion Audit Checklist

Use when Robert wants to delete an old Hermes profile after renaming or replacing it with another profile.

## Goal

Confirm the replacement profile can serve the old profile's role without losing durable operating context, profile-local procedures, or important state.

## Compare before deletion

1. **Profile registration and aliases**
   - Run `hermes profile list` and `hermes profile show <old>` / `<new>`.
   - Check wrapper aliases. If the old profile has an alias, either remove it or repoint it:
     - `hermes profile alias <old> --remove`
     - `hermes profile alias <new> --name <old-alias>`

2. **Normalized core files**
   - Compare `profile.yaml`, `config.yaml`, `SOUL.md`, `AGENTS.md`, `README.md`, `.env`, `shell-hooks-allowlist.json`, and `cron/jobs.json`.
   - Normalize expected path/name changes first, e.g. `profiles/vault` → `profiles/librarian`.
   - Treat path rewrites in `terminal.cwd` and hook commands as expected, not discrepancies.

3. **Hooks and guardrails**
   - Ensure hook files exist in the new profile and are equivalent after path normalization.
   - Ensure `config.yaml` hook commands point at the new profile path.
   - If `AGENTS.md` references guard/precommit scripts, verify those scripts exist in the new profile too.

4. **Skills**
   - Confirm class-level local skills needed for the role are present and enabled in the new profile.
   - For Vault/Librarian, verify the focused Obsidian suite: `vault-umbrella`, `vault-ingestion`, `vault-retrieval`, `vault-audit-fix`, `vault-graph-hygiene`, `vault-cron-ingestion`, `vault-compounding-loop`, `vault-external-workflow-evaluation`, and `vault-guardrails`.
   - Compare old profile-local `skills` or `skills.bak` against the new profile, but distinguish historical backups from active skills.

5. **Durable memories and sessions**
   - Check `memories/USER.md` and `memories/MEMORY.md`. These may contain durable user/profile operating rules that are not in config.
   - Compare `state.db` size and counts for `sessions` / `messages` if transcript recall matters. Export or preserve the old DB if needed.

6. **Cron, scripts, templates, runtime**
   - Empty `cron/jobs.json` in both profiles is safe; non-empty jobs need migration or explicit retirement.
   - Copy or intentionally retire profile-local `scripts/`, `templates/`, and `runtime/` directories. Do not assume they are cache just because they are outside config.
   - For Vault/Librarian, `vault-health-check.py`, `_stale_guard.py`, and `_precommit_guard.py` are important if referenced by docs or cron patterns.

7. **Auth and provider coverage**
   - Compare `auth.json` structurally without printing secrets: provider names and credential-pool provider names are enough.
   - Missing extra provider pools may be acceptable if the replacement profile's configured provider works, but call out the loss before deletion.

8. **Gateway/channel state**
   - `gateway_state.json` can be stale; verify with `hermes profile list` rather than trusting the file.
   - `channel_directory.json` with empty platform lists is usually non-critical, but non-empty routes should be migrated or exported.

9. **Project/vault working tree equivalence**
   - For profile-owned repos, compare `git status --short --branch`, `rev-parse HEAD`, tracked file counts, and untracked/modified counts.
   - Clean working trees at the same commit and remote are strong evidence the content itself is migrated.

## Deletion readiness wording

Use a two-part verdict:

- **Can the new profile serve the role?** yes/no based on config, skills, hooks, and working tree.
- **Is deletion safe right now?** yes/no based on whether memories, session DB, scripts, auth coverage, aliases, and state have been migrated or intentionally discarded.

Do not delete in the same audit unless Robert explicitly asks for deletion after seeing the discrepancies.