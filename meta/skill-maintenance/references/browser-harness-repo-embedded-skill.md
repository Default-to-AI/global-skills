# Browser-harness repo-embedded skill collision

## When this matters

Use this when a git-backed skill repo also contains its own `SKILL.md` at repo root and a nested canonical skill under `skills/<name>/SKILL.md`, and Hermes starts reporting an ambiguous skill name after an update.

## Reproduced shape

`browser-harness` upgraded upstream to a layout where:
- repo root contained `SKILL.md`
- canonical nested skill lived at `skills/browser-harness/SKILL.md`
- in v0.1.3 the nested file could be a symlink to `../../SKILL.md`

That produced two practical failure modes:
1. Hermes registered both root and nested copies, so bare `skill_view(name="browser-harness")` became ambiguous.
2. Deleting only the root file broke the nested skill when the nested file was a symlink to the root.

## Safe repair pattern

1. Inspect whether the nested skill file is a real file or a symlink.
2. If the nested file is a symlink to the root `SKILL.md`, replace it with a real file copy first.
3. Remove the redundant root `SKILL.md`.
4. Reinstall the editable tool package so runtime metadata matches the updated repo state.
5. Re-verify both:
   - skill loading: bare-name `skill_view(...)` resolves cleanly
   - runtime: the CLI still attaches and can open a new tab

## Why this belongs in skill maintenance

This is not a browser-automation lesson. It is a skill-library hygiene lesson about repo-backed skills that embed their own installable package and ship multiple candidate `SKILL.md` paths.

## Verification checklist

- nested `skills/<name>/SKILL.md` exists
- nested file is not a symlink to a deleted root file
- root duplicate removed
- editable install refreshed if the repo also ships a CLI/tool
- Hermes no longer reports ambiguous skill name
