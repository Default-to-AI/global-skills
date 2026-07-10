# Hermes Model Pricing Reference — June 2026

This file is a **starting shortcut**, not a decision boundary. When optimizing models, check available subscriptions first — a Codex/Portal/Groq subscription at zero marginal cost beats any OpenRouter paid pricing.

## Subscription-First Selection Order

1. Subscription-covered providers first: OpenAI Codex, Nous Portal, Groq, etc.
2. OpenRouter free-tier models second: anything with the `:free` suffix.
3. OpenRouter paid models last.

When the user has subscription access, prefer that provider for aux and delegation unless the task has a specific quality reason to use a paid OpenRouter model.

## OpenRouter Auxiliary Model Pricing (paid tier)


Snapshot from OpenRouter `/api/v1/models` on 2026-06-10. Prices are per 1M tokens.
Update this when new Flash/Lite generations drop.

## Current Best-Value Models

| Model ID | Prompt | Completion | Vision | Context | Notes |
|----------|--------|------------|--------|---------|-------|
| `google/gemini-2.5-flash` | $0.30 | $2.50 | ✅ text+image+audio+video+file | 1M | Best all-around aux. Use for Vision, Curator |
| `google/gemini-2.5-flash-lite` | $0.10 | $0.40 | ✅ text+image+audio+video+file | 1M | Cheapest with vision. Use for all text-only slots |
| `google/gemini-3.1-flash-lite` | $0.25 | $1.50 | ✅ text+image+video+file+audio | 1M | Newer gen, better than 2.5 Flash Lite. Use if 2.5 Flash Lite retires |
| `google/gemini-3.5-flash` | $1.50 | $9.00 | ✅ text+image+video+file+audio | 1M | Near-Pro quality. Too expensive for aux unless Vision quality is critical |
| `openai/gpt-5.4-nano` | $0.20 | $1.25 | ✅ text+image+file | 400K | OpenAI's cheapest. Decent alternative to Gemini Lite |
| `openai/gpt-5.4-mini` | $0.75 | $4.50 | ✅ text+image+file | 400K | Too expensive for aux vs Gemini equivalents |
| `meta-llama/llama-4-maverick` | $0.15 | $0.60 | ✅ text+image | 1M | Free-tier available. Good alternative, slightly weaker at vision |
| `qwen/qwen3.7-plus` | $0.40 | $1.60 | ✅ text+image | 1M | Solid all-rounder |
| `stepfun/step-3.7-flash` | $0.20 | $1.15 | ✅ text+image+video | 256K | Cheapest with video support |

## Model Selection Rules (subscription-first)

1. **Subscription providers beat OpenRouter paid routing** — if a paid subscription covers the task, use it. Free at the margin vs $0.10–$2.50/M OpenRouter pricing.
2. **OpenRouter free tier second** — free `:free` models are viable for non-critical text aux slots when subscription quota is stressed.
3. **Vision → strongest available at zero marginal cost** — if the subscription gives a vision-capable model (e.g. `o4-mini` on Codex), use it for routine auxiliary vision. Quality trade-off is acceptable vs paying $0.30/M for Google Flash. Reserve Google Flash for vision-critical use cases only.
4. **MCP** → auto (main model) — MCP tool routing is tightly coupled to main model behavior. Leave untouched.
5. **Simplification** — one subscription model for all text aux slots. Price gaps between flash and lite vanish when everything is covered by subscription.

## How to Refresh This Data

```bash
curl -s "https://openrouter.ai/api/v1/models" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for m in data['data']:
    n=m['name'].lower()
    if any(t in n for t in ['flash-lite','flash','nano','mini','maverick','scout']):
        p=m.get('pricing',{})
        print(f\"{m['id']:55s} prompt={p.get('prompt','?'):>12s} comp={p.get('completion','?'):>12s}\")
"
```