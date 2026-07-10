# Live Smoke Snippets

Reusable snippets for validating Hermes auxiliary routes. Run from the `hermes-agent` checkout so imports resolve.

## Title generation

```bash
python -u - <<'PY'
import json, time, traceback
from agent.title_generator import generate_title

start = time.perf_counter()
try:
    title = generate_title(
        'Verify Hermes auxiliary title generation model.',
        'Title generation should return a short descriptive title.',
        timeout=30.0,
        main_runtime=None,
    )
    print(json.dumps({'ok': bool(title), 'elapsed_s': round(time.perf_counter()-start, 2), 'title': title}, ensure_ascii=False))
except Exception as exc:
    print(json.dumps({'ok': False, 'elapsed_s': round(time.perf_counter()-start, 2), 'error': repr(exc), 'traceback_tail': traceback.format_exc().splitlines()[-8:]}, ensure_ascii=False))
PY
```

## Skills hub

```bash
python -u - <<'PY'
import json, time, traceback
from agent.auxiliary_client import call_llm

messages = [
    {'role': 'system', 'content': 'You are a concise skills hub router smoke-test responder. Return only JSON.'},
    {'role': 'user', 'content': 'For query "Hermes Agent configuration", return JSON with keys intent, recommended_skill, confidence. Short strings only.'},
]
start = time.perf_counter()
try:
    resp = call_llm(task='skills_hub', messages=messages, temperature=0, max_tokens=120, timeout=35)
    text = (resp.choices[0].message.content or '').strip()
    print(json.dumps({'ok': bool(text), 'elapsed_s': round(time.perf_counter()-start, 2), 'text': text}, ensure_ascii=False))
except Exception as exc:
    print(json.dumps({'ok': False, 'elapsed_s': round(time.perf_counter()-start, 2), 'error': repr(exc), 'traceback_tail': traceback.format_exc().splitlines()[-8:]}, ensure_ascii=False))
PY
```

## Vision with explicit provider/model override

Use this when `vision_analyze` still appears to use stale config after a config change.

```bash
python -u - <<'PY'
import base64, json, mimetypes, time, traceback
from pathlib import Path
from agent.auxiliary_client import call_llm

p = Path('C:/Users/Tiger/path/to/image.png')
print(json.dumps({'exists': p.exists(), 'size_bytes': p.stat().st_size if p.exists() else None, 'path': str(p)}), flush=True)
if not p.exists():
    raise SystemExit(2)

mime = mimetypes.guess_type(str(p))[0] or 'image/png'
data = base64.b64encode(p.read_bytes()).decode('ascii')
messages = [{
    'role': 'user',
    'content': [
        {'type': 'text', 'text': 'Describe this image in one concise paragraph. Transcribe visible text exactly.'},
        {'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{data}'}},
    ],
}]

start = time.perf_counter()
try:
    resp = call_llm(
        task='vision',
        provider='openai-codex',
        model='gpt-5.5',
        messages=messages,
        max_tokens=500,
        temperature=0.1,
        timeout=120,
    )
    text = (resp.choices[0].message.content or '').strip()
    print(json.dumps({'ok': bool(text), 'elapsed_s': round(time.perf_counter()-start, 2), 'analysis': text}, ensure_ascii=False, indent=2))
except Exception as exc:
    print(json.dumps({'ok': False, 'elapsed_s': round(time.perf_counter()-start, 2), 'error': repr(exc), 'traceback_tail': traceback.format_exc().splitlines()[-12:]}, ensure_ascii=False, indent=2))
PY
```

## Codex image generation backend direct smoke test

Use this after enabling the bundled `image_gen/openai-codex` plugin when the current session has not reloaded the image generation registry.

```bash
OPENAI_IMAGE_MODEL=gpt-image-2-low python -u - <<'PY'
import importlib.util, json, os, time, traceback
from pathlib import Path

plugin = Path('C:/Users/Tiger/AppData/Local/hermes/hermes-agent/plugins/image_gen/openai-codex/__init__.py')
spec = importlib.util.spec_from_file_location('openai_codex_image_plugin_smoke', plugin)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
provider = mod.OpenAICodexImageGenProvider()
print(json.dumps({'stage': 'availability', 'available': provider.is_available(), 'model_env': os.environ.get('OPENAI_IMAGE_MODEL')}), flush=True)

start = time.perf_counter()
prompt = 'Minimal dark square smoke-test icon: one green check mark, three small gold dots, no text, no watermark.'
try:
    result = provider.generate(prompt, aspect_ratio='square')
    result['elapsed_s'] = round(time.perf_counter() - start, 2)
    print(json.dumps(result, indent=2, ensure_ascii=False), flush=True)
except Exception as exc:
    print(json.dumps({'success': False, 'elapsed_s': round(time.perf_counter()-start, 2), 'error': repr(exc), 'traceback_tail': traceback.format_exc().splitlines()[-10:]}, indent=2), flush=True)
PY
```

## Config commands

```bash
# Create recovery handle first.
ts=$(date +%Y%m%d_%H%M%S)
cp /c/Users/Tiger/AppData/Local/hermes/config.yaml /c/Users/Tiger/AppData/Local/hermes/.hermes/backups/config-before-aux-change-$ts.yaml

# Use hermes config set; direct patch/file edits may be blocked for config.yaml.
hermes config set auxiliary.vision.provider openai-codex
hermes config set auxiliary.vision.model gpt-5.5
hermes plugins enable openai-codex
```
