# KaTeX rendered-math regressions

Use this reference when a React UI shows raw LaTeX or monospace pseudo-math instead of structured math.

## Failure pattern

A card intended to show values like `\bar{X}`, `Z \ge z_\alpha`, or `\text{P-value}` used plain spans such as:

```tsx
<span className="font-mono">{parameterSymbol} = {value}</span>
```

This produced visible raw text (`\bar{X}`) or inconsistent pseudo-math instead of KaTeX-rendered output.

## Fix pattern

1. Confirm the project already uses `react-katex` (`InlineMath`, `BlockMath`) elsewhere.
2. Replace plain value spans with `InlineMath`:

```tsx
<span dir="ltr" className="inline-block text-[var(--color-text-primary)]">
  <InlineMath math={`${parameterSymbol} = ${formatNumber(value)}`} />
</span>
```

3. For p-values and text labels inside math, use `\text{...}`:

```tsx
<InlineMath math={`\text{P-value} = ${pValue.toFixed(4)}`} />
<InlineMath math={`\text{P-value} \ge \alpha`} />
```

4. For JSX props containing LaTeX backslashes, prefer expression syntax:

```tsx
parameterSymbol={'\bar{X}'}
```

Avoid quoted JSX attributes when the number of backslashes matters; quoted attributes pass literal backslashes.

## Test pattern

- Add a regression that renders the component and checks `.katex`/MathML exists.
- Do **not** simply assert the full HTML excludes strings like `Z = 0.3912`: KaTeX stores the source TeX inside hidden `<annotation encoding="application/x-tex">...` nodes.
- Instead assert the old raw wrapper/class is gone, or strip `annotation` nodes before visible-text assertions.

Example assertion shape:

```ts
expect(html).toContain('class="katex"');
expect(html).toContain('annotation encoding="application/x-tex">Z \\ge 2.3268');
expect(html).not.toContain('class="font-mono text-[var(--color-text-primary)]"');
```

## Verification

After automated tests pass, browser-check the actual card/section when the defect is visual. Accessibility snapshots may include both visual text and hidden annotation text, so inspect either the screenshot or a DOM clone with annotations removed.
