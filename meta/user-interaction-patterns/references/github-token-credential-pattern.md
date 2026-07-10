---
title: Git Token Detection Pattern
date-witnessed: 2026-05-23
project: northstar-2.0
---

## Locating the GitHub token in this environment

```python
import os, subprocess

# Source 1: ~/.hermes/.env — primary location
env_path = os.path.expanduser('~/.hermes/.env')
with open(env_path) as f:
    for line in f:
        if line.startswith('GITHUB_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

# Source 2: gh credential helper — checks gh hosts.yml
# gh is pre-configured with the credential helper url:
#   git config credential.https://github.com.helper=!/usr/local/bin/gh auth git-credential
# This means plain git push works if the user has authed gh in that host context.
# BUT non-interactive scripts cannot call gh auth git-credential (it prompts).
```

**Preferred script pattern:** Source `GITHUB_TOKEN` from `~/.hermes/.env`, inject into remote URL for push, then restore clean URL.

```bash
# Read from env file (bash)
export GITHUB_TOKEN=$(grep '^GITHUB_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/Default-to-AI/Northstar2.0.git"
git push origin HEAD:main
git remote set-url origin https://github.com/Default-to-AI/Northstar2.0.git  # sanitize
```

---

## Auth check before push

```python
r = subprocess.run(['git', 'ls-remote', 'origin', 'HEAD'], ...)
# exit 0 → authenticated; non-zero → check token scope or re‑gen PAT
```

If `ls-remote` fails with `Permission denied`, the token is missing `repo` scope or targets the wrong account.

---

## Northstar-2.0 repo location

| Location | Remote | Role |
|---|---|---|
| `/mnt/c/Users/Tiger/northstar` | `https://github.com/Default-to-AI/northstar-dashboard.git` | Windows path — possibly stale |
| `/home/linux/.hermes/projects/northstar-2.0` | `https://github.com/Default-to-AI/Northstar2.0.git` | **Canonical** — cron, scripts, Vercel target |

Always use the Hermes WSL path for all automation.
