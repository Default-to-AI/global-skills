# Windows Discord cron delivery debugging

Use this when a Hermes cron on Windows appears to run but the Discord channel stays empty or `cron list`/`cronjob list` status disagrees with what the scheduler log implies.

## Durable pattern

Two independent systems can fail at once:
1. **delivery ownership** — another Hermes profile owns the Discord bot token
2. **script resolution / stdout capture** — the cron runner cannot find the intended script or classifies the run as silent

Treat them separately.

## 1) Clear cross-profile gateway contention first

Typical symptom in `agent.log` / gateway logs:
- `Discord bot token already in use (PID ...)`

On multi-profile setups, identify the owning process and profile, then stop the competing gateway before trusting any delivery test.

Verification target:
- no more `bot token already in use` lines for Discord before the rerun

## 2) Verify delivery with the scheduler log, not cron metadata alone

`last_status: ok` in the cron listing is not sufficient proof of channel delivery.

Use the scheduler log line as the primary positive evidence:
- `cron.scheduler: Job '<job_id>': delivered to discord:<channel_id>`

If the user still cannot see the message, keep debugging. A metadata `ok` without a delivery log line is not enough.

## 3) On Windows, relative cron script names may resolve under the Hermes scripts dir

Observed resolver path:
- `C:/Users/Tiger/AppData/Local/hermes/scripts/...`

Even when the job's `workdir` says something else, the cron runner may still look for the relative `script` name in the Hermes scripts directory. When `jobs.json` or `last_error` shows `Script not found:` under that path, the practical fix is:
- place the wrapper script at the exact resolver path Hermes is using
- then update the cron job so `script` and stored `workdir` both match that same directory

Do not assume `workdir` alone controls script lookup.

## 4) If direct Python stdout works but cron says silent, interpose a tiny wrapper

Typical silent-run symptom:
- `script produced no output, skipping AI call`
- or `(no_agent): empty stdout — silent run`

If running the collector directly prints valid output but the cron runner still sees silence, use a tiny wrapper script that:
- runs the real collector
- captures stdout
- writes a local copy to a debug artifact file
- re-emits stdout verbatim

This gives you:
- a stable file to inspect (`cron_stdout_latest.txt`-style)
- a cleaner place to debug resolution/capture behavior
- a safer production script target than repeatedly swapping the main collector

## 5) Final verification order

1. Stop competing gateways using the same Discord bot token
2. rerun the cron manually
3. inspect `agent.log` for `delivered to discord:<channel_id>`
4. confirm the cron's persisted `last_status` also converges to `ok`
5. only then call the recurring job healthy

## Notes

This is not a claim that Hermes cron is generally broken on Windows. The durable lesson is the repair sequence:
- clear gateway ownership conflicts
- verify via delivery log
- align script path with the resolver's real lookup location
- use a wrapper when direct script capture and cron capture diverge
