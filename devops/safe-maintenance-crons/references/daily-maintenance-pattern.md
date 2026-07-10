# Daily maintenance cron pattern

Use this when an agent is allowed to self-maintain but must stay inside a hard safety box.

## Recommended shape

- **Script layer:** deterministic local collector emits JSON
- **LLM layer:** reads injected JSON first, then decides whether to make 0-3 small fixes
- **Toolsets:** `terminal,file,skills,memory`
- **Delivery:** `origin`

## Collector checklist

- include command, exit code, stdout, stderr, timeout flag
- apply per-command timeouts
- scan candidate clutter without deleting it
- separate categories:
  - stale one-off plans
  - stale request dumps
  - stale state snapshots
  - temp artifact candidates
- exclude backup mirrors and self-referential backup trees

## Prompt checklist

### Must allow
- read-only verification
- reversible local fixes
- skill patches for class-level lessons
- memory add/replace for durable facts only
- tightening the cron's own restrictions when the first run proves they are too loose

### Must forbid
- broad deletion
- memory deletion
- transcript/session/log/state deletion
- package installs or auto-fix upgrade commands
- auth/provider/billing changes
- cross-profile edits
- backup repo edits
- speculative `.bak` cleanup
- creation of durable run-note clutter unless a real fix requires it

## First-run audit

The first manual run is part of setup, not optional.

Inspect for:
- job ran successfully
- delivery target correct
- output concise
- no accidental durable note creation
- no out-of-scope edits

If the first run creates clutter, patch the prompt immediately. Save the lesson in the skill; do not normalize the clutter.
