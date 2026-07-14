# Gateway restart + disabled-MCP verification pattern

Use this when a Hermes gateway is leaking warnings from a dead MCP endpoint (for example repeated `getaddrinfo failed`, `NXDOMAIN`, or `MCP: 0 tool(s)` lines) and the config fix is `mcp_servers.<name>.enabled: false`.

## Core lesson
A config edit alone is **not proof** that the leak is gone. If the gateway already booted with the old config, it can keep retrying the dead MCP endpoint until the gateway process is restarted.

## Durable pattern
1. **Prove the endpoint is actually dead**
   - Verify with an independent DNS check (for example DoH or `getaddrinfo`) so you do not mistake a transient app warning for a real dead host.
   - Distinguish `NXDOMAIN` / no resolution from normal transport failures.

2. **Confirm the config-side stop condition**
   - Read the live config and confirm the server is marked `enabled: false`.
   - If possible, read the registration logic and verify disabled servers are skipped entirely, not merely hidden from tool exposure.

3. **Assume a restart is required unless proven otherwise**
   - If the warning appears after the config edit, treat the current gateway as stale in-memory state.
   - Do not claim success just because the YAML changed.

4. **Do not restart the gateway from inside the gateway process tree**
   - On Hermes desktop, `hermes gateway restart` can be blocked from a child terminal owned by the gateway because the restart would kill the invoking process tree.
   - Safe paths:
     - run the restart from a separate shell outside the gateway, or
     - schedule a one-shot local cron/script that runs detached from the gateway process tree.

5. **Verify after the restart boundary, not globally**
   - Use the last `Starting Hermes Gateway` line (or equivalent positive restart marker) as the boundary.
   - Grep `agent.log` / gateway logs only for leak lines **after** that restart timestamp.
   - Required proof is positive: `no nous-mcp / getaddrinfo / 0-tool lines after restart`.

## Good verification shape
- precondition: dead endpoint proven independently
- config: `enabled: false` present
- restart: detached one-shot or external shell
- post-restart proof: no matching leak lines after the restart boundary

## Pitfalls
- **False closeout:** declaring victory because the YAML now says `enabled: false`
- **Wrong restart surface:** trying to restart from an in-gateway child shell
- **Weak grep:** searching the whole log and finding old errors, instead of filtering after the restart boundary
- **Misclassification:** treating a dead MCP host as a scheduler problem when the real issue is stale gateway state

## Related pattern: Windows cron relay for restart/verification
When the gateway restart will terminate the current chat session, queue the restart and the post-restart verifier as separate one-shot cron scripts. Let the verifier deliver the PASS/FAIL result asynchronously after the gateway reconnects.