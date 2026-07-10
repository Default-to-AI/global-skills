# Windows GitHub HTTPS auth + non-embed verification

## Durable lesson from this setup pass

Two independent issues can stack during gbrain bootstrap and look like one failure:

1. **Git transport mismatch** — the artifacts initializer may advertise a canonical HTTPS remote while still deriving an SSH-form push path.
2. **Embedding-provider setup gap** — source wireup may succeed through source creation, then fail during `gbrain sync` because the configured embedding provider requires an API key that is not set yet.

Treat them separately.

## Reliable sequence

### A. Force HTTPS transport when the machine is authenticated with `gh`

```bash
gh auth setup-git >/dev/null 2>&1 || true
GIT_CONFIG_COUNT=1 \
GIT_CONFIG_KEY_0=url.https://github.com/.insteadOf \
GIT_CONFIG_VALUE_0=git@github.com: \
bin/gstack-artifacts-init --remote https://github.com/<owner>/<repo> --url-form-supported false
git -C ~/.gstack config url.https://github.com/.insteadOf git@github.com:
```

The per-command rewrite gets the initializer through bootstrap; the `git -C ~/.gstack config ...` line makes future pushes from the artifacts repo honor HTTPS too.

### B. If strict wireup fails on embeddings, prove the core path first

Typical failing pattern:
- source gets created
- worktree exists
- `gbrain sync` aborts with an embedding-model API-key complaint

Verification command:

```bash
gbrain sync --repo ~/.gstack-brain-worktree --no-embed --yes
```

Interpretation:
- If this succeeds, the DB URL, worktree, and source registration are fine.
- Remaining work is only embedding-provider configuration.

## Notes on output interpretation

### Safe to ignore during this phase

- `Prepared statements disabled (PgBouncer transaction-mode convention on port 6543)`
- `Detached HEAD ... skipping git pull`
- `0 markdown files`

These do not invalidate the bootstrap by themselves.

### Requires action

- Any error indicating Git cannot authenticate/push because it is still using `git@github.com:` on a machine without SSH key auth.
- Any source add/remove error showing the source path is not the intended worktree.
- Embedding-model errors only after the non-embed verification is already clean.
