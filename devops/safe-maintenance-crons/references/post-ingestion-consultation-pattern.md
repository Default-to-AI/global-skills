# Post-Ingestion Consultation Pattern

Embedded in `inbox-action` prompts after ingestion completes. Replaces the old "Discussion Mode" with a structured, factual, conversational loop.

## Full Pattern

```markdown
## Post-Ingestion Consultation (REQUIRED — execute after ingestion complete)

### 1. Expert Synthesis
Provide a concise 3-5 bullet expert summary of what was ingested:
- Key insights, patterns, and actionable items extracted
- What this material means in the context of the vault and Robert's objectives
- Any gaps, uncertainties, or items that need Robert's input

### 2. Connect to Existing Vault Knowledge
Search and reference explicitly:
- Related extracts, concepts, guides in the target domain wiki
- Cross-domain links via wiki/index.md, wiki/log.md, and wikilinks
- Existing plugins, tools, or workflows in the vault that relate
- Any existing Hermes skills, configs, or architecture that this touches

### 3. Recommend Next Steps with Tradeoffs
For each plausible next action, present:
- **What** it is (e.g., integrate plugin, build skill, create guide, defer)
- **Benefits** — concrete value to Robert, the vault, or agent orchestration
- **Costs/Risks** — maintenance burden, compatibility, token cost, latency, drift from upstream
- **Dependencies** — what must exist or be decided first
- **Integration check** — if it's a plugin/tool: can it install in Hermes? Config needed? Compatible with current architecture?

### 4. Ask Robert (Conversational, No Artifact)
**Do NOT produce a document or decision record.** Instead, ask directly:
>
"Do you want to: (a) Discuss integration now, (b) Dive deep on [specific topic], (c) Build/implement [specific thing], (d) Defer, or (e) Something else?"

Wait for Robert's reply. If Robert asks for clarification or provides context, incorporate it and re-ask.

### 5. Clarification Protocol
If you are uncertain about any recommendation, connection, or tradeoff:
- **Ask Robert directly** — do not guess or drift
- Frame as: "I'm unsure about [X]. Robert, can you clarify [specific question]?"
- Do not proceed with a recommendation until uncertainty is resolved

### 6. Brainstorming Mode
If Robert wants to explore options before deciding:
- Use `brainstorming` skill to generate structured options
- Stay conversational until Robert signals "let's do [X]"
- Only then propose a concrete execution plan with steps

---

Key constraints: No artifact produced, factual only (ask if uncertain), conversational until concrete plan, use `brainstorming` skill for option generation.

Origin: Added after Robert requested post-ingestion consultation that synthesizes, connects, recommends, and asks — not just summarizes.