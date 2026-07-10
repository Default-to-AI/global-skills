# Windows multi-profile gateway stop cleanup

Use when a specialist profile gateway (for example `employee` or `librarian`) was told to stop, but Hermes still reports it as running.

## Symptom pattern

- `HERMES_PROFILE=<name> hermes gateway stop` reports success.
- `HERMES_PROFILE=<name> hermes gateway status` says `No gateway process detected`.
- But `hermes gateway list` or `hermes profile list` still shows the profile as running.
- On Windows, stale runtime files may remain under `profiles/<name>/`:
  - `gateway_state.json`
  - `gateway.pid`
  - `gateway.lock`
  - `logs/.__gateway.lock`

## Important verification detail

Do **not** use `/proc/<pid>` checks for this on Windows git-bash. That is Linux logic and can produce false conclusions here.

Instead, verify the recorded PID with Windows task inspection. In git-bash, bypass MSYS argument rewriting:

```bash
MSYS2_ARG_CONV_EXCL='*' tasklist.exe /FI "PID eq <pid>" /FO LIST
```

If the process still exists as `pythonw.exe`, kill it explicitly:

```bash
MSYS2_ARG_CONV_EXCL='*' taskkill.exe /PID <pid> /T /F
```

## Cleanup sequence

1. Stop the profile gateway normally first:
   ```bash
   HERMES_PROFILE=<name> hermes gateway stop
   ```
2. Read `profiles/<name>/gateway_state.json` and note the PID.
3. Verify that PID with `tasklist.exe` using `MSYS2_ARG_CONV_EXCL='*'`.
4. If still alive, kill it with `taskkill.exe /PID <pid> /T /F`.
5. Rewrite `profiles/<name>/gateway_state.json` to:
   - `gateway_state: stopped`
   - `pid: null`
   - `restart_requested: false`
   - a truthful `exit_reason`
6. Remove stale runtime markers if present:
   - `profiles/<name>/gateway.pid`
   - `profiles/<name>/gateway.lock`
   - `profiles/<name>/logs/.__gateway.lock`
7. Re-check:
   - `hermes gateway list`
   - `hermes profile list`

## Positive verification

Success means **all** of these are true:

- `hermes gateway list` shows the profile as `not running`
- `hermes profile list` shows the profile gateway as `stopped`
- `tasklist.exe` reports no task matching the old PID

## Why this matters

The misleading split is: per-profile `gateway status` can say the active profile has no live process, while the global list still treats a stale Windows PID/lock combination as alive. Clean both the process and the runtime markers.