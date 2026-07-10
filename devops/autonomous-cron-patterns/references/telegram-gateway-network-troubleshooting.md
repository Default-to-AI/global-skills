# Telegram Gateway Network Troubleshooting

## Quick Diagnosis

When Telegram gateway shows as running but adapter fails to connect:

```bash
# 1. Check gateway status
hermes gateway status
# Should show: "Gateway process running (PID: XXXXX)"

# 2. Check gateway logs
tail -f C:\Users\Tiger\AppData\Local\hermes\logs\gateway.log
# Look for: "[Telegram] Connected to Telegram (polling mode)" + "✓ telegram connected"
# If seeing: "Primary api.telegram.org connection failed" + "Fallback IP 149.154.166.110 failed" → network block

# 3. Test network connectivity
curl -v --connect-timeout 10 https://api.telegram.org
ping -n 4 149.154.166.110

# 4. Check DNS resolution
nslookup api.telegram.org
# Should return: 149.154.166.110 and/or IPv6 address
```

## Common Failure Modes

| Scenario | DNS | TCP to 443 | Fix |
|----------|-----|------------|-----|
| College/corporate network | ✅ Resolves | ❌ Timeout | Network firewall block — use VPN/proxy or wait for home network |
| Home network | ✅ Resolves | ✅ Connects | Should work automatically |
| VPN connected | ✅ Resolves | ✅ Connects | Works if VPN allows Telegram |
| DNS hijacking | ❌ Wrong IP | ❌ Timeout | Check DNS server, use 8.8.8.8 |

## Observed Pattern (This Session)

**College network**:
- DNS resolves `api.telegram.org` → `149.154.166.110`
- Both primary and fallback IP timeout on port 443
- Gateway retries with exponential backoff (1m → 2m → 4m → 8m → 30m → 5m)
- **No Hermes config issue** — purely network layer

**Home network**:
- Same DNS resolution
- IPv6 connects successfully (73ms ping)
- Gateway auto-recovers on retry attempt #8
- Logs show: `[Telegram] Connected to Telegram (polling mode)` + `✓ telegram connected`

## Gateway Auto-Recovery

Hermes gateway has built-in reconnection logic:
- Exponential backoff: 1min, 2min, 4min, 8min, 30min, 5min (then repeats 5min)
- No manual intervention needed
- Will reconnect automatically when network allows

## Proxy Configuration (If Needed)

If on restricted network long-term, configure proxy in `.env`:

```env
# In C:\Users\Tiger\AppData\Local\hermes\.env
HTTPS_PROXY=http://your-proxy-host:port
# Or SOCKS5:
# HTTPS_PROXY=socks5://your-proxy-host:port
```

Then restart gateway:
```bash
hermes gateway restart
```

## Verification Checklist

After network change or proxy config:
- [ ] `hermes gateway status` shows running process
- [ ] Gateway log shows `[Telegram] Connected to Telegram (polling mode)`
- [ ] Gateway log shows `✓ telegram connected` or `✓ telegram reconnected successfully`
- [ ] Channel directory shows your chat target
- [ ] Test message from Telegram reaches Hermes and gets reply
- [ ] Cron job delivery works: `hermes cron run <job_id>` → check Telegram

## Cron-to-Telegram Delivery Verification

**Positive signal (required)**:
```
Job '<job_id>': delivered to telegram:8137298532 via live adapter
```

**Not sufficient**:
- `Last run: ok` — job completed but may not have reached Telegram
- Gateway process running — adapter may be disconnected

**Always verify**: Check gateway log for `delivered to telegram:<chat_id> via live adapter`