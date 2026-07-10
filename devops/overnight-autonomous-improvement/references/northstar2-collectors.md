# Northstar 2.0 Collector Inventory

## Seed Universe Scripts (scripts/)

| Script | Purpose |
|--------|---------|
| `seed_sp500.py` | Seed S&P 500 constituents |
| `seed_qqq.py` | Seed Nasdaq 100 constituents |
| `seed_dow30.py` | Seed Dow 30 constituents |
| `seed_themes.py` | Seed thematic ETFs/baskets |
| `refresh_universes.py` | Refresh all universe tables |
| `run-pipeline.py` | Orchestrate full pipeline |
| `run-scanner.py` | Run scanner |
| `collect_evidence.py` | Collect evidence packets |
| `test_yf.py` | Test yfinance connectivity |

## Research Engine Collectors (scripts/research_engine/)

| Module | CLI Entry | Purpose |
|--------|-----------|---------|
| `briefing.py` | `python -m scripts.research_engine.briefing` | Morning briefing pipeline |
| `collect_events.py` | `python -m scripts.research_engine.collect_events` | Earnings, macro, catalyst events |
| `decision_workflow.py` | `python -m scripts.research_engine.decision_workflow` | Committee decision workflow |
| `fetch_history.py` | `python -m scripts.research_engine.fetch_history` | Historical price/fundamental data |
| `scoring.py` | `python -m scripts.research_engine.scoring` | Factor scoring models |
| `sector_metrics.py` | `python -m scripts.research_engine.sector_metrics` | Sector-level metrics |
| `outcomes.py` | `python -m scripts.research_engine.outcomes` | Forward return outcomes tracking |
| `migrations.py` | `python -m scripts.research_engine.migrations` | DB schema migrations |
| `db.py` | - | SQLite connection helper |
| `sector_metrics.py` | - | Sector computations |

## Free Data Sources Used

- **yfinance** - Price history, fundamentals (no key)
- **SEC EDGAR** - Company facts, filings (no key, rate limited)
- **Finnhub Free** - Quotes, news, basic fundamentals (free tier key)
- **IBKR Flex** - Portfolio positions, transactions (requires IBKR account)

## Overnight Loop Collector Order (from session)

```python
# Prerequisite: git identity for commits (RUN ONCE IN REPO)
# git config user.email "bot@project.local"
# git config user.name "Overnight Bot"

# v3 Loop (with multi-agent pipeline)
# 1. Seed universes
run("python -m scripts.seed_sp500")
run("python -m scripts.seed_qqq")
run("python -m scripts.seed_dow30")
run("python -m scripts.seed_themes")
run("python -m scripts.refresh_universes")

# 2. Research engine - multi-agent pipeline (TradingAgents pattern)
# Stage 1: Analysts
run("python -m scripts.research_engine.briefing")
run("python -m scripts.research_engine.collect_events")
run("python -m scripts.research_engine.fetch_history")
run("python -m scripts.research_engine.scoring")
run("python -m scripts.research_engine.sector_metrics")
# Stage 2: Decision Workflow (committee/debate)
run("python -m scripts.research_engine.decision_workflow")
# Stage 3: Outcomes Tracking (reflection/memory)
run("python -m scripts.research_engine.outcomes")

# 3. Build + Verify
run("npm run build")
run("npx tsc --noEmit")
run("npm run lint")
run("npm test -- --run")

# 4. Commit
git_commit(f"chore: overnight v3 iteration {ITERATION} - research + UI + build verify")
```

## Notes

- CIK map bug: `collectors/` scripts reference `../../cik-map.json` but actual path is `../cik-map.json` from `src/services/research-engine/collectors/`
- SQLite is canonical store at `data/northstar.db` (inferred)
- `briefing.py` is the main pre-market pipeline entry point