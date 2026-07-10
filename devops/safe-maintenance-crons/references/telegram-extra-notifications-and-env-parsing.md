# Telegram extra notifications and `.env` parsing for backup/relay crons

Use this when a maintenance cron must emit **extra Telegram messages** (start/success/failure) to the **same chat** that will also receive the cron's final delivery.

## When it applies

All three must be true:
1. the job is running as a cron,
2. the extra notification chat is the same as the cron final-delivery chat,
3. you need more than one user-visible message from the run.

## Durable pattern

- Send the cron's final report through normal Hermes cron delivery.
- Send the extra start/success/failure notifications directly through the Telegram Bot API.
- Treat Bot API `{"ok": true, ...}` as the positive verification signal for each extra notification.

## Why

Same-target duplicate-delivery protection can suppress an explicit `send_message` to the same Telegram chat that will already receive the cron's final response.

## Safe `.env` token lookup pattern

When building a tiny inline Python helper from a terminal tool call, do **not** search for the entire literal `TELEGRAM_BOT_TOKEN=...` line. Secret masking/redaction can mutate that text in the tool transcript and produce broken inline code.

Use key-name matching instead:

```python
from pathlib import Path

key = 'TELEGRAM_BOT_TOKEN'
token = None
for raw in Path('C:/Users/Tiger/AppData/Local/hermes/.env').read_text(encoding='utf-8', errors='replace').splitlines():
    if raw.split('=', 1)[0].strip() == key:
        token = raw.split('=', 1)[1].strip()
        break
if not token:
    raise SystemExit('missing TELEGRAM_BOT_TOKEN')
```

## Verification

Require both:
- Telegram Bot API response contains `"ok": true`
- returned `chat.id` matches the intended target chat

Then separately verify the backup or relay script itself by exit code and useful stdout/stderr.
