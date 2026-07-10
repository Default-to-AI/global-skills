# Extensive Session Configuration for Hermes Agent

## Security Restriction

**The Hermes agent CANNOT modify its own config files directly.** Attempting to use `patch` or `write_file` on `~/.hermes/config.yaml` or any `~/.hermes/profiles/*/config.yaml` will fail with:

```
Refusing to write to Hermes config file: C:\Users\Tiger\AppData\Local\hermes\config.yaml
Agent cannot modify security-sensitive configuration. Edit ~/.hermes/config.yaml directly or use 'hermes config' instead.
```

**Always use the `hermes config set` CLI for config changes.**

---

## Settings for Extensive Work Sessions

### Main Config (`~/.hermes/config.yaml`)

| Setting | Default | Extensive Session Value | Command |
|---------|---------|------------------------|---------|
| `agent.max_turns` | 90 | 500 | `hermes config set agent.max_turns 500` |
| `code_execution.max_tool_calls` | 50 | 500 | `hermes config set code_execution.max_tool_calls 500` |
| `delegation.max_iterations` | 50 | 500 | `hermes config set delegation.max_iterations 500` |
| `delegation.child_timeout_seconds` | 600 | 3600 | `hermes config set delegation.child_timeout_seconds 3600` |
| `goals.max_turns` | 20 | 500 | `hermes config set goals.max_turns 500` |

### Per-Profile Configs (`~/.hermes/profiles/<name>/config.yaml`)

Each profile has its own `agent.max_turns` and `goals.max_turns`. Engineer also has `delegation.max_iterations`.

```bash
# Engineer profile (used for implementation/debugging)
hermes config set agent.max_turns 500 --profile engineer
hermes config set delegation.max_iterations 500 --profile engineer
hermes config set delegation.child_timeout_seconds 3600 --profile engineer
hermes config set goals.max_turns 500 --profile engineer

# Strategist profile (used for planning/reasoning)
hermes config set agent.max_turns 500 --profile strategist
hermes config set goals.max_turns 500 --profile strategist

# Reviewer profile (used for QA/audit)
hermes config set agent.max_turns 500 --profile reviewer
hermes config set goals.max_turns 500 --profile reviewer

# Vault profile (used for knowledge maintenance)
hermes config set agent.max_turns 500 --profile vault
hermes config set goals.max_turns 500 --profile vault

# Writer profile (used for docs/prose)
hermes config set agent.max_turns 500 --profile writer
hermes config set goals.max_turns 500 --profile writer
```

### Applying All at Once

```bash
# Main config
hermes config set agent.max_turns 500
hermes config set code_execution.max_tool_calls 500
hermes config set delegation.max_iterations 500
hermes config set delegation.child_timeout_seconds 3600
hermes config set goals.max_turns 500

# All profiles
for p in engineer strategist reviewer vault writer; do
  hermes config set agent.max_turns 500 --profile "$p"
  hermes config set goals.max_turns 500 --profile "$p"
done
# Engineer also needs delegation settings
hermes config set delegation.max_iterations 500 --profile engineer
hermes config set delegation.child_timeout_seconds 3600 --profile engineer
```

### Verification

```bash
# Check main config
hermes config get agent.max_turns
hermes config get code_execution.max_tool_calls
hermes config get delegation.max_iterations
hermes config get delegation.child_timeout_seconds
hermes config get goals.max_turns

# Check per-profile
for p in engineer strategist reviewer vault writer; do
  echo "=== $p ==="
  hermes config get agent.max_turns --profile "$p"
  hermes config get goals.max_turns --profile "$p"
done
```

---

## Important Notes

1. **Restart required** — Config changes take effect on new session. In CLI: exit and relaunch. In gateway: `/restart` or `hermes gateway restart`.

2. **Session reset** — Tool/skill enablement changes also need `/reset` (new session) or process restart.

3. **Profile isolation** — Each profile has fully isolated config. Changes to one don't affect others.

4. **Windows paths** — Config lives at `%LOCALAPPDATA%\hermes\config.yaml` and `%LOCALAPPDATA%\hermes\profiles\<name>\config.yaml`

5. **YAML BOM** — If `hermes config edit` opens in Notepad, ensure it saves as UTF-8 **without BOM** or `hermes` will error with "HTTP 400 No models provided".

---

## Related

- Main skill: `hermes-agent` (configuration, profiles, troubleshooting)
- Profile management: `references/profile-skill-audit-prune.md`
- Windows quirks: `references/windows-cli-desktop-path-map.md`