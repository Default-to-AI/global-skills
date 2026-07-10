#!/usr/bin/env bash
# install-suggested-followups.sh
#
# Companion installer for the install-suggested-followups skill
# (see ../SKILL.md for the contract).
#
# Fixes over v1 (per code review):
#   - heredoc delimiter is QUOTED so backticks / $ / em-dashes land literally;
#     no \`-escaping inside the spec body anymore
#   - fingerprint accepts bare `## Followup Suggestions` heading in addition
#     to the canonical `(mandatory output format)` variant, so a user who
#     already has the loop terminator phrases in their `~/.knowledge.md`
#     gets a no-op on first run instead of a partial-coverage escalation
#   - jq-resilient `hermes profile show --json` parsing with sed fallback
#
# Exit codes:
#   0   installed and verified (or no-op because already installed)
#   1   generic error
#   64  EX_USAGE — ambiguous runtime, partial coverage w/ conflicts, etc.
#   73  EX_CANTCREAT — write failed

set -u
# Note: deliberately NOT using `set -e`; we handle errors on the lines
# that need it so the install report still prints on failure.

PROG_NAME="install-suggested-followups.sh"

# ---------- Defaults ----------
RUNTIME="auto"
TARGET_OVERRIDE=""
DRY_RUN=0

# ---------- Args ----------
for arg in "$@"; do
  case "$arg" in
    --runtime=*)  RUNTIME="${arg#*=}" ;;
    --target=*)   TARGET_OVERRIDE="${arg#*=}" ;;
    --dry-run)    DRY_RUN=1 ;;
    --help|-h)    : "${HELP:=1}" ;;
    *) printf 'ERROR: unknown argument: %s\n' "$arg" >&2
       printf 'Try: %s --help\n' "$PROG_NAME" >&2
       exit 64 ;;
  esac
done

if [ "${HELP:-0}" -eq 1 ]; then
  cat <<'USAGE'
install-suggested-followups.sh — companion installer for the skill

USAGE:
  install-suggested-followups.sh [--runtime=auto|hermes|codex|claude|generic]
                                 [--target=/abs/path]
                                 [--dry-run] [--help]

OPTIONS:
  --runtime=<name>   Pick which runtime to target. Default: auto.
  --target=<path>    Override the auto-detected file path.
  --dry-run          Print what would happen without writing.
  --help             Show this help.

EXIT CODES:
  0   installed and verified (or no-op because already installed)
  1   generic error
  64  EX_USAGE — ambiguous runtime, partial coverage, etc.
  73  EX_CANTCREAT — write failed
USAGE
  exit 0
fi

# ---------- Runtime guard ----------
case "$RUNTIME" in
  auto|hermes|codex|claude|generic) ;;
  *) printf 'ERROR: invalid --runtime=%s (allowed: auto|hermes|codex|claude|generic)\n' "$RUNTIME" >&2
     exit 64 ;;
esac

# ---------- The canonical spec block ----------
# Verbatim text from SKILL.md "The Required Behavior (the spec)".
# QUOTED heredoc ('EOF') = NO shell expansion of any kind.  Backticks,
# $vars, em-dashes, and the inner ```markdown fence all land literally,
# so the bytes that hit the target file are byte-identical to SKILL.md.
read -r -d '' SPEC_BLOCK <<'EOF_SPEC_TAIL'

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

EOF_SPEC_TAIL

# Spec-block heading as a single literal for reporting.
SPEC_BLOCK_HEADER='## Followup Suggestions (mandatory output format)'

# ---------- Runtime anchor table ----------
HOME_DIR="${HOME:-}"
HERMES_PROFILES_DIR="$HOME_DIR/.hermes/profiles"

declare -a CANDIDATES  # each entry: "<runtime>|<path>|<priority>"

add_candidate() {
  local rt="$1" path="$2" pri="$3"
  [ -f "$path" ] && CANDIDATES+=("$rt|$path|$pri")
}

# Hermes: active profile first (try `hermes profile show` then jq,
# fall back to first profile dir alphabetically), then root-level SOUL/AGENTS.
HERMES_ACTIVE_PROFILE=""
if command -v hermes >/dev/null 2>&1; then
  if command -v jq >/dev/null 2>&1; then
    # jq-resilient parse — survives pretty-printed JSON and nested fields.
    HERMES_ACTIVE_PROFILE=$(hermes profile show --json 2>/dev/null \
      | jq -r '
          ( .name                // empty )
          ,( .profile.name       // empty )
          ,( .active_profile.name // empty )
          ,( .profiles[]? | select(.isActive==true or .active==true) | .name // empty )
          ,( .profiles[]? | .name // empty )
        ' 2>/dev/null | head -1)
  else
    # Fallback: simple grep on the first quoted "name" field (single-line output).
    HERMES_ACTIVE_PROFILE=$(hermes profile show --json 2>/dev/null \
      | grep -E '"(name|active_profile)"[[:space:]]*:' \
      | head -1 \
      | sed -n 's/.*"[[:space:]]*"\([^"]*\)".*/\1/p')
  fi
fi
if [ -z "$HERMES_ACTIVE_PROFILE" ] && [ -d "$HERMES_PROFILES_DIR" ]; then
  HERMES_ACTIVE_PROFILE=$(ls -1 "$HERMES_PROFILES_DIR" 2>/dev/null | head -1)
fi

if [ -n "$HERMES_ACTIVE_PROFILE" ]; then
  add_candidate "hermes" "$HERMES_PROFILES_DIR/$HERMES_ACTIVE_PROFILE/SOUL.md"   10
  add_candidate "hermes" "$HERMES_PROFILES_DIR/$HERMES_ACTIVE_PROFILE/AGENTS.md" 11
fi
add_candidate "hermes" "$HOME_DIR/.hermes/SOUL.md"   20
add_candidate "hermes" "$HOME_DIR/.hermes/AGENTS.md" 21

# Codex / Codebuff CLI / bare Codex CLI
add_candidate "codex" "$HOME_DIR/.knowledge.md"            30
add_candidate "codex" "$HOME_DIR/.knowledge.local.md"      31
add_candidate "codex" "$HOME_DIR/.codex/instructions.md"   32
add_candidate "codex" "$HOME_DIR/.codex/AGENTS.md"         33

# Claude Code
add_candidate "claude" "$HOME_DIR/.claude/CLAUDE.md" 40

# Generic AGENTS.md-based runners
add_candidate "generic" "./AGENTS.md"                              50
add_candidate "generic" "$HOME_DIR/.config/agents/AGENTS.md"       51

# ---------- Resolve target ----------
TARGET_RUNTIME=""
TARGET_PATH=""

if [ -n "$TARGET_OVERRIDE" ]; then
  TARGET_PATH="$TARGET_OVERRIDE"
  case "$(basename "$TARGET_PATH")" in
    SOUL.md|AGENTS.md)             TARGET_RUNTIME="hermes"  ;;
    knowledge.md|knowledge.local.md) TARGET_RUNTIME="codex" ;;
    instructions.md)               TARGET_RUNTIME="codex"   ;;
    CLAUDE.md)                     TARGET_RUNTIME="claude"  ;;
    *)                             TARGET_RUNTIME="unknown" ;;
  esac
  if [ ! -f "$TARGET_PATH" ]; then
    if [ "$DRY_RUN" -eq 0 ]; then
      parent="$(dirname "$TARGET_PATH")"
      mkdir -p "$parent" 2>/dev/null || {
        printf 'ERROR: cannot create parent directory %s\n' "$parent" >&2
        exit 73
      }
    fi
  fi
else
  declare -a FILTERED=()
  for entry in "${CANDIDATES[@]}"; do
    rt="${entry%%|*}"
    if [ "$RUNTIME" = "auto" ] || [ "$RUNTIME" = "$rt" ]; then
      FILTERED+=("$entry")
    fi
  done

  if [ "${#FILTERED[@]}" -eq 0 ]; then
    printf 'ERROR: no candidate system file found for runtime=%s\n' "$RUNTIME" >&2
    printf 'Hint: pass --target=/abs/path/to/system_file to specify one explicitly.\n' >&2
    exit 64
  fi

  if [ "${#FILTERED[@]}" -eq 1 ]; then
    PICK="${FILTERED[0]}"
    TARGET_RUNTIME="${PICK%%|*}"
    rest="${PICK#*|}"; TARGET_PATH="${rest%|*}"
  else
    # Multiple candidates exist for the active runtime filter.
    if [ "$RUNTIME" != "auto" ]; then
      # Pick the lowest priority value (= most specific).
      MIN_PRIORITY=9999
      for entry in "${FILTERED[@]}"; do
        rest="${entry#*|}"; pri="${rest##*|}"
        if [ "$pri" -lt "$MIN_PRIORITY" ]; then MIN_PRIORITY="$pri"; fi
      done
      PICK=""
      for entry in "${FILTERED[@]}"; do
        rest="${entry#*|}"; pri="${rest##*|}"
        if [ "$pri" -eq "$MIN_PRIORITY" ]; then PICK="$entry"; break; fi
      done
      TARGET_RUNTIME="${PICK%%|*}"
      rest="${PICK#*|}"; TARGET_PATH="${rest%|*}"
    else
      # Runtime = auto + multiple runtime signals: escalate.
      printf 'ERROR: ambiguous runtime. Found candidate files for several runtimes:\n' >&2
      for entry in "${FILTERED[@]}"; do
        rt="${entry%%|*}"; rest="${entry#*|}"; path="${rest%|*}"
        printf '  - [%s] %s\n' "$rt" "$path" >&2
      done
      printf '\nRe-run with --runtime=hermes|codex|claude|generic to pick one,\nor --target=/abs/path/to/file for an explicit override.\n' >&2
      exit 64
    fi
  fi
fi

# ---------- Fingerprint ----------
# Already-installed detector.  Accepts EITHER the canonical spec-block
# heading OR the bare `## Followup Suggestions` heading, AS LONG AS the
# terminator + polish clauses are present.  This is the user's existing
# `~/.knowledge.md` shape (the user's hand-written patch produced a bare
# heading), so a re-run correctly reports "no-op" instead of escalating.
fingerprint_satisfied() {
  local path="$1"
  [ -f "$path" ] || return 1
  grep -qF 'Main objective was done.' "$path" 2>/dev/null || return 1
  grep -qF 'Optional polish:'         "$path" 2>/dev/null || return 1
  if   grep -qF '## Followup Suggestions (mandatory output format)' "$path" 2>/dev/null; then return 0
  elif grep -qE '^## Followup Suggestions[[:space:]]*$'             "$path" 2>/dev/null; then return 0
  else return 1
  fi
}

if fingerprint_satisfied "$TARGET_PATH"; then
  cat <<EOF_REPORT
Runtime detected:   $TARGET_RUNTIME
Canonical file:     $TARGET_PATH
Action taken:       no-op (already installed)
Section heading:    $SPEC_BLOCK_HEADER
Reload required:    yes — restart your agent / open a new session if the runtime caches its prompt
EOF_REPORT
  exit 0
fi

# Partial coverage: terminator or polish present but no compatible heading.
PARTIAL=0
if [ -f "$TARGET_PATH" ]; then
  if ! grep -qF '## Followup Suggestions (mandatory output format)' "$TARGET_PATH" 2>/dev/null \
     && ! grep -qE '^## Followup Suggestions[[:space:]]*$'           "$TARGET_PATH" 2>/dev/null; then
    if grep -qF 'Main objective was done.' "$TARGET_PATH" 2>/dev/null \
       || grep -qF 'Optional polish:'         "$TARGET_PATH" 2>/dev/null; then
      PARTIAL=1
    fi
  fi
fi

if [ "$PARTIAL" -eq 1 ]; then
  cat <<EOF_REPORT
Runtime detected:   $TARGET_RUNTIME
Canonical file:     $TARGET_PATH
Action taken:       SKIPPED — partial coverage detected
EOF_REPORT
  printf '\nPartial coverage: the file contains one of the followups-terminator\nphrases ("Main objective was done." or "Optional polish:") but is missing\nboth the canonical heading AND a bare "## Followup Suggestions" heading.\n\nManual merge required — do NOT silently overwrite content the user may\nhave kept on purpose. Either:\n  (a) merge the spec block in manually, or\n  (b) pass --target=/abs/path to a different file, or\n  (c) remove the partial content first, then re-run.\n' >&2
  exit 64
fi

# ---------- Dry run short-circuit ----------
if [ "$DRY_RUN" -eq 1 ]; then
  cat <<EOF_REPORT
Runtime detected:   $TARGET_RUNTIME
Canonical file:     $TARGET_PATH
Action taken:       DRY-RUN (no write)
Section heading:    $SPEC_BLOCK_HEADER
The spec block would be appended to this file. Re-run without --dry-run to apply.
EOF_REPORT
  exit 0
fi

# ---------- Append ----------
mkdir -p "$(dirname "$TARGET_PATH")" 2>/dev/null || {
  printf 'ERROR: cannot create parent directory %s\n' "$(dirname "$TARGET_PATH")" >&2
  exit 73
}

if [ ! -f "$TARGET_PATH" ]; then
  : > "$TARGET_PATH"
fi

# Insert leading blank line only if the existing file is non-empty,
# so the heading doesn't smash into previous content.
if [ -s "$TARGET_PATH" ]; then
  printf '\n' >> "$TARGET_PATH"
fi

# `cat <<<` rather than `printf '%s\n'` so a future edit that adds `%`
# characters to the spec block cannot trigger format-substitution.
# Wrap in a brace group so we can also append an explicit trailing
# newline (preserving byte parity with the prior printf-based append)
# and treat the whole block as one atomic append for error handling.
{
  cat <<< "$SPEC_BLOCK"
  printf '\n'
} >> "$TARGET_PATH" 2>/dev/null || {
  printf 'ERROR: failed to append spec block to %s\n' "$TARGET_PATH" >&2
  exit 73
}

# ---------- Verify ----------
HEADING_OK=0; TERMINATOR_OK=0; POLISH_OK=0
grep -qF "$SPEC_BLOCK_HEADER"     "$TARGET_PATH" && HEADING_OK=1
grep -qF "Main objective was done." "$TARGET_PATH" && TERMINATOR_OK=1
grep -qF "Optional polish:"         "$TARGET_PATH" && POLISH_OK=1

LINES_TOTAL=$(wc -l < "$TARGET_PATH" 2>/dev/null | tr -d ' ')

cat <<EOF_REPORT
Runtime detected:   $TARGET_RUNTIME
Canonical file:     $TARGET_PATH
Action taken:       appended
Section heading:    $SPEC_BLOCK_HEADER
Spec size:          $LINES_TOTAL total lines (target file)
Verification:
  - heading present:    $([ "$HEADING_OK"    -eq 1 ] && echo yes || echo no)
  - terminator present: $([ "$TERMINATOR_OK" -eq 1 ] && echo yes || echo no)
  - polish present:     $([ "$POLISH_OK"     -eq 1 ] && echo yes || echo no)
Reload required:    yes — restart your agent / open a new session so the updated prompt concatenates
EOF_REPORT

if [ "$HEADING_OK" -ne 1 ] || [ "$TERMINATOR_OK" -ne 1 ] || [ "$POLISH_OK" -ne 1 ]; then
  printf '\nWARNING: verification did not return green on all signals.\nRe-check %s manually.\n' "$TARGET_PATH" >&2
  exit 1
fi

exit 0
