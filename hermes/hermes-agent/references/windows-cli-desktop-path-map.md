# Windows CLI/Desktop Hermes path map

Use this when a user asks whether multiple Hermes-looking folders are the same system, or whether `hermes update` will mutate a dev checkout.

## Verified example layout

Observed live paths:
- working directory: `C:\Users\Tiger`
- `HERMES_HOME`: `C:\Users\Tiger\AppData\Local\hermes`
- live CLI launcher: `C:\Users\Tiger\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes`
- live runtime repo: `C:\Users\Tiger\AppData\Local\hermes\hermes-agent`
- Desktop Electron profile: `C:\Users\Tiger\AppData\Roaming\Hermes`
- separate dev checkout: `C:\Users\Tiger\hermes-agent`

## Meaning of each path

### `C:\\Users\\Tiger\\AppData\\Local\\hermes`

Operational Hermes home. Shared backend state lives here:
- `config.yaml`
- `.env`
- `auth.json`
- `state.db`
- `logs\...`
- `profiles\...`
- `skills\...` — **may be a Windows SymbolicLink** to an external folder (e.g., `C:\\Users\\Tiger\\AI Hub\\Global Skills`). Verify with `powershell Get-Item <path> | Select LinkType, Target` before assuming it's a real directory.
- runtime repo under `hermes-agent\...`

### `C:\Users\Tiger\AppData\Roaming\Hermes`

Desktop-only Electron userData. Contains shell/app-state such as:
- `connection.json`
- `Preferences`
- `Local State`
- `Cache\...`
- `Network\...`
- `Session Storage\...`
- `composer-images\...`

### `C:\Users\Tiger\hermes-agent`

Standalone source checkout. Not live unless `command -v hermes` or Desktop update-root resolution points at it.

### `C:\Users\Tiger\.hermes`

Legacy/alternate Hermes home path. May be active on some installs, but do not assume. Verify with `HERMES_HOME`, `hermes config path`, or Desktop's home-resolution logic.

## Desktop local-mode interpretation

When Desktop `connection.json` contains local mode, interpret it as:
- Desktop runs as a GUI frontend
- Desktop keeps its Electron state under `%APPDATA%\Hermes`
- Desktop points at the local Hermes backend under `HERMES_HOME`

Conclusion: same backend, different frontend state.

## Update target checklist

1. Resolve launcher:
   - `command -v hermes`
   - `hermes --version`
2. Confirm project root reported by Hermes.
3. Inspect the repo at that root:
   - git remote
   - current branch
4. Treat that repo as the update target.

## Symlink awareness checklist

When mapping Hermes paths on Windows, also verify:
- `skills` directory under `HERMES_HOME` — may be a `SymbolicLink` to an external "Global Skills" folder (or similar). Use PowerShell `Get-Item <path> | Select LinkType, Target` to confirm. `ls -la` in git-bash shows it as a regular directory (inode identical to target).
- If symlinked, the symlink target is the effective skills source; curator, skill installs, and profile reconciliation operate on the resolved path.

## Verified update takeaway

In the verified session, the live install repo was:
- `C:\Users\Tiger\AppData\Local\hermes\hermes-agent`

The separate checkout at `C:\Users\Tiger\hermes-agent` was not the active runtime and therefore was not the normal `hermes update` target.

## Caution

If the live install repo is on a non-main branch, future `hermes update` behavior follows that branch context. Path mapping alone is not enough; branch state can change what "update" means.