# Cron Working Directory Fix

## Problem
Hermes cron runner resolves relative script paths from its working directory (typically `C:\Users\Tiger\AppData\Local\hermes\hermes-agent` or similar), NOT from the `scripts/` folder where scripts actually live.

## Symptoms
```
RuntimeError: [Errno 2] No such file or directory: 'vault_cron_wrappers/vault_cron_inbox_prepare.py'
```

But the script exists at `C:\Users\Tiger\AppData\Local\hermes\scripts\vault_cron_wrappers\vault_cron_inbox_prepare.py`

## Root Cause
Cron job configured with:
```yaml
script: "vault_cron_wrappers/vault_cron_inbox_prepare.py"
# No workdir set
```

Runner looks for: `C:\Users\Tiger\AppData\Local\hermes\hermes-agent\vault_cron_wrappers\...` (wrong)

## Fix
Set explicit `workdir` on the cron job:

```bash
hermes cron update <job_id> --workdir "C:/Users/Tiger/AppData/Local/hermes/scripts"
```

Or via cronjob tool:
```json
{
  "action": "update",
  "job_id": "<job_id>",
  "workdir": "C:/Users/Tiger/AppData/Local/hermes/scripts"
}
```

## Affected Jobs (This Session)
All Vault Daily Check jobs using `vault_cron_wrappers/...` scripts:
- `d1aaf240382d` — Agent Skills
- `5937d30de249` — AI Sphere
- `61be6a72460b` — Hermes
- `c7f02ce985a6` — Smaller Domains
- `b52875c87676` — Inbox Preparation
- `de63a7345bb3` — Vault Skills Health

Plus:
- `8ec5375cb9b1` — daily-hermes-maintenance (script in root scripts/)
- `46bcd9762783` — Dependency audit (new script in root scripts/)

## Verification
After fix, test run:
```bash
hermes cron run <job_id>
# Should complete without "No such file or directory"
```

## Prevention
All new cron jobs using scripts in `scripts/` or subdirectories MUST have `workdir` set at creation time.