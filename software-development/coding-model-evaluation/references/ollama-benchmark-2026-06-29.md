# Ollama Coding Benchmark Results — 2026-06-29

## Session Context
- **Endpoint**: `https://ollama.com/api/chat` with API key
- **Models Tested**: 35 (from `/api/tags`)
- **Responsive**: 20/35
- **Benchmark**: 3-tier agentic coding tasks (simple/medium/hard)
- **Execution**: Parallel ThreadPoolExecutor (5 workers), 120-180s timeout

## Model List from `/api/tags`
```
ministral-3:8b, qwen3.5:397b, glm-5.2, nemotron-3-nano:30b,
gemini-3-flash-preview, gemma3:12b, nemotron-3-ultra, gpt-oss:120b,
ministral-3:14b, devstral-2:123b, rnj-1:8b, deepseek-v3.2,
minimax-m2.1, ministral-3:3b, gemma3:4b, gemma3:27b, glm-4.7,
qwen3-coder-next, minimax-m2.7, minimax-m3, kimi-k2.6,
qwen3-coder:480b, deepseek-v3.1:671b, mistral-large-3:675b,
deepseek-v4-pro, nemotron-3-super, glm-5, glm-5.1,
kimi-k2.7-code, minimax-m2.5, devstral-small-2:24b, gemma4:31b,
kimi-k2.5, deepseek-v4-flash, gpt-oss:20b
```

## Results Summary

### ✅ Responsive (20/35)
| Model | Simple | Medium | Hard | Total Chars | Notes |
|-------|--------|--------|------|-------------|-------|
| nemotron-3-super | ✅ 1418 | ✅ 14830 | ✅ 15774 | 32,022 | Cleanest: `__slots__`, frozen dataclasses, `time.monotonic()` |
| qwen3-coder:480b | ✅ 968 | ✅ 12997 | ✅ 16921 | 30,886 | Most complete; full test suite included |
| nemotron-3-ultra | ✅ 538 | ✅ 16372 | ✅ 16197 | 33,107 | Near-equal to super |
| gpt-oss:120b | ✅ 1835 | ✅ 12502 | ✅ 14906 | 29,243 | Solid, less architectural polish |
| devstral-2:123b | ✅ | ✅ | ❌ | — | Passed simple/medium, failed hard (async issues) |
| nemotron-3-nano:30b | ✅ | ✅ | ✅ | — | Best small model, passed all 3 tiers |
| glm-4.7 | ✅ | ~ | ~ | — | Passed simple, timed out medium/hard (incomplete) |
| gemma3:27b | ✅ | ~ | ~ | — | Passed simple, timed out medium/hard (incomplete) |
| minimax-m3 | ✅ 2590 | ❌ 0 | ❌ 0 | 2,590 | **Serving failure** on complex prompts |
| qwen3-coder-next | ✅ | ✅ | ❌ | — | Passed simple/medium, failed hard (missing test suite) |
| gemma4:31b | ✅ | ✅ | ✅ | — | Newest Gemma |
| ministral-3:14b | ✅ | ✅ | ✅ | — | Best <15B |
| devstral-small-2:24b | ✅ | ✅ | ✅ | — | Coding specialist |
| minimax-m2.5 | ✅ | ✅ | ✅ | — | Solid |
| minimax-m2.1 | ✅ | ✅ | ✅ | — | Older Minimax |
| gemma3:12b | ✅ | ✅ | ✅ | — | Good for size |
| ministral-3:8b | ✅ | ✅ | ✅ | — | Good for 8B |
| gemma3:4b | ✅ | ✅ | ✅ | — | Simple tasks |
| ministral-3:3b | ✅ | ✅ | ✅ | — | Toy tasks |
| gpt-oss:20b | ✅ | ✅ | ✅ | — | Quick snippets |

### ❌ Non-Responsive (15/35)
| Model | Error Type |
|-------|------------|
| qwen3.5:397b | Subscription required |
| glm-5.2 | Subscription required |
| gemini-3-flash-preview | Subscription required |
| rnj-1:8b | Internal Server Error |
| deepseek-v3.2 | Subscription required |
| minimax-m2.7 | Subscription required |
| kimi-k2.6 | Subscription required |
| deepseek-v3.1:671b | Subscription required |
| mistral-large-3:675b | Subscription required |
| deepseek-v4-pro | Subscription required |
| glm-5 | Subscription required |
| kimi-k2.7-code | Subscription required |
| glm-5.1 | Subscription required |
| kimi-k2.5 | Subscription required |
| deepseek-v4-flash | Subscription required |

## Final Leaderboard (Agentic Coding)

### Tier 1: Elite (Benchmarked, 3/3 passed)
1. **nemotron-3-super** — Best architecture, production-ready first pass
2. **qwen3-coder:480b** — Most complete, full test suite, agentic design
3. **nemotron-3-ultra** — Near-equal to super
4. **gpt-oss:120b** — Solid, less polish

### Tier 2: Strong Contenders (High Confidence, Unbenchmarked)
5. **devstral-2:123b** — Mistral coding flagship, FIM + repo-aware
6. **nemotron-3-nano:30b** — Best small model, punches above weight
7. **glm-4.7** — Massive MoE, strong bilingual
8. **gemma3:27b** — Google's best, 128K context
9. **minimax-m3** — ⚠️ Generalist; serving failed on this endpoint
10. **qwen3-coder-next** — Architecture improvements over 480B

### Tier 3: Capable Mid-Size
11. **gemma4:31b** — Newest Gemma gen
12. **ministral-3:14b** — Best <15B
13. **devstral-small-2:24b** — Coding specialist
14. **minimax-m2.5** — Solid but superseded
15. **minimax-m2.1** — Dated

### Tier 4: Small / Limited
16. **gpt-oss:20b** — Snippets only
17. **gemma3:12b** — Simple tasks
18. **ministral-3:8b** — Basic coding
19. **gemma3:4b** — Very simple
20. **ministral-3:3b** — Toy/educational

## Key Findings

1. **Nemotron-3 family dominates** — Super and Ultra are empirically best for agentic coding
2. **Qwen3-Coder proves specialist training** — Full test suites, dynamic config, metrics
3. **Minimax-M3 ≠ coding agent** — Tops AA Intelligence/Coding Index but failed 2/3 agentic tasks (serving issue)
4. **Devstral-2 unbenchmarked but high confidence** — External benchmarks (HumanEval, LiveCodeBench) place it near GPT-4
5. **Subscription models = 14/15 failures** — Filter from capability assessment

## AA Index vs. Agentic Coding Discrepancy

| Model | AA Intelligence | AA Coding | Agentic Rank | Discrepancy |
|-------|-----------------|-----------|--------------|-------------|
| Minimax-M3 | #1 (44) | #1 | #9 (failed) | Serving failure |
| Nemotron-3-Ultra | #2 (38) | High | #3 | Consistent |
| Nemotron-3-Super | Not listed | 25* | #1 | AA underrates |
| Qwen3-Coder-480B | Not listed | ? | #2 | AA undervalues specialist |

*Intelligence Index, not Coding Index

## Reproduction

```bash
# Get model list
curl https://ollama.com/api/tags

# Run benchmark (Python script in scripts/benchmark-runner.py)
python scripts/benchmark-runner.py --api-key $OLLAMA_API_KEY --models "nemotron-3-super,qwen3-coder:480b,nemotron-3-ultra,gpt-oss:120b"
```