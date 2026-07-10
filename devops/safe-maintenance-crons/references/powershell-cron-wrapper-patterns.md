# PowerShell Cron Wrapper Patterns for Windows Hermes

## The core problem

On this Windows Hermes host, `cronjob(action="create")` requires `script` to be relative to `~/.hermes/scripts/`. If you pass a `.ps1` file, the cron executor runs it **as a Python script**, causing `SyntaxError: invalid syntax at line 2 ($ErrorActionPreference = 'SilentlyContinue')`.

## Solution: Python launcher + PowerShell wrapper

Create a pair for each cron target:

```
~/.hermes/scripts/vault_cron_wrappers/
  vault_cron_agent_skills.py      ← cronjob script (Python)
  vault_cron_agent_skills.ps1     ← actual PowerShell collector
```

### Python launcher template

```python
import subprocess, sys, os

script = os.path.join(os.path.dirname(__file__), 'vault_cron_agent_skills.ps1')
ps = r'C:\Program Files\PowerShell\7\powershell.exe'
if not os.path.exists(ps):
    ps = 'powershell.exe'

res = subprocess.run(
    [ps, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace',      # KEY: non-UTF-8 bytes from PowerShell won't crash reader
    timeout=300
)

print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)

sys.exit(res.returncode)
```

### PowerShell wrapper template

```powershell
# Vault cron wrapper: Agent Skills
$ErrorActionPreference = 'SilentlyContinue'
$collector = 'C:\Users\Tiger\AppData\Local\hermes\scripts\vault_domain_maintenance_collect.ps1'
$ps7 = 'C:\Program Files\PowerShell\7\powershell.exe'
if (-not (Test-Path -LiteralPath $ps7)) { $ps7 = 'powershell.exe' }

$stdout = ''; $stderr = ''; $exitCode = 1
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $ps7
# QUOTE multi-word args: '"AI Sphere"' not AI Sphere
$psi.Arguments = @(
    '-NoProfile','-ExecutionPolicy','Bypass','-File',$collector,
    '-VaultRoot','C:\Users\Tiger\Vault',
    '-Domain','"Agent Skills"',
    '-GroupName','"Agent Skills"'
) -join ' '

$psi.WindowStyle = 'Hidden'
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true

$p = [System.Diagnostics.Process]::Start($psi)
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$exitCode = $p.ExitCode

$out = ''
if ($stdout) { $out = $stdout }
elseif ($stderr) { $out = $stderr }
$out
exit $exitCode
```

## Critical patterns

| Pattern | Why it matters |
|---------|----------------|
| `encoding='utf-8', errors='replace'` in Python launcher | PowerShell can emit non-UTF-8 bytes (0x90 etc.) that crash `text=True` decode |
| Quote multi-word domain args: `'"AI Sphere"'` | `-join ' '` splits on spaces; unquoted becomes two args (`AI` `Sphere`) |
| Hidden window + hidden shell exec | Keeps cron output clean; no console flicker |
| Preserve exit code via `sys.exit(res.returncode)` | Cron status `ok`/`error` mirrors collector health |
| Return both stdout and stderr | Wrapper output becomes agent prompt injection |

## Collector argument quoting rule

When the PS wrapper passes args to the collector via `ProcessStartInfo.Arguments`, always quote multi-word string args:

```powershell
# BAD - becomes two separate args: -Domain AI Sphere
'-Domain','AI Sphere'

# GOOD - single arg: -Domain "AI Sphere"
'-Domain','"AI Sphere"'
```

This applies to: `-Domain`, `-GroupName`, `-StatePath`, and any user-supplied string that may contain spaces.

## Verification checklist per cron wrapper

1. ✅ Python launcher runs directly: `python vault_cron_xyz.py` → emits collector JSON, exits 0
2. ✅ PS wrapper runs directly: `pwsh -File vault_cron_xyz.ps1` → emits collector JSON, exits 0
3. ✅ Cronjob with `script: vault_cron_wrappers/vault_cron_xyz.py` triggers → `last_status: ok`
4. ✅ Telegram output uses agreed format (bold title + 🟢/🟡/🔴, bold section headers, `---` separators)
5. ✅ Non-ASCII / non-UTF-8 bytes from collector don't crash subprocess reader

## Files created in this session

| File | Purpose |
|------|---------|
| `vault_cron_agent_skills.py` / `.ps1` | Agent Skills domain collector |
| `vault_cron_ai_sphere.py` / `.ps1` | AI Sphere domain collector |
| `vault_cron_hermes.py` / `.ps1` | Hermes domain collector |
| `vault_cron_small_domains.py` / `.ps1` | Academia/Finance rotating collector |
| `vault_cron_inbox_prepare.py` / `.ps1` | Inbox frontmatter-only prep collector |
| `vault_cron_vault_skills_health.py` / `.ps1` | Vault skills alignment collector |

All 6 use the same launcher/wrapper pattern.