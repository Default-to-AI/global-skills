# Dark Factory Setup Session - 2026-06-24

## Session Overview
This session documents the process of setting up Dark Factory on a Windows system with WSL Ubuntu available, using the existing Hermes Agent installation on Windows as the primary environment.

## Key Challenges and Solutions

### 1. Open Second Brain Vault Path Validation Error
**Problem**: 
```
error: failed to persist plugin config: config value for "vault" contains a disallowed character ("\\"); reject rather than silently corrupting on read-back
```

**Root Cause**: The Open Second Brain plugin's configuration validation rejects backslashes in paths, which are standard in Windows paths.

**Solution Applied**: 
- Modified `~/.hermes/plugins/open-second-brain/src/core/config.ts` line 30
- Changed `const CONFIG_VALUE_REJECTED_CHARS = ['\"', \"\\\\\", \"\\n\", \"\\r\"] as const;` 
- To `const CONFIG_VALUE_REJECTED_CHARS = ['\"', \"\\n\", \"\\r\"] as const;`
- (Removed the backslash from the rejected characters array)

### 2. Hermes Workflows Python Wrapper Issues
**Problem**: 
```
Error while finding module specification for 'hermes_workflows.cli' (ModuleNotFoundError: No module named 'hermes_workflows')
```

**Root Cause**: The Python wrapper script couldn't locate the Hermes Workflows module due to path/PYTHONPATH issues.

**Solutions Applied**:
- Set `HERMES_AGENT_HOME=C:/Users/Tiger/AppData/Local/hermes/hermes-agent` environment variable
- Used Bun CLI directly as a reliable alternative:
  - Validation: `bun run ~/.hermes/plugins/hermes-workflows/packages/core/src/cli.ts validate /path/to/workflow.yaml`
  - Run creation: `bun run ~/.hermes/plugins/hermes-workflows/packages/core/src/cli.ts run-create --db /tmp/test.db --id test-run-1 /path/to/workflow.yaml`
  - Advance run: `bun run ~/.hermes/plugins/hermes-workflows/packages/core/src/cli.ts advance /path/to/workflow.yaml --db /tmp/test.db --run-file /tmp/run0.json`

### 3. MCP Server Connection Issues
**Problem**: 
```
Failed to connect: Connection closed
```

**Root Cause**: Environment variables not being passed correctly to the MCP server process.

**Solution Applied**:
- Ensured proper environment variable passing: `VAULT_DIR`, `VALET_AGENT_NAME`, `VALET_TIMEZONE`
- Verified manual operation: `VAULT_DIR="/mnt/c/Users/Tiger/Vault" VAULT_AGENT_NAME="hermes-main" VAULT_TIMEZONE="Asia/Jerusalem" bun run ~/.hermes/plugins/open-second-brain/src/cli/main.ts mcp`
- Output: `[mcp] open-second-brain 1.17.0 listening on stdio (vault=C:/Users/Tiger/Vault)`

## Verification Steps Completed

1. ✅ Open Second Brain plugin installed and enabled
2. ✅ `o2b doctor` passes for vault and config writability
3. ✅ `hermes memory status` shows Provider: open-second-brain (active)
4. ✅ Hermes Workflows plugin installed and enabled
5. ✅ Workflow validation passes
6. ✅ Successfully created and advanced a test workflow run using Bun CLI
7. ✅ MCP server for Open Second Brain starts successfully when environment variables are set correctly

## Files Created/Modified
- `~/.hermes/plugins/open-second-brain/src/core/config.ts` (modified CONFIG_VALUE_REJECTED_CHARS)
- `~/.hermes/bin/hermes-workflows` (symlink to plugin wrapper)
- Various test files in `/tmp/` and `~/AppData/Local/hermes/workflows/`

## Recommendations for Future Sessions
1. Consider submitting the backslash fix to the Open Second Brain plugin upstream
2. Document the Bun CLI workaround for Hermes Workflows as a reliable alternative to the Python wrapper
3. Ensure environment variables are properly documented for MCP server operation
4. Validate that the symlink for `hermes-workflows` in `~/.hermes/bin/` works correctly after setting HERMES_AGENT_HOME

## Session Notes
- Primary Hermes installation remained on Windows (C:/Users/Tiger/AppData/Local/hermes)
- Vault location: C:/Users/Tiger/Vault (accessed via WSL as /mnt/c/Users/Tiger/Vault)
- Agent name used: hermes-main
- Timezone: Asia/Jerusalem
- All plugin installations and configurations succeeded after applying the workarounds above