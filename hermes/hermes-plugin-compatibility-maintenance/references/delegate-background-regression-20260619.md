# Delegate background regression — 2026-06-19

## Scenario
A local Hermes plugin named `delegate-profile-contract` monkey-patched `delegate_task` to preserve `profile` support, but Hermes core later added `background` support to `delegate_task`.

## Symptom
Delegation failed with:
- `_install_delegate_runtime_patch.<locals>.patched_delegate_task() got an unexpected keyword argument 'background'`

## Root cause pattern
The plugin mirrored an older core signature and manually forwarded arguments. After core evolution, the plugin was stale.

## Concrete evidence
### Plugin enabled globally
`C:\Users\Tiger\AppData\Local\hermes\config.yaml`
- `plugins.enabled` included `delegate-profile-contract`

### Stale plugin wrapper
`C:\Users\Tiger\AppData\Local\hermes\plugins\delegate-profile-contract\__init__.py`
- `patched_delegate_task(...)` accepted `goal, context, profile, toolsets, tasks, max_iterations, acp_command, acp_args, role, parent_agent`
- it did **not** accept `background`

### Current core signature
`C:\Users\Tiger\AppData\Local\hermes\hermes-agent\tools\delegate_tool.py`
- `delegate_task(..., role: Optional[str] = None, background: Optional[bool] = None, parent_agent=None)`

## Forwarding paths that required updates
1. runtime wrapper function signature
2. forwarding call into `original_delegate_task(...)`
3. invoke-tool interceptor forwarding from `function_args`
4. tool registry handler forwarding from `args`
5. invoke-tool wrapper signature itself, because current core dispatch passes middleware arguments beyond the older 7-argument shim

## Minimal fix
Thread `background` through all delegate paths and update the dispatch shim to forward the current `invoke_tool` call shape:
- accept `skip_tool_request_middleware`
- accept `tool_request_middleware_trace`
- accept/pass `*extra_args, **extra_kwargs` for future core additions
- pass `background=function_args.get("background")` in the delegate intercept path
- pass `background=args.get("background")` in the registry handler

When wrapping an older core `delegate_task` that may not accept `background`, inspect the original signature and only include `background` if the original accepts it or has `**kwargs`.

## Verification shape after patch
Use both isolated smokes and live-module smokes:
1. `py_compile.compile()` on the plugin file.
2. Import the plugin in a fresh Python process.
3. Fake old/new delegate modules and assert the wrapper forwards `background` while preserving `profile` behavior.
4. Fake `agent.agent_runtime_helpers.invoke_tool` with current 9-positional-argument shape and assert:
   - non-`delegate_task` calls forward to the original function with middleware args intact
   - `delegate_task` calls forward `profile` and `background` into the patched delegate function
5. Fake `tools.registry.registry.register` and assert the registered handler forwards `background`.
6. Import real `tools.delegate_tool`, call `plugin.register(None)`, and assert:
   - `profile` exists in `DELEGATE_TASK_SCHEMA`
   - `background` remains in `DELEGATE_TASK_SCHEMA`
   - `runtime_helpers.invoke_tool` includes the current middleware parameters
7. Call the real registered `delegate_task(goal="smoke", profile="default", background=True, parent_agent=None)` and expect the normal `requires a parent agent context` error, not a Python `TypeError`.

Expected: no argument error; async calls after a Hermes/WebUI restart should return a delegation handle / background dispatch result.
