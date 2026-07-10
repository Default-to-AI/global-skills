# Cron → Telegram verification

Use this when the question is not "is cron configured" but "did Telegram actually receive the cron message?"

## Minimum proof chain

1. `hermes gateway status`
   - Need: gateway process running.
2. `hermes cron status`
   - Need: no warning that the gateway is down.
3. `~/.hermes/logs/gateway.log`
   - Need a fresh Telegram connection line:
     - `[Telegram] Connected to Telegram (polling mode)`
     - `✓ telegram connected`
4. Trigger a fresh event if needed:
   - `hermes cron run <job_id>`
   - Wait for the next scheduler tick.
5. `~/.hermes/logs/agent.log`
   - Need both:
     - `Job '<name>' has deliver=origin but no origin; falling back to telegram home channel` (only when applicable)
     - `Job '<job_id>': delivered to telegram:<chat_id> via live adapter`

## Interpretation

- `Last run: ok` is not enough.
- `Job completed successfully` is not enough.
- The decisive line is `delivered to telegram:<chat_id> via live adapter`.

## Useful sequence

1. `hermes gateway status`
2. `hermes cron list --all`
3. `hermes gateway start` if needed
4. `hermes cron run <job_id>`
5. Inspect `gateway.log` and `agent.log`

## Windows note

On Windows, the gateway may be installed as a Scheduled Task and still not have a live gateway process. Treat `No gateway process detected` as a hard blocker for automatic cron delivery until restarted.
