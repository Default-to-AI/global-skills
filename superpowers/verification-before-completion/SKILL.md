---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| UI / HTML / SVG / chart / script artifact works | Run it in its natural environment, observe the output, and confirm the visible/runtime behavior | Static code inspection, successful file write, or "no errors" |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Hitting a tool/iteration limit and implying completion anyway instead of naming unfinished verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Use `completion-contract-loop` when done criteria can drift → Verify each requirement → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Multi-step work / final-story gate:**
```
✅ For multi-step work, the final completion claim must name the critical last story/step, the exact verification command or runtime check used for it, and the observed result.
✅ If earlier steps are done but the last critical story lacks evidence, report partial completion only.
❌ "Most of it is done so the task is done"
❌ Marking the whole task complete when the final critical step has no verification evidence
```

**Interrupted work:**
```
✅ State completed artifacts exactly → State unverified/incomplete steps → Do not claim final completion
❌ "Done" after a tool limit, timeout, or partial patch pass without fresh verification
```

**Credential-bearing launches / config changes:**
```
✅ If the task requires a literal secret or password value to be applied, the real launch/config command must use that literal value (even if tool output later redacts it) and verification must prove the resulting service/config is the one you just started.
✅ If you replaced the secret with `***`, `<redacted>`, or another placeholder in the command itself, treat the configuration as UNVERIFIED — you have only tested the placeholder, not the requested value.
❌ Claiming "password set" or "config applied" when the shell command you actually ran contained a masked placeholder instead of the literal requested value.
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Multi-Step Review / Plan-Tracking Addendum

When reviewing or verifying work that follows a written implementation plan, do not keep the checklist only in chat context.

### Repo-visible progress tracking
- Create or update a repo-visible progress note (for example under `temp/` or another non-release scratch area) that marks task/step status.
- Record both **status** (`done` / `pending` / `blocked`) and **evidence** (command result, source inspection result, manual check status).
- Update that file during the session as verification evidence changes.
- For vague or multi-requirement completion criteria, load `completion-contract-loop` and track requirements as `missing` / `weak` / `proved` / `contradicted` instead of using a loose checklist.

### Distinguish gate-passing from feature completion
Passing tests, TypeScript, lint, or build is **not** enough to claim the feature is complete.

For feature/UI work, explicitly separate:
1. **Automated gates** — tests, compiler, lints, build
2. **Acceptance integration** — is the new code actually wired into the real feature path?
3. **Manual/runtime checks** — browser/UI behavior when required by the task

If (1) passes but (2) fails, report **partial verification only** and block completion.

### Source-backed acceptance checks
If acceptance depends on removing old UI or wiring in new logic, run targeted source checks and record the counts/locations.
Examples:
- exact legacy labels still present
- old state variable still referenced
- new component/import/hook absent from the integration file

These checks are evidence for whether the implementation plan's acceptance criteria are truly met.

### When browser/manual validation is incomplete
If the browser reaches the app shell but the UI does not render correctly in the validation environment, do **not** pretend the manual check passed.
Instead:
- state that manual validation remains incomplete,
- preserve the automated verification evidence,
- use source inspection to determine whether the integration is complete enough for a PASS/FAIL verdict.

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
