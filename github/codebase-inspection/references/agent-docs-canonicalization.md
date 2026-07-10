# Agent-docs canonicalization pattern

Use this reference when a project has many docs plus agent/bot/workflow boundaries.

## What happened

A project contained substantial strategy docs, a role prompt, dashboard-rendered markdown, generated data files, and scripts. The user asked whether it would benefit from `CODEX.md` or other agent-facing docs. During review, the user corrected canon:

- Dynamic option metrics belonged to the bot, not the analysis agent.
- Covered calls required 100 shares, not 200.
- The analysis agent's role was log auditing, settings improvement, and CSP-universe recommendations grounded in evidence.

## Durable pattern

1. Create a coding-agent operations file (`CODEX.md`) when a repo has:
   - non-obvious generated files;
   - multiple roles/tools/bots;
   - docs that future agents must read in a specific order;
   - domain safety boundaries.
2. Add a docs index (`docs/INDEX.md`) when the docs folder has multiple overlapping files.
3. Add a canonical source-of-truth doc (`docs/canonical-rules.md`) when docs contain repeated thresholds, role boundaries, or rules likely to drift.
4. When the user corrects canon, patch the source-of-truth doc first, then search and patch all stale language across markdown.
5. Verify any app that imports/renders markdown still builds.

## Search terms that caught drift

Adapt these to the domain:

- stale thresholds (`15-45`, `7-45`, hard-coded dollar caps)
- stale role claims (`pre-screen`, `agent owns`, `bot owns`)
- obsolete requirements (`200 shares`, `80%`, exact caps)
- dynamic metrics mistakenly assigned to analysis agents (`IV/RV`, `VRP`, `DTE`, `delta`, `spread`, `yield`)

## Output standard

Report:

- files created;
- files patched;
- canonical rules now enforced;
- verification command and result;
- known non-blocking warnings.
