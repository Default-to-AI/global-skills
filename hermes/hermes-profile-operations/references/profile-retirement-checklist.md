# Profile Retirement Checklist

Use this reference when discontinuing one Hermes profile after another profile has inherited its role.

## Preflight

- Confirm successor profile exists and `hermes profile show <successor>` works.
- Confirm old profile exists and is stopped.
- Identify whether shared resources are symlinks/junctions (`skills`, `Vault`, other large trees). Preserve the same link style in the successor.
- Prefer simple filesystem copy/move backups over a full `hermes profile export` if the profile is large or export stalls.

## Successor Migration

1. Create a timestamped snapshot under `profile-retirement-backups/` containing successor files likely to be changed:
   - `config.yaml`, `auth.json`, `SOUL.md`, `AGENTS.md`, `profile.yaml`, `README.md`, `.env`, `shell-hooks-allowlist.json`
   - `memories/`, `scripts/`, `templates/`, `runtime/`, `cron/` when present
2. Normalize old profile config into successor:
   - replace old absolute profile paths with successor paths
   - verify `terminal.cwd` and `hooks.pre_tool_call.command` point to successor
3. Copy old profile durable assets into successor:
   - `memories/*.md`
   - `scripts/`
   - `templates/`
   - `runtime/`
4. Normalize copied scripts/docs that reference `profiles/<old>` to `profiles/<successor>`.
5. Merge `auth.json`:
   - preserve successor values on key collision
   - add missing old `providers` and `credential_pool` entries
6. Archive old sessions instead of overwriting active successor session DB:
   - copy `state.db`, `state.db-wal`, `state.db-shm`, `channel_directory.json`, `gateway_state.json`
   - target: `profiles/<successor>/retired-<old>-session-archive/`
   - write a manifest with old profile, successor profile, timestamp, and backup paths

## Alias Retirement

Repoint old command aliases before removing the old profile:

```bash
hermes profile alias <old> --remove
hermes profile alias <successor> --name <old>
hermes profile alias <successor>
```

Verify wrapper contents if needed:

```bash
sed -n '1,5p' /c/Users/Tiger/.local/bin/<old>.bat
```

Expected: old wrapper calls `hermes -p <successor>`.

## Move-Out Retirement

Do not immediately hard-delete the old profile. Move it out of active profiles:

```python
from pathlib import Path
import os, datetime
base = Path('C:/Users/Tiger/AppData/Local/hermes')
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.rename(base/'profiles/<old>', base/f'profile-retirement-backups/<old>-profile-retired-backup-{ts}')
```

This removes the profile from Hermes discovery while preserving a rollback copy.

## Verification

Run all relevant checks:

```bash
hermes profile list
hermes profile show <successor>
hermes profile show <old> || true
hermes -p <successor> config check
hermes -p <successor> skills list | grep -i '<domain-skill-pattern>'
```

If a stale-plugin guard exists, run it from the successor profile:

```bash
PYTHONIOENCODING=utf-8 python scripts/_precommit_guard.py
```

Verify archived sessions if applicable:

```python
import sqlite3
con = sqlite3.connect('retired-<old>-session-archive/state.db')
cur = con.cursor()
print(cur.execute('select count(*) from sessions').fetchone()[0])
print(cur.execute('select count(*) from messages').fetchone()[0])
```

## Common Failures

- `mklink /J` under Git Bash creates a malformed relative junction: use Python `subprocess.run(['cmd.exe','/C','mklink','/J', native_link, native_target])` with native `C:\\...` paths.
- Old profile still appears in `hermes profile list`: old directory was not moved out of `profiles/`.
- Old command still targets deleted profile: alias was not repointed.
- Successor loses recent session history: old `state.db` was copied over successor `state.db` instead of archived separately.
