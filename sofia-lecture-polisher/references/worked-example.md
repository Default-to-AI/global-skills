# Reference: Worked Example (input → output)

A minimal before/after pair so a future agent can see the transformation at a glance without re-reading the SKILL.md.

## Input (raw transcript fragment)

```
[00:15:15] Student — ניר מאיר שטילרמן:
    זה איי ועוד 23 חלקי 2, יכול להייות? זה התוחלת של איקס, נכון מאוד.

[00:15:31] Sofia (Prof):
    אוקיי, אז נכון, התוחלת של איקס שמתפלג אחיד, בואו נרשום את זה פה למטה.
    אם יש לנו איזשהו איקס, נו, מה זה היה ועזוב פה? בסוף נלחמים על דברים מפגרים פה.
    אז אם ישנו איזשהו איקס, אני באמת לא מבינה מה הולך פה. שמתפלג אחיד בין איי לבי,
    התוחלת של איקס זה אכן איי פלוס בי, חלקי 2. ואם כבר אנחנו מדברים פה על נוסחאות,
    אז גם שונות של איקס, שמתפלג אחיד רציף, שימו לב, פי מינוס איי בריבוע,
```

## After Stage 1 (clean)

```
[00:15:31] Sofia (Prof):
    התוחלת של איקס שמתפלג אחיד, אם יש איקס שמתפלג אחיד בין איי לבי,
    התוחלת של איקס זה איי פלוס בי, חלקי 2. ושונות של איקס, שמתפלג אחיד רציף,
    שימו לב, בי מינוס איי בריבוע חלקי 12.
```

(Drop: student turn, אוקיי, נו, "מה זה היה ועזוב פה", "אני באמת לא מבינה מה הולך פה", "בסוף נלחמים על דברים מפגרים פה", all of the 0% content WiFi/mouse complaints.)

## After Stage 3 (polished)

```markdown
### Section A — Unbiased Estimator

**Pre-flight**
- **What's going on:** Is the proposed estimator $T$ unbiased for the unknown lower bound $a$?
- **Distribution in play:** $X \sim U(a, 23)$ — continuous uniform (time/length is continuous, never discrete).
- **Formulas to remember:**
  - $E(X) = \dfrac{a+b}{2}$  (expectation of uniform)
  - $V(X) = \dfrac{(b-a)^2}{12}$  (variance of uniform)
  - $E(\bar X) = E(X)$  (linearity of expectation; reused in CLT)
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
```

## What to learn from this

- The 5-layer structure compresses ~2 minutes of raw transcript into ~25 lines of polished output.
- Every formula gets a Hebrew gloss in the `Formulas to remember` bullets (rendered as a `FormulaBlock` chip downstream).
- The `Narration` is exactly one Hebrew sentence with the math inline — that's a hard rule, not a guideline.
- The "⇒" arrow appears only in `Solution Execution` to mark a conclusion of a sub-step, not in `Final Answer` (which stands on its own).
