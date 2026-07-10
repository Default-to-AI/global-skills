# Windows desktop cron Python stdout bug — no-agent jobs on Hermes

## Use case
Hermes cron job on Windows desktop shows a contradiction:
- the backing script clearly runs and writes a fresh non-empty report artifact
- but the scheduler logs `Job '<id>' (no_agent): empty stdout — silent run`
- Discord/Telegram delivery is skipped even though the generated message body exists on disk

## Symptom chain from this session
1. Cron job produced a fresh report file with full content (`cron_stdout_latest.txt`).
2. Direct manual script execution also produced non-empty stdout.
3. A forced run from the existing chat process still logged:
   - `empty stdout — silent run`
   - `agent returned [SILENT] — skipping delivery`
4. The cron scheduler source showed Python scripts run through `sys.executable`.
5. Patching the runner to swap `pythonw.exe` -> `python.exe` on Windows fixed the issue **only after triggering from a fresh Hermes CLI process**.
6. Fresh-process verification then logged:
   - `cron.scheduler: Job 'a2dc823824b0': delivered to discord:1522203691208282213`

## Minimal repair
Patch `hermes-agent/cron/scheduler.py` in the Python-script branch:

```python
py_exec = sys.executable
if sys.platform == "win32":
    py_path = Path(py_exec)
    if py_path.name.lower() == "pythonw.exe":
        python_console = py_path.with_name("python.exe")
        if python_console.exists():
            py_exec = str(python_console)
argv = [py_exec, str(path)]
```

## Critical verification rule
After patching scheduler code, do **not** trust a rerun from the already-running chat/gateway process alone. That process may still hold the old imported scheduler module.

Use one of these:
- `hermes cron run <job_id>` from a fresh CLI process
- restart the gateway/scheduler process, then rerun

## Interpretation rule
If all three are true:
- script-owned artifact contains fresh full report text
- direct manual execution prints fine
- scheduler still says `empty stdout — silent run`

then the bug is in the **scheduler runtime / interpreter path**, not in the report script.
