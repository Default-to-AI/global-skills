# Docs Drift Cron Debugging Pattern

Use this reference when a script-backed research cron fails noisily and the user received an alert before the agent repaired the job.

## Failure class

A recurring docs-drift job failed with:

- `AttributeError: 'list' object has no attribute 'items'`
- a prior misconfiguration also used the literal script value `"none"`, which Hermes treated as a real script path instead of "no script"

## Repair pattern

1. Inspect the cron output artifact under `cron/output/<job_id>/` first.
   - This tells you what prompt, injected script output, and final error the scheduler actually saw.
2. Inspect the persisted job definition.
   - Look for stale `script` values, malformed prompt text, wrong delivery target, or mismatched enabled toolsets.
3. Run the collector directly outside cron.
   - Confirm whether the collector itself works before blaming the prompt.
4. Normalize the collector output contract.
   - Prefer a top-level object like `{ "drifts": [...] }` over a bare JSON list.
   - Make the prompt name the exact field it should consume.
5. Fix configuration mistakes at the source.
   - Never leave sentinel strings like `"none"` in `script`.
6. Rerun the cron immediately.
   - Verify `last_status`, `execution_success`, and the new output artifact before closing.

## Durable lessons

- Raw failure delivery is not completion; follow-through requires diagnosis, fix, rerun, and verification.
- For injected script output, explicit contracts beat implied structure.
- When a cron and a direct script run disagree, the output artifact is the source of truth for what cron actually processed.

## Use in future jobs

Apply this pattern to any research/radar cron that:
- injects structured collector output into an LLM prompt
- reports to Telegram or another user-facing channel
- needs a fast repair loop when the scheduler emits an error instead of a brief
