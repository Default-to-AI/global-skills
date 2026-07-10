# Documentation-Drift Cron Calibration

Use this note when a cron job scans merged PRs for missing docs updates and starts producing noisy findings.

## Core rule

Treat documentation-drift detection as a **user-facing contract audit**, not a file-touch audit.

Broad implementation files such as `hermes_cli/main.py`, `hermes_cli/config.py`, and `tools/*.py` are only entry points for inspection. They are not sufficient evidence on their own.

## Trigger matrix

### CLI docs drift

Report only when the PR changes something a user could reasonably expect in the CLI reference, for example:
- new or removed flags
- changed flag semantics
- help text that changes documented invocation behavior
- new/removed subcommands
- `argparse` passthrough semantics that alter how users call the command

Do **not** report when the PR only changes:
- startup wiring
- routing logic
- dashboard boot behavior
- profile selection internals
- background task startup

### Environment-variable docs drift

Report only when the PR changes a **user-facing env-var contract**, for example:
- env var added / removed / renamed / deprecated
- precedence order of documented env vars changed
- documented variable now controls different behavior
- a deprecated documented variable is intentionally removed from user-facing surfaces

Do **not** report when the PR only changes:
- internal guard vars
- process-env passthrough allowlists
- Windows location vars needed only for subprocess launching
- implementation details that never belonged in the env-var reference

### Config docs drift

Report when a PR changes a documented config key's:
- name
- allowed values
- default
- material meaning

A behavior change to a documented option counts even when the key name stayed the same.

### Tool docs drift

Report when tool schema or user-visible tool behavior changes, such as:
- tool name
- parameters
- descriptions
- requirement gating visible to users
- materially different built-in-tool behavior the docs describe

## Require a proof quote

Before reporting a docs gap, include one short quoted line from the PR diff showing the user-facing contract change.

This sharply reduces false positives because purely internal changes usually fail the quote test.

## Real calibration examples

### False positives to suppress

- `hermes_cli/main.py` changed to start background MCP discovery for dashboard `/api/ws` sessions.
  - Why suppress: internal startup behavior; no CLI syntax/help change.

- `hermes_cli/main.py` added an `HERMES_DESKTOP` routing guard.
  - Why suppress: internal routing guard, not a user-facing env-var contract.

- `tools/mcp_tool.py` expanded Windows safe-env passthrough.
  - Why suppress: subprocess plumbing, not an env-var reference change.

### Likely real findings

- `agent.coding_context` behavior changed so `auto` no longer demotes and `focus` does.
  - Why keep: documented config option changed meaning.

- Anthropic env-var status precedence / deprecated `HERMES_TOOL_PROGRESS*` user-facing visibility changed.
  - Why keep: documented env-var meaning/visibility changed.

## Prompt patch pattern after a noisy first run

When the first cron run over-reports, patch the job prompt to add:
1. a strict "user-facing changes only" rule
2. category-specific trigger criteria
3. a mandatory quoted proof point
4. explicit suppression of uncertain cases
5. calibration examples from the bad run

That converts the first noisy run into training data for the next clean run.
