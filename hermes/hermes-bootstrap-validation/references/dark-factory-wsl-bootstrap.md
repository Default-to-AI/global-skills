# Dark Factory WSL bootstrap reference

Concrete patterns validated during a full WSL bootstrap.

## Clean reinstall without losing the old home

```bash
systemctl --user stop hermes-gateway 2>/dev/null || true
mv /home/linux/.hermes /home/linux/.hermes-backup-<timestamp>
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup
```

Why:
- preserves the old environment as a recovery handle
- prevents reuse of old `.env`, sessions, auth, cron, and gateway state
- avoids installer wizard stalls during a controlled bootstrap

## Codex auth + real smoke test

```bash
hermes auth add openai-codex
hermes config set model.provider openai-codex
hermes config set model.default gpt-5.4
hermes chat -q "Reply with exactly: OK" -Q --provider openai-codex -m gpt-5.4
```

Observed pitfall:
- auth succeeded, but normal chat still failed until the default provider/model was switched away from a template Anthropic config.

## Open Second Brain bootstrap

```bash
hermes plugins install itechmeat/open-second-brain --enable
~/.hermes/plugins/open-second-brain/scripts/o2b install-cli
mkdir -p /home/linux/dark-factory-brain
o2b init --vault /home/linux/dark-factory-brain --name "Dark Factory Brain" --agent-name "dark-factory" --timezone "Asia/Jerusalem"
o2b brain init --vault /home/linux/dark-factory-brain --primary-agent "dark-factory"
hermes memory setup open-second-brain
```

## `o2b doctor` codegraph pitfall

Observed behavior:
- doctor checked the wrong adjacent directory for `code_graph` and failed on an unrelated path.

Fix pattern:

```bash
cd /home/linux/.hermes/plugins/open-second-brain
codegraph init .
o2b doctor --vault /home/linux/dark-factory-brain --repo /home/linux/.hermes/plugins/open-second-brain
```

## Hermes Workflows CLI publication

Install alone was not enough; the wrapper had to be published to PATH.

```bash
hermes plugins install itechmeat/hermes-workflows --enable
ln -sf /home/linux/.hermes/plugins/hermes-workflows/bin/hermes-workflows /home/linux/.local/bin/hermes-workflows
hermes-workflows --help
```

Then verify Hermes sees workflows in tool availability.

## Minimal smoke workflow pattern

Use a manual global workflow with one agent node and explicit success/failure edges.

Key checks:

```bash
bun run /home/linux/.hermes/plugins/hermes-workflows/packages/core/src/cli.ts validate /home/linux/.hermes/workflows/global/<name>.workflow.yaml
bun run /home/linux/.hermes/plugins/hermes-workflows/packages/core/src/cli.ts compile-preview /home/linux/.hermes/workflows/global/<name>.workflow.yaml
hermes-workflows run <workflow-id>
hermes-workflows status <run-id>
```

Acceptance signal:
- the run reaches `completed`
- the node output matches the expected smoke string exactly
