# Reusable Task Templates for Coding Benchmarks

## Tier 1: Simple — Single Function
```
Write a Python function that takes a list of integers and returns the sum of all even numbers. Include type hints and a docstring.
```

**Expected**: ~10-20 lines, `def sum_evens(numbers: list[int]) -> int:`, docstring, type hints

---

## Tier 2: Medium — Class with State & Concurrency
```
Implement a thread-safe LRU cache in Python with get/put operations, max size, and TTL expiration. Include tests.
```

**Expected**: 
- `class LRUCache:` with `__init__(maxsize: int, ttl: float)`
- `get(key) -> Optional[Any]`, `put(key, value) -> None`
- `threading.RLock` or `asyncio.Lock` for thread-safety
- TTL cleanup (background thread or lazy expiry)
- Tests: basic ops, eviction, TTL expiry, thread safety

---

## Tier 3: Hard — Production Component with Metrics & Dynamic Config
```
Design a Python async rate limiter using token bucket algorithm that works across multiple asyncio tasks. Support dynamic rate changes, burst allowance, and provide metrics (requests allowed, rejected, current tokens). Write clean, production-ready code with comprehensive tests.
```

**Expected**:
- `class AsyncTokenBucketRateLimiter:` with `__init__(rate: float, burst: int)`
- `acquire() -> bool` (async, returns True if allowed)
- `update_rate(new_rate: float, new_burst: Optional[int] = None)` (dynamic config)
- `metrics` property returning `RateLimitMetrics(allowed: int, rejected: int, current_tokens: float)`
- `time.monotonic()` for refill (immune to clock changes)
- `asyncio.Lock` for thread-safety across tasks
- Comprehensive tests: basic limiting, burst, dynamic update, metrics, concurrent access
- Type hints throughout, docstrings, `__slots__` for performance

---

## Variant Templates (for language/domain coverage)

### Rust Version (Tier 2)
```
Implement a thread-safe LRU cache in Rust with get/put, max size, and TTL. Use `std::sync::RwLock` or `parking_lot`. Include tests.
```

### Go Version (Tier 2)
```
Implement a thread-safe LRU cache in Go with get/put, max size, and TTL. Use `sync.RWMutex`. Include tests.
```

### Kubernetes Manifest (Tier 3 variant)
```
Create a production-ready Kubernetes Deployment + Service + HPA for a stateless API service. Include: resource limits, liveness/readiness probes, pod disruption budget, network policy, and Prometheus ServiceMonitor. Output as kustomize overlay structure.
```

### React Component (Tier 2 variant)
```
Build an accessible, typed React component: virtualized list with windowing, keyboard navigation, and loading skeleton. Use TanStack Virtual or react-window. TypeScript, CSS modules, Storybook stories.
```

---

## Execution Parameters (Standardized)
```python
PARAMS = {
    "temperature": 0.1,
    "max_tokens": 4096,
    "top_p": 0.95,
    "stream": False
}
```

## Verification Checklist (per response)
- [ ] Valid JSON response parsed
- [ ] `message.content` non-empty
- [ ] Python: `python -m py_compile <file>` passes
- [ ] Python: `pytest <test_file>` passes (if tests included)
- [ ] Key patterns present (type hints, docstrings, async/await for async tasks)