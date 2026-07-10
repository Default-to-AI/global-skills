---
name: sofia-lecture-polisher
description: Turn a raw Hebrew statistics lecture transcript (e.g. from a Sofia Katzman video call with timestamped student turns and lots of filler like אוקיי / בסדר / נו) into a polished, publishable study walkthrough with a fixed 6-element section structure (Question / Pre-flight / Solution with between-step commentary / Final Answer / HandwrittenNote narration / Exam Traps). Use when the user asks to "polish", "clean up", "structure", or "publish-ready" a Hebrew/English statistics lecture transcript that covers Point Estimation, Uniform Distribution, Normal Distribution, CLT, or Hypothesis Testing; the output should be a single Markdown file (default filename `v2-<short-slug>_polished_log.md`) ready to feed a React walkthrough page. Triggers on phrases like "polish this transcript", "make it publish-ready", "structure Sofia's lecture", "Hebrew stats lecture walkthrough", "6-element study notes".
metadata:
  short-description: Polish raw Hebrew stats lecture into 6-element walkthrough
---

# Sofia Lecture Polisher

Convert a raw, filler-heavy Hebrew lecture transcript (Sofia Katzman style — point estimation, uniform/normal/CLT/hypothesis testing) directly into a single polished, publishable Markdown walkthrough. The output is the **finished deliverable** — no intermediate clean/noise files are produced.

The output is a single `.md` file with inline LaTeX wrapped in `$...$`. Every section follows the same 6-element structure; every conceptual comment Sofia makes is preserved; every student turn is dropped.

## When to use this skill

- A raw transcript file exists (timestamped, lots of אוקיי / נו / בסדר, interleaved student names).
- Target output is a polished study walkthrough a student can read end-to-end before an exam.
- Subject is one of: point estimation, uniform / normal / CLT, hypothesis testing, confidence intervals, sampling distributions.
- The downstream renderer expects inline LaTeX (`$X \sim U(a,b)$`) embedded in Hebrew sentences.

Do NOT use this skill for:
- Pure English math lectures (different language conventions; different student dynamics).
- Lecture summaries that are already structured — the input must contain timestamps and filler to justify the pipeline.
- Generating the React component (that's `web/src/components/ExamWalkthrough.tsx`; the polished log is its data source).

## Pipeline (single stage: in-memory clean → structure)

```
raw transcript (.md or .txt, with timestamps)
   │
   │  in memory only — do NOT write intermediate files
   │  - drop every line whose speaker is a student (names listed below)
   │  - drop environmental noise (military planes, pen/mouse frustration, WiFi drops)
   │  - drop leading interjections (אוקיי, בסדר, טוב, סליחה, אה, נו, רגע, יפה, כן, נכון מאוד, חבר)
   │  - collapse the speaker's own self-corrections into the surviving form
   │  - rewrite spoken math as canonical LaTeX
   │  - keep every LaTeX-equivalent expression verbatim
   ▼
[STRUCTURE]  →  v2-<short-slug>_polished_log.md  ←  THE ONLY DELIVERABLE
```

The cleaning happens **in memory** while reading. There is no `sofia-transcript-clean.md` and no `sofia-transcript-redundancy.md` — only the final polished log is written. This is the user's chosen output shape; do not introduce intermediate artifacts even if the user previously had them.

### Student names to drop verbatim

- ניר מאיר שטילרמן
- נדב לוי
- Goldman Gal
- refael ishakbayev
- Any other `Student — <name>:` or generic `Student:` turn.

### Environment noise to drop

- Military planes passing ("מטוס צבאי עובר", etc.)
- WiFi / battery / pen / mouse frustration
- Reconnect chatter ("התחברו עוד פעם החבר'ה", "אוי, הרבה מדי, סליחה")
- Self-correction meta-comments with no informational value ("אני באמת לא מבינה מה הולך פה", "בסוף נלחמים על דברים מפגרים פה")

### Leading interjections to strip

When they appear at the start of a sentence and carry no info:
אוקיי, בסדר, טוב, סליחה, אה, נו, רגע, יפה, כן, נכון מאוד, חבר

Preserve when part of a phrase: "בסדר גמור", "יפה מאוד", "כל הכבוד" stay.

### Spoken math → LaTeX

Replace Sofia's phonetic math with canonical LaTeX:
- "איי פלוס בי חלקי שתיים" → `$E(X) = \dfrac{a+b}{2}$`
- "בי מינוס איי בריבוע חלקי שתיים" → `$V(X) = \dfrac{(b-a)^2}{12}$`
- "טי שווה 2 כפול הממוצע פחות 23" → `$T = 2\bar X - 23$`
- "זד שווה 22.2 פחות 22 חלקי שורש 1 חלקי 72" → `$Z = \dfrac{22.2 - 22}{\sqrt{1/72}}$`

When in doubt, write it the way it would appear on a blackboard — variables in math italic, operators spaced.

### Self-corrections

Keep the final form. "20.6… no wait, 20.2" → keep only "20.2".

## Output structure (6 elements per section)

This is the **only deliverable**. The user explicitly defined this shape — honor it exactly.

```markdown
# v2 — Statistics Exam Walkthrough (Polished Study Page)
**Lecturer:** <name>
**Source lecture:** <path-to-raw-transcript> (~hh:mm:ss)
**Topics:** <comma-separated list>
**Document convention:** Every section is a Question with these 6 elements:
1. **Pre-flight** — Sofia's framing before any computation.
2. **Solution Execution** — the worked mathematics, step by step. **Each step may carry its own commentary** explaining what was just done or why ("between-step commentary" — preserve Sofia's mid-step clarifications, drawing references, and method-choice notes).
3. **Final Answer** — the result distilled into one or two mathematical-notation statements.
4. **HandwrittenNote (Narration)** — Sofia's first-person Hebrew voice, written as if to the student. One sentence; math inline in $...$.
5. **Exam Traps / Things to Pay Attention To / Traps** — the conceptual warnings and exam traps.

> Notation: $a$ = lower bound of a uniform; $b$ = upper bound; $X$ = original variable; $\bar X$ = sample mean; $\mu$ = expectation; $\sigma^2$ = variance; $Z$ = standard-normal score.
> CDF = פונקציית התפלגות. PDF = פונקציית צפיפות.

---

## Exam Question Map

**Q1 — <one-line topic>** (distribution summary, n=…, estimator)
- **A** — <question in one line>  →  **<result>**
- **B** — …
…

**Q2 — <one-line topic>** (distribution summary)
- **A** — …
…
```

## Per-question body

```markdown
## Question N — <English topic title>
**Setup:** <full Hebrew problem statement, single paragraph, math in $...$>

### Section <letter> — <English title>

**1. Pre-flight**
- **What's going on:** <one English sentence>
- **Distribution in play:** <name and parameters>
- **Formulas to remember:** (one per bullet, with Hebrew gloss in parens)
  - `<latex>` (Hebrew gloss)
  - …
- **How to approach:** <2–3 English sentences>

**2. Solution Execution**  ← WITH BETWEEN-STEP COMMENTARY
1. **<step name>:**
   `<latex line>`
   > **Commentary:** <one or two sentences explaining the step, including Sofia's drawing references ("Picture the axis at 22, the line at 22.5, so the intersection is X > 22.5"), method-choice notes, or "why this and not the other way" callouts.>
2. **<step name>:**
   `<latex line>`
   > **Commentary:** …

**3. Final Answer**
- `<one or two LaTeX lines>`

**4. HandwrittenNote (Narration)**
<one Hebrew sentence, first-person, with math in $...$>
> _Handwritten note voice — as Sofia would write it in a margin annotation to a student._

**5. Exam Traps / Things to Pay Attention To / Traps**
- <conceptual point 1>
- **Critical conceptual trap:** <the central param-vs-estimate / conditional-prob-range / CLT-vs-original-normal trap, if any>
- <conceptual point N>
```

### Between-step commentary — the key change

The previous version collapsed the Solution Execution into a flat numbered list. This version requires **commentary under each step**, formatted as a blockquote starting with `> **Commentary:**`. Sofia's between-step explanations cover:

- **Drawing references** ("נוסיף ציור כמובן" → "Picture the normal curve with mean 22; mark 22.2 on the axis; we want the area to its left.")
- **Method-choice notes** ("רצוי מתוך המצוי" → "We'll use the desired/actual length ratio since it's the fastest of the three methods; the PDF rectangle-area method gives the same answer but the height cancels either way.")
- **"Why this and not the other"** ("לא צריכים את משפט הגבול המרכזי כי ה-X עצמו נורמלי" → "No CLT needed here — the original X is normal, so the sample mean is normal for any n.")
- **Self-correction callouts** ("לא 1 פחות, אלא פשוט מוסיפים מינוס" → "Note: don't subtract from 1 — just flip the sign; Z at the 0.1 percentile is the negative of Z at the 0.9 percentile.")

If Sofia did not actually interject commentary at a given step, skip the blockquote for that step. Don't invent commentary that wasn't in the source.

## Appendices (mandatory)

End the file with two appendices:

**Appendix 1 — Formula Cheat-Sheet**

Markdown table pulling every formula Sofia wrote, with the gloss she gave for it.

| Concept | Formula | Notes |
|---|---|---|
| Uniform expectation | `$E(X) = \dfrac{a+b}{2}$` | continuous uniform on `$[a,b]$` |
| Uniform variance | `$V(X) = \dfrac{(b-a)^2}{12}$` | |
| … | … | … |

**Appendix 2 — Sofia's Consolidated Exam Traps**

Numbered list, 1 sentence each, distilled from the section-level commentary. Roughly 6–10 items per lecture.

```markdown
1. **Parameter vs estimate:** never write "a = 20.2"; the parameter is unknown, only T = 20.2 is found.
2. **Conditional prob range:** result must be in [0,1]; swapping numerator/denominator is the top error.
3. **Desired/actual only for uniform** — fails for normal (density isn't flat).
…
```

End with the line: `*Generated from <raw-transcript-filename>. Structure: Pre-flight → Solution (with between-step commentary) → Final Answer → HandwrittenNote → Exam Traps per section, preserving Sofia Katzman's full conceptual framing.*`

## Hebrew ↔ Math rules

- **Hebrew sentence with math inline**: keep the Hebrew, wrap the math in `$...$`.
  - ✅ `העומד $T$ הוא חסר הטיה ל-$a$`
  - ❌ `T is unbiased for a`
- **PDF / CDF definitions** in the glosses (use these exact Hebrew terms):
  - PDF = פונקציית צפיפות
  - CDF = פונקציית התפלגות
- **Variables**: `$X$, $Y$, $T$, $a$, $b$, $\bar X$, $\mu$, $\sigma^2$, $Z$` — always math-italic.
- **Numbers in math**: never inside a Hebrew word; if it's a value, it goes in `$...$`. If it's an ordinal ("סעיף א'"), it stays Hebrew.
- **Rejection regions** in the traps: list the events in `$...$` for portability.
- **Don't translate Sofia's phonetic math** ("איי פלוס בי חלקי שתיים") literally; rewrite as canonical LaTeX.

## Common pitfalls

- **Don't merge adjacent sections** when they reuse the same distribution. Q1.A and Q1.B share `U(a, 23)`, but they're two different sub-questions and get two sections (sometimes combined under a single `### Section A & B —` header when they share a single solution flow).
- **Don't drop Sofia's self-corrections that change the answer.** If she says "20.6… no wait, 20.2", the answer is 20.2 — the correction is part of the conceptual content.
- **Don't re-number sections.** If the original exam calls them א', ב', ג', …, use those letters in the TOC and section headers.
- **Don't auto-link formulas across sections** — each section's formulas should be self-contained for printing / PDF.
- **Don't translate the Setup line.** The Setup is a verbatim problem statement in Hebrew.
- **Critical trap flag**: only on the *first* bullet of the traps section for the section where Sofia explicitly flagged it. Don't propagate to other sections.
- **Between-step commentary must come from the source.** If Sofia didn't say anything between two math lines, don't insert a `> **Commentary:**` block to fill space. Empty step ⇒ no blockquote.
- **Don't write a `sofia-transcript-clean.md`.** The user does not want intermediate files. The cleaning is in-memory; the only output is the polished log.

## Verification (always run after writing the file)

1. Confirm the file starts with `# v2 — Statistics Exam Walkthrough (Polished Study Page)`.
2. Confirm every section has all 5 numbered subheadings (Pre-flight / Solution Execution / Final Answer / HandwrittenNote / Exam Traps).
3. Confirm the Exam Question Map at the top lists every section.
4. Confirm Hebrew narration lines have their math wrapped in `$...$`.
5. Confirm the two appendices are present and complete.
6. Confirm the trailing `*Generated from …*` line is present.
7. Confirm there is no `sofia-transcript-clean.md` and no `sofia-transcript-redundancy.md` written alongside — the polished log is the only deliverable.

## Output file naming

- Polished output: `v2-<short-slug>_polished_log.md` where `<short-slug>` is the lecture's topic in 1–3 kebab-case words.
  - Examples: `v2-sofia_polished_log.md`, `v2-hypothesis_polished_log.md`, `v2-clt_polished_log.md`.
- Intermediate artifacts: **none**. Do not write `sofia-transcript-clean.md` or `sofia-transcript-redundancy.md`. If they exist from a prior run, that's the user's choice — but the skill itself does not produce them.

## Downstream consumers

This skill produces the data file consumed by:
- `web/src/components/examWalkthroughData.ts` — typed `ExamQuestion` / `ExamSection` objects. The polished log is the human source; the TS file is the typed mirror.
- `web/src/components/ExamWalkthrough.tsx` — renders the 5 elements as cards/handwritten notes in RTL Hebrew.

The companion skill `exam-walkthrough-scaffold` (in this folder's `exam-walkthrough-scaffold/` subdirectory) covers the polish → scaffold step: it takes this skill's output and produces the typed data file + the React page + the `App.tsx` / `SiteHeader.tsx` nav wiring.

## Pipeline summary (this folder is an umbrella)

```
raw transcript  ──►  [sofia-lecture-polisher]  ──►  v2-…_polished_log.md  ──►  [exam-walkthrough-scaffold]  ──►  ExamWalkthrough.tsx
```

The polish stage now produces **only** the final polished log — no clean file, no noise log. The polished log is the durable handoff; the scaffold skill consumes it directly.
