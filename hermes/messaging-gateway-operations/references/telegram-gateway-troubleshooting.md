# Telegram gateway troubleshooting

This note captures the diagnosis pattern when Hermes is configured for Telegram but the messaging path is not actually live.

## What happened in this session

- `hermes gateway status` showed the Windows scheduled task as registered/running, but the gateway log later showed Telegram adapter load failure.
- The TUI/CLI was available, but that did **not** mean Telegram was working.
- The live gateway process had to be restarted after fixing the runtime environment.

## What to check

1. `hermes gateway status`
   - Confirm a real process is running.
   - Do not stop at the scheduled task being present.
2. `~/.hermes/logs/gateway.log`
   - Look for:
     - `python-telegram-bot not installed`
     - `No adapter available for telegram`
     - `Chat not found`
     - reconnect/network warnings
3. Hermes venv import check
   - Run the interpreter from Hermes's venv and verify `import telegram` succeeds.

## Repair pattern

If the gateway log says Telegram's Python dependency is missing:

```bash
".../hermes-agent/venv/Scripts/python.exe" -m pip install "python-telegram-bot[webhooks]==22.6"
hermes gateway restart
```

Notes:
- Install into Hermes's own venv so the running gateway process can import it.
- Restart is required because the current gateway process will not pick up the new package until it is replaced.

## Success criteria

- `hermes gateway status` shows the process running.
- The gateway log shows Telegram connected, not just attempted.
- A real Telegram message round-trips through Hermes.
