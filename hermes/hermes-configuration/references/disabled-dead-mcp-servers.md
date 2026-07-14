# Disabled dead MCP servers

Use this pattern when a configured MCP server has become permanently invalid or noisy, but you want to preserve the config block for later recovery.

## Proven repair pattern
1. Verify the endpoint is actually dead with live evidence.
   - Examples: DNS `NXDOMAIN`, reproducible `getaddrinfo failed`, HTTP connect failure from multiple resolvers.
2. Disable the server instead of deleting the block:
   - `hermes config set mcp_servers.<server-name>.enabled false`
3. Re-read `config.yaml` and confirm the flag persisted.
4. Restart the relevant Hermes process (gateway / fresh session) or wait for config reload.
5. Re-check logs and confirm the startup warning stopped.

## Why this is better than deleting the block
- Avoids direct edits to `config.yaml`, which may be blocked by Hermes's config guard or race with a live process.
- Preserves the original URL and surrounding settings so re-enable is trivial if the provider restores the service.
- `enabled: false` removes the server from active connection attempts, so startup no longer retries it and no longer emits repeated warning noise.

## Example symptom chain
- Config still contains an MCP server URL.
- Every gateway start retries it several times.
- Logs show connection noise such as `getaddrinfo failed` or `0 tool(s) from 0 server(s)`.
- Endpoint verifies as dead (for example the hostname returns `NXDOMAIN`).

## Example: Nous MCP
A concrete case on this host: `mcp.nousresearch.com` returned `NXDOMAIN` while `nousresearch.com` itself still resolved. The correct repair was **not** to hunt for a guessed replacement URL; it was to disable `mcp_servers.nous-mcp.enabled` and stop the warning leak until a live replacement is verified.
