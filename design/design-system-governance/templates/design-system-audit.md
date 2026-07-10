# Design System Audit Report Template

Used by `design-system-governance` skill. Copy and fill for each audit.

---

# Design System Audit Report — {Project Name}

**Date:** {YYYY-MM-DD}
**Scope:** {e.g., DESIGN.md vs tokens.json/tailwind.theme.json/index.css vs src/components}
**Auditor:** {Agent/Person}
**Method:** frontend-design skill + Three-Layer Method verification

---

## Executive Summary

| Metric | Score | Status |
|--------|-------|--------|
| Spec Completeness | {XX}% | {✅/🟡/🔴} |
| Token Fidelity | {XX}% | {✅/🟡/🔴} |
| Component Compliance | {XX}% | {✅/🟡/🔴} |
| RTL/Hebrew Support | {XX}% | {✅/🟡/🔴} |
| Dark/Light Mode | {XX}% | {✅/🟡/🔴} |
| Signature Elements | {XX}% | {✅/🟡/🔴} |

**Overall:** {Summary sentence}

---

## 1. Spec Layer Assessment (DESIGN.md)

### Strengths
- {Bullet points}

### Gaps
- {Bullet points}

---

## 2. Token Fidelity

| Token Category | tokens.json | tailwind.theme.json | index.css | Match DESIGN.md |
|----------------|-------------|---------------------|-----------|-----------------|
| Colors | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Spacing | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Rounded | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Typography | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Light mode | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Motion | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |
| Signature elements | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} |

---

## 3. Component Library (`src/components/ui/`)

| Component | Exists | Uses Semantic Tokens | Follows DESIGN.md Spec | RTL Ready | Issues |
|-----------|--------|---------------------|------------------------|-----------|--------|
| {Component} | {✅/❌} | {✅/❌} | {✅/❌} | {✅/❌} | {Notes} |

**Missing per DESIGN.md §Component Usage Map:**
- {List missing components}

---

## 4. Calculator Component Compliance

### Systematic Violations

| Violation | DESIGN.md Rule | Files | Count |
|-----------|----------------|-------|-------|
| {e.g., Hardcoded font sizes} | {Rule} | {Files} | {Count} |

### Specific Examples
```
{File}:L{Line}: {Code snippet}
→ Fix: {Semantic token}
```

### What's Working
- {Checklist}

---

## 5. RTL / Hebrew Support

| Aspect | Status | Notes |
|--------|--------|-------|
| Page-level dir="rtl" | {✅/❌} | |
| Container-level RTL | {✅/❌} | |
| Math/KaTeX isolation | {✅/❌} | |
| Component library RTL props | {✅/❌} | |

---

## 6. Dark / Light Mode

| Aspect | Status | Notes |
|--------|--------|-------|
| CSS custom property inversion | {✅/❌} | |
| Accents preserved in light | {✅/❌} | |
| WCAG AA both modes | {✅/❌} | |

---

## 7. Signature Elements

| Element | DESIGN.md Spec | In index.css | In Components |
|---------|----------------|--------------|---------------|
| {.accent-bar} | {Spec} | {✅/❌} | {✅/❌} |

---

## 8. Motion & Reduced Motion

| Aspect | Status |
|--------|--------|
| prefers-reduced-motion respected | {✅/❌} |
| Motion tokens in CSS/@theme | {✅/❌} |

---

## 9. Anti-Pattern Check

| Anti-Pattern | Found? | Where |
|--------------|--------|-------|
| Generic Tailwind defaults | {✅/❌} | |
| Magic numbers in components | {✅/❌} | |

---

## 10. Prioritized Remediation Plan

### P0 — Critical (Blocks feature work)
1. {Action} — {Files} — {Effort}
2. {Action} — {Files} — {Effort}

### P1 — High (Design system completeness)
1. {Action} — {Files} — {Effort}

### P2 — Medium (Polish)
1. {Action} — {Files} — {Effort}

---

## 11. Verification Checklist

| Check | Status | Evidence |
|-------|--------|----------|
| Distinctive point of view | {✅/❌} | |
| 4–6 semantic color tokens | {✅/❌} | |
| 2–3 deliberate font choices | {✅/❌} | |
| Intentional layout structure | {✅/❌} | |
| Subject-specific copy | {✅/❌} | |
| Purposeful motion | {✅/❌} | |
| Dark & light both designed | {✅/❌} | |
| Signature element exists | {✅/❌} | |
| Zero hardcoded text-[Npx] | {✅/❌} | |
| Zero generic Tailwind colors | {✅/❌} | |
| Zero raw hex in components | {✅/❌} | |
| All primitives exist in ui/ | {✅/❌} | |
| All signature elements in CSS | {✅/❌} | |
| RTL + math LTR verified | {✅/❌} | |
| WCAG AA both themes | {✅/❌} | |

---

## 12. Next Steps

{Numbered list with owners and dependencies}