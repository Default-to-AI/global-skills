# Hermes CLI Direct Import Patterns (Windows Workaround)

## Problem
On this Windows Hermes host, the venv Python (`venv/Scripts/python.exe`) hangs on imports. Calling `hermes` CLI via `subprocess.run()` from Python scripts inherits this hang, causing cron timeouts with misleading `RuntimeError: [Errno 2] No such file or directory` errors.

## Solution: Direct Python Imports

Use system Python with `sys.path.insert(0, hermes_agent_root)` and import internal functions directly:

```python
import sys
sys.path.insert(0, r"C:\Users\Tiger\AppData\Local\hermes\hermes-agent")

# Status
from hermes_cli.status import show_status
import argparse
args = argparse.Namespace(all=True, deep=False)
show_status(args)

# Memory
from hermes_cli.memory_setup import memory_command
args = argparse.Namespace(memory_command='status', json=False)
memory_command(args)

# Curator
from hermes_cli.curator import _cmd_status
args = argparse.Namespace()
_cmd_status(args)

# Cron
from hermes_cli.cron import cron_command
args = argparse.Namespace(cron_command='list', json=False, ids_only=False)
cron_command(args)

# Config check
from hermes_cli.config import config_command
args = argparse.Namespace(config_command='check')
config_command(args)

# Doctor (may still be slow - uses subprocess internally)
from hermes_cli.doctor import run_doctor
args = argparse.Namespace()
run_doctor(args)
```

## Verified Working Modules (Session 2026-06-18)

| Module | Function | Tested | Notes |
|--------|----------|--------|-------|
| `hermes_cli.status` | `show_status(args)` | ✅ | ~2s, full status |
| `hermes_cli.curator` | `_cmd_status(args)` | ✅ | ~1s |
| `hermes_cli.memory_setup` | `memory_command(args)` | ✅ | ~1s |
| `hermes_cli.cron` | `cron_command(args)` | ✅ | ~1s |
| `hermes_cli.config` | `config_command(args)` | ✅ | ~1s |
| `hermes_cli.doctor` | `run_doctor(args)` | ⚠️ | Slow (60s+ timeout), may hang |

## Collector Script Refactor Pattern

**Before (hangs)**:
```python
def run_cmd(*args, timeout=45):
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return {"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode}

command_outputs = {
    "status_all": run_cmd("hermes", "status", "--all", timeout=30),
    "memory_status": run_cmd("hermes", "memory", "status", timeout=20),
    "curator_status": run_cmd("hermes", "curator", "status", timeout=20),
    "cron_list": run_cmd("hermes", "cron", "list", timeout=20),
    "doctor": run_cmd("hermes", "doctor", timeout=60),
    "config_check": run_cmd("hermes", "config", "check", timeout=20),
}
```

**After (works)**:
```python
import sys
sys.path.insert(0, r"C:\Users\Tiger\AppData\Local\hermes\hermes-agent")

def get_status_all():
    from hermes_cli.status import show_status
    import argparse, io, contextlib
    args = argparse.Namespace(all=True, deep=False)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        show_status(args)
    return buf.getvalue()

def get_memory_status():
    from hermes_cli.memory_setup import memory_command
    import argparse, io, contextlib
    args = argparse.Namespace(memory_command='status', json=False)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        memory_command(args)
    return buf.getvalue()

# ... similar for curator, cron, config
```

## Diagnostic Evidence (2026-06-18)

- `subprocess.run(["hermes", "status", "--all"], timeout=30)` → **TIMEOUT (124)**
- `subprocess.run([venv_python, "-c", "print('hello')"], timeout=10)` → **TIMEOUT (124)**
- `system_python -c "sys.path.insert(0, hermes_root); from hermes_cli.status import show_status; show_status(args)"` → **WORKS (~2s)**
- `system_python -c "import hermes_cli.config; ..."` → **WORKS**

## Root Cause Hypothesis

Windows venv Python has a deadlock or initialization issue when:
1. Spawned as subprocess from another Python process
2. Importing heavy modules (hermes_cli has 500+ imports)

System Python with manual `sys.path` insertion avoids the venv activation overhead and works reliably.