---
name: exam-walkthrough-scaffold
description: Turn a polished Hebrew statistics lecture walkthrough (the output of the `sofia-lecture-polisher` skill, e.g. `v2-sofia_polished_log.md`) into a runnable React page scaffold for the `statisti-kal` app — `web/src/components/ExamWalkthrough.tsx` + typed `examWalkthroughData.ts`. Use when the user asks to "scaffold the page", "build the React walkthrough from the polished log", "wire the lecture to a component", or "convert v2 polished log to ExamWalkthrough". Triggers on phrases like "scaffold ExamWalkthrough", "convert polished log to data file", "Hebrew lecture → React page", "build the walkthrough component from the markdown".
metadata:
  short-description: Polish transcript → React page scaffold
---

# Exam Walkthrough Scaffold (polished log → React page)

Turn a polished Hebrew statistics lecture walkthrough (the `v2-…_polished_log.md` produced by the `sofia-lecture-polisher` skill) into the two files that render it in the `statisti-kal` app:

1. `web/src/components/examWalkthroughData.ts` — typed `ExamQuestion[]` data (the durable content).
2. `web/src/components/ExamWalkthrough.tsx` — the React page that renders the 7 layers (page shell + 5 inner layers) using the verified UI primitives.

This skill is the second stage of a two-stage pipeline:

```
raw transcript  →  [sofia-lecture-polisher]  →  polished log  →  [this skill]  →  ExamWalkthrough.tsx
```

Do NOT use this skill on raw or cleaned transcripts. Polish them first.

## When to use this skill

- A `v2-…_polished_log.md` file exists, in the 5-layer per-section format produced by `sofia-lecture-polisher`.
- The target repo is `statisti-kal` (`web/src/components/ui/`, RTL, no `react-router`).
- The user wants a fully wired page rendered in the existing nav (header chip + TOC + accordion body).

Do NOT use this skill for:
- Direct conversion to a different component library (the layer→component mapping is repo-specific).
- Single-page print/PDF output (different deliverable; no React needed).
- Lifting the data into a different routing model (this app is a state-switcher, not `react-router`).

## What the polished log gives you (5 layers per section)

For each `### Section <letter> — <title>` in the polished log, the content sits under these subheadings (in this exact order):

1. **Pre-flight** — `**What's going on:**`, `**Distribution in play:**`, `**Formulas to remember:**` (bullet list with formula + Hebrew gloss), `**How to approach:**`
2. **Solution Execution** — numbered steps, each with a LaTeX line
3. **Final Answer** — one or two distilled LaTeX lines
4. **Narration** — one Hebrew sentence with inline math
5. **Sofia's Commentary & Exam Traps** — bullet list; first bullet may start with **Critical conceptual trap:**

Plus the per-question **Setup** line and the top-of-file **Exam Question Map**.

## Output structure (always both files, in this order)

### File 1: `web/src/components/examWalkthroughData.ts`

The typed data mirror. Every section in the polished log becomes one `ExamSection`. The fields are deliberately **flat strings**, not React nodes, so the data file stays importable from server-side contexts and remains reviewable in code review.

```ts
/**
 * examWalkthroughData.ts
 * Typed content for the "מבחן לדוגמא (Hy3)" exam walkthrough page.
 *
 * Source: <path-to-polished-log.md>
 * Every section preserves the 5-layer structure from the polished log.
 * Hebrew narration is kept verbatim and inline with LaTeX math.
 */

export interface FormulaRef {
  /** Variable / formula name shown as a recall chip. */
  name: string;
  /** Hebrew meaning of the formula (parenthetical gloss). */
  meaning: string;
  /** LaTeX (no surrounding $). */
  latex: string;
}

export interface ExamSection {
  /** Stable id — also the TOC accordion-open target. */
  id: string;
  /** h4 TOC label, e.g. "סעיף A — חסר הטיה". */
  tocLabel: string;
  /** Short Hebrew label shown on the accordion trigger. */
  subtitleHe: string;
  preFlight: {
    whatsGoingOn: string;
    distribution?: string;
    approach: string;
    formulas: FormulaRef[];
  };
  /** Each entry is one LaTeX line rendered as a BlockMath. */
  solution: string[];
  /** LaTeX for the distilled final answer. */
  finalAnswer: string;
  narration: string;
  /** Bullet points for Sofia's commentary / exam traps. */
  commentary: string[];
  isCriticalTrap?: boolean;
}

export interface ExamQuestion {
  id: string;
  /** h2 TOC label, e.g. "שאלה 1 — אמידה נקודתית". */
  tocLabel: string;
  titleHe: string;
  descriptionHe?: string;
  sections: ExamSection[];
}

export const examData: ExamQuestion[] = [/* … per the polished log … */];
```

### File 2: `web/src/components/ExamWalkthrough.tsx`

The renderer. It imports `examData` and maps each question to a `QuestionCard` and each section to a `SectionContent`.

## Layer → component mapping (verified against `statisti-kal/web/src/components/ui/`)

This is the locked mapping; do not invent alternatives.

| # | Layer | Component | File | Notes |
|---|---|---|---|---|
| 0 | Page shell | `PageLayout` | `ui/PageLayout.tsx` | `dir="rtl"` default; auto-renders `CyberneticBackground`, `TableOfContents`, `ScrollToTopButton`. |
| 1 | Question heading | `SectionHeader` (+ `h2[data-toc]`) | `ui/Heading.tsx` | Top-level TOC entry. |
| 2 | Section collapsible | `Accordion` (NOT in barrel) | `ui/Accordion.tsx` | Import directly. |
| 3 | Pre-flight | `Card` + `ReadingFormulaBlock` | `ui/Card.tsx`, `ui/FormulaBlock.tsx` | One `ReadingFormulaBlock` per formula. |
| 4 | Solution Execution | `ReadingCalcBlock` (one per step) | `ui/FormulaBlock.tsx` | Renders LaTeX with the calc styling. |
| 5 | Final Answer | `ResultBlock` | `ui/ResultBlock.tsx` | Hero result with Award icon. |
| 6 | Narration | `HandwrittenNote` | `ui/HandwrittenNote.tsx` | Sofia's first-person Hebrew voice. Defaults to `align="center"`. |
| 7 | Commentary | `InsightBlock` (default) / `AlertBlock` (critical trap) | `ui/FormulaBlock.tsx` | Distinguish conceptual notes vs exam traps. |

### Verified prop signatures (the parts we use)

```ts
PageLayout: { header?, footer?, children, dir?: 'ltr'|'rtl', contentWidthClassName?, outerClassName? }
SectionHeader: { title, description?, level?: 'page'|'section'|'subsection', accent?: 'brass'|'teal'|'crimson'|'cobalt', withAccentBar?: boolean, className? }
Card: { children, className?, variant?: 'default'|'raised'|'transparent' }
CardHeader: { title, icon?, className? }
CardBody: { children, className? }
ResultBlock: { children: ReactNode, isReject?: boolean, className?, ...HTMLAttributes }
HandwrittenNote: { children: ReactNode, className?, align?: 'start'|'center'|'end' }
ReadingFormulaBlock: { children, formulaName?, translation?, wrapperClassName?, contentWidthClassName?, className? }
ReadingCalcBlock: { children, wrapperClassName?, contentWidthClassName?, className? }
InsightBlock: { children, className? }
AlertBlock: { children, className? }
Accordion: { items: AccordionItem[], allowMultiple?, variant?: 'default'|'bordered'|'card', size?, defaultOpenFirst?, onChange?, className? }
AccordionItem: { key: string, trigger: ReactNode, content: ReactNode, icon?, disabled?, className? }

// math
import { BlockMath, InlineMath } from 'react-katex';
```

## Barrel caveat (critical)

`Accordion` is **not** exported from `web/src/components/ui/index.ts`. You must import it directly:

```ts
import { Accordion } from '../components/ui/Accordion';
```

If the user wants barrel cleanliness, add the export to `ui/index.ts`:

```ts
export { Accordion, AccordionItem } from './Accordion';
export type { AccordionProps, AccordionItem as AccordionItemType, AccordionSize, AccordionVariant } from './Accordion';
```

⭐ Recommend the barrel export — it matches every other primitive.

## Template skeleton (the canonical `ExamWalkthrough.tsx`)

Use this skeleton verbatim. The only file-specific values are the imports of the data, the per-section JSX inside `SectionContent`, and the layered data wiring.

```tsx
import React, { useEffect, useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import {
  PageLayout,
  SectionHeader,
  Card, CardHeader, CardBody,
  ResultBlock,
  HandwrittenNote,
  ReadingFormulaBlock,
  ReadingCalcBlock,
  InsightBlock,
  AlertBlock,
} from '../components/ui';
// Accordion is NOT in the barrel — import directly (or extend ui/index.ts):
import { Accordion } from '../components/ui/Accordion';
import { examData, type ExamSection, type ExamQuestion } from './examWalkthroughData';

const CONTENT_WIDTH_CLASS = 'w-full max-w-[65rem] mx-auto';

/* ─── Section renderer: Pre-flight → Solution → Final → Narration → Commentary ─── */

function SectionContent({ section }: { section: ExamSection }): React.ReactElement {
  return (
    <div className="space-y-3">
      {/* Layer 3 — Pre-flight */}
      <Card variant="raised" className={CONTENT_WIDTH_CLASS}>
        <CardHeader title="גישה והכנות" />
        <CardBody className="space-y-2 text-sm leading-relaxed">
          <p><strong>מה קורה:</strong> {section.preFlight.whatsGoingOn}</p>
          {section.preFlight.distribution && (
            <p><strong>התפלגות:</strong> {section.preFlight.distribution}</p>
          )}
          <p><strong>גישה:</strong> {section.preFlight.approach}</p>
          <div className="space-y-2 pt-2">
            {section.preFlight.formulas.map((f, i) => (
              <ReadingFormulaBlock
                key={i}
                contentWidthClassName={CONTENT_WIDTH_CLASS}
                wrapperClassName="py-1"
                formulaName={f.name}
                translation={f.meaning}
              >
                <BlockMath math={f.latex} />
              </ReadingFormulaBlock>
            ))}
          </div>
        </CardBody>
      </Card>

      {/* Layer 4 — Solution Execution */}
      <div className="space-y-2">
        {section.solution.map((s, i) => (
          <ReadingCalcBlock
            key={i}
            contentWidthClassName={CONTENT_WIDTH_CLASS}
            wrapperClassName="py-1"
          >
            <BlockMath math={s} />
          </ReadingCalcBlock>
        ))}
      </div>

      {/* Layer 5 — Final Answer */}
      <Card variant="raised" className={CONTENT_WIDTH_CLASS}>
        <CardHeader title="תוצאה סופית" />
        <CardBody>
          <ResultBlock className="py-2">
            <BlockMath math={section.finalAnswer} />
          </ResultBlock>
        </CardBody>
      </Card>

      {/* Layer 6 — Narration (HandwrittenNote defaults to align="center") */}
      <HandwrittenNote className={CONTENT_WIDTH_CLASS}>
        {/* section.narration contains Hebrew with inline $...$ math.
            Render as raw children — math is preserved by react-katex via
            the surrounding context. If a segment has Hebrew around $...$,
            split it into text + <InlineMath/>. */}
        {splitMathInline(section.narration)}
      </HandwrittenNote>

      {/* Layer 7 — Commentary / Exam Traps */}
      {section.isCriticalTrap ? (
        <AlertBlock className={CONTENT_WIDTH_CLASS}>
          <ul className="list-disc pr-5 space-y-1">
            {section.commentary.map((line, i) => (
              <li key={i}>{line}</li>
            ))}
          </ul>
        </AlertBlock>
      ) : (
        <InsightBlock className={CONTENT_WIDTH_CLASS}>
          <ul className="list-disc pr-5 space-y-1">
            {section.commentary.map((line, i) => (
              <li key={i}>{line}</li>
            ))}
          </ul>
        </InsightBlock>
      )}
    </div>
  );
}

/* Split a string like "העומד $T$ הוא חסר הטיה ל-$a$" into
   ["העומד ", <InlineMath math="T"/>, " הוא חסר הטיה ל-", <InlineMath math="a"/>, "."] */
function splitMathInline(text: string): React.ReactNode {
  const parts: React.ReactNode[] = [];
  const re = /\$([^$]+)\$/g;
  let lastIndex = 0;
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = re.exec(text)) !== null) {
    if (m.index > lastIndex) parts.push(text.slice(lastIndex, m.index));
    parts.push(<InlineMath key={i++} math={m[1]} />);
    lastIndex = m.index + m[0].length;
  }
  if (lastIndex < text.length) parts.push(text.slice(lastIndex));
  return parts;
}

/* ─── Question card: h2 TOC + Accordion of sections ─── */

function QuestionCard({ question }: { question: ExamQuestion }): React.ReactElement {
  const items = question.sections.map((s) => ({
    key: s.id,
    // h4[data-toc] → TOC level-2 entry that auto-fires toc-open-path
    trigger: (
      <h4
        data-toc
        data-toc-level="4"
        data-toc-label={s.tocLabel}
        data-toc-open={s.id}
        className="font-bold text-[var(--color-text-primary)]"
      >
        {s.subtitleHe}
      </h4>
    ),
    content: <SectionContent section={s} />,
  }));

  return (
    <section className="space-y-4">
      <h2 data-toc data-toc-label={question.tocLabel} className="sr-only">
        {question.tocLabel}
      </h2>
      <SectionHeader
        title={question.titleHe}
        description={question.descriptionHe}
        level="section"
        accent="brass"
      />
      <Card variant="default">
        <Accordion items={items} allowMultiple variant="bordered" size="md" />
      </Card>
    </section>
  );
}

/* ─── Page shell: TOC event → accordion state bridge ─── */

function ExamWalkthroughInner(): React.ReactElement {
  const [openIds, setOpenIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent<{ ids: string[] }>).detail;
      if (!detail?.ids) return;
      setOpenIds((prev) => {
        const next = new Set(prev);
        for (const id of detail.ids) next.add(id);
        return next;
      });
    };
    window.addEventListener('toc-open-path', handler);
    return () => window.removeEventListener('toc-open-path', handler);
  }, []);

  return (
    <>
      {examData.map((q) => (
        <QuestionCard key={q.id} question={q} />
      ))}
      {/* SSR-safe: openIds is consumed by the TOC→accordion bridge above.
          If you want to push the open-set back into the Accordion
          (instead of having Accordion own its own state), switch to
          <Accordion controlledOpenKeys={Array.from(openIds)} ... />. */}
    </>
  );
}

const ExamWalkthrough: React.FC = () => (
  <PageLayout dir="rtl">
    <ExamWalkthroughInner />
  </PageLayout>
);

export default ExamWalkthrough;
```

> **Important honest note about the TOC→accordion bridge.**
> The TOC component (`ui/TableOfContents.tsx`) DOES fire a `toc-open-path` `window` event when a heading with `data-toc-open` is clicked. But the `Accordion` primitive does NOT listen for that event — it owns its own `useState<Set<string>>`. So the bridge in `ExamWalkthroughInner` is required for "click TOC child → open accordion" to actually work. Without it, the TOC click scrolls and flashes the heading, but the accordion stays closed. Keep the `useEffect` listener unless you're willing to give up the click-to-open affordance.

## Wiring into `App.tsx` and `SiteHeader.tsx`

The `statisti-kal` app has no `react-router`. It uses a `useState<ActivePage>` state-switcher in `App.tsx` and chip-style nav in `SiteHeader.tsx`.

### 1. Extend the `SitePage` / `ActivePage` union

**`web/src/components/SiteHeader.tsx`** (line 4):
```ts
export type SitePage = 'landing' | 'hypothesis' | 'point-estimation' | 'forward' | 'inverse' | 'table' | 'formula-sheet' | 'summary' | 'regression' | 'exam-walkthrough';
```

**`web/src/App.tsx`** (line 18):
```ts
type ActivePage = 'landing' | 'hypothesis' | 'point-estimation' | 'normal' | 'summary' | 'regression' | 'exam-walkthrough';
```

### 2. Add the nav chip in `SiteHeader.tsx`

Inside the file (after the existing `summaryItem`):
```ts
const examWalkthroughItem: NavItem = {
  id: 'exam-walkthrough',
  label: 'מבחן לדוגמא (Hy3)',  // or 'מדריך הבחינה' if the user prefers
  icon: <ScrollText className="h-4 w-4 shrink-0" />,
  group: 'reference',
};
```

In the `<nav>` block, alongside the other `reference`-group chips:
```tsx
<NavButton item={examWalkthroughItem} isActive={activePage === 'exam-walkthrough'} onNavigate={onNavigate} />
```

`ScrollText` is already imported from `lucide-react` in `SiteHeader.tsx`.

### 3. Allow the page in `handleNavigate` in `App.tsx`

In `handleNavigate` (around line 129), add `'exam-walkthrough'` to the allow-list `if`:
```ts
if (page === 'landing' || page === 'hypothesis' || page === 'point-estimation' || page === 'summary' || page === 'regression' || page === 'exam-walkthrough') {
  setActivePage(page);
  return;
}
```

### 4. Render the page block in `App.tsx`

Alongside the other conditional page blocks (around line 338 onward, mirroring `point-estimation`):
```tsx
{activePage === 'exam-walkthrough' ? (
  <PageLayout
    header={<SiteHeader activePage="exam-walkthrough" onNavigate={handleNavigate} />}
    footer={<SiteFooter onNavigate={handleNavigate} />}
  >
    <ExamWalkthrough />
  </PageLayout>
) : null}
```

Add the import at the top of `App.tsx`:
```ts
import ExamWalkthrough from './components/ExamWalkthrough';
```

## Navigation behavior (2 levels)

- **Header** → one chip `מבחן לדוגמא (Hy3)` switches the whole page (level-0 entry point).
- **TOC** → auto-builds 2 levels from headings:
  - Each `h2[data-toc]` (the per-question invisible heading) → top TOC row.
  - Each `h4[data-toc-level="4"]` (the accordion trigger) → indented child.
- **Click a TOC child** → fires `toc-open-path` event → `ExamWalkthroughInner` listener adds the id to `openIds`. The accordion opens that item.

> If you want the TOC children to *also* scroll the question heading into view, ensure the `h2` has a real layout box (remove `className="sr-only"` if you want the heading visible; keep it if you want only the `SectionHeader` composite to be the visible question title).

## Hebrew ↔ math rules (carried over from the polish step)

- **Hebrew sentence with math inline** → keep the Hebrew, wrap the math in `$...$`. The TSX `splitMathInline` helper turns it into text + `<InlineMath/>` segments.
- **PDF / CDF glosses** in the `Formulas to remember` bullets:
  - PDF = פונקציית צפיפות
  - CDF = פונקציית התפלגות
- **Variables**: `$X$, $Y$, $T$, $a$, $b$, $\bar X$, $\mu$, $\sigma^2$, $Z$` — always math-italic.
- **Don't translate the Setup line.** It's a verbatim Hebrew problem statement.

## Verification (always run after writing the files)

In this order, in the worktree root:

1. **Type check** — `npx tsc --noEmit` (in `web/`) → must report 0 errors.
2. **Color lint** — `node web/scripts/lint-colors.mjs` → must report 0 violations. Raw `slate`/`gray`/`zinc` are forbidden.
3. **Build** — `npm run build` (in `web/`) → must complete.
4. **Dev server** — `npm run dev` on port 3001 → curl `http://localhost:3001/` and confirm 200 OK.
5. **Visual smoke test** — open the page, confirm:
   - The `מבחן לדוגמא (Hy3)` chip is in the header (it is by default — SiteHeader is RTL so the chip appears on the right).
   - Clicking the chip switches the page to the walkthrough.
   - The TOC has 2 levels (one row per question, indented children per section).
   - Clicking a TOC child opens the matching accordion.
   - The `גישה והכנות` pre-flight card appears at the top of every section.
   - The `HandwrittenNote` narration is visually centered and uses the handwriting font.
   - The `תוצאה סופית` final-answer card has the Award icon.
6. **RTL** — confirm the page is RTL (header chip on the right, math blocks force `dir="ltr"` internally).

If any step fails, fix the root cause and re-verify. Don't paper over with `// @ts-ignore` or `// eslint-disable`.

## Common pitfalls

- **Forgetting to add `Accordion` to the barrel** → the import line will compile but TS may complain about missing types. Either import from `../components/ui/Accordion` directly (works) or add the export to `ui/index.ts` (cleaner).
- **Putting the narration string raw into `HandwrittenNote`** → math will render as text. Always run it through `splitMathInline`.
- **Forgetting `allowMultiple`** → opening one section collapses the others. Default is `false`; explicitly set `true` for a study guide.
- **Forgetting to mirror `'exam-walkthrough'` to the `handleNavigate` allow-list** → clicking the chip does nothing. The `if` chain gates it.
- **Re-using the same `id` across sections** → TOC anchors collide. Use a stable, unique `id` per section (e.g. `q1-a`, `q1-b`, `q2-c`).
- **Forgetting the `data-toc-open` attr on the section `h4`** → clicking the TOC child won't open the accordion. The `toc-open-path` event only fires when the attribute is present and non-empty.
- **Using `sr-only` on the question `h2` AND the `SectionHeader` composite as the visible title** → makes the heading invisible to sighted users but still picked up by the TOC. That's the intended pattern; do not remove the `sr-only` thinking it's dead code.

## Worked example: converting a Section D block

Given this in the polished log:

```markdown
### Section D — Conditional Probability

**Pre-flight**
- **What's going on:** Asian elephant Y ~ U(21,23). Find P(Y>22.5 | Y>22).
- **Distribution in play:** Continuous uniform on [21,23].
- **Formulas to remember:**
  - $P(A\mid B)=\frac{P(A\cap B)}{P(B)}$  (conditional probability; result must lie in [0,1])
  - "רצוי מתוך מצוי" (desired/actual length ratio — **uniform only**)
- **How to approach:** Translate words to events; use the length-ratio method.

**Solution Execution**
1. **Conditional form:**
   $P(Y>22.5 \mid Y>22) = \frac{P(Y>22.5)}{P(Y>22)}$
2. **Substitute lengths:**
   Denominator $23-22=1$, numerator $23-22.5=0.5$.
   $= \frac{0.5}{1} = 0.5$

**Final Answer**
- $P(Y>22.5 \mid Y>22) = \frac{0.5}{1} = 0.5$

**Narration**
זו ההסתברות שהריון של פילה יהיה ארוך מ-22.5 חודשים, מתוך פילות שהן בחודש ה-22 ולא ילדו עוד.

**Sofia's Commentary & Exam Traps**
- If you get a conditional probability > 1, you swapped numerator and denominator.
- The "desired/actual" length ratio works **only** for uniform (density height is constant).
```

The corresponding `ExamSection` in `examWalkthroughData.ts`:

```ts
{
  id: 'q1-d',
  tocLabel: 'סעיף D — הסתברות מותנית',
  subtitleHe: 'הסתברות מותנית',
  preFlight: {
    whatsGoingOn: 'משתנה חדש — פילה אסיאתית Y~U(21,23). מוצאים P(Y>22.5 | Y>22).',
    distribution: 'התפלגות אחידה רציפה על [21,23].',
    approach: 'מתרגמים לאירועים: Y>22 (תנאי), רוצים Y>22.5 בתנאי זה. משתמשים ביחס אורך-קטע.',
    formulas: [
      { name: 'הסתברות מותנית', meaning: 'חייבת להיות בין 0 ל-1', latex: 'P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)}' },
      { name: 'רצוי מתוך מצוי', meaning: 'עובד רק להתפלגות אחידה', latex: '\\dfrac{\\text{אורך רצוי}}{\\text{אורך מצוי}}' },
    ],
  },
  solution: [
    'P(Y>22.5 \\mid Y>22) = \\dfrac{P(Y>22.5)}{P(Y>22)}',
    '\\text{מכנה}=23-22=1,\\quad \\text{מונה}=23-22.5=0.5',
    '= \\dfrac{0.5}{1} = 0.5',
  ],
  finalAnswer: 'P(Y>22.5 \\mid Y>22) = \\dfrac{0.5}{1} = 0.5',
  narration: 'זו ההסתברות שהריון של פילה יהיה ארוך מ-22.5 חודשים, מתוך פילות שהן בחודש ה-22 ולא ילדו עוד.',
  commentary: [
    'אם יצאה הסתברות מותנית > 1 — החלפת מונה ומכנה. הטעות הכי נפוצה כאן.',
    'היחס "רצוי/בפועל" עובד רק להתפלגות אחידה (גובה הצפיפות קבוע).',
  ],
}
```

A full multi-section example (Sections A through F) is in `references/polished-log-to-data.md`.

## How this skill fits with `sofia-lecture-polisher`

| Stage | Skill | Input | Output |
|---|---|---|---|
| 1 | `sofia-lecture-polisher` | raw transcript | `v2-…_polished_log.md` |
| 2 | `exam-walkthrough-scaffold` (this skill) | polished log | `examWalkthroughData.ts` + `ExamWalkthrough.tsx` + nav wiring |

Run stage 1 first. The polished log is the durable artifact and the only thing this skill consumes. Don't try to skip stage 1 — the data file's stable shape comes from the 5-layer structure the polish step enforces.
