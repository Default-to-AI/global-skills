# React legacy runtime integration tests

Use this reference when a large React/Vite monolith needs proof that shared logic or shared UI is actually wired at runtime.

## Pattern

1. Prefer SSR rendering (`renderToStaticMarkup`) of the real component/page when browser-level tests are not available.
2. Seed browser state explicitly before render:
   - define `globalThis.window` with `localStorage.getItem/setItem/removeItem/clear`;
   - populate the exact persisted keys that drive the mode/input under test.
3. Mock only unrelated heavy dependencies:
   - chart containers/axes/series can be replaced with passthrough/null components when the chart is not the assertion target;
   - keep the component under test and shared logic/display real.
4. Assert semantic runtime output, not source text:
   - `data-decision="fail-to-reject"` / `data-decision="reject"`;
   - visible Hebrew labels for mode contracts;
   - exact boundary cases that reproduced the failure;
   - representative variants across modes/tails when divergence risk was reported.
5. Console discipline:
   - spy on `console.error` during render;
   - filter only a known benign legacy SSR warning if unavoidable;
   - throw on any unexpected console error.
6. Cold-start handling:
   - first isolated run of a large monolith test can be slower because Vite/Vitest transforms KaTeX/charts/React dependencies;
   - if repeated reruns pass and the test is behaviorally correct, set a focused per-test timeout or reduce harness weight rather than falling back to source-grep.

## Anti-pattern caught

A source-grep “integration” test that checks imports, variable names, or string counts can pass while math/state wiring is wrong. Use grep only for static cleanup facts, never as the sole proof for business logic or UI behavior.

## Example assertions

```tsx
expect(html).toContain('data-decision="fail-to-reject"');
expect(renderCalculator({ HT_testType: 'single' })).toContain('ערך בודד');
expect(renderCalculator({ HT_testType: 'mean' })).toContain('ממוצע מדגם');
expect(renderCalculator({ HT_testType: 'sum' })).toContain('סכום מדגם');
```
