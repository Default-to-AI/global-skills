# Profile renaming with shared skill junctions

Use this reference when replacing a dedicated Vault-style Hermes profile with a renamed successor profile while preserving shared skills.

## What to verify

- Compare `profile.yaml`, `config.yaml`, `SOUL.md`, `AGENTS.md`, `README.md`, `.env`, hooks, shell-hook allowlist, and `cron/jobs.json` between old and new profiles.
- Normalize expected path/name changes before declaring a diff meaningful (for example `profiles/vault` -> `profiles/librarian`).
- Check model/provider blocks explicitly; users may expect either exact inheritance or intentional upgrade.
- Check `auth.json` provider and credential-pool coverage separately from config.
- Check `state.db` session/message counts if historical recall matters.
- Check profile aliases before deletion; stale wrapper scripts can survive profile deletion.

## Windows junction pattern

When one profile's `skills` directory is a Windows junction, make the successor profile inherit that attribute rather than copying a real directory.

Typical target seen in Robert's setup:

```text
C:\Users\Tiger\Agents\Agent-Skills
```

Preserve the current real directory first:

```bash
mv /c/Users/Tiger/AppData/Local/hermes/profiles/<profile>/skills \
   /c/Users/Tiger/AppData/Local/hermes/profiles/<profile>/skills.pre-junction-backup-$(date +%Y%m%d_%H%M%S)
```

Create the junction via Python `subprocess.run([...])` with native Windows paths. This avoids Git-Bash/MSYS eating backslashes or treating `C:/...` as a switch:

```python
from pathlib import Path
import os, subprocess
link = Path('C:/Users/Tiger/AppData/Local/hermes/profiles/<profile>/skills')
target = Path('C:/Users/Tiger/Agents/Agent-Skills')
if os.path.lexists(link):
    raise SystemExit(f'refusing: {link} already exists')
subprocess.run(['cmd.exe', '/C', 'mklink', '/J', str(link), str(target)], check=True)
```

Avoid hand-typed `cmd //c mklink /J ...` from Git-Bash unless path quoting/conversion is fully controlled. Failed attempts can create malformed relative junctions; remove only the bogus reparse point with `os.rmdir(path)`.

## Deletion readiness rule

Do not call the old profile ready for obliteration merely because the successor can operate. It is ready only after either migrating or intentionally discarding:

- local memories (`memories/USER.md`, `memories/MEMORY.md`)
- unique profile scripts/templates/runtime files referenced by profile docs
- session database/history if needed
- auth credential pools if needed
- gateway/channel state if active
- profile aliases/wrapper scripts

Operational switchover and no-loss deletion are different conclusions.
