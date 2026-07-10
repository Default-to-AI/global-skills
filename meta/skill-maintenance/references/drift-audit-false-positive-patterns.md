# Skill Drift Audit False-Positive Patterns

Use this reference when maintaining `scripts/skill-audit-collector.py` or interpreting shared-skills/profile drift reports.

## Lessons from 2026-06-20 cron repair

A raw comparison of `shared-skills` names against `skills_list()` can over-report drift unless it mirrors Hermes' actual skill offer filters and filesystem layouts.

### 1. Support both shared skill layouts
Hermes installs can contain both:

- `shared-skills/<category>/<skill>/SKILL.md`
- `shared-skills/<skill>/SKILL.md` for uncategorized/root-level skills

If the collector only scans `*/*/SKILL.md`, root-level skills such as `browser`, `dogfood`, `grill-me`, `tdd`, or `yuanbao` may be misclassified as `extra_skills_in_cli` even though they are valid shared skills.

### 2. Parse block-style `skills.external_dirs`
Profile configs commonly use YAML block lists:

```yaml
skills:
  external_dirs:
  - C:/Users/Tiger/AppData/Local/hermes/shared-skills
```

Regexes that only match inline lists (`external_dirs: [...]`) create false `has_external_dirs: false` reports. Parse indentation-aware child list items or use a YAML parser.

### 3. Separate true missing from intentionally hidden
`skills_list()` is an offer/index surface, not a raw filesystem dump. It hides skills by design when:

- `platforms:` excludes the current OS
- `environments:` is not active, e.g. `environments: [kanban]` outside Kanban
- `skills.disabled` contains the skill in the profile config

The audit should report these separately:

- `shared_skills_missing_from_cli` — actionable drift only
- `shared_skills_hidden_by_platform` — expected host-platform filtering
- `shared_skills_hidden_by_environment` — expected runtime relevance filtering
- `shared_skills_disabled_in_profile` — expected profile policy filtering

### 4. Treat repeated identical local-only skills as promotion candidates
When the same local-only skill appears identically across the main profiles, prefer promoting it to shared-skills over deleting profile copies. Verify identical content with a directory hash before promotion.

### 5. Keep the collector packaged with the skill
When fixing the live collector at `C:/Users/Tiger/AppData/Local/hermes/scripts/skill-audit-collector.py`, also sync the packaged script under `skill-maintenance/scripts/skill-audit-collector.py` in default/shared/profile-local copies so future agents load the corrected implementation.
