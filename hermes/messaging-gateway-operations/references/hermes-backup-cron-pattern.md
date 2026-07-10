# Hermes Backup Cron Pattern

Reusable pattern for backing up `C:\Users\Tiger\AppData\Local\hermes` to GitHub via cron with Telegram notifications.

---

## Script: `C:\Users\Tiger\AppData\Local\hermes\scripts\hermes-backup.py`

```python
#!/usr/bin/env python3
r"""
Hermes backup script — runs every 12h via cron.
- Copies C:\Users\Tiger\AppData\Local\hermes → C:\Backups\hermes
- Commits & pushes to https://github.com/Default-to-AI/hermes-backup.git
- Returns exit code 0 on success, non-zero on failure
"""
import os, sys, subprocess
from datetime import datetime
from pathlib import Path

SRC = Path("C:/Users/Tiger/AppData/Local/hermes")
DST = Path("C:/Backups/hermes")
REPO_URL = "https://github.com/Default-to-AI/hermes-backup.git"
BRANCH = "main"

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)

def main():
    stamp = datetime.now().strftime("%d/%m/%Y at %H:%M")
    print(f"[BACKUP] Starting — {stamp}")

    # 1. Mirror with exclusions (robocopy)
    try:
        run([
            "robocopy", str(SRC), str(DST),
            "/MIR", "/R:2", "/W:2",
            "/NFL", "/NDL", "/NJH", "/NJS", "/XJ",
            "/XD", "__pycache__", ".pytest_cache", "node_modules", ".git", "backups", "bin",
            "/XF", "*.log", "*.pyc", "*.sqlite", "*.db", ".env.local", "uv.exe",
        ])
    except subprocess.CalledProcessError as e:
        if e.returncode >= 8:  # robocopy: >=8 = error
            print(f"[BACKUP] FAILED (copy) — {stamp}")
            return 1

    # 2. Init git repo if needed
    git_dir = DST / ".git"
    if not git_dir.exists():
        run(["git", "init"], cwd=DST)
        run(["git", "remote", "add", "origin", REPO_URL], cwd=DST)
        run(["git", "branch", "-M", BRANCH], cwd=DST)

    # 3. Commit & push
    try:
        run(["git", "add", "-A"], cwd=DST)
        status = run(["git", "status", "--porcelain"], cwd=DST)
        if status.stdout.strip():
            run(["git", "commit", "-m", f"auto-backup {stamp}"], cwd=DST)
            run(["git", "push", "-u", "origin", BRANCH], cwd=DST)
            print(f"[BACKUP] Pushed commit: auto-backup {stamp}")
        else:
            print("[BACKUP] No changes to commit")
    except subprocess.CalledProcessError as e:
        print(f"[BACKUP] FAILED (git) — {stamp}")
        print(e.stderr)
        return 1

    print(f"[BACKUP] Complete — {stamp}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## Cron Job (agent-mode for Telegram)

```bash
cronjob action=create \
  name=hermes-backup-12h \
  schedule="0 3,15 * * *" \
  deliver="telegram:8137298532" \
  prompt="Run the Hermes backup workflow and report status to Telegram.

Steps:
1. Send a start message to Telegram chat 8137298532: '🔄 Hermes backup started — DD/MM/YYYY at HH:MM' (use current local time in Tel Aviv timezone)
2. Run the backup script: python \"C:/Users/Tiger/AppData/Local/hermes/scripts/hermes-backup.py\"
3. If the script exits with code 0, send success message: '✅ Hermes backup complete — DD/MM/YYYY at HH:MM'
4. If the script exits with non-zero code, send failure message: '❌ Hermes backup FAILED — DD/MM/YYYY at HH:MM\n[include the script's stdout/stderr]'

The script handles:
- Robocopy mirror from C:\Users\Tiger\AppData\Local\hermes to C:\Backups\hermes (excluding backups/, bin/, __pycache__, .pytest_cache, node_modules, .git, *.log, *.pyc, *.sqlite, *.db, .env.local, uv.exe)
- Git commit & push to https://github.com/Default-to-AI/hermes-backup.git (main branch)
- Uses gh CLI authentication (already configured)

Timezone: Asia/Jerusalem (Tel Aviv) — current local time for timestamps."
```

---

## Key Pitfalls Learned

| Issue | Fix |
|-------|-----|
| Python docstring `\U` in `C:\Users\...` treated as unicode escape | Use raw docstring: `r\"\"\"...\"\"\"` |
| Large files (>100MB) in `backups/` and `bin/` block push | Exclude via `/XD backups bin` **before first commit** |
| robocopy `/XD` prevents copy but `/MIR` doesn't delete excluded dirs from dest | Clean dest (`rm -rf backups bin`) and reset `.git` before first successful run |
| `hermes gateway send` command doesn't exist | Use agent-mode cron (`no_agent=false`) with `send_message` tool |
| Telegram messages need dynamic timestamps | Agent-mode cron runs LLM which generates timestamp at runtime |

---

## Verification Checklist

- [ ] `python scripts/hermes-backup.py` exits 0
- [ ] `git -C C:/Backups/hermes log --oneline -1` shows commit with timestamp
- [ ] `git -C C:/Backups/hermes ls-remote origin` shows ref
- [ ] `hermes cron run <job_id>` → `delivered to telegram:<chat_id> via live adapter` in agent.log
- [ ] Telegram receives final cron delivery (✅ success message in agent's final response)
- [ ] **Note**: Start message via `hermes send` to same target is skipped by same-target guard — only final response reaches Telegram unless direct Bot API workaround is used