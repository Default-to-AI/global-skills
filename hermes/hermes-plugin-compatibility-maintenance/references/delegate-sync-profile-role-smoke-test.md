# Delegate sync profile/role smoke test

## When to use
Use after touching a plugin that patches `delegate_task` to preserve extra contract fields such as `profile`, especially when you need to prove the sync path still accepts newer or non-core arguments like `role` alongside the required `parent_agent` runtime context.

## Goal
Prove that sync delegation:
1. accepts `profile`, `role`, and `parent_agent` without raising `TypeError`, and
2. returns the normal JSON result string shape through every patched forwarding path.

## Minimal verification pattern
Run a controlled Python smoke against the installed plugin and live Hermes modules, but stub child creation/execution so no real subagent or model call runs:
- import the installed plugin and live Hermes modules
- call `plugin.register(None)`
- patch `tools.delegate_tool._resolve_delegation_credentials` to return inert inherited creds
- patch `tools.delegate_tool._load_config` with a small `max_spawn_depth`/`max_iterations` config
- patch `tools.delegate_tool._build_child_agent` to return a fake child carrying `_delegate_role`
- patch `tools.delegate_tool._run_single_child` to return a known completed result
- exercise ALL relevant sync paths:
  - direct `tools.delegate_tool.delegate_task(...)`
  - `tools.registry.registry.get_entry("delegate_task").handler(...)`
  - `agent.agent_runtime_helpers.invoke_tool(..., "delegate_task", ...)`

## Assertions
- no `TypeError` is raised for `profile`, `role`, or `parent_agent`
- each path returns a **string**, not a dict/object
- `json.loads(result)["results"][0]["status"] == "completed"`
- the result summary proves explicit `role` survived forwarding (for example `done via role=orchestrator`)
- delegate schema still contains `profile`

## Why this pattern matters
A profile-preserving plugin can succeed in one path while still dropping fields in another:
- direct runtime wrapper
- invoke-tool interception
- registry re-registration handler

Stubbing child execution isolates the contract test from real delegation while still proving the argument plumbing and return shape across the live patched stack.
