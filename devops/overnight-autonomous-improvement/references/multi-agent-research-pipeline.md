# Multi-Agent Research Pipeline Pattern (TradingAgents-Inspired)

Source: `C:\Users\Tiger\AI Hub\Projects\TradingAgents` - LangGraph-based multi-agent trading research system.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  TRADINGAGENTS GRAPH (LangGraph)                              │
├─────────────────────────────────────────────────────────────┤
│  1. ANALYSTS (parallel)                                       │
│     ├─ Market Analyst      → price/volume/technicals         │
│     ├─ Social Analyst      → social sentiment                │
│     ├─ News Analyst        → news/events/catalysts           │
│     └─ Fundamentals Analyst → financial statements/ratios    │
├─────────────────────────────────────────────────────────────┤
│  2. RESEARCH DEBATE (Bull vs Bear)                            │
│     ├─ Bull Researcher     → optimistic case                 │
│     ├─ Bear Researcher     → pessimistic case                │
│     └─ Research Manager    → synthesis + investment plan     │
├─────────────────────────────────────────────────────────────┤
│  3. RISK DEBATE (Aggressive/Conservative/Neutral)             │
│     ├─ Aggressive Debator  → maximize upside                 │
│     ├─ Conservative Debator → minimize downside              │
│     ├─ Neutral Debator     → balanced view                   │
│     └─ Portfolio Manager   → final trade decision            │
├─────────────────────────────────────────────────────────────┤
│  4. MEMORY & REFLECTION                                       │
│     ├─ TradingMemoryLog    → past decisions + outcomes       │
│     ├─ Reflector           → learn from forward returns      │
│     └─ Checkpointer        → resume crashed runs             │
└─────────────────────────────────────────────────────────────┘
```

## Key Patterns for Overnight Loops

### Stage 1: Parallel Analysts (Data Collection)
```python
# Run independently, no dependencies between them
run("python -m scripts.research_engine.briefing")      # Market context
run("python -m scripts.research_engine.collect_events") # Catalysts
run("python -m scripts.research_engine.fetch_history")  # Price history
run("python -m scripts.research_engine.scoring")        # Factor scores
run("python -m scripts.research_engine.sector_metrics") # Sector context
```

### Stage 2: Decision Workflow (Debate Synthesis)
```python
# Consumes all analyst outputs, produces committee decisions
run("python -m scripts.research_engine.decision_workflow")
```

### Stage 3: Outcomes Tracking (Reflection)
```python
# Computes forward returns, stores for future memory
run("python -m scripts.research_engine.outcomes")
```

## State Management (AgentState)

```python
# From tradingagents/agents/utils/agent_states.py
class AgentState(MessagesState):
    company_of_interest: str
    trade_date: str
    
    # Analyst reports
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str
    
    # Debate states
    investment_debate_state: InvestDebateState  # bull/bear history
    investment_plan: str
    
    trader_investment_plan: str
    
    risk_debate_state: RiskDebateState  # aggressive/conservative/neutral
    final_trade_decision: str
    
    # Memory
    past_context: str  # Same-ticker decisions + cross-ticker lessons
```

## Memory & Reflection Loop

```python
# From TradingAgentsGraph._resolve_pending_entries()
# Runs at START of each new run for same ticker
def resolve_pending_entries(ticker):
    pending = memory_log.get_pending_entries(ticker)
    for entry in pending:
        raw, alpha, days = fetch_returns(entry.date)
        if raw is None: continue  # not enough data yet
        
        reflection = reflector.reflect_on_final_decision(
            final_decision=entry.decision,
            raw_return=raw,
            alpha_return=alpha,
            benchmark_name="SPY"
        )
        memory_log.batch_update_with_outcomes(updates)
```

## Adapting to Northstar 2.0

| TradingAgents Component | Northstar 2.0 Equivalent |
|-------------------------|--------------------------|
| Market Analyst | `briefing.py` + `fetch_history.py` |
| News/Social Analyst | `collect_events.py` |
| Fundamentals Analyst | `scoring.py` (factor models) |
| Bull/Bear Debate | `decision_workflow.py` (committee) |
| Risk Debate | Risk governance in `config/risk-model/v1.json` |
| Portfolio Manager | Committee output → trade playbook |
| TradingMemoryLog | `decision_outcomes` table + Obsidian thesis notes |
| Reflector | `outcomes.py` forward returns |
| Checkpointer | SQLite transaction log (implicit) |

## Implementation in Overnight Loop

```python
def run_research_pipeline():
    log("RESEARCH: Running multi-agent pipeline...")
    
    # Stage 1: Analysts (parallel data collection)
    log("  Stage 1: Analysts collecting data...")
    run("python -m scripts.research_engine.briefing")
    run("python -m scripts.research_engine.collect_events")
    run("python -m scripts.research_engine.fetch_history")
    run("python -m scripts.research_engine.scoring")
    run("python -m scripts.research_engine.sector_metrics")
    
    # Stage 2: Decision workflow (committee/debate)
    log("  Stage 2: Decision workflow (committee)...")
    run("python -m scripts.research_engine.decision_workflow")
    
    # Stage 3: Outcomes tracking (reflection/memory)
    log("  Stage 3: Outcomes tracking...")
    run("python -m scripts.research_engine.outcomes")
```

## Advanced Overnight Loop v3 Pattern (from session)

The v3 loop adds **live research subagent framework** and **incremental UI improvements**:

```python
# v3 overnight_loop.py structure
def run_live_research_subagents(iteration):
    """Spawn subagents for live research (when delegate_task available)"""
    log(f"RESEARCH: Live research phase {iteration}...")
    # In background context: log intent for main context to act on
    # Actual subagents would run: delegate_task(goal="find new data sources", ...)

def apply_ui_improvements(iteration):
    """Apply incremental UI improvements to CommandCenter.tsx"""
    log(f"UI: Applying iteration {iteration} improvements...")
    # Priority: build validation after each change
    # 1. Responsive grid layout (grid-cols-1 lg:grid-cols-2 xl:grid-cols-3)
    # 2. Semantic color tokens (bg-card, text-primary, text-muted-foreground)
    # 3. LIVE indicator with pulse animation + current time
    # 4. Consistent font-mono, text-[10px] for dense data
    # 5. max-w-full instead of max-w-[1200px]

# In iteration():
run_live_research_subagents(ITERATION)
apply_ui_improvements(ITERATION)
```

**Morning deliverable enhanced:**
- `overnight_v3.log` with research + UI phases
- Git commits include meaningful UI changes
- Clean build/lint/test traceability