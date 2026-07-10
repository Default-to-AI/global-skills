# Vault PowerShell automation

Use this reference when vault work also touches the companion PowerShell suite at `C:\Program Files\PowerShell\7\scripts\Vault`.

## Control-surface map

- `New-VaultPrompt.ps1` — generates structured prompts and operator-facing mode descriptions
- `Test-VaultHealth.ps1` — emits vault-health diagnosis, including JSON for Hermes consumption
- `Test-VaultAudit.ps1` — performs the structured audit and writes report artifacts
- `Test-VaultScripts.ps1` — fast regression harness for script-suite changes
- `Vault-PromptCore.ps1` — shared prompt/authority helpers used by the suite

## Durable integration lessons

1. Keep vault docs authoritative.
   - Script-generated prompts must point Hermes back to the live vault docs in this order:
     `AGENTS.md -> vault-guide.md -> vault-index.md -> domain wiki/index.md -> domain wiki/log.md`
   - Diagnostic output is accessory context, not the procedure source of truth.

2. Treat the suite as runtime infrastructure.
   - Edits here affect Hermes-facing vault operations, not just local operator UX.
   - Use a recovery handle before editing.

3. Resolve PowerShell explicitly.
   - Prefer script-local resolution of the concrete `pwsh.exe` path instead of assuming `pwsh` is available on PATH.
   - Apply the same resolution strategy to child-process and background-job execution paths.

4. Verify with real script runs.
   - Minimum gate after edits: `Test-VaultScripts.ps1 -Fast`
   - Also run one live entrypoint such as:
     - `New-VaultPrompt.ps1 -ListModes`
     - `Test-VaultHealth.ps1 -Json -SkipTodoist -NoSimilarity`

5. Keep mode contracts legible.
   - Distinguish interactive approval-gated modes from Hermes-safe automated modes.
   - If a mode description changes, update the smoke test assertions too.

## Good change targets

- authority/order-of-operations text drift
- mode-description drift
- child-process `pwsh` invocation portability
- report/output-path correctness
- regression tests that assert stale prompt contracts

## Avoid

- treating health findings as script bugs without verification
- letting generated prompt text outrank live vault docs
- editing vault content when the actual task is script integration
