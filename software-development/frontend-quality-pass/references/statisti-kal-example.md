# Statisti-Kal example

## Situation
A frontend project had strong product/design energy but weak release discipline:
- TypeScript errors present
- 2 failing render tests
- canonical docs and a lint script were accidentally ignored by `.gitignore`
- bundle size needed measurement before optimization claims
- temporary root artifacts existed from planning/progress work

## Winning sequence
1. Create durable plan and task tracking.
2. Repair `.gitignore` so governance/docs/lint script are trackable.
3. Fix compiler errors.
4. Update tests where failures came from intentional UI/content drift.
5. Add/repair narrow design-system enforcement (`lint-colors`).
6. Build and introduce vendor chunking.
7. Run final `git diff --check`, staged diff check, test/build rerun.
8. Remove temporary scratch artifacts.

## Verification snapshot
- `npm run lint:tsc` → pass
- `npm run lint:colors` → pass, 74 files scanned, 0 violations
- `npm test -- --reporter=dot` → 7 files passed, 29 tests passed
- `npm run build` → pass
- initial main app chunk reduced from 763.79 KB to 205.47 KB after vendor chunking
- `git check-ignore` confirmed previously ignored canonical files were now trackable
- final `git diff --check` caught trailing whitespace in docs late; fix it and rerun the full gate

## Durable lesson
The late catch matters: even after core gates are green, documentation or staged-scope defects can still invalidate the handoff. Always end with repo-hygiene verification, not just app verification.

## Deferred correctly
These were named and left out of the release-quality pass:
- decomposing a 4k+ line calculator component
- broad heading/semantic cleanup across pages
- lockfile/package-manager normalization without active install/CI breakage
- URL navigation redesign
- KaTeX Hebrew-text cleanup inside math expressions

## Reusable rule
A quality pass is not a redesign sprint. Restore trust first, then hand the user a clean next frontier.