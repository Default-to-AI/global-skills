# Explicit-Command Cron Pattern

**Problem:** Open-ended prompts like "review candidates and delete safe items" cause the LLM to:
- Make poor tool choices (execute_code, write_file, skills instead of terminal)
- Hallucinate deletions or create artifacts
- Time out on complex reasoning

**Solution:** Give the LLM a precise sequence of shell commands to run.

## Template

```markdown
**Steps:**
1. Run collector, get JSON.
2. Run THESE EXACT COMMANDS (one per line, check exit codes):

```
# Category 1: description
command1
command2
...

# Category 2: description
command3
command4
...
```

3. Run collector AGAIN to verify what's left.
4. Send ONE Telegram message with summary.
```

**Rules:**
- Use ONLY `terminal` tool
- Run commands sequentially, check each exit code
- If a command fails, continue with next, note in report
- Max runtime: 5 minutes
```

## Applied Example (Hermes cleanup)

See the `hermes-cleanup-daily` cron prompt for the full worked example with:
- `__pycache__` removal (explicit paths + find for plugins)
- Age-based `find -delete` for logs, caches, screenshots
- Profile-level loops for per-profile cleanup
- Explicit denylist for `backups/pre-update-*.zip` (report only)

## Key Insight

The LLM is reliable at **executing a fixed command list** and **reporting results**. It is NOT reliable at "judge each candidate and decide."