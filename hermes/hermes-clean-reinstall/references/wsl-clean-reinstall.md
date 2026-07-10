# WSL clean reinstall reference

## What triggered this skill

A user asked for a Dark Factory setup on WSL and later chose to replace the existing Hermes environment with a fresh one.

## Durable lessons from the session

1. `curl ... install.sh | bash` is **not** a clean reinstall if `/home/<user>/.hermes` still exists.
   - The installer will reuse the existing home.
   - It will keep old `.env` and `config.yaml`.
   - It may resume old gateway/auth/messaging state.

2. `--skip-setup` is the right first pass for automation.
   - It allows the installer to finish without blocking in the wizard.
   - Then run `hermes doctor --fix` and start auth deliberately.

3. Old messaging tokens can create the appearance of a hang.
   - The installer may pause at gateway-install prompts after printing `Messaging platform token detected!`.
   - That is not a broken install; it is leftover state leaking into setup.

4. On WSL from Git Bash/MSYS, direct host-side path calls can be mangled.
   - Prefer `wsl.exe bash -lc '...'` with explicit Linux paths.
   - Avoid relying on mixed host/WSL path interpolation when moving `/home/<user>/.hermes`.

## Concrete recovery pattern

```bash
wsl.exe bash -lc 'systemctl --user stop hermes-gateway 2>/dev/null || true; mv /home/<user>/.hermes /home/<user>/.hermes-backup-YYYYMMDD-HHMMSS'
wsl.exe bash -lc 'curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup'
wsl.exe bash -lc 'source ~/.bashrc >/dev/null 2>&1 || true; hermes doctor --fix'
wsl.exe bash -lc 'source ~/.bashrc >/dev/null 2>&1 || true; hermes status'
```

## Clean-state signals after reinstall

- no messaging platforms configured
- gateway stopped
- zero cron jobs
- zero sessions
- no Codex auth yet
- default config recreated from template
