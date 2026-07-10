# Violation Taxonomy — Design System Audit

Used by `design-system-governance` skill for systematic detection and classification.

---

## P0 — Blocks All Feature Work (Invariant: Must be 0 before Environment features)

| Code | Pattern | Regex | Fix | Example |
|------|---------|-------|-----|---------|
| **P0-HS** | Hardcoded font size | `text-\[[0-9]px\]` | Replace with semantic token (`text-caption`, `text-body-xs`, `text-mono-xs`, `text-heading-label`, `text-body-sm`, `text-body-base`, `text-mono-sm`, `text-mono-base`) | `text-[11px]` → `text-caption` |
| **P0-HP** | Hardcoded padding | `p-\[[0-9]` | Replace with `var(--spacing-N)` or semantic component | `p-[6px]` → `p-1.5` or `padding: var(--spacing-3)` |
| **P0-HR** | Hardcoded border radius | `rounded-\[[0-9]` | Replace with `var(--rounded-*)` or semantic component | `rounded-[6px]` → `rounded-md` or `border-radius: var(--rounded-md)` |
| **P0-GC** | Generic Tailwind color | `slate-\|zinc-\|gray-\|neutral-\|stone-` | Replace with semantic `var(--color-*)` | `border-slate-800` → `border-[var(--color-border)]` |
| **P0-RX** | Raw hex in component | `#[0-9a-fA-F]{6}` (in .tsx/.ts) | Replace with `var(--color-*)` | `#D4A843` → `var(--color-accent-brass)` |
| **P0-SE** | Missing signature element | (manual check) | Implement in CSS per DESIGN.md §Signature Elements | `.accent-bar`, `.curve-glow`, `.stagger-in`, `.pulse-brass` |
| **P0-RM** | Missing prefers-reduced-motion | (manual check) | Add `@media (prefers-reduced-motion: reduce)` for all animations | Disable `.stagger-in`, `.pulse-brass`, `.curve-glow` transitions |

---

## P1 — Design System Completeness (After P0, Before Complex Features)

| Code | Pattern | Check | Fix |
|------|---------|-------|-----|
| **P1-MP** | Missing primitive component | DESIGN.md §Component Usage Map vs `src/components/ui/` | Build per spec (Button, Input, Badge, Table, Tooltip, Accordion, FormulaBlock, Modal, Heading) |
| **P1-NC** | Non-compositional components | Components build inline className soup instead of composing from ui/ primitives | Refactor to import and compose from ui/ |
| **P1-MT** | Missing motion tokens | `--motion-duration-*`, `--motion-easing-*`, `--motion-stagger-delay` not in CSS/@theme | Add to `:root` in index.css |

---

## P2 — Polish (Can Parallel with Features)

| Code | Pattern | Check | Fix |
|------|---------|-------|-----|
| **P2-LM** | Light mode unverified | Visual test all components in light mode | Fix contrast, verify accents unchanged |
| **P2-VR** | No visual regression tests | Chromatic/Percy/screenshot diff missing | Add to CI |
| **P2-DC** | Component API undocumented | No Storybook or similar | Document component props, variants, states |

---

## Token Mapping Reference (DESIGN.md → Semantic Replacements)

| Hardcoded | Context Clues | Semantic Token | DESIGN.md Spec |
|-----------|---------------|----------------|----------------|
| `text-[9px]` | any | `text-caption` | caption: 0.6875rem (11px), 700, uppercase |
| `text-[10px]` | error, badge, mono | `text-caption` | caption |
| `text-[10px]` | body, secondary | `text-body-xs` | body-xs: 0.75rem (12px) |
| `text-[11px]` | error, badge, mono, accent | `text-caption` | caption |
| `text-[11px]` | body, secondary, primary | `text-body-xs` | body-xs |
| `text-[11px]` | mono, tabular | `text-mono-xs` | mono-xs: 0.75rem (12px), 500 |
| `text-[11px]` | heading-like (font-black/extrabold) | `text-body-sm` | body-sm: 0.875rem (14px) |
| `text-[12px]` | body, accent | `text-body-xs` | body-xs |
| `text-[12px]` | mono, tabular | `text-mono-xs` | mono-xs |
| `text-[13px]` | body, secondary, primary | `text-body-sm` | body-sm: 0.875rem (14px) |
| `text-[13px]` | mono, tabular | `text-mono-sm` | mono-sm: 0.875rem (14px), 500 |
| `text-[15px]` | body, primary, accent | `text-body-base` | body-base: 1rem (16px) |
| `text-[15px]` | mono, tabular | `text-mono-base` | mono-base: 1rem (16px), 500 |
| `sm:text-[10px]` | responsive | `sm:text-caption` | — |
| `sm:text-[11px]` | responsive | `sm:text-caption` | — |
| `sm:text-[12px]` | responsive | `sm:text-body-xs` | — |
| `sm:text-[13px]` | responsive | `sm:text-body-sm` | — |
| `sm:text-[15px]` | responsive | `sm:text-body-base` | — |

### Form Labels (block + font-bold + mb-1)
| Hardcoded | Semantic Token |
|-----------|----------------|
| `text-[10px]` / `text-[11px]` | `text-heading-label` (0.75rem, 800, 0.05em letter-spacing, uppercase) |

---

## Greppable Detection Scripts

```bash
#!/bin/bash
# detect-p0.sh — Run in project root
# Returns non-zero if any P0 violations found

set -e

echo "=== P0-HS: Hardcoded font sizes ==="
grep -rn "text-\[[0-9]px\]" src/ --include="*.tsx" --include="*.ts" || true

echo "=== P0-HP: Hardcoded padding ==="
grep -rn "p-\[[0-9]" src/ --include="*.tsx" --include="*.ts" || true

echo "=== P0-HR: Hardcoded border radius ==="
grep -rn "rounded-\[[0-9]" src/ --include="*.tsx" --include="*.ts" || true

echo "=== P0-GC: Generic Tailwind colors ==="
grep -rn "slate-\|zinc-\|gray-\|neutral-\|stone-" src/ --include="*.tsx" --include="*.ts" | grep -v "var(--color" || true

echo "=== P0-RX: Raw hex in components ==="
grep -rn "#[0-9a-fA-F]\{6\}" src/ --include="*.tsx" --include="*.ts" | grep -v "tokens.json\|tailwind.theme.json\|DESIGN.md" || true

echo "=== P0-SE: Signature elements check ==="
for elem in ".accent-bar" ".curve-glow" ".stagger-in" ".pulse-brass"; do
  if ! grep -q "$elem" src/index.css; then
    echo "MISSING: $elem"
  fi
done

echo "=== P0-RM: prefers-reduced-motion ==="
if ! grep -q "prefers-reduced-motion" src/index.css; then
  echo "MISSING: prefers-reduced-motion media query"
fi
```

---

## Remediation Scripts (Bulk Replacement)

```bash
#!/bin/bash
# remediate-p0-hardcoded-sizes.sh — Apply semantic token replacements
# Run AFTER audit, review diffs before commit

set -e

# Map of hardcoded → semantic (order matters: specific before general)
declare -A REPLACEMENTS=(
  # Error messages (highest priority - most distinct context)
  ['text-\[var\(--color-error\)\] text-\[10px\] font-bold']='text-[var(--color-error)] text-caption font-bold'
  ['text-\[var\(--color-error\)\] text-\[11px\] font-bold']='text-[var(--color-error)] text-caption font-bold'
  ['text-\[var\(--color-error\)\] text-\[10px\]']='text-[var(--color-error)] text-caption'
  ['text-\[var\(--color-error\)\] text-\[11px\]']='text-[var(--color-error)] text-caption'
  ['text-\[var\(--color-error\)\] text-\[9px\]']='text-[var(--color-error)] text-caption'
  
  # Badge/chip text (px-2.5 py-0.5 rounded-full context)
  ['text-\[10px\] font-black']='text-caption font-black'
  ['text-\[11px\] font-black']='text-caption font-black'
  ['text-\[12px\] font-black']='text-body-xs font-black'
  
  # Form labels (block + font-bold + mb-1)
  ['block text-\[10px\] font-bold text-\[var\(--color-text-secondary\)\] mb-1']='block text-heading-label text-[var(--color-text-secondary)] mb-1'
  ['block text-\[11px\] font-bold text-\[var\(--color-text-secondary\)\] mb-1']='block text-heading-label text-[var(--color-text-secondary)] mb-1'
  
  # Mono/tabular contexts
  ['font-mono text-\[10px\]']='font-mono text-mono-xs'
  ['font-mono text-\[11px\]']='font-mono text-mono-xs'
  ['font-mono text-\[12px\]']='font-mono text-mono-xs'
  ['font-mono text-\[13px\]']='font-mono text-mono-sm'
  ['font-mono text-\[15px\]']='font-mono text-mono-base'
  ['tabular-nums text-\[13px\]']='tabular-nums text-mono-sm'
  ['tabular-nums text-\[15px\]']='tabular-nums text-mono-base'
  
  # Body text with text-secondary
  ['text-\[var\(--color-text-secondary\)\] text-\[10px\]']='text-[var(--color-text-secondary)] text-body-xs'
  ['text-\[var\(--color-text-secondary\)\] text-\[11px\]']='text-[var(--color-text-secondary)] text-body-xs'
  ['text-\[var\(--color-text-secondary\)\] text-\[12px\]']='text-[var(--color-text-secondary)] text-body-xs'
  ['text-\[var\(--color-text-secondary\)\] text-\[13px\]']='text-[var(--color-text-secondary)] text-body-sm'
  ['text-\[var\(--color-text-secondary\)\] text-\[15px\]']='text-[var(--color-text-secondary)] text-body-base'
  
  # Body text with text-primary
  ['text-\[var\(--color-text-primary\)\] text-\[10px\]']='text-[var(--color-text-primary)] text-body-xs'
  ['text-\[var\(--color-text-primary\)\] text-\[11px\]']='text-[var(--color-text-primary)] text-body-xs'
  ['text-\[var\(--color-text-primary\)\] text-\[12px\]']='text-[var(--color-text-primary)] text-body-xs'
  ['text-\[var\(--color-text-primary\)\] text-\[13px\]']='text-[var(--color-text-primary)] text-body-sm'
  ['text-\[var\(--color-text-primary\)\] text-\[15px\]']='text-[var(--color-text-primary)] text-body-base'
  
  # Accent colors
  ['text-\[var\(--color-accent-cobalt\)\] text-\[10px\]']='text-[var(--color-accent-cobalt)] text-caption'
  ['text-\[var\(--color-accent-cobalt\)\] text-\[11px\]']='text-[var(--color-accent-cobalt)] text-caption'
  ['text-\[var\(--color-accent-cobalt\)\] text-\[12px\]']='text-[var(--color-accent-cobalt)] text-body-xs'
  ['text-\[var\(--color-accent-cobalt\)\] text-\[13px\]']='text-[var(--color-accent-cobalt)] text-body-sm'
  ['text-\[var\(--color-accent-cobalt\)\] text-\[15px\]']='text-[var(--color-accent-cobalt)] text-body-base'
  
  # Responsive
  ['sm:text-\[15px\]']='sm:text-body-base'
  ['sm:text-\[13px\]']='sm:text-body-sm'
  ['sm:text-\[12px\]']='sm:text-body-xs'
  ['sm:text-\[11px\]']='sm:text-caption'
  ['sm:text-\[10px\]']='sm:text-caption'
  ['sm:text-\[9px\]']='sm:text-caption'
  
  # Standalone
  ['text-\[9px\]']='text-caption'
)

# Apply to all .tsx/.ts files in src/
for file in $(find src -name "*.tsx" -o -name "*.ts"); do
  for pattern in "${!REPLACEMENTS[@]}"; do
    sed -i "s/${pattern}/${REPLACEMENTS[$pattern]}/g" "$file"
  done
done

echo "Replacements applied. Review with git diff."
```

> **Warning:** These scripts are aggressive. Always run on a clean branch, review `git diff` thoroughly, and run `npm run build` + `npm run lint:colors` after.