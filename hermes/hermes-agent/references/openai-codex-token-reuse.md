# openai-codex Token Reuse Collision — Reproduction & Root Cause

## Scenario (from session 2026-06-06)

**Symptom:** Vault profile shows 401 error, disappears quickly. Profile fails to start.

**Root cause found in `~/.hermes/profiles/vault/auth.json`:**
```json
"active_provider": "openai-codex",
"providers": {
  "openai-codex": {
    "last_auth_error": {
      "code": "refresh_token_reused",
      "message": "Codex refresh token was already consumed by another client (e.g. Codex CLI or VS Code extension). Run `codex` in your terminal to generate fresh tokens, then run `hermes auth` to re-authenticate.",
      "reason": "credential_pool_refresh_failure",
      "relogin_required": true,
      "at": "2026-06-06T02:54:26.419041+00:00"
    }
  }
}
```

**Cross-profile impact:** Checked all 5 profiles — same credential pool entry ID (`473ea6` or similar) used across vault, engineer, reviewer, strategist, writer for openai-codex. When Codex CLI/VS Code consumed the refresh token, **all profiles using that pool entry** were blocked simultaneously.

| Profile | Active Provider | Codex Status |
|---------|----------------|--------------|
| vault | openai-codex | ❌ refresh_token_reused (Jun 6) |
| engineer | nous | ❌ refresh_token_reused (Jun 1) — if switched |
| reviewer | openai-codex | ⚠️ stale token (Jun 1 refresh) — likely blocked |
| strategist | nous | ❌ usage_limit_reached — if switched |
| writer | openai-codex | ⚠️ stale token (Jun 1 refresh) — likely blocked |

## Why This Happens

1. User runs `codex` (CLI) or uses VS Code Codex extension → performs OAuth device code flow
2. Tokens written to `%USERPROFILE%\.codex\auth.json` (Windows) / `~/.codex/auth.json` (WSL)
3. User runs `hermes auth` → adds credential to profile's `credential_pool.openai-codex[]` with `source: "manual:device_code"`
4. **Multiple profiles** add the **same credential pool entry** (same refresh token)
5. Later, user runs `codex` again or VS Code refreshes → **consumes the refresh token** (OAuth spec: refresh tokens are single-use)
6. All Hermes profiles referencing that credential pool entry now have a **dead refresh token**
7. Next token refresh attempt fails with `refresh_token_reused`

## Fix Verification (Post-Session)

After running `codex` locally and `HERMES_PROFILE=vault hermes auth`:

```json
"providers": {
  "openai-codex": {
    "access_token": "***",
    "refresh_token": "***",
    "last_auth_error": null  // ← cleared
  }
}
```

Profile starts cleanly.

## Prevention

- Avoid running `codex` CLI and Hermes profiles concurrently when both use openai-codex
- Use different providers per profile where possible (e.g., vault→nous, reviewer→openai-codex)
- Monitor `last_auth_error` in auth.json for early detection
- Consider dedicated Codex accounts per profile if isolation is critical