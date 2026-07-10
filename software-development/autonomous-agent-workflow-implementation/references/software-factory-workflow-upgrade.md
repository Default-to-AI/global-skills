# Software Factory Workflow Upgrade Reference

## Use case
A user wanted a "dark factory" for software development: always-ready orchestration, not manufacturing metaphors or a flat demo queue.

## Durable lessons
1. **Translate metaphor into operating stages**
   - Replace vague "factory" wording with explicit software-delivery stages.
   - Good default sequence:
     - intake
     - specification
     - architecture
     - verification planning
     - implementation fanout
     - integration gate
     - documentation
     - release readiness
     - completed

2. **Deepen the controller and the verifier together**
   - After adding more stages, the old shallow simulation may fail purely because its timeout/assertions are obsolete.
   - Fix the harness to assert stage history and artifact persistence, not just "did it finish quickly?"

3. **Stage-specific agent outputs matter**
   - Documentation agent can own intake/project brief and later handoff docs.
   - Architecture agent can own both spec refinement and system design, but the outputs must be different.
   - QA should have an early planning gate and a later integration/release gate.

4. **README lag is common after a concept pivot**
   - If the user complains that the README still reflects the old metaphor, assume the docs are stale and patch them in the same implementation pass.

## Concrete verification pattern
- Run the end-to-end simulation.
- Confirm projects hit `completed`.
- Confirm every expected stage appears in `stage_history`.
- Confirm durable work items and archived results were written.
- Confirm docs describe the same staged behavior that the simulation proved.

## Why this matters
Without these corrections, the system looks implemented but still behaves like a proof-of-concept: shallow workflow, stale docs, and a verifier that reports false negatives after the architecture improves.
