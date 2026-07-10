# Telegram Flood Control Mitigation Pattern

This reference documents the rate-limiting and backoff pattern implemented in `gateway/platforms/telegram.py` to prevent Telegram 429 RetryAfter (flood control) errors.

## Problem

Telegram enforces ~30 messages/second per chat. Bursty outbound traffic (streamed replies, status edits, batched sends) triggers 429 RetryAfter responses. The gateway previously retried immediately or with fixed small waits, causing repeated flood violations.

In one session, a 21,180-character inbound batch was aggregated by the text-batching logic, then sent as multiple rapid chunks, triggering flood control.

## Solution — Three Layers

### 1. Outbound Token-Bucket Rate Limit (per chat)

```python
# Class constants
_SEND_RATE_LIMIT_PER_CHAT = 20.0   # sustained msg/s per chat
_SEND_BURST_ALLOWANCE = 5          # token-bucket bucket size

# Runtime state
self._send_buckets: Dict[str, Tuple[float, float]] = {}  # chat -> (tokens, last_ts)

# Called before each chunk send
await self._acquire_send_slot(chat_id)
```

Conservative 20 msg/s with burst of 5 respects the 30 msg/s limit with headroom. Configurable via:
- `HERMES_TELEGRAM_SEND_RATE_LIMIT`
- `HERMES_TELEGRAM_SEND_BURST`

### 2. Exponential Backoff on Flood Control (429 RetryAfter)

```python
_FLOOD_INITIAL_BACKOFF = 1.0   # seconds, doubled each retry
_FLOOD_MAX_BACKOFF = 30.0      # cap

# Per-chat backoff state
self._flood_backoff: Dict[str, float] = {}

# In send() and edit_message() catch blocks:
backoff = self._flood_backoff.get(chat_id, self._FLOOD_INITIAL_BACKOFF)
wait = float(retry_after) if retry_after is not None else backoff
wait = min(wait, self._FLOOD_MAX_BACKOFF)
await asyncio.sleep(wait)
self._flood_backoff[chat_id] = min(backoff * 2, self._FLOOD_MAX_BACKOFF)
```

- Uses Telegram's `retry_after` when provided, otherwise exponential backoff
- Caps at 30 seconds
- Resets on successful send/edit (non-flood path)

### 3. Inbound Text Batch Cap

```python
_MAX_TEXT_BATCH_TOTAL = 8000  # characters

# In _enqueue_text_event():
total_len = len(existing.text or "") if existing else chunk_len
if total_len >= self._MAX_TEXT_BATCH_TOTAL:
    logger.warning(...)
    await self._flush_text_batch(key)
    return
```

Forces immediate flush at 8000 chars instead of accumulating unbounded (prevents 20k+ char batches).

## Files Changed

- `gateway/platforms/telegram.py` — +94 lines, surgical changes

## Verification

```bash
python -m py_compile gateway/platforms/telegram.py
python -c "from gateway.platforms.telegram import TelegramAdapter; from gateway.run import GatewayRunner"
```

## Reversibility

All changes are additive (new methods, new instance state, env-configurable constants). No existing behavior removed. Can be reverted with a single `git checkout gateway/platforms/telegram.py`.