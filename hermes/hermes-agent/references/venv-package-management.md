# Hermes venv package management

When Hermes (CLI, gateway, plugins, or skills) reports a missing Python module, the package **must be installed into the Hermes venv**, not system Python.

## Verified fix: honcho-ai (2026-06-05)

**Symptom:** Gateway log showed:
```
WARNING plugins.memory.honcho: Honcho background session init failed: honcho-ai is required for Honcho integration. Install it with: pip install honcho-ai
```

**Root cause:** `honcho-ai` was installed in system Python (`C:\Users\Tiger\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\`) but Hermes runs in its own venv at:
```
C:\Users\Tiger\AppData\Local\hermes\hermes-agent\venv\Scripts\python
```

**Fix:**
```bash
/c/Users/Tiger/AppData/Local/hermes/hermes-agent/venv/Scripts/python -m pip install honcho-ai
```

**Verification:**
```bash
/c/Users/Tiger/AppData/Local/hermes/hermes-agent/venv/Scripts/python -c "import honcho; print(honcho.__version__)"
# Output: 2.1.2
```

## General pattern

Always use the Hermes venv python explicitly:
- Windows: `%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python -m pip install <package>`
- Linux/macOS: `$HERMES_HOME/hermes-agent/venv/bin/python -m pip install <package>`

Or from within a running Hermes session, the `terminal` tool uses the venv automatically.

**Never** use bare `pip install` or system Python `python -m pip install` — those target the wrong interpreter.