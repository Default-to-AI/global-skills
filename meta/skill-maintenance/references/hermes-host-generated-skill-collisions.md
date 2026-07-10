# Hermes host-generated skill collision pattern

## When this happens
A repo-backed skill pack can ship source skills and also generate Hermes-host docs into a nested output tree such as:

- `skills/<category>/<repo>/SKILL.md`
- `skills/<category>/<repo>/.hermes/skills/<generated-skill>/SKILL.md`

After generation, both the source umbrella and the generated Hermes-host umbrella may be visible to skill discovery.

## Observed pattern
With the gstack repo, `bun run gen:skill-docs --host hermes` generated:

- `.hermes/skills/gstack/SKILL.md`
- `.hermes/skills/gstack-office-hours/SKILL.md`
- many other `gstack-*` outputs

At the same time the source repo already contained:

- `gstack/SKILL.md`
- `gstack/office-hours/SKILL.md`

Result: bare loads like `skill_view(name='gstack')` became ambiguous because two different `SKILL.md` files exposed the same frontmatter name.

## Correct handling
1. Expect ambiguity after host-doc generation if source and generated trees coexist.
2. Validate generated output with an explicit path, not a bare skill name.
3. Prefer one of these verification paths:
   - `skill_view(name='gstack/.hermes/skills/gstack')`
   - `read_file()` against the generated `SKILL.md`
   - `skills_list(category='gstack')` first, then load the exact categorized path
4. Do not assume an ambiguous bare name means the generator failed. It often means both source and generated trees are present.

## What to save as the lesson
Save the loading pattern, not a negative claim about the tool. The durable rule is:

> When validating generated Hermes-host skills from a vendored repo, use explicit categorized/generated paths because source and generated skill trees can coexist and make bare names ambiguous.
