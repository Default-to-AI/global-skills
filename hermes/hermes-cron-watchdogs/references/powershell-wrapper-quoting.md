# PowerShell Wrapper Quoting Pattern (Windows Hermes)

## The core issue
On this Windows Hermes host, cron wrappers use `ProcessStartInfo` to launch the vault collector via `pwsh.exe`. When passing multi-word domain names (e.g. `Agent Skills`, `AI Sphere`), the argument must survive string concatenation intact.

## What fails
| Approach | Error |
|----------|-------|
| `$psi.ArgumentList = New-Object List[string]` | `'ArgumentList' is a ReadOnly property` |
| `$psi.ArgumentList.Add('...')` | `You cannot call a method on a null-valued expression` |
| `-join ' '` without quoting | Domain becomes two args: `Agent` `Skills` → collector throws `Selected domain 'Agent' is not an auditable current domain` |

## Working pattern
```powershell
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $ps7
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.WindowStyle = 'Hidden'

$argList = @(
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-File', $collector,
    '-VaultRoot', 'C:\Users\Tiger\Vault',
    '-Domain', '"Agent Skills"',     # escaped quotes: '\"Agent Skills\"'
    '-GroupName', '"Agent Skills"'
)
$psi.Arguments = $argList -join ' '

$p = [System.Diagnostics.Process]::Start($psi)
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$exitCode = $p.ExitCode

if ($stdout) { $stdout }
elseif ($stderr) { $stderr }
exit $exitCode
```

## Rule
For any parameter that may contain spaces (`-Domain`, `-GroupName`, `-StatePath`, etc.), wrap the **value** in escaped double quotes inside the PowerShell array: `'\"Multi Word Value\"'`. The `-join ' '` will produce a single argv token: `-Domain "Agent Skills"`.

## Files using this pattern
| Wrapper | Domain |
|---------|--------|
| `vault_cron_agent_skills.ps1` | Agent Skills |
| `vault_cron_ai_sphere.ps1` | AI Sphere |
| `vault_cron_hermes.ps1` | Hermes |
| `vault_cron_small_domains.ps1` | Academia / Finance (rotating) |
| `vault_cron_inbox_prepare.ps1` | (no domain arg) |
| `vault_cron_vault_skills_health.ps1` | (no domain arg) |

## Verification
1. Run wrapper directly: `pwsh -File vault_cron_agent_skills.ps1` → collector emits JSON with `selected_domain: "Agent Skills"`
2. Trigger cron job → `last_status: ok` and output artifact shows correct domain