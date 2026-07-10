# Installation Guide — Wondel Skills into Hermes

---

## Prerequisites

- Hermes Agent installed and running
- Git available
- ~/.hermes/skills/ directory exists

---

## Quick Install (Tier 1 — 6 Skills)

```bash
# 1. Clone source repo (MIT licensed)
git clone https://github.com/bilalmirza2001/skills ~/Developer/wondel-skills

# 2. Create product-strategy category if needed
mkdir -p ~/.hermes/skills/product-strategy

# 3. Copy Tier 1 skills
for skill in jobs-to-be-done blue-ocean-strategy crossing-the-chasm storybrand-messaging predictable-revenue lean-startup; do
  cp -r ~/Developer/wondel-skills/$skill ~/.hermes/skills/product-strategy/
done

# 4. Verify installation
hermes skills list | grep -E "jobs-to-be-done|blue-ocean|crossing|storybrand|predictable|lean-startup"
```

Expected output: 6 skills listed under `product-strategy` category.

---

## Full Install (All 21 Skills)

```bash
# Copy all skill directories (skip IDE config dirs)
for skill in ~/Developer/wondel-skills/*/; do
  name=$(basename "$skill")
  # Skip non-skill directories
  [[ "$name" =~ ^\. ]] && continue
  [[ "$name" == "scripts" ]] && continue
  cp -r "$skill" ~/.hermes/skills/product-strategy/
done
```

---

## Hermes Integration Notes

### Skill Format Compatibility

Wondel skills use `.claude/skills/<name>/SKILL.md` format which is **compatible with Hermes**:
- YAML frontmatter with `name`, `description`, `version`
- Markdown body with usage patterns
- `references/` directory for support files

Hermes reads skills from `~/.hermes/skills/<category>/<skill-name>/SKILL.md`.

### Category Placement

Recommended: `product-strategy` (new category) or `software-development` (existing).

```yaml
# In SKILL.md frontmatter
category: software-development  # or product-strategy
```

### Auto-Load Behavior

Hermes loads skills automatically on startup. To verify:
```bash
hermes skills list --category product-strategy
# or
hermes skills list | grep product-strategy
```

---

## Testing a Skill

After install, test invocation in a Hermes session:

```text
Use jobs-to-be-done skill to analyze our SaaS product positioning
```

Expected: Agent applies Christensen's JTBD framework — identifies hiring managers, competing "hires", struggle moments.

---

## Updating Skills

Source repo updates:
```bash
cd ~/Developer/wondel-skills
git pull
# Re-copy changed skills
cp -r jobs-to-be-done ~/.hermes/skills/product-strategy/
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Skill not appearing in `hermes skills list` | Check SKILD.md has valid YAML frontmatter; restart Hermes |
| Category not found | Create `~/.hermes/skills/product-strategy/` directory |
| Reference files not loading | Ensure `references/` dir is inside skill dir, not at category level |
| YAML parse error | Quote strings with colons; escape special chars |

---

## License

Source: https://github.com/bilalmirza2001/skills — MIT License. Free for commercial use, modification, distribution.