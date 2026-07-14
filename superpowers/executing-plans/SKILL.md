---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed
5. Before touching files, inspect the current branch/worktree state. If a matching isolated feature worktree already exists and contains partial implementation, resume there after verifying the current file state and running the relevant verification commands. Do not recreate work or blindly re-apply plan steps that are already present.
6. Re-validate the plan's highest-severity assumptions against the live target workspace before executing. In monorepos or split repos, verify you are reading the governing subproject files rather than a root stub. Re-run the claimed missing test/build/lint command in the real target app before preserving any P0/P1 finding from an earlier review.
7. If the plan was derived from your own prior review, treat those review claims as provisional until re-checked live. Explicitly retract and rewrite any false positive before implementation.

See `references/revalidating-plan-assumptions.md` for the monorepo/root-stub pitfall and the pre-execution recheck sequence.

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed
5. If the plan includes commit checkpoints but the repo/session policy says not to commit without explicit user approval, do not auto-commit. Treat those commit steps as progress markers and continue executing the technical work plus verification unless the user has explicitly authorized commits.

For long multi-plan chains, update durable plan checkboxes and TodoWrite state at every completed plan boundary. If execution is interrupted by context or tool-call limits, close with a deterministic resume handoff: last completed plan/task, exact active task id/status, files changed, verifications already run, and the next command/check to run.

For PowerShell-script plans, also consult `references/powershell-plan-execution-pitfalls.md` before integrating helper scripts, dot-sourcing shared functions, or adding smoke tests.

### Step 3: Complete Development

For PowerShell-script plans, also consult `references/powershell-plan-execution-pitfalls.md` before integrating helper scripts or dot-sourcing shared functions.

### Step 3: Complete Development

After all tasks complete and verified:
- If the plan file contains `generated_by: hermes` and `artifact_lifecycle: delete-after-implemented`, update the plan metadata to `status: implemented` immediately after successful verification. Do not leave generated one-off plans in a stale draft state.
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **using-git-worktrees** - Ensures isolated workspace (creates one or verifies existing)
- **writing-plans** - Creates the plan this skill executes
- **finishing-a-development-branch** - Complete development after all tasks
