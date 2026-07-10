# Reference: Polished-log section → `ExamSection` worked example

A full mapping for a complete 6-section question, so a future agent has a one-to-one input/output reference and doesn't have to re-derive the field shapes from the skill body.

## Source (from `v2-sofia_polished_log.md`)

### Section A — Unbiased Estimator

**Pre-flight**
- **What's going on:** Is the proposed estimator $T$ unbiased for the unknown lower bound $a$?
- **Distribution in play:** $X \sim U(a, 23)$ — continuous uniform.
- **Formulas to remember:**
  - $E(X) = \dfrac{a+b}{2}$  (expectation of uniform)
  - $V(X) = \dfrac{(b-a)^2}{12}$  (variance of uniform)
  - $E(\bar X) = E(X)$  (linearity of expectation)
  - $V(\bar X) = \dfrac{V(X)}{n}$  (independent sample)
- **How to approach:** Compute $E(T)$ using linearity; if it equals $a$, the estimator is unbiased and Bias=0, so $MSE = V(T)$.

**Solution Execution**
1. **Unbiasedness:**
   $E(T) = E(2\bar X - 23) = 2E(\bar X) - 23$
   $E(X) = \dfrac{a+23}{2}$ and $E(\bar X) = E(X)$, so
   $E(T) = 2 \cdot \dfrac{a+23}{2} - 23 = a + 23 - 23 = a$.
   ⇒ **$T$ is unbiased for $a$.**

**Final Answer**
- $E(T) = a$ ⇒ $T$ is unbiased for $a$.

**Narration**
העומד $T$ הוא חסר הטיה ל-$a$, כלומר התוחלת שלו שווה בדיוק לפרמטר שרוצים לאמוד.

**Sofia's Commentary & Exam Traps**
- Unbiasedness is about the **estimator's expectation**, not any single computed value.
- $E(\bar X) = E(X)$ holds by linearity of expectation; this is the same fact reused in the CLT.

### Section C — Point Estimate Calculation (the "critical trap" example)

**Pre-flight**
- **What's going on:** Plug the sample $(21,21,21,22,23)$ into $T = 2\bar X - 23$ to estimate $a$.
- **How to approach:** Compute $\bar X$ from the five observations, substitute.

**Solution Execution**
Sample: $(21,21,21,22,23)$.
$\bar X = \dfrac{21 \cdot 3 + 22 + 23}{5} = \dfrac{108}{5} = 21.6$.
$T = 2(21.6) - 23 = 43.2 - 23 = 20.2$.

**Final Answer**
$T = 20.2$ (the estimate of $a$; $a$ itself remains unknown).

**Narration**
זהו האומדן ל-$a$ המתקבל מהמדגם — שים לב שזה הערך של העומד $T$ ולא של הפרמטר $a$ עצמו, שהוא נשאר לא ידוע לנצח.

**Sofia's Commentary & Exam Traps**
- **Critical conceptual trap:** $20.2$ is the *estimate* $T$, **not** the parameter $a$. Writing "a = 20.2" is **wrong** — write "T = 20.2".
- Multiple-choice questions often offer "a = 20.2" as a distractor. Don't take it.

## Output (in `examWalkthroughData.ts`)

```ts
{
  id: 'q1',
  tocLabel: 'שאלה 1 — אמידה נקודתית והתפלגות אחידה',
  titleHe: 'שאלה 1 — אמידה נקודתית והתפלגות אחידה',
  descriptionHe:
    'משך זמן היריון של פילה אפריקאית מתפלג אחיד בין a ל-23 חודשים. ביולוג דגם n=5 פילות והציע את העומד T=2X̄-23 לאמידת a.',
  sections: [
    // ─── Section A: plain commentary, no critical trap ───
    {
      id: 'q1-a',
      tocLabel: 'סעיף A — חסר הטיה',
      subtitleHe: 'חסר הטיה',
      preFlight: {
        whatsGoingOn: 'Is the proposed estimator T unbiased for the unknown lower bound a?',
        distribution: 'X ~ U(a, 23) — continuous uniform (time/length is continuous, never discrete).',
        approach: 'Compute E(T) using linearity; if it equals a, the estimator is unbiased and Bias=0, so MSE = V(T).',
        formulas: [
          { name: 'תוחלת אחידה', meaning: 'expectation of uniform', latex: 'E(X) = \\dfrac{a+b}{2}' },
          { name: 'שונות אחידה', meaning: 'variance of uniform', latex: 'V(X) = \\dfrac{(b-a)^2}{12}' },
          { name: 'תוחלת ממוצע', meaning: 'linearity of expectation', latex: 'E(\\bar X) = E(X)' },
          { name: 'שונות ממוצע', meaning: 'requires independence', latex: 'V(\\bar X) = \\dfrac{V(X)}{n}' },
        ],
      },
      solution: [
        'E(T) = E(2\\bar X - 23) = 2E(\\bar X) - 23',
        'E(X) = \\dfrac{a+23}{2} \\;\\text{and}\\; E(\\bar X) = E(X)',
        'E(T) = 2 \\cdot \\dfrac{a+23}{2} - 23 = a + 23 - 23 = a',
        'T \\text{ is unbiased for } a',
      ],
      finalAnswer: 'E(T) = a \\;\\Rightarrow\\; T \\text{ is unbiased for } a',
      narration: 'העומד $T$ הוא חסר הטיה ל-$a$, כלומר התוחלת שלו שווה בדיוק לפרמטר שרוצים לאמוד.',
      commentary: [
        'Unbiasedness is about the **estimator\'s expectation**, not any single computed value.',
        'E($\\bar X$) = E(X) holds by linearity of expectation; this is the same fact reused in the CLT.',
      ],
    },

    // ─── Section C: critical trap, isCriticalTrap: true ───
    {
      id: 'q1-c',
      tocLabel: 'סעיף C — הערכה נקודתית',
      subtitleHe: 'הערכה נקוקדתית',
      preFlight: {
        whatsGoingOn: 'Plug the sample (21, 21, 21, 22, 23) into T = 2$\\bar X$ - 23 to estimate a.',
        approach: 'Compute $\\bar X$ from the five observations, then substitute.',
        formulas: [
          { name: 'אומדן נקודתי', meaning: 'point estimate formula', latex: 'T = 2\\bar X - 23' },
        ],
      },
      solution: [
        '\\bar X = \\dfrac{21 \\cdot 3 + 22 + 23}{5} = \\dfrac{108}{5} = 21.6',
        'T = 2(21.6) - 23 = 43.2 - 23 = 20.2',
      ],
      finalAnswer: 'T = 20.2',
      narration: 'זהו האומדן ל-$a$ המתקבל מהמדגם — שים לב שזה הערך של העומד $T$ ולא של הפרמטר $a$ עצמו, שהוא נשאר לא ידוע לנצח.',
      commentary: [
        '**Critical conceptual trap:** 20.2 is the *estimate* T, **not** the parameter a. Writing "a = 20.2" is **wrong** — write "T = 20.2".',
        'Multiple-choice questions often offer "a = 20.2" as a distractor. Don\'t take it.',
      ],
      isCriticalTrap: true,
    },
  ],
},
```

## Field-by-field rules

| Source (polished log) | Target (`ExamSection`) | Rule |
|---|---|---|
| `### Section X — <English title>` | `tocLabel: 'סעיף X — <Hebrew translation>'` | Translate the title; keep the letter. |
| `**Pre-flight` → `**What's going on:**` | `preFlight.whatsGoingOn` | English sentence verbatim. |
| `**Distribution in play:**` | `preFlight.distribution` | Optional; omit if absent. |
| `**How to approach:**` | `preFlight.approach` | English sentences verbatim. |
| `**Formulas to remember:**` bullets | `preFlight.formulas[]` | One formula per bullet. `name` = short Hebrew label, `meaning` = English gloss in parens, `latex` = canonical LaTeX (no surrounding `$`). |
| `**Solution Execution**` numbered steps | `solution[]` | One LaTeX line per step, no `$` wrapping. Drop the step title, drop the `⇒` arrow (keep it as a `\Rightarrow` or just inline text if you want). |
| `**Final Answer**` | `finalAnswer` | One or two LaTeX lines concatenated; drop the bullet markers. |
| `**Narration**` | `narration` | The Hebrew sentence **with** its `$...$` math preserved verbatim (the renderer splits them later). |
| `**Sofia's Commentary & Exam Traps**` bullets | `commentary[]` | One bullet per item, including any `**Critical conceptual trap:**` prefix preserved as-is. |
| If a section's first commentary bullet starts with `**Critical conceptual trap:**` | `isCriticalTrap: true` | Drives `AlertBlock` instead of `InsightBlock`. |

## What NOT to translate

- The **Setup** line per question → goes to `descriptionHe` verbatim.
- The **Narration** sentence → keep Hebrew, keep math inline.
- The **Commentary** bullets → keep them in their original language (typically English in the polished log).
- The **Notation** block at the top of the polished log → don't promote it to data; it lives in the page header / cheatsheet.
