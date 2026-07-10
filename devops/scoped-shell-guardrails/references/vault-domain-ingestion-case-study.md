# Scoped Guardrail Case Study — Vault Domain Ingestion

## Durable Lesson

A scoped-ingestion workflow had three distinct mutation channels:

1. direct file edits (`write_file`, `patch`)
2. deterministic script writes triggered through `terminal`
3. Python writes triggered through `execute_code`

The original policy only screened the outer tool call and direct path targets, which left indirect writes under-governed.

## Mutation Classes to Model

### Protected global file
- Example: top-level generated catalog / global index
- Risk: a "safe-looking" maintenance script rewrites it as a side effect
- Guardrail shape: block mutating write mode; allow only explicit read-only forms like `--stats`, `--dry-run`, or `--check`

### Generated scoped file
- Example: target-domain `index.md` or `log.md`
- Risk: regeneration is valid only for the active target, but the same command can rewrite another domain
- Guardrail shape: require active-domain marker plus matching command/env signal

### Out-of-scope ordinary wiki/content file
- Example: another domain's wiki page reached during audit-fix
- Risk: workflow decides the edit is "safe" and mutates outside the target domain
- Guardrail shape: when scoped mode is active, approval-gate any wiki/content edit outside the active domain

## Practical Pattern

- keep read-only verification commands globally allowed
- treat global repair as a different mode from scoped ingestion
- store the active target in a runtime marker file
- require matching target signal for scoped regeneration commands
- verify both command policy and path policy
- finish with changed-file classification

## Verification Payloads Worth Reusing

- protected direct write -> block
- read-only stats/check commands -> allow
- global mutating script write mode -> block
- unrelated-domain rebuild -> block
- matching in-scope rebuild with active marker -> allow
- active-domain content/log/index patch -> allow
- out-of-scope wiki/content patch during scoped mode -> block
- `execute_code` direct write or subprocess mutator -> block

## Why This Belongs in a Class-Level Skill

This is not just a vault quirk. It generalizes to any workflow where the policy is:

> allow writes inside one target boundary, but do not silently mutate protected or unrelated material through helper scripts or interpreter escapes.
