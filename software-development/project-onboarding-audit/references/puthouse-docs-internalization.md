# PutHouse Project Onboarding Audit Notes

## Context

The user asked to investigate a project with a dense docs folder, understand its purpose, and decide whether it would benefit from `CODEX.md` or other guidance files.

## Durable pattern captured

This was not primarily a code review. It was a **project onboarding audit** combining docs internalization, implementation shape inspection, and agent-guidance recommendations.

## Project shape observed

- Domain: PutHouse options-income paper-trading evaluation.
- Core strategies: covered calls and cash-secured puts.
- Agent role: post-trade log auditing and strategy optimization, not dynamic option-chain screening.
- Key docs: `AGENT.md`, `STRATEGY.md`, `PARAMETERS.md`, and several `docs/*.md` strategy/risk explainers.
- Dashboard: React/Vite app under `dashboard/` with log builder, hypothesis view, and screener table.
- Static screener: Python/yfinance script under `scripts/screener.py` that writes generated outputs.
- Generated outputs: `dashboard/src/assets/screener_data.json`, `scripts/screener.db`, `dashboard/dist/`.

## Corrected project canon

The user corrected two important interpretations:

- **IV/RV/VRP/DTE/delta/spread/yield screening is bot-owned.** The analysis agent may cite these only as logged evidence of why the bot placed, skipped, exited, or canceled; it should not use them as independent live-selection gates.
- **Covered calls require 100 shares.** Do not infer a 200-share minimum from other cap language unless the user or actual platform behavior confirms it.

The agent role should be framed as:

> Log auditor / analyst that improves PutHouse settings and identifies stocks worth adding to the CSP universe because they are likely to generate premium, grounded in logs and evidence rather than live option-chain picking.

## Recommendation logic used

Recommended `CODEX.md` because:

- `AGENT.md` was a domain/trading role prompt, not a coding-agent operations guide.
- The project had generated files and commands a coding agent should understand before editing.
- Domain rules were spread across many docs and contained thresholds that agents must not guess.
- Some scripts were data-refreshing and should not be run casually during an audit.

Also recommended or created:

- `docs/INDEX.md` for docs reading order.
- `docs/canonical-rules.md` as the single source of truth for agent boundaries and project canon.
- Root `.gitignore` for generated outputs and dependency directories.
- `docs/trading-log-format.md` for parser/log-builder input expectations.

## Pitfall highlighted

When docs contain both general option mechanics and project-specific rules, preserve the user's confirmed project canon. Do not overinterpret secondary constraints like an 80% cap into a new share minimum when the user confirms that 100 shares is canonical.

When a tool limit interrupts a docs cleanup, report exact completed files and unfinished verification steps rather than implying the cleanup is complete.
