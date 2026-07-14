# Revalidating plan assumptions before execution

Use this when the plan came from an earlier review pass, especially in monorepos or split frontend/backend repos.

## Why
A plan can contain correct structure but wrong premises. High-severity findings from a review are often based on whichever config file was read first. In monorepos, that can be a root stub instead of the active app package.

## Mandatory re-checks before touching files
1. Verify the active workspace/subproject path, not just the repo root.
2. Re-open the exact runtime/config file that governs the target (`package.json`, test config, build config, app entrypoint).
3. Re-run the claimed missing verification command in the real subproject before repeating the claim.
4. If the plan is based on your own prior review, treat every P0/P1 claim as untrusted until re-verified live.

## Concrete pitfall
- **False positive:** declaring "no test runner configured" from a root `package.json` stub.
- **Correct check:** inspect the target app's package file and test config (`web/package.json`, `vitest.config.ts`, etc.), then run the real test command in that subproject.

## What to do when the claim is wrong
- Retract it explicitly.
- Update todo/plan wording before continuing.
- Execute the real gap, not the stale one.

## Heuristic
If a repo has multiple `package.json` files, do not trust the first one you read as the execution target.