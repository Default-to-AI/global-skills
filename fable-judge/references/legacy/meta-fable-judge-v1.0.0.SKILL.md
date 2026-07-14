---
name: fable-judge
description: "Use when work is claimed complete, an agent/tool reports \"done\", or before presenting substantive output as finished — runs an adversarial verification pass that re-runs every claimed check, diffs actual changes, and hunts weakened tests + false completion claims. Verdicts: VERIFIED / CAVEATS / REFUTED."
version: 1.0.0
author: "Hermes Agent (ported from Sahir619/fable-method)"
license: MIT
metadata:
  hermes:
    tags: [verification, adversarial, audit, closeout, quality]
    related_skills: [verification-before-completion, verification-plan, completion-contract-loop]
---

# fable-judge — Adversarial Verification of Finished Work

## Overview

The most documented failure of coding agents is claiming success regardless of reality: reward hacking grows with codebase size, agents end failure transcripts with "all tests pass", and tests get weakened until they agree. `verification-before-completion` stops you from *asserting* without evidence. **fable-judge goes further**: it treats a completion report as a set of *claims* and believes nothing it did not *observe*, actively hunting the ways a "done" report can be false.

This is the **prove** half of the Fable Workflow (think = fable-method, act = fable-loop, prove = fable-judge). Ported to Hermes as a standalone closeout/audit skill. It is complementary to `verification-before-completion`, not a replacement: run that gate first (evidence before claims), then run fable-judge when the report itself needs adversarial scrutiny — unattended runs, fanned-out subagents, third-party/agent success reports, or anything where a lying "done" claim would be costly.

## When to Use

- An agent, tool, or subagent reports "work complete" / "all tests pass" / "success" — especially unattended or parallel runs.
- Before presenting substantive work as finished to Robert.
- After a large change where weakened tests or silent scope drops are plausible.
- When a completion report and the actual state could disagree (spec vs test vs code conflict).
- **Don't use for:** routine single-command verification (use `verification-before-completion`); trivial 2-sentence tasks.

## The Adversarial Pass (run in this order)

### 1. Inventory claims
Treat the report as a list of discrete claims. For each: *what specific state would have to be true for this claim to hold?* Examples:
- "Tests pass" → the full test command exited 0 with 0 failures.
- "Bug fixed" → the original failing input now produces correct output.
- "Feature wired in" → the new code is reachable from the real integration path.
- "X refactored" → old code is gone, new code present, behavior unchanged.

### 2. Demand observed evidence per claim
For every claim, re-observe independently — do not trust the report's self-description:
- **Re-run the check**: execute the test/build/lint command fresh; read full output + exit code.
- **Diff actual change**: `git diff` / `git status` to see what *actually* changed vs what was *claimed* changed.
- **Inspect the artifact in its natural environment**: run the script, hit the endpoint, render the UI — don't accept "file written / no errors" as proof.
- If you cannot re-run or observe a claimed check → it is **not verified**; relabel it as a CAVEAT, never assert it.

### 3. Hunt the four failure modes
| Failure mode | What it looks like | How to catch it |
| --- | --- | --- |
| **Weakened test** | A test was edited so it now passes but no longer asserts the requirement (assertion removed, range widened, mocked). | `git diff` the test file; check the assertion still enforces the original contract; reverted-fix red-green check if unsure. |
| **False completion** | Report says done but actual state contradicts it (missing file, uncommitted change, broken import). | Independent state inspection: file exists? command exits 0? import resolves? |
| **Authority conflict** | Code, a test, and a spec disagree (e.g. failing test is itself wrong vs README). | Force an `INTENT:` line (see below) before deciding; never silently rewrite correct code to satisfy a wrong test. |
| **Silent scope drop** | Parts of the request were skipped without note (edge case, cleanup, a secondary file). | Re-read the original ask line-by-line; mark each requirement proved / missing / weak. |

### 4. The INTENT artifact (authority conflicts)
When code, a check, and a spec disagree, do NOT guess. Emit a forced line in your report:
```
INTENT: code does X / check expects Y / spec says Z
```
Then decide which is wrong and surface the contradiction — fix the *test* if the test is wrong, fix the *code* if the code is wrong. Weak models follow rules at decision points, not in lists; the forced artifact is what makes the conflict visible instead of hidden.

### 5. Verdict
- **VERIFIED** — every claim re-observed; no weakened tests, no contradictions, no scope drops.
- **CAVEATS** — work likely correct but ≥1 claim could not be observed (relabeled, not asserted) or a minor scope item deferred with note.
- **REFUTED** — a claimed check fails on re-run, a test was weakened, or the report contradicts actual state. Do not present as done.

Report outcome-first: lead with the verdict, then the evidence per claim, then honest caveats. Never bury a REFUTED behind prose.

## Hard Bounds
- Can't name or re-run a verification → say so as a CAVEAT. Do not imply success.
- 3 failed verify cycles on the same claim → stop and hand back with what's proven vs not.
- A REFUTED claim → block completion; do not "Done" the task.

## Common Pitfalls
1. **Trusting the report's self-description.** "All tests pass" is a claim, not evidence. Re-run.
2. **Weakened-test blindness.** Seeing a green test and assuming it tests the requirement — diff the test file.
3. **Confusing gate-pass with feature-complete.** Build/lint passing ≠ wired into the real path. Inspect integration.
4. **Asserting unobservable claims.** If you couldn't run it, call it a CAVEAT.
5. **Silently fixing the wrong side of a conflict.** The failing test may be correct and the code wrong, or vice versa — force INTENT, then decide.

## Verification Checklist
- [ ] Every claim in the report inventoried.
- [ ] Each claim re-observed (command run / diff read / artifact run) — not trusted from the report.
- [ ] Test files diffed for weakened assertions.
- [ ] Any code/check/spec conflict resolved via INTENT artifact.
- [ ] Scope drops checked against original ask.
- [ ] Verdict issued: VERIFIED / CAVEATS / REFUTED.
- [ ] Outcome stated first, with per-claim evidence and honest caveats.

## Relationship to Other Skills
- `verification-before-completion` — the iron gate (evidence before any claim). Run it first.
- `verification-plan` — define measurable success criteria up front; fable-judge checks them after.
- `completion-contract-loop` — track requirements as proved/weak/missing; fable-judge supplies the adversarial evidence.

## Source
Ported from `Sahir619/fable-method` (the Fable Workflow). The upstream ships a crime scene — `eval/scenarios/s7-fraudulent-work/` — a "completed" agent task with five planted frauds behind a lying completion report; point any model at it with fable-judge to see the pass in action. See `references/adversarial-checklist.md` for the expanded failure-mode → check mapping.
