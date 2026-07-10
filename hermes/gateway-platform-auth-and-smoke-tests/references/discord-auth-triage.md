# Discord auth triage for Hermes gateway

## Durable signals

### 401 Unauthorized / `Improper token has been passed`
Meaning: Discord rejected `DISCORD_BOT_TOKEN` during login.

Most likely causes:
1. Bot token was reset/rotated in the Discord Developer Portal and Hermes still has the old one.
2. The wrong credential was copied from the Developer Portal.

Important distinction:
- **Application ID** and **Public Key** come from **General Information** and do **not** authenticate the bot.
- **DISCORD_BOT_TOKEN** comes from the **Bot** tab and is the value Hermes needs for login.

## New server pitfall
Creating a new Discord server does not move the existing bot into it.
A working bot must still be invited to the new guild via OAuth2 URL Generator.

Recommended scopes:
- `bot`
- `applications.commands`

## Routing vs auth
If `DISCORD_HOME_CHANNEL` changed recently, keep it as a separate check.
A 401 must be fixed before channel-ID debugging matters.

## Smoke-test choice
Use `hermes send --to discord ...` for a direct outbound test once credentials are correct.
Use gateway restart/log inspection only when validating the full conversational path.

## Windows Hermes note
On Windows/git-bash, prefer `$HERMES_HOME` for Hermes files. Do not assume `~/.hermes` points at the active home.
