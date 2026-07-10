# PowerShell Plan Execution Pitfalls

Use when executing implementation plans that refactor PowerShell scripts or shared helper modules.

## Import-safe helper scripts

When a helper `.ps1` both defines functions and supports direct CLI execution, guard the executable footer so dot-sourcing does not emit output or run side effects:

```powershell
if ($MyInvocation.InvocationName -ne ".") {
    $result = Test-SomeHealth
    if ($Json) { $result | ConvertTo-Json -Depth 6 }
    else { "Human summary..." }
}
```

Verification pattern:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -Command ". 'C:\path\to\Helper.ps1'; if (Get-Command Test-SomeHealth -ErrorAction SilentlyContinue) { 'dot-source-ok' }"
```

## Dot-sourcing inside functions

Dot-sourcing a helper inside a function loads functions into that function's scope. Do not assume the imported function will exist later in the caller/script scope. Either:

1. dot-source the helper at script scope before any function uses it, or
2. call the imported helper from inside the same wrapper function that dot-sourced it.

Safe wrapper pattern:

```powershell
function Get-HealthFromHelper {
    $helperPath = Join-Path $PSScriptRoot "Helper.ps1"
    if (-not (Test-Path -LiteralPath $helperPath)) { return $null }

    . $helperPath
    if (-not (Get-Command Test-SomeHealth -ErrorAction SilentlyContinue)) { return $null }

    return Test-SomeHealth
}
```

## Verification discipline for long plan chains

For multi-plan work, update durable plan checkboxes and `todo` state at every completed plan boundary. If execution is interrupted by context/tool-call limits, the final response must include:

- last completed plan/task,
- exact active task id/status,
- files changed,
- verifications already run,
- next command/check to run.

This makes resumption deterministic instead of relying on chat reconstruction.

## Bounded verification for slow PowerShell health/audit paths

Some vault health/audit scripts have optional slow phases such as similarity scans. If the exact verification command times out at the harness foreground cap, do not mark the plan failed immediately when the slow phase is orthogonal to the refactor. Preserve the verification intent with an explicit bounded mode such as `-NoSimilarity` or `-Fast`, and record the timeout in the durable plan checklist. The follow-up smoke plan should own bounded coverage for the slow path.

Pattern:

```powershell
$out = & "C:\path\to\Test-VaultHealth.ps1" -VaultRoot "C:\Users\Tiger\Vault" -Json -NoSimilarity
$obj = $out | ConvertFrom-Json
if ($obj.recommended_mode -notin @("targeted-ingest", "full-vault-diagnosis", "no-action-needed")) {
    throw "Unsupported recommended_mode: $($obj.recommended_mode)"
}
```

## Smoke tests should not leave vault artifacts

When refactoring smoke suites, write reports/prompts/progress files under a unique temp root instead of the vault's `maintenance/scripts-outputs` tree unless the test specifically verifies that production output location. Clean the temp root before exit and add a positive cleanup check when practical.

Pattern:

```powershell
$smokeRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("vault-script-smoke-{0}" -f ([guid]::NewGuid()))
try {
    # write reports/prompts/progress under $smokeRoot
}
finally {
    Remove-Item -LiteralPath $smokeRoot -Recurse -Force -ErrorAction SilentlyContinue
}
```

## Negative controls for retired-term regressions

For smoke tests that assert retired commands/modes do not reappear, add a negative-control check using a temporary mock file, not the real script. This proves the detector would fail if a retired term existed while avoiding dirtying production files.

Pattern:

```powershell
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("negative-control-{0}" -f ([guid]::NewGuid()))
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
try {
    $mock = Join-Path $tempDir "mock.md"
    "Use tasks-review" | Set-Content -LiteralPath $mock -Encoding UTF8
    $retired = Select-String -Path (Join-Path $tempDir "*.md") -Pattern "inbox-review|tasks-review|master-tasks\.md|full-vault-cleanup" -SimpleMatch:$false
    if (-not $retired) { throw "Negative control failed: retired term was not detected." }
}
finally {
    Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
}
```

## Hermes profile hook guardrail cleanup plans

When a plan edits Hermes profile-local guardrails (for example `profiles/<name>/hooks/*.py` or profile `config.yaml`), treat it as cross-profile work and pass the tool's explicit cross-profile opt-in after the user has directed that profile edit. Do not modify the current/default profile by assumption; first verify the runtime profile with `hermes -p <profile> hooks list`.

Guardrail cleanup verification should use direct JSON payloads against the hook scripts, not real protected-file edits. Cover at least:

- deny paths: protected docs, `Types/*`, and `scripts/*` should return a JSON `decision: block`;
- safe path: a temp path outside the vault should return `{}` / pass;
- ask-first paths: domain `wiki/index.md` and `wiki/log.md` should return the configured approval block/warn behavior.

Run `python -m py_compile` on edited hook modules and `hermes -p <profile> hooks doctor` after edits. If doctor reports "script modified since approval" but the hook still exists, is allowlisted, and emits valid JSON, do **not** automatically run `hermes hooks revoke`; revocation requires next-runtime user consent and is an admin follow-up, not a functional plan failure.
