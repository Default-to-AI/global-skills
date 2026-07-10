# Shell Hook Enforcement Boundary

Session lesson: vault profile hooks enforce `pre_tool_call` on the outer Hermes tool invocation. They do not act as filesystem monitors for subprocess writes.

## Proven boundary

- Direct `write_file` / `patch` calls can be blocked by target path.
- `terminal` hooks inspect only the command string. If the command is `python scripts/build_catalog.py`, the hook does not see that the script later writes `vault-index.md`.
- `execute_code` can write via Python APIs or subprocesses unless separately guarded or disallowed for vault writes.

## Mutation paths to remember

- `python scripts/build_catalog.py` writes `vault-index.md` through `build_catalog()`.
- `python scripts/build_index.py "Agent Skills"` writes `Agent Skills/wiki/index.md` through `build_domain_index(domain)`.
- Direct patches to ordinary out-of-scope domain pages are not blocked unless policy protects them; scope must be enforced by workflow, not only path deny rules.

## Recommended guardrail shape

1. Treat target-domain ingestion and global vault repair as different modes.
2. During ingestion, allow only target-domain raw/wiki/index/log changes plus explicitly planned related notes.
3. Run global audit commands read-only by default.
4. Require approval for mutating global scripts such as `build_catalog.py` write mode or `build_index.py` for unrelated domains.
5. Require an explicit `HERMES_VAULT_TARGET_DOMAIN='<Domain>'` marker before allowing `build_index.py '<Domain>'` during ingestion.
6. Add `execute_code` screening so raw Python cannot silently write protected or out-of-scope vault files.
7. Add a final changed-path check before reporting ingestion success.
