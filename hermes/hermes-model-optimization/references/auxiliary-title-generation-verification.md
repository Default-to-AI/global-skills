# Auxiliary Title Generation Verification

Use this reference when validating whether a Hermes auxiliary `title_generation` model assignment is actually working, especially after moving it to OpenRouter or another cheaper provider.

## Core lesson

Manual session renaming is not a valid test of the Title generation auxiliary model. Commands such as `hermes sessions rename <id> <title>` bypass the auxiliary title-generation path completely.

A valid check must exercise Hermes' `title_generation` auxiliary task itself, then inspect logs/config for the provider/model used.

## What to verify

1. Confirm the configured slot in `config.yaml`:
   - `auxiliary.title_generation.provider`
   - `auxiliary.title_generation.model`
2. Trigger the actual title-generation path, not a manual rename.
3. Inspect `logs/agent.log` for lines like:
   - `agent.auxiliary_client: Auxiliary title_generation: using <provider> (<model>) at <base_url>`
4. Treat hangs/timeouts/empty streams as failed runtime verification even if the config is correct.

## Known pitfall

Large/free OpenRouter models can be poor choices for title generation even though the task is easy. Title generation needs low latency and reliable short completions, not raw model size. Prefer fast, stable, inexpensive models over giant free models.

## Direct probe pattern

If normal UI/session creation does not trigger title generation, a direct Python probe from the Hermes agent checkout can exercise the same helper path:

```bash
cd /c/Users/Tiger/AppData/Local/hermes/hermes-agent
./venv/Scripts/python.exe - <<'PY'
from agent.title_generator import generate_title

title = generate_title(
    'Can we verify auxiliary title generation?',
    'Yes, verify the configured title-generation model.',
    timeout=45,
)
print('TITLE_RESULT=' + repr(title))
PY
```

After the probe, check `logs/agent.log` and `logs/errors.log`. If the probe hangs beyond the requested timeout or the terminal timeout, kill the stray process and report that the route is configured but the selected model is not runtime-reliable.

## Reporting standard

Distinguish clearly between:

- **Config verified**: the slot points to the expected provider/model.
- **Runtime verified**: the actual auxiliary call returned and logs show the expected provider/model.
- **Failed runtime verification**: config is set, but the model hangs, drops streams, or returns no usable title.
