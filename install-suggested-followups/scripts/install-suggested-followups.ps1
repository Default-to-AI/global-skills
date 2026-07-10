# install-suggested-followups.ps1
#
# Companion installer for the install-suggested-followups skill
# (see ../SKILL.md for the contract).
#
# PowerShell variant of install-suggested-followups.sh. Same logic, same
# flags, same exit codes:
#
#   0   installed and verified (or no-op because already installed)
#   1   generic error
#   64  EX_USAGE — ambiguous runtime, partial coverage, etc.
#   73  EX_CANTCREAT — write failed
#
# Fixes over v1 (per code review):
#   - Spec block uses bare backticks (NOT \`-escaped).  Single-quoted
#     PowerShell here-strings (`@'...'@`) are already literal; the
#     \`-escapes were producing `\`## Followup Suggestions\`` text in the
#     output instead of inline-code backticks.
#   - Write path uses `[System.IO.File]::AppendAllText` with UTF-8 no-BOM
#     encoding.  Avoids `Add-Content -Encoding UTF8` which writes UTF-8
#     WITH BOM on Windows PowerShell 5.1 (the default on most installs).
#   - Fingerprint accepts bare `## Followup Suggestions` heading in
#     addition to the canonical `(mandatory output format)` variant
#     so a user who already has the loop terminator phrases in their
#     `~/.knowledge.md` gets a no-op on first run.
#
# Usage:
#   pwsh -File ./install-suggested-followups.ps1                          # auto-detect
#   pwsh -File ./install-suggested-followups.ps1 -Runtime claude         # pick Claude
#   pwsh -File ./install-suggested-followups.ps1 -Target ~/.claude/CLAUDE.md
#   pwsh -File ./install-suggested-followups.ps1 -DryRun                 # no writes

[CmdletBinding()]
param(
    [string]$Runtime = 'auto',
    [string]$Target  = '',
    [switch]$DryRun,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'
$ProgName = 'install-suggested-followups.ps1'

# ---------- Help ----------
if ($Help) {
    @'

install-suggested-followups.ps1 — companion installer for the skill

USAGE:
  pwsh -File ./install-suggested-followups.ps1 [-Runtime auto|hermes|codex|claude|generic]
                                               [-Target /abs/path]
                                               [-DryRun] [-Help]

PARAMETERS:
  -Runtime <name>   Pick which runtime to target. Default: auto.
  -Target  <path>   Override the auto-detected file path.
  -DryRun           Print what would happen without writing.
  -Help             Show this help.

EXIT CODES:
  0   installed and verified (or no-op because already installed)
  1   generic error
  64  EX_USAGE — ambiguous runtime, partial coverage, etc.
  73  EX_CANTCREAT — write failed
'@
    exit 0
}

# ---------- Runtime guard ----------
$allowed = @('auto','hermes','codex','claude','generic')
if ($allowed -notcontains $Runtime) {
    Write-Error "ERROR: invalid -Runtime '$Runtime' (allowed: auto|hermes|codex|claude|generic)"
    exit 64
}

# ---------- The canonical spec block ----------
# Verbatim text from SKILL.md "The Required Behavior (the spec)".
# Single-quoted PowerShell here-string (`@'...'@`)  = NO interpolation and
# NO escape processing.  Backticks / $ / em-dashes / the inner ```markdown
# fence all land as their literal characters.  The bytes that hit the
# target file are byte-identical to SKILL.md.
$SpecBlockHeader = '## Followup Suggestions (mandatory output format)'

$SpecBlock = @'


## Followup Suggestions (mandatory output format)

Mandatory output format for every reply — defined at the system layer and
required to match across sessions, reloads, and devices. End every reply
with a `## Followup Suggestions` section written as plain markdown prose —
never as a clickable host card or suggestion tool, which forces an
infinite suggestion loop.

Each followup MUST start with a **bold title** that opens with an action
verb and ends with `:` followed by a single descriptive sentence.

In the per-reply output, the section looks like this:

```markdown
## Followup Suggestions

- **<Action verb + concrete subject>:** <single sentence describing the next step the user can take>.
- **<Action verb + concrete subject>:** <single sentence describing the next step the user can take>.
- **<Action verb + concrete subject>:** <single sentence describing the next step the user can take>.
```

Rules:

1. Every followup MUST begin with `**...**` ending in `:`. No exceptions.
2. The description after the colon is one sentence — concrete and
   immediately actionable. No vague prompts like "iterate" or "improve".
3. Until the task is genuinely complete, push back, propose
   alternatives, and explain refinements directly in the followups. Do
   NOT just echo the user's last message back as a followup.
4. When the task is genuinely done, the prose above the section MUST
   contain the literal line `Task complete.` AND the first followup
   MUST open with the literal phrase `**Main objective was done.**`.
   Any remaining followups MUST start with `**Optional polish:**`
   and never be framed as work required to consider the turn complete.
5. Do NOT emit the host's clickable suggestions UI (cards, buttons,
   `suggest_followups` tool, etc.) for this purpose — that produces
   the suggestion loop. Plain markdown only.


'@

# ---------- Runtime anchor table ----------
$HomeDir       = if ($env:HOME) { $env:HOME } else { $env:USERPROFILE }
$HermesDir     = Join-Path $HomeDir '.hermes'
$HermesProfs   = Join-Path $HermesDir 'profiles'
$ClaudeDir     = Join-Path $HomeDir '.claude'
$CodexDir      = Join-Path $HomeDir '.codex'

$Candidates    = @()

function Add-Candidate {
    param([string]$Rt, [string]$Path, [int]$Pri)
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        $Script:Candidates += [pscustomobject]@{
            Runtime  = $Rt
            Path     = $Path
            Priority = $Pri
        }
    }
}

# Hermes: active profile first (try `hermes profile show --json` with
# graceful JSON parsing, fall back to first profile dir alphabetically).
$ActiveProfile = ''
if (Get-Command hermes -ErrorAction SilentlyContinue) {
    try {
        $raw = & hermes profile show --json 2>$null | Out-String
        if ($raw) {
            $obj = $raw | ConvertFrom-Json -ErrorAction SilentlyContinue
            if ($null -ne $obj) {
                # Walk a few common shapes; first hit wins.
                if ($obj.PSObject.Properties.Name -contains 'name' -and $obj.name) {
                    $ActiveProfile = [string]$obj.name
                } elseif ($obj.PSObject.Properties.Name -contains 'active_profile' -and $obj.active_profile.name) {
                    $ActiveProfile = [string]$obj.active_profile.name
                } elseif ($obj.PSObject.Properties.Name -contains 'profiles' -and $obj.profiles -is [System.Array]) {
                    $cand = $obj.profiles | Where-Object { $_.isActive -eq $true -or $_.active -eq $true } | Select-Object -First 1
                    if (-not $cand) { $cand = $obj.profiles | Select-Object -First 1 }
                    if ($cand -and $cand.PSObject.Properties.Name -contains 'name') {
                        $ActiveProfile = [string]$cand.name
                    }
                }
            }
        }
    } catch { }
}
if (-not $ActiveProfile -and (Test-Path -LiteralPath $HermesProfs -PathType Container)) {
    $first = Get-ChildItem -LiteralPath $HermesProfs -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($first) { $ActiveProfile = $first.Name }
}

if ($ActiveProfile) {
    Add-Candidate 'hermes' (Join-Path $HermesProfs "$ActiveProfile\SOUL.md")   10
    Add-Candidate 'hermes' (Join-Path $HermesProfs "$ActiveProfile\AGENTS.md") 11
}
Add-Candidate 'hermes' (Join-Path $HermesDir 'SOUL.md')   20
Add-Candidate 'hermes' (Join-Path $HermesDir 'AGENTS.md') 21

# Codex / Codebuff CLI / bare Codex CLI
Add-Candidate 'codex' (Join-Path $HomeDir '.knowledge.md')           30
Add-Candidate 'codex' (Join-Path $HomeDir '.knowledge.local.md')     31
Add-Candidate 'codex' (Join-Path $CodexDir  'instructions.md')       32
Add-Candidate 'codex' (Join-Path $CodexDir  'AGENTS.md')             33

# Claude Code
Add-Candidate 'claude' (Join-Path $ClaudeDir 'CLAUDE.md') 40

# Generic AGENTS.md-based runners
Add-Candidate 'generic' '.\AGENTS.md'                                      50
Add-Candidate 'generic' (Join-Path $HomeDir '.config\agents\AGENTS.md')   51

# ---------- Resolve target ----------
$TargetRuntime = ''
$TargetPath    = ''

function Resolve-RuntimeFromFileName {
    param([string]$FileName)
    switch ($FileName) {
        'SOUL.md'       { return 'hermes'  }
        'AGENTS.md'     { return 'hermes'  }
        'knowledge.md'  { return 'codex'   }
        'knowledge.local.md' { return 'codex' }
        'instructions.md' { return 'codex' }
        'CLAUDE.md'     { return 'claude'  }
        default         { return 'unknown' }
    }
}

if ($Target) {
    $TargetPath    = $Target
    $TargetRuntime = Resolve-RuntimeFromFileName (Split-Path -Leaf $TargetPath)
    if (-not (Test-Path -LiteralPath $TargetPath)) {
        if (-not $DryRun) {
            $parent = Split-Path -Parent $TargetPath
            if (-not (Test-Path -LiteralPath $parent)) {
                New-Item -ItemType Directory -Path $parent -Force | Out-Null
            }
        }
    }
} else {
    $filtered = $Candidates | Where-Object { $_.Runtime -eq $Runtime -or $Runtime -eq 'auto' }

    if (-not $filtered) {
        Write-Error "ERROR: no candidate system file found for Runtime='$Runtime'. Hint: pass -Target /abs/path/to/file."
        exit 64
    }

    if ($filtered.Count -eq 1) {
        $pick         = $filtered[0]
        $TargetRuntime = $pick.Runtime
        $TargetPath    = $pick.Path
    } else {
        if ($Runtime -ne 'auto') {
            $minPri = ($filtered | Measure-Object -Property Priority -Minimum).Minimum
            $pick   = $filtered | Where-Object { $_.Priority -eq $minPri } | Select-Object -First 1
            $TargetRuntime = $pick.Runtime
            $TargetPath    = $pick.Path
        } else {
            Write-Host 'ERROR: ambiguous runtime. Found candidate files for several runtimes:' -ForegroundColor Red
            foreach ($c in $filtered) {
                Write-Host ("  - [{0}] {1}" -f $c.Runtime, $c.Path)
            }
            Write-Host "`nRe-run with -Runtime hermes|codex|claude|generic to pick one, or -Target /abs/path/to/file for an explicit override."
            exit 64
        }
    }
}

# ---------- Fingerprint ----------
# Already-installed detector.  Accepts EITHER the canonical spec-block
# heading OR the bare `## Followup Suggestions` heading, AS LONG AS the
# terminator + polish clauses are present.  This is the user's existing
# `~/.knowledge.md` shape (the hand-written patch produced a bare
# heading), so a re-run correctly reports "no-op" instead of escalating.
function Test-Contains {
    param([string]$Path, [string]$Literal)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $content = Get-Content -LiteralPath $Path -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $false }
    return $content.Contains($Literal)
}

function Test-Regex {
    param([string]$Path, [string]$Pattern)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    return [bool](Select-String -LiteralPath $Path -Pattern $Pattern -Quiet -ErrorAction SilentlyContinue)
}

function Test-AlreadyInstalled {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    if (-not (Test-Contains -Path $Path -Literal 'Main objective was done.')) { return $false }
    if (-not (Test-Contains -Path $Path -Literal 'Optional polish:'))         { return $false }
    if      (Test-Contains -Path $Path -Literal '## Followup Suggestions (mandatory output format)')            { return $true }
    elseif  (Test-Regex     -Path $Path -Pattern '^## Followup Suggestions\s*$')                              { return $true }
    else   { return $false }
}

if (Test-AlreadyInstalled $TargetPath) {
    @"
Runtime detected:   $TargetRuntime
Canonical file:     $TargetPath
Action taken:       no-op (already installed)
Section heading:    $SpecBlockHeader
Reload required:    yes - restart your agent / open a new session if the runtime caches its prompt
"@
    exit 0
}

# Partial coverage: terminator or polish present but no compatible heading.
$partial = $false
if (Test-Path -LiteralPath $TargetPath -PathType Leaf) {
    $hasCanonicalHeading = Test-Contains -Path $TargetPath -Literal '## Followup Suggestions (mandatory output format)'
    $hasBareHeading      = Test-Regex     -Path $TargetPath -Pattern   '^## Followup Suggestions\s*$'
    if (-not $hasCanonicalHeading -and -not $hasBareHeading) {
        if (Test-Contains -Path $TargetPath -Literal 'Main objective was done.' `
         -or Test-Contains -Path $TargetPath -Literal 'Optional polish:') {
            $partial = $true
        }
    }
}

if ($partial) {
    @"
Runtime detected:   $TargetRuntime
Canonical file:     $TargetPath
Action taken:       SKIPPED - partial coverage detected
"@
    Write-Host @'

Partial coverage: the file contains one of the followups-terminator
phrases ("Main objective was done." or "Optional polish:") but is missing
both the canonical heading AND a bare "## Followup Suggestions" heading.

Manual merge required - do NOT silently overwrite content the user may
have kept on purpose. Either:
  (a) merge the spec block in manually, or
  (b) pass -Target /abs/path to a different file, or
  (c) remove the partial content first, then re-run.
'@ -ForegroundColor Yellow
    exit 64
}

# ---------- Dry run short-circuit ----------
if ($DryRun) {
    @"
Runtime detected:   $TargetRuntime
Canonical file:     $TargetPath
Action taken:       DRY-RUN (no write)
Section heading:    $SpecBlockHeader
The spec block would be appended to this file. Re-run without -DryRun to apply.
"@
    exit 0
}

# ---------- Append ----------
$parent = Split-Path -Parent $TargetPath
if (-not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

if (-not (Test-Path -LiteralPath $TargetPath)) {
    New-Item -ItemType File -Path $TargetPath -Force | Out-Null
}

# Insert leading blank line only if the existing file is non-empty,
# so the heading doesn't smash into previous content.
$leadingNewline = ''
$existing = Get-Item -LiteralPath $TargetPath -ErrorAction Stop
if ($existing.Length -gt 0) {
    $leadingNewline = "`n"
}

# UTF-8 NO BOM.  `Add-Content -Encoding UTF8` writes UTF-8 *with* BOM on
# Windows PowerShell 5.1 (the default), which can corrupt the leading
# heading detection in downstream markdown parsers.  Use raw byte-stream
# append for portable UTF-8 without BOM on 5.1 AND 7.x.
$payload = $leadingNewline + $SpecBlock
$bytes   = [System.Text.Encoding]::UTF8.GetBytes($payload)
$stream  = [System.IO.File]::Open(
    $TargetPath,
    [System.IO.FileMode]::Append,
    [System.IO.FileAccess]::Write,
    [System.IO.FileShare]::Read)
try {
    $stream.Write($bytes, 0, $bytes.Length)
} finally {
    $stream.Dispose()
}

# ---------- Verify ----------
$headingOk    = Test-Contains -Path $TargetPath -Literal $SpecBlockHeader
$terminatorOk = Test-Contains -Path $TargetPath -Literal 'Main objective was done.'
$polishOk     = Test-Contains -Path $TargetPath -Literal 'Optional polish:'

$linesTotal = (Get-Content -LiteralPath $TargetPath | Measure-Object -Line).Lines

@"
Runtime detected:   $TargetRuntime
Canonical file:     $TargetPath
Action taken:       appended
Section heading:    $SpecBlockHeader
Spec size:          $linesTotal total lines (target file)
Verification:
  - heading present:    $(if ($headingOk)    { 'yes' } else { 'no' })
  - terminator present: $(if ($terminatorOk) { 'yes' } else { 'no' })
  - polish present:     $(if ($polishOk)     { 'yes' } else { 'no' })
Reload required:    yes - restart your agent / open a new session so the updated prompt concatenates
"@

if (-not ($headingOk -and $terminatorOk -and $polishOk)) {
    Write-Host "`nWARNING: verification did not return green on all signals. Re-check $TargetPath manually." -ForegroundColor Yellow
    exit 1
}

exit 0
