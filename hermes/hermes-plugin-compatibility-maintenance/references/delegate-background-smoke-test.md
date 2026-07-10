# Delegate background handle smoke test

## When to use
Use after patching a plugin that intercepts `delegate_task` or runtime tool dispatch, especially when Hermes core adds a new delegate parameter like `background`.

## Goal
Prove that `background=true`:
1. does not raise a Python `TypeError`, and
2. returns the normal async delegation handle shape (`status=dispatched`, `delegation_id`, `mode=background`).

## Minimal verification pattern
Run a controlled Python smoke against the installed plugin and live Hermes modules, but stub the expensive side effects:
- replace `tools.delegate_tool._build_child_agent` with a fake child builder
- replace `tools.async_delegation.dispatch_async_delegation` with a stub returning a known handle
- call `plugin.register(None)`
- exercise BOTH paths:
  - `agent.agent_runtime_helpers.invoke_tool(..., "delegate_task", {background: True, ...})`
  - `tools.registry.registry.get_entry("delegate_task").handler(...)`

## Assertions
- `json.loads(result)["status"] == "dispatched"`
- `json.loads(result)["delegation_id"]` exists
- `json.loads(result)["mode"] == "background"`
- delegate schema still contains both `profile` and `background`
- no `TypeError` is raised anywhere in the invoke-tool shim, plugin wrapper, or registry handler path

## Why this pattern matters
A plugin can look fixed by source inspection while still failing in one forwarding path:
- runtime wrapper
- invoke-tool interception
- registry re-registration handler

Stubbing async dispatch isolates the contract test from real child execution and lets you verify the returned handle shape safely and quickly.
