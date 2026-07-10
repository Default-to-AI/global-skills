# Repo-generated skill pack layouts

Use this when a third-party or vendored repo under a Hermes skill tree appears to contain an extra nested `.hermes/skills/` directory and the structure looks suspicious.

## Pattern

A repo-backed skill pack can legitimately contain all three layers at once:

1. **Source repo root** — the cloned upstream project directory.
2. **Generated Hermes host outputs** — packaged skills under `.hermes/skills/<skill>/SKILL.md` after running the repo's generator for `--host hermes`.
3. **Repo-root umbrella skill** — sometimes a root `SKILL.md` also exists for the repo itself.

This is not automatically corruption or duplication. It often means the repo is both:
- the source material used to generate Hermes-native skills, and
- a loadable umbrella skill tree after generation.

## Investigation sequence

1. Identify which files are **source** versus **generated outputs**.
2. Check whether the same frontmatter `name:` now appears in both the source umbrella and generated skill output.
3. Verify loads with an explicit path-qualified name when ambiguity is expected.
4. Only remove a repo-root `SKILL.md` if another umbrella already covers that role and you have positive evidence the duplicate causes ambiguity.

## Integration lesson from the G-stack case

When the generated skills are valid but their existence is not obvious from the raw tree:
- keep the generated `.hermes/skills/...` layout intact;
- add or update AGENTS routing rules so future agents know which skill names to invoke for common intents;
- explain the tree in terms of **source repo vs generated Hermes outputs**, not as a mysterious nested folder.

## Verification-path lesson

If AGENTS documentation references verification scripts like `_precommit_guard.py`, resolve whether the script is:
- install-root scoped, or
- profile-local/repo-local.

Do not assume `C:/Users/Tiger/AppData/Local/hermes/scripts/...` exists just because AGENTS says `scripts/...`.
In the G-stack integration session, the correct guard lived under the active profile:
`C:/Users/Tiger/AppData/Local/hermes/profiles/librarian/scripts/_precommit_guard.py`

The durable lesson is **scope the path from the active repo/profile first**, not that a global scripts directory is absent in general.
