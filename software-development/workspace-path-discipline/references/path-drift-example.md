# Path drift example

## Scenario
The agent verified/build-tested from `web/` in terminal, then used a file-tool path that still included the `web/` prefix.

## Failure shape
Intended file:
- `web/src/components/SiteHeader.tsx` from repo root

Actual failing resolution after operating from `web/`:
- `.../web/web/src/components/SiteHeader.tsx`

## Durable lesson
When terminal work shifts into a subdirectory, pause before the next file-tool call and re-anchor the path. The correct fix is not "retry harder"; it is "drop the duplicated path segment and re-run once".

## Good recovery
- Notice the doubled segment in the error path.
- Switch the file-tool target from `web/src/...` to `src/...` when the effective workspace is already `web/`.
- Avoid a third identical retry; inspect and correct the anchor first.

## Why this matters
This class of mistake burns turns, creates fake uncertainty, and can be misread as a tool failure. Treat it as a path-discipline problem.