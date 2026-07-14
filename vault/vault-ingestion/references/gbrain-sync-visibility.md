# GBrain Sync Visibility for Git-Backed Vault Ingests

Use this after a vault ingest when Robert expects the new material to be queryable through `gbrain`.

## Durable lesson
`gbrain sync` may key off the **git-tracked delta**, not the plain working tree. In a git-backed vault, newly created raw/extract/report files can be invisible to sync until they are committed.

## Symptom pattern
- `gbrain sync --source vault-tiger` exits 0
- preview says something like `1 changed source(s)` but `~0 new tokens`
- sync output never shows a meaningful embed/import phase for the new files
- `gbrain query "<new source term>"` returns `No results`
- `git status --short` still shows the new ingest artifacts as `??` or modified but uncommitted

## Correct move
1. Finish the ingest properly first: raw/wiki/index/log/report/audit.
2. Inspect `git status --short` for the touched vault files.
3. If the new ingest artifacts are untracked or modified, commit the ingestion set to the vault backup repo.
4. Re-run `gbrain sync --source vault-tiger`.
5. Verify with a **positive retrieval check** such as `gbrain query "agency-agents"` or another source-specific term.
6. Only then claim the material is queryable.

## Reporting rule
Do not present `sync` exit code alone as proof. Queryability requires positive evidence from `gbrain query`, `gbrain search`, or another live retrieval path.

## Scope boundary
This is a workflow rule for Robert's git-backed vault + gbrain setup, not a universal negative claim about gbrain. Capture the fix pattern, not "gbrain is broken".
