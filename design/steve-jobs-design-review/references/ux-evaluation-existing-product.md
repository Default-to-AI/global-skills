# UX Evaluation Pattern — Existing Product Audit

**Source Session:** northstar-2.0 statistics calculator Steve Jobs review (2026-06-17)
**Method:** Binary verdicts (Brilliant/Shit), cut list, "one thing to perfect"

---

## Context

Applied `steve-jobs-design-review` skill to an **existing** product (not pre-launch concept).
Product: Hebrew RTL statistics calculator with live bell curve chart.

---

## Adaptation for Existing Product Audit

### Standard Skill Triggers (from SKILL.md)
- Pre-launch gate
- Feature triage
- Design concept selection

### Extended Trigger: **Existing Product UX Audit**
- Product ships but feels bloated/confusing
- Need ruthless prioritization for refactor
- Stakeholders disagree on what to fix first

---

## Adapted Output Format

For existing products, add these sections to standard output:

### 1. Binary Verdict Table (Extended)
| Screen/Flow | Verdict | One-Sentence Rationale |
|-------------|---------|------------------------|
| [Screen] | BRILLIANT/SHIT | [Why — references core user job] |

### 2. The Cut List (Kill These)
| Feature | Reason (Jobs Principle) |
|---------|-------------------------|
| [Feature] | "Good idea but dilutes the one job" / "System-centric, not user-centric" |

### 3. The Keep List (Double Down)
| Element | Why It's the Hero |
|---------|-------------------|
| [Element] | [Connects to core user job + emotional resonance] |

### 4. The One Thing to Perfect
> Single sentence: the screen/flow/interaction that must be flawless.

### 5. Jobs-Style Rationale (Four Quotes)
Map findings to Jobs/Isaacson/Segall principles:
- **On Simplicity** — "Simple can be harder than complex..."
- **On Focus** — "Focus means saying no to the hundred other good ideas..."
- **On End-to-End Ownership** — "Jobs reviewed the box, the unboxing, the first boot..."
- **On Emotional Resonance** — "Usable is the floor. Makes the user feel understood is the bar."

### 6. Verdict: SHIP / DON'T SHIP
Explicit gate with prerequisites.

### 7. What the Losers Teach Us
Each cut feature teaches a product principle (progressive disclosure, contextual reference, decisions as outcomes).

---

## Application Notes

**Difference from Pre-Launch Gate:**
- Pre-launch: evaluating concepts before building
- Existing product: evaluating *running code* with real usage patterns
- Must reference actual implementation (file:line) not just mockups
- Cut list becomes refactor backlog, not "don't build"

**Hebrew RTL Specifics:**
- "One job" must account for RTL mental model (right-to-left scanning)
- Chart reads right-to-left but axes are LTR — cognitive load
- Helper modal interrupts RTL flow — inline tooltips better

**Academic Instrument Context:**
- "Emotional resonance" = trust/relief/anxiety reduction for students
- "Hero" = live visualization that confirms mental model
- "Noise" = reference material masquerading as calculation UI

---

## Reusable Verdict Templates

| Pattern | Verdict | Rationale Template |
|---------|---------|-------------------|
| Live data viz that shows answer instantly | BRILLIANT | "Only thing that makes [abstract concept] visceral. Real-time, responsive, accurate." |
| Tabbed interface for distinct mental models | SHIT | "System-centric, not user-centric. User thinks '[task]', not '[internal module name]'." |
| 10+ visible input fields | SHIT | "Cognitive overload. No progressive disclosure. No smart defaults." |
| Reference dump (formulas, help, matrices) | SHIT | "Cataloged, not contextual. User hunts for answer instead of seeing it." |
| Modal for help/definitions | SHIT | "Interruption. Contextual inline help (tooltips, empty states) would be 10x better." |
| Dark-first with intentional light mode | BRILLIANT | "Feels designed in both. Respects prefers-color-scheme. Accents preserved = brand." |
| RTL + math LTR isolation | BRILLIANT | "Flawless execution. Craft that earns trust. No other tool does this right." |
| Semantic color system with domain meaning | BRILLIANT | "Not decoration — meaning. When user sees [color], they know '[domain concept]'." |

---

## Next Session Usage

When auditing existing products:
1. Load `steve-jobs-design-review` skill
2. Add context: "Existing product audit — apply binary verdicts to running screens, produce cut list for refactor backlog"
3. Use verdict templates above for speed
4. Output `ux-evaluation.md` with all 7 sections