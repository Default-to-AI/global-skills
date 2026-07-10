# Dashboard Operations Buttons Debugging

## Problem
The Operations section on the System page (Run doctor, Create backup, Security audit, Update skills, Prompt size, Support dump, Migrate config) appear to do nothing when clicked — no error, no spinner, no visible result.

## Root Cause (Loopback Mode)
When the dashboard runs on `127.0.0.1`/`localhost` without `--insecure`, it uses **legacy token auth** (`auth_required: false`). The SPA reads `window.__HERMES_SESSION_TOKEN__` injected by the server into the HTML:

```html
<script>
  window.__HERMES_SESSION_TOKEN__="0fcPkmvlytFh7mt8VwxOC9Aje5TzpW0KuecJ43ADywU";
  window.__HERMES_AUTH_REQUIRED__=false;
</script>
```

But in the browser console on the live dashboard, `window.__HERMES_SESSION_TOKEN__` returns **`null`** — the React app mounts and the token variable disappears before `fetchJSON()` reads it. Result: no `X-Hermes-Session-Token` header sent → 401 Unauthorized.

## Verification

```bash
# Extract token from dashboard HTML
curl -s http://127.0.0.1:9119/system | sed -n 's/.*window.__HERMES_SESSION_TOKEN__="\([^"]*\)".*/\1/p'

# Test with token (works)
curl -X POST -H "X-Hermes-Session-Token: <TOKEN>" http://127.0.0.1:9119/api/ops/doctor

# Test without token (fails - what browser sends)
curl -X POST http://127.0.0.1:9119/api/ops/doctor
```

## Backend Spawning Works
The `_spawn_hermes_action()` function in `hermes_cli/web_server.py` correctly spawns background processes on Windows:

```python
cmd = [sys.executable, "-m", "hermes_cli.main", *subcommand]
proc = subprocess.Popen(cmd, cwd=PROJECT_ROOT, ...)
```

Logs write to `~/.hermes/logs/action-<name>.log` and status is at `/api/actions/<name>/status`.

## Action Log Files
Mapped in `_ACTION_LOG_FILES`:
- `doctor` → `action-doctor.log`
- `security-audit` → `action-security-audit.log`
- `backup` → `action-backup.log`
- `import` → `action-import.log`
- `checkpoints-prune` → `action-checkpoints-prune.log`
- `skills-install` → `action-skills-install.log`
- `skills-uninstall` → `action-skills-uninstall.log`
- `skills-update` → `action-skills-update.log`
- `curator-run` → `action-curator-run.log`
- `prompt-size` → `action-prompt-size.log`
- `dump` → `action-dump.log`
- `config-migrate` → `action-config-migrate.log`

## Fix Needed (Frontend)
The token injection must survive React hydration. Options:
1. Move to `window.__HERMES_CONFIG__` object that persists
2. Use a `<meta name="hermes-session-token" content="...">` tag
3. Stash token in `sessionStorage` before React mounts

File to patch: `web/src/pages/SystemPage.tsx` → `runOp()` calls `api.runDoctor()` etc. which use `fetchJSON()` from `web/src/lib/api.ts:51`.

## Related Files
- `hermes_cli/web_server.py:_spawn_hermes_action()` — spawning logic
- `hermes_cli/web_server.py:_ACTION_LOG_FILES` — log mapping
- `web/src/lib/api.ts:fetchJSON()` — token injection
- `web/src/pages/SystemPage.tsx:runOp()` — button handlers