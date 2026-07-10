# Auxiliary Model Smoke-Test Recipes

These recipes are distilled from a live Hermes auxiliary-model verification session. Adapt provider/model names from `config.yaml`; do not hardcode the examples as global defaults.

## Title generation

Run from the Hermes Agent repo so imports resolve:

```bash
timeout 55s python -u - <<'PY'
import json, time, traceback
from agent.title_generator import generate_title

print('START title_generation live route', flush=True)
start = time.perf_counter()
try:
    title = generate_title(
        'Verify Hermes auxiliary title generation model.',
        'Title generation should return a short descriptive title.',
        timeout=30.0,
        main_runtime=None,
    )
    print(json.dumps({
        'ok': bool(title),
        'elapsed_s': round(time.perf_counter() - start, 2),
        'title': title,
    }, ensure_ascii=False), flush=True)
except Exception as exc:
    print(json.dumps({
        'ok': False,
        'elapsed_s': round(time.perf_counter() - start, 2),
        'error': repr(exc),
        'traceback_tail': traceback.format_exc().splitlines()[-8:],
    }, ensure_ascii=False), flush=True)
PY
```

Pass condition: `ok: true` and a non-empty 3–7 word-ish title.

## Skills hub route

```bash
timeout 55s python -u - <<'PY'
import json, time, traceback
from agent.auxiliary_client import call_llm

print('START skills_hub live route', flush=True)
messages = [
    {'role': 'system', 'content': 'You are a concise skills hub router smoke-test responder. Return only JSON.'},
    {'role': 'user', 'content': 'For query "Hermes Agent configuration", return JSON with keys intent, recommended_skill, confidence. Short strings only.'},
]
start = time.perf_counter()
try:
    resp = call_llm(task='skills_hub', messages=messages, temperature=0, max_tokens=120, timeout=35)
    text = (resp.choices[0].message.content or '').strip()
    print(json.dumps({'ok': bool(text), 'elapsed_s': round(time.perf_counter() - start, 2), 'text': text}, ensure_ascii=False), flush=True)
except Exception as exc:
    print(json.dumps({'ok': False, 'elapsed_s': round(time.perf_counter() - start, 2), 'error': repr(exc)}, ensure_ascii=False), flush=True)
PY
```

Pass condition: non-empty structured text or JSON that matches the prompt.

## Vision route

Use a deterministic tiny image fixture with known content, then ask the configured vision route to describe it. If using tool calls, prefer `vision_analyze` with an absolute local path or URL. A failure like this is specific and actionable:

```text
404 — No endpoints found that support image input
```

Interpretation: the configured model/provider may be valid for text but is not a working image-input endpoint. Change `auxiliary.vision` to a model/provider that supports image input; do not generalize this into “vision is broken.”

## Image generation route

Preferred path:

1. Call the built-in `image_generate` tool.
2. Verify the returned path or URL exists/reaches and has non-zero image bytes.
3. If unavailable, read the error as setup guidance, not a permanent feature limitation.

Common setup fixes:

- FAL backend: set `FAL_KEY` or add usable Nous Portal credits.
- Krea backend: set `KREA_API_KEY`.
- Codex-auth backend: enable the bundled `image_gen/openai-codex` plugin and ensure Codex/ChatGPT OAuth credentials exist.

If a plugin was just enabled, it may take effect only in the next Hermes session. Same-session backend verification can direct-import the provider:

```bash
OPENAI_IMAGE_MODEL=gpt-image-2-low python -u - <<'PY'
import importlib.util, json, os, time
from pathlib import Path

plugin = Path('C:/Users/Tiger/AppData/Local/hermes/hermes-agent/plugins/image_gen/openai-codex/__init__.py')
spec = importlib.util.spec_from_file_location('openai_codex_image_plugin_smoke', plugin)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
provider = mod.OpenAICodexImageGenProvider()
print(json.dumps({'stage': 'availability', 'available': provider.is_available(), 'model_env': os.environ.get('OPENAI_IMAGE_MODEL')}), flush=True)

start = time.perf_counter()
result = provider.generate(
    'Minimal dark square smoke-test icon: one green check mark, three small gold dots, no text, no watermark.',
    aspect_ratio='square',
)
result['elapsed_s'] = round(time.perf_counter() - start, 2)
print(json.dumps(result, indent=2, ensure_ascii=False), flush=True)
PY
```

Pass condition: `success: true`, concrete `image` path/URL, and verified bytes/reachability.

## Reporting format

Keep the report concise:

- route name and provider/model;
- pass/fail status;
- exact returned proof or error;
- elapsed time;
- any config change and recovery handle;
- whether a restart/new session is needed.
