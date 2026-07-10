# Obsidian skill location and compatibility

## Location invariant

Robert's focused Obsidian skill suite lives under the global Hermes home skill root:

- `C:\Users\Tiger\AppData\Local\hermes\skills\obsidian\`

Do **not** place the focused suite under `profiles\vault\skills\obsidian\`.

## Compatibility exception

A legacy compatibility wrapper may still exist at:

- `C:\Users\Tiger\AppData\Local\hermes\profiles\vault\skills\note-taking\obsidian\SKILL.md`

That wrapper is allowed only as a routing bridge for older prompts, handoffs, or habits. It should point at the focused skills in the global `skills\obsidian` tree rather than duplicating the procedures.

## Maintenance rule

When refactoring, splitting, or relocating Robert's vault skill suite:

1. Treat `HERMES_HOME\skills\obsidian` as the canonical destination.
2. Update the compatibility wrapper if its routing text changes.
3. Update plan and handoff artifacts in `C:\Users\Tiger\AppData\Local\hermes\plans\` and `...\handoffs\` so future agents do not drift back to profile-local placement.
4. Verify the focused skills are discoverable from the global `obsidian` category after the move.

## Pitfall

A common failure mode is preserving the old vault-profile destination in documentation after the files were moved. When location changes, patch the implementation plan and handoff in the same pass so the written spec matches the filesystem.