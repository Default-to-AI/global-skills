# Compound Engineering to Hermes

## Question Pattern
Can an external agent/plugin ecosystem artifact be installed into Hermes directly, and if not, can its workflow still be implemented?

## Concrete Example
Upstream artifact: `EveryInc/compound-engineering-plugin`

## Findings
- The **Compound Engineering methodology** ports well to Hermes.
- The **existing EveryInc plugin repo is not Hermes-native** and should not be treated as directly installable into Hermes.

## Why
### Reusable parts
- plan → work → review → compound loop
- skill-oriented workflow entry points
- multi-agent review concept
- compounding knowledge capture

### Non-reusable as-is
- harness-specific plugin metadata for Claude/Codex/Cursor-style environments
- harness-specific tool names and interaction assumptions
- upstream install commands that target non-Hermes runtimes

## Hermes-native mapping
- planning artifacts → `.hermes/plans/`
- execution routing → `delegate_task`
- visible task state → `todo`
- review fan-out → parallel delegated reviewers
- compounding → skills + memory
- custom automation beyond skills → Hermes plugin only if needed

## Recommendation Pattern
1. Decide whether the user wants **direct installation** or **functional equivalence**.
2. If direct installation is impossible, say so plainly.
3. Preserve leverage by recommending a **skill-first port**.
4. Add a Hermes plugin only for missing hook/tool behavior after the workflow proves useful.

## Good Closeout Sentence
"Yes, the workflow is implementable in Hermes; no, the upstream plugin is not directly installable as-is. Start with a Hermes-native skill port, then add a plugin only where skills are insufficient."
