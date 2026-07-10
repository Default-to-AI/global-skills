# Discord DM allowlist troubleshooting

Use this when Discord channel posting works but DM interaction fails or logs `Unauthorized user`.

## Symptom pattern
- `hermes send --to discord:<target>` succeeds.
- The bot can post in a guild channel.
- DM messages produce no reply, or the gateway logs `Unauthorized user: <discord-user-id> (<display-name>) on discord`.

## What this usually means
Outbound delivery is healthy. The failure is on the inbound authorization path, usually `DISCORD_ALLOWED_USERS`.

## Durable fix
Prefer the numeric Discord user ID in `DISCORD_ALLOWED_USERS`:

```env
DISCORD_ALLOWED_USERS=460882902419374111
```

This is more reliable than a username for DM testing.

## Why usernames can fail
Some Discord allowlist flows resolve usernames to IDs by searching shared guild members. That can fail when:
- the bot and user do not share a guild member list the adapter can search,
- the bot lacks the member context needed for resolution,
- DM testing happens before the username-resolution pass succeeds.

## Important distinction
- `AI Degen` can be the display name.
- `ai.degen` can be the username/handle.
- The safest allowlist entry is still the numeric user ID.

## Verification
After changing `DISCORD_ALLOWED_USERS`:
1. reconnect or restart the gateway if the running process caches the old allowlist,
2. send a fresh DM,
3. confirm the log shows inbound Discord activity without a new `Unauthorized user` warning.
