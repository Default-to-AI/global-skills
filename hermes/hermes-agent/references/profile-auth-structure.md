# Hermes Profile auth.json — Annotated Schema

## Top-Level Structure

```json
{
  "version": 1,
  "providers": { "provider-name": { ...current active tokens... } },
  "credential_pool": { "provider-name": [ { ...stored credentials... } ] },
  "active_provider": "provider-name",
  "updated_at": "ISO8601",
  "suppressed_sources": { "provider-name": ["source-id", ...] }
}
```

## `providers.<name>` — Active Token Set

What the profile **currently uses** for requests. Updated on successful refresh or re-auth.

```json
"openai-codex": {
  "access_token": "***",      // Short-lived access token
  "refresh_token": "***",     // Refresh token (single-use per OAuth spec)
  "last_auth_error": {              // Present only on failure
    "provider": "openai-codex",
    "code": "refresh_token_reused", // Error code
    "message": "Human-readable...",
    "reason": "credential_pool_refresh_failure",
    "relogin_required": true,       // User action needed
    "at": "2026-06-06T02:54:26.419041+00:00"
  },
  "base_url": "https://chatgpt.com/backend-api/codex"
}
```

**Key fields:**
- `last_auth_error` — **Diagnostic goldmine**. If present, profile is blocked. `relogin_required: true` means `hermes auth` needed.
- `expires_at` / `expires_in` — For providers that include them (nous, etc.)

## `credential_pool.<name>[]` — Stored Credentials

Array of credential entries available for rotation. Each entry:

```json
{
  "id": "473ea6",                          // Unique pool entry ID
  "label": "openai-codex-oauth-1",         // Human label
  "auth_type": "oauth",                    // "oauth" | "api_key"
  "priority": 0,                           // Rotation priority (lower = preferred)
  "source": "manual:device_code",          // Origin: "device_code", "manual:device_code", "env:VAR", "gh_cli"
  "access_token": "***",             // Current access token (may be stale)
  "refresh_token": "***",            // Refresh token (critical for OAuth)
  "last_status": "ok" | "exhausted" | null,// Last known health
  "last_status_at": 1780357990.3567476,    // Unix timestamp of last check
  "last_error_code": 429,                  // If last_status != "ok"
  "last_error_reason": "usage_limit_reached",
  "last_error_message": "The usage limit has been reached",
  "last_error_reset_at": 1780361063.0,     // When quota resets (unix)
  "base_url": "https://chatgpt.com/backend-api/codex",
  "last_refresh": "2026-05-25T14:19:18.772565Z", // Last successful refresh
  "request_count": 0                       // Usage counter
}
```

**Critical observations:**
- Same `id` across profiles = **shared token** = shared failure domain
- `source: "manual:device_code"` → came from `~/.codex/auth.json` via `hermes auth`
- `last_status: "exhausted"` + `last_error_reason: "usage_limit_reached"` = quota hit
- `suppressed_sources` in root prevents auto-discovery from re-adding known-bad sources

## `active_provider` — Routing Target

Single string: which provider the profile routes LLM calls to. Must have valid entry in `providers.<name>` or `credential_pool.<name>[]`.

## `suppressed_sources` — Auto-Discovery Blocklist

```json
"suppressed_sources": {
  "openai-codex": ["device_code"],
  "gemini": ["env:GOOGLE_API_KEY", "env:GEMINI_API_KEY"],
  "deepseek": ["env:DEEPSEEK_API_KEY"]
}
```

Prevents Hermes from repeatedly trying known-failing credential sources during auto-discovery.

## Profile Config Link

`~/.hermes/profiles/<name>/config.yaml`:
```yaml
model:
  provider: openai-codex   # Must match a provider with valid auth
```

If `model.provider` points to a provider with no valid credentials in `auth.json`, profile fails at startup.