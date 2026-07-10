# Fallback Provider Verification

Use this note when Robert asks whether Hermes fallback providers are **actually wired and working**, not just present in `config.yaml`.

## What this session established

### 1. Parser truth beats YAML appearance
Hermes reads `fallback_providers` via `hermes_cli/fallback_config.py`, which accepts only dict-shaped entries with `provider` and `model` keys.

Works:

```yaml
fallback_providers:
  - provider: openrouter
    model: nvidia/nemotron-3-super-12b-a12b:free
```

Does **not** work:

```yaml
fallback_providers:
  - openrouter:nvidia/nemotron-3-super-12b-a12b:free
```

A string entry is ignored. The fastest proof is:

```bash
hermes fallback list
```

If the output says `No fallback providers configured`, the runtime chain is empty.

## 2. Safe live smoke test pattern
Do not break the user's real profile to test fallback. Use a temporary `HERMES_HOME`.

Minimal pattern:
1. Create a temp dir.
2. Copy `.env` and `auth.json` into it.
3. Write a minimal `config.yaml` with:
   - a deliberately broken **primary** endpoint (`http://127.0.0.1:9/...` is useful for connection failure),
   - a correctly-shaped fallback entry.
4. Run:

```bash
HERMES_HOME="$TMP_HOME" hermes fallback list
HERMES_HOME="$TMP_HOME" hermes chat -q 'Reply with exactly FALLBACK_OK' -Q --ignore-rules --source tool
HERMES_HOME="$TMP_HOME" hermes logs agent --since 5m --level INFO -n 200
```

## 3. How to read the outcome

### Good activation proof
Look for log lines like:

- `Fallback activated: <primary> → <fallback> (<provider>)`
- request lines showing the fallback provider + model

That proves the **mechanism** worked.

### Distinguish mechanism failure from target failure
If the logs show `Fallback activated` and the request still dies with something like:

- `HTTP 400: <model> is not a valid model ID`

then Hermes fallback is working, but the configured fallback target is bad.

## 4. Recommended operator sequence
1. `hermes fallback list` — parser sanity check
2. temp-home smoke test — mechanism check
3. log inspection — distinguish activation vs invalid fallback model/provider

## Session-specific finding captured here
The specific string shorthand form below looked plausible in `config.yaml` but was ignored by Hermes:

```yaml
fallback_providers:
  - openrouter:nvidia/nemotron-3-super-12b-a12b:free
```

After converting to dict shape, Hermes recognized the chain, activated fallback correctly, and then failed later because the OpenRouter model ID itself was invalid. That distinction matters: **first bug = inert config shape, second bug = invalid fallback target**.
