# Repo-local discovery and persisted-path verification

Use this when a Hermes plugin or wrapper can discover a project-local artifact at start time but later lifecycle actions may run from another cwd.

## Pattern
1. Reproduce with the highest-level entrypoint the operator uses.
2. Read the resolver path, not just the failing command output.
3. Check what run state persists:
   - only logical id -> risky for repo-local artifacts
   - resolved absolute path -> durable across cwd changes
4. Patch both layers when needed:
   - initial discovery root for the wrapper/CLI
   - persisted resolved path for later `status` / `advance` / `advance-all`
5. Verify from a different cwd than the start cwd.

## Good verification shape
- Start run inside the repo.
- Confirm run state includes the persisted absolute workflow/spec path.
- Change to `/tmp` or another unrelated cwd.
- Run `status` and `advance-all` there.
- Expect both to succeed without re-registering global roots.

## WSL editing note
If the repo is under `/home/...` in WSL while Hermes workspace tools are rooted on `C:\\Users\\...`, avoid direct file-tool writes to Linux absolute paths. Patch from inside WSL or execute a helper script through `/mnt/c/...` and remove it afterward.
