# Windows auth and verification

Validated session workflow for the local Todoist CLI on this Windows host.

## Binary
- CLI binary worked at `C:\Windows\todoist.exe`
- `todoist --help` reported version `0.24.0`

## Config location
The bundled README in the Windows tarball states the config lives at:
- `C:\Users\Tiger\.config\todoist\config.json`

Minimal config shape:
```json
{
  "token": "<TODOIST_API_TOKEN>"
}
```

## Safe update pattern
1. Back up the existing config first.
2. Write the token into `config.json`.
3. Run `todoist sync`.
4. Verify with `todoist projects` and `todoist list`.

Example recovery-handle pattern:
- `C:\Users\Tiger\.config\todoist\backups\config.json.<timestamp>.bak`

## Live verification sequence that worked
1. `todoist sync` → exit code 0
2. `todoist projects` → returned:
   - `#Inbox`
   - `#Personal`
   - `#Agents`
3. `todoist list --filter '(overdue | today)'` → empty but successful
4. `todoist list` → returned live tasks, proving auth + sync + read path were working

## Interpretation notes
- Empty filtered output can simply mean no matching tasks.
- Successful `projects` plus successful unfiltered `list` is positive evidence of a live authenticated session.
