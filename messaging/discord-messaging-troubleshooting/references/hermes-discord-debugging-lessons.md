# Hermes Discord debugging lessons

## Durable troubleshooting pattern

When Hermes works in a Discord channel but fails in DMs, separate the problem into independent layers and verify each one with evidence:

1. **Bot auth / server membership**
   - Confirm the bot token is valid and the adapter logs `Connected as ...`.
   - Confirm the bot was invited with the needed scopes (`bot`, `applications.commands`).
   - Verify the target server/channel IDs after any server rebuild or re-invite.

2. **Inbound transport**
   - Check gateway logs for `inbound message: platform=discord ...`.
   - If inbound messages appear, Discord transport is working; do not blame the token or gateway connection.

3. **Allowlist / identity resolution**
   - Hermes Discord allowlists can involve usernames and numeric IDs.
   - Shared-guild resolution matters for DM users: if username-based allowlisting is transformed into numeric IDs, the user must be resolvable from a guild the bot can see.
   - If DM requests show `Unauthorized user` after inbound logging succeeds, inspect allowlist behavior before chasing model/runtime issues.

4. **Agent/runtime crash path**
   - If inbound logging succeeds but the user gets `unexpected error`, inspect Hermes/gateway logs for Python tracebacks.
   - One proven failure mode: `mcp_servers` configured as a YAML list instead of a mapping/dictionary, producing `AttributeError: 'list' object has no attribute 'items'` during agent startup.
   - Correct shape example:
     ```yaml
     mcp_servers:
       nous-mcp:
         url: https://mcp.nousresearch.com
         priority: 1
     ```

## User-handling lesson

For Hermes setup/troubleshooting, prefer direct verification and direct edits when the agent has access. Do not bounce obvious local file checks or safe config edits back to the user unless the file/tool guardrails truly block the change or the step requires an external UI.

## Session-specific evidence captured here

- Bot invite scopes used: `bot`, `applications.commands`
- Example working home channel/server IDs were updated during the session.
- DM troubleshooting involved distinguishing Discord transport success from downstream Hermes config failure.
