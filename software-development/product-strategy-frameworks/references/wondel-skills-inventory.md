# Wondel Skills Inventory (2026-06-06)

Complete catalog from https://github.com/bilalmirza2001/skills (MIT licensed, 21 skills)

---

## Skill Directory Structure

Each skill directory contains:
- `SKILL.md` — Main skill definition (Claude Code / Hermes compatible)
- `reference/` or `references/` — Book frameworks, checklists, templates, prompts

---

## All 21 Skills

| Directory | Skill Name | Book/Framework | Category |
|-----------|------------|----------------|----------|
| `blue-ocean-strategy` | blue-ocean-strategy | Kim & Mauborgne — *Blue Ocean Strategy* | Strategy |
| `cro-methodology` | cro-methodology | CRO frameworks | Marketing/Growth |
| `crossing-the-chasm` | crossing-the-chasm | Moore — *Crossing the Chasm* | Product/GTM |
| `design-everyday-things` | design-everyday-things | Norman — *Design of Everyday Things* | UX/Design |
| `design-sprint` | design-sprint | GV — *Sprint* | Product/Process |
| `drive-motivation` | drive-motivation | Pink — *Drive* | Leadership |
| `hooked-ux` | hooked-ux | Eyal — *Hooked* | Product/Retention |
| `influence-psychology` | influence-psychology | Cialdini — *Influence* | Sales/Psychology |
| `ios-hig-design` | ios-hig-design | Apple — Human Interface Guidelines | Design/Mobile |
| `jobs-to-be-done` | jobs-to-be-done | Christensen — *JTBD* | Product/Strategy |
| `lean-startup` | lean-startup | Ries — *The Lean Startup* | Startup/Process |
| `made-to-stick` | made-to-stick | Heath Brothers — *Made to Stick* | Communication |
| `negotiation` | negotiation | Voss — *Never Split the Difference* | Sales/Negotiation |
| `predictable-revenue` | predictable-revenue | Ross/Aaron — *Predictable Revenue* | Sales/Outbound |
| `refactoring-ui` | refactoring-ui | Wathan/Schoger — *Refactoring UI* | Design/Frontend |
| `scorecard-marketing` | scorecard-marketing | Scorecard funnel methodology | Marketing |
| `storybrand-messaging` | storybrand-messaging | Miller — *Building a StoryBrand* | Marketing/Messaging |
| `top-design` | top-design | Elite agencies (Locomotive, AREA 17, Studio Freight) | Design |
| `traction-eos` | traction-eos | Wickman — *Traction* | Operations/Strategy |
| `ux-heuristics` | ux-heuristics | Nielsen/Norman — 10 Heuristics | UX/Design |
| `web-typography` | web-typography | Santa Maria — *On Web Typography* | Design/Frontend |

---

## Wondel Site Prompts (Copy-Pasteable)

From https://skills.wondel.ai/ — each maps to a skill:

| Prompt | Skill |
|--------|-------|
| "Help me uncover the real Job to Be Done..." | jobs-to-be-done |
| "Design a Grand Slam Offer..." | hundred-million-offers (not in repo) |
| "Score our pitch on the SUCCESs checklist..." | made-to-stick |
| "Build a Strategy Canvas... Four Actions Framework" | blue-ocean-strategy |
| "Run a full CRO audit..." | cro-methodology + influence-psychology |
| "Walk me through the full StoryBrand brand script..." | storybrand-messaging |
| "Design a complete scorecard funnel..." | scorecard-marketing |
| "Apply Nielsen's 10 heuristics... Norman's framework" | ux-heuristics + design-everyday-things |
| "Diagnose onboarding drop-off using B=MAP... Hook Model" | improve-retention (not in repo) + hooked-ux |
| "Create a Vision/Traction Organizer... AMP" | traction-eos + drive-motivation |
| "Write responses to objections using tactical empathy..." | negotiation + influence-psychology |
| "Design Cold Calling 2.0 outbound process..." | predictable-revenue |
| "Design launch strategy with STEPPS... $0 budget" | contagious (not in repo) + one-page-marketing (not in repo) |
| "Build a Build-Measure-Learn experiment card..." | lean-startup + design-sprint |
| "Audit typography... Refactoring UI hierarchy... CSS" | web-typography + refactoring-ui |
| "Design homepage for Awwwards... micro-interactions" | top-design |
| "Check iOS app against HIG..." | ios-hig-design |
| "Map product against whole product model... beachhead" | crossing-the-chasm |

**Note**: Three skills referenced on Wondel site are not in the GitHub repo: `hundred-million-offers`, `improve-retention`, `contagious`, `one-page-marketing`. May be added later.

---

## Priority Ranking for Hermes Integration

### Tier 1 (Install First) — Core Strategic Value
1. `jobs-to-be-done` — Foundational for product discovery
2. `blue-ocean-strategy` — Strategic positioning tool
3. `crossing-the-chasm` — B2B SaaS GTM complete
4. `storybrand-messaging` — Messaging/brand complete template
5. `predictable-revenue` — Sales process complete
6. `lean-startup` — Experiment infrastructure

### Tier 2 — Growth & Operations
7. `traction-eos` — VTO + planning
8. `design-sprint` — 5-day sprint structure
9. `hooked-ux` — Retention mechanics
10. `influence-psychology` — Cialdini audit tool
11. `negotiation` — Tactical empathy scripts
12. `drive-motivation` — AMP framework

### Tier 3 — Design/UX Specialized
13. `refactoring-ui` — Overlaps with `ce-frontend-design`
14. `web-typography` — Overlaps with `ce-frontend-design`
15. `ux-heuristics` — Standalone audit value
16. `design-everyday-things` — Norman principles
17. `ios-hig-design` — iOS specific
18. `top-design` — Overlaps with `ce-frontend-design`
19. `scorecard-marketing` — Quiz funnel specific
20. `made-to-stick` — SUCCESs checklist
21. `cro-methodology` — CRO audit specific

---

## Installation Commands

```bash
# Clone once
git clone https://github.com/bilalmirza2001/skills ~/Developer/wondel-skills

# Install Tier 1 (6 skills)
for skill in jobs-to-be-done blue-ocean-strategy crossing-the-chasm storybrand-messaging predictable-revenue lean-startup; do
  cp -r ~/Developer/wondel-skills/$skill ~/.hermes/skills/product-strategy/
done

# Verify
hermes skills list | grep -E "jobs-to-be-done|blue-ocean|crossing|storybrand|predictable|lean-startup"
```