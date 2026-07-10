# Primitive Building Patterns — DESIGN.md Consumption

Patterns established during P1 remediation of `statistics` (react-example) project.

---

## 1. Token Consumption Pattern (Mandatory)

Every primitive MUST consume DESIGN.md tokens via CSS custom properties:

```tsx
// ✅ CORRECT — semantic tokens via var()
<button className="
  bg-[var(--color-accent-cobalt-strong)]
  text-white
  border-[var(--color-accent-cobalt-dark)]
  hover:bg-[var(--color-accent-cobalt-dark)]
  rounded-[var(--rounded-md)]
">

// ❌ WRONG — raw hex
<button className="bg-[#6366F1] text-white border-[#4338CA]">

// ❌ WRONG — generic Tailwind colors
<button className="bg-indigo-600 text-white border-indigo-700">

// ❌ WRONG — hardcoded sizes
<button className="px-4 py-2 text-base rounded-md">
```

**Token Categories:**
| Token Prefix | Source | Example |
|--------------|--------|---------|
| `--color-*` | DESIGN.md Colors | `var(--color-accent-cobalt)`, `var(--color-border)` |
| `--spacing-*` | DESIGN.md Spacing | `var(--spacing-4)` (16px) |
| `--rounded-*` | DESIGN.md Rounded | `var(--rounded-md)` (8px) |
| `--text-*` | DESIGN.md Typography | `var(--text-heading-section)` |
| `--motion-*` | DESIGN.md Motion | `var(--motion-duration-normal)` |

---

## 2. Primitive Component Structure Template

```tsx
/**
 * PrimitiveName.tsx
 * Per DESIGN.md §Component Usage Map — [Semantic Need]
 * [X variants: variant1, variant2, ...]
 * All tokens consume DESIGN.md via var(--color-*), var(--spacing-*), var(--rounded-*)
 */

import React, { forwardRef, HTMLAttributes } from 'react';

export type PrimitiveVariant = 'variant1' | 'variant2' | 'variant3';
export type PrimitiveSize = 'sm' | 'md' | 'lg';

export interface PrimitiveProps extends HTMLAttributes<HTMLElement> {
  variant?: PrimitiveVariant;
  size?: PrimitiveSize;
  // ... other semantic props
}

const VARIANT_CLASSES: Record<PrimitiveVariant, string> = {
  variant1: 'bg-[var(--color-...)] text-[var(--color-...)] border-[var(--color-...)] ...',
  variant2: 'bg-[var(--color-...)] ...',
  // ...
};

const SIZE_CLASSES: Record<PrimitiveSize, string> = {
  sm: 'px-2 py-1 text-xs ...',
  md: 'px-3 py-2 text-sm ...',
  lg: 'px-4 py-3 text-base ...',
};

export const PrimitiveName = forwardRef<HTMLElement, PrimitiveProps>(
  function PrimitiveName(
    {
      variant = 'variant1',
      size = 'md',
      className = '',
      children,
      ...rest
    },
    ref,
  ) {
    return (
      <element
        ref={ref}
        className={`
          /* base classes */
          ${VARIANT_CLASSES[variant]}
          ${SIZE_CLASSES[size]}
          ${className}
        `}
        {...rest}
      >
        {children}
      </element>
    );
  },
);

PrimitiveName.displayName = 'PrimitiveName';
```

---

## 3. RTL Support Pattern (Hebrew + Math)

**Rule:** Hebrew containers use `dir="rtl"`, math/numeric content uses `dir="ltr"`

```tsx
// Container / Page level — RTL for Hebrew
<div dir="rtl" className="...">
  {/* Form labels, button text, headings — RTL */}
  
  {/* Inputs with numeric values — LTR */}
  <Input dir="ltr" value={mean} onChange={setMean} />
  
  {/* Math formulas — LTR (KaTeX forces this via CSS) */}
  <InlineMath math="\\mu" />
  
  {/* Select with Hebrew options — RTL */}
  <Select dir="rtl" options={[{value: 'a', label: 'אפשרות א'}]} />
</div>
```

**KaTeX Isolation (already in src/index.css):**
```css
.katex {
  direction: ltr !important;
  display: inline-block !important;
  unicode-bidi: isolate !important;
  white-space: nowrap !important;
}
```

---

## 4. Primitive-Specific Patterns

### Button Variants Mapping

| DESIGN.md Spec | Variant | Token Classes |
|----------------|---------|---------------|
| Primary action | `primary` | `bg-[var(--color-accent-cobalt-strong)] text-white border-[var(--color-accent-cobalt-dark)]` |
| Secondary action | `secondary` | `bg-[var(--color-surface-raised)] text-[var(--color-text-primary)] border-[var(--color-border)]` |
| Ghost/tertiary | `ghost` | `bg-transparent text-[var(--color-text-primary)] border-transparent` |
| Danger/destructive | `danger` | `bg-[var(--color-error)] text-white border-[var(--color-error)]` |
| Success/confirm | `success` | `bg-[var(--color-success)] text-white border-[var(--color-success)]` |

### Badge Semantic Variants

| DESIGN.md Spec | Variant | Token Classes | Use Case |
|----------------|---------|---------------|----------|
| H₀ reference, critical values | `brass` | `bg-[var(--color-accent-brass)]/15 text-[var(--color-accent-brass)] border-[var(--color-accent-brass)]` | α threshold, critical Z |
| Power, acceptance (1-β) | `teal` | `bg-[var(--color-accent-teal)]/15 text-[var(--color-accent-teal)] border-[var(--color-accent-teal)]` | Power badge, acceptance region |
| Type I error (α), rejection | `crimson` | `bg-[var(--color-accent-crimson)]/15 text-[var(--color-accent-crimson)] border-[var(--color-accent-crimson)]` | α badge, rejection region |
| Z-scores, standard normal | `cobalt` | `bg-[var(--color-accent-cobalt-bg)] text-[var(--color-accent-cobalt)] border-[var(--color-accent-cobalt-line)]` | Z-score badge, primary interactive |
| Generic/muted | `neutral` | `bg-[var(--color-surface-raised)] text-[var(--color-text-secondary)] border-[var(--color-border)]` | Default status |

### Input/Select/Label Pattern

```tsx
// Label uses heading-label scale
<Label required size="md" dir="rtl">
  תוחלת המבוקשת (μ):
</Label>

// Input uses mono font, text-center, ltr for numbers
<Input
  type="number"
  value={meanInput}
  onChange={setMeanInput}
  dir="ltr"
  size="md"
  placeholder="100"
  error={meanError}
/>

// Select uses rtl for Hebrew options
<Select
  value={calcType}
  onChange={setCalcType}
  dir="rtl"
  options={[
    { value: 'area', label: 'חישוב שטח' },
    { value: 'inverse', label: 'חישוב הפוך' },
  ]}
/>
```

---

## 5. Export Pattern (Barrel File)

Always export from `src/components/ui/index.ts`:

```ts
// --- Primitives (DESIGN.md Component Usage Map) ---
export { PrimitiveName } from './PrimitiveName';
export type { PrimitiveProps, PrimitiveVariant, PrimitiveSize } from './PrimitiveName';
```

---

## 6. Verification Checklist (Per Primitive)

```bash
# 1. Build
npm run build

# 2. Token discipline
npm run lint:colors

# 3. No hardcoded sizes
grep -rn "text-\\[[0-9]px\\]" src/components/ui/PrimitiveName.tsx || echo "CLEAN"

# 4. No generic colors
grep -rn "slate-\\|zinc-\\|gray-\\|neutral-\\|stone-" src/components/ui/PrimitiveName.tsx | grep -v "var(--color" || echo "CLEAN"

# 5. No raw hex
grep -rn "#[0-9a-fA-F]\\{6\\}" src/components/ui/PrimitiveName.tsx || echo "CLEAN"

# 6. Exports from barrel
grep -q "export.*PrimitiveName" src/components/ui/index.ts && echo "✅ Exported" || echo "❌ Missing export"

# 7. TypeScript types exported
grep -q "export type.*PrimitiveProps" src/components/ui/index.ts && echo "✅ Types exported" || echo "❌ Missing types"
```

---

## 7. Git Hygiene for Review Artifacts

Add to `.gitignore` before P1 work:

```gitignore
# Review artifacts (generated by ce-code-review)
.review_*.json
review_findings.json
performance_review.json
design-system-audit.md
ux-evaluation.md
docs/reviews/

# Local scripts directory (untracked local tooling)
scripts/
```

---

## 8. Motion Token Integration

Signature elements in `src/index.css` use motion tokens:

```css
:root {
  --motion-duration-fast: 150ms;
  --motion-duration-normal: 280ms;
  --motion-duration-slow: 500ms;
  --motion-duration-choreographed: 1000ms;
  --motion-easing-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --motion-easing-entrance: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-easing-exit: cubic-bezier(0.4, 0, 1, 1);
  --motion-stagger-delay: 50ms;
}

@media (prefers-reduced-motion: reduce) {
  .stagger-in > * { animation: none !important; opacity: 1; transform: none; }
  .pulse-brass, .pulse-success, .pulse-error { animation: none !important; }
  .curve-glow { transition: none !important; }
}
```

Primitives using Framer Motion should reference these:

```tsx
<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{
    duration: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--motion-duration-normal')) / 1000,
    ease: getComputedStyle(document.documentElement).getPropertyValue('--motion-easing-entrance').trim(),
  }}
>
```