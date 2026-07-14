# Ollama-cloud fallback & chat-probe notes

Condensed notes from a live gbrain Windows/MSYS session where `dream` had to use
Ollama-cloud (`minimax-m3`) with local Ollama (`qwen3:1.7b`) as a real fallback.

## Durable findings

- gbrain v0.42.x exposed an `ollama` provider but **not** a separate `ollama-cloud` recipe.
  Treat cloud-hosted Ollama as the same provider family: keep `chat_model` in `ollama:<model>`
  form and route cloud access through the Ollama base URL / API key.
- A direct cloud chat probe against `https://ollama.com/v1/chat/completions` with Bearer auth
  and model `minimax-m3` returned a valid response. That is the authoritative liveness check for
  the chat path.
- `gbrain doctor` and config parsing are not enough to prove `dream` / `autopilot` can propose.
  When chat is unreachable, those commands may still look healthy.
- For `dream` / `autopilot`, unreachable chat can degrade into a **graceful skip** with JSON like:
  - `"status": "skipped"`
  - `"phases": []`
  and still exit 0.
- Because the command can exit successfully after skipping, `chat_fallback_chain` alone does not
  guarantee a usable fallback for automation.

## Wrapper pattern

Use a wrapper script for automation commands that may skip quietly:

1. Run the cloud attempt first.
2. Capture the JSON output.
3. Detect the skip signature (`"phases": []` or `"status": "skipped"`).
4. Temporarily switch `chat_model` to a **locally loaded** fallback model.
5. Re-run locally.
6. Restore the original cloud `chat_model` afterward.

Important implementation detail:
- If the cloud model is not installed locally, the wrapper must switch the model name during the
  local attempt. Example proven in session:
  - cloud: `ollama:minimax-m3`
  - local: `ollama:qwen3:1.7b`

## Probe-first cron pattern

For recurring `dream` / cleanup jobs:

1. Run a small direct chat probe first.
2. If probe fails, report that cloud chat is down and that the wrapper may fall back locally.
3. Then run the real automation command through the wrapper.
4. In the report, note whether the wrapper logged a local fallback.

This prevents a false sense of success where the cron exits cleanly but actually produced no
proposal phases.

## Verification examples

Positive cloud proof:
- a real `dream` output contains a non-empty `phases` array including proposal work such as
  `propose_takes`.

Positive fallback proof:
- a forced-skip/mock test shows:
  - cloud attempt
  - fallback banner
  - local JSON with `propose_takes`
  - exit 0
  - `chat_model` restored to the cloud value afterward

## Boundaries

- Do not store raw provider keys in the skill or in memory.
- Do not encode temporary network failures as a permanent rule; encode the probe/wrapper pattern.
- Do not claim a separate `ollama-cloud` provider exists unless live source inspection proves it.
