#!/usr/bin/env python3
"""Acknowledge environmental <head> spawnSync ETIMEDOUT sync failures in
gbrain's sync-failures ledger. These are hard-blocked by design (sync.ts
~line 2713) so `gbrain sync --skip-failed` cannot clear them.

Only flips entries that are:
  path == "<head>" AND code == "UNKNOWN" AND "ETIMEDOUT" in error
  AND state == "open" AND not already acknowledged.

Preserves the audit trail (does NOT delete). Everything else untouched.
"""
import json
import os
from datetime import datetime, timezone

LEDGER = os.path.expanduser(r"~/.gbrain/sync-failures.jsonl")


def main() -> None:
    if not os.path.exists(LEDGER):
        print(f"no ledger at {LEDGER}; nothing to do")
        return
    with open(LEDGER, "r", encoding="utf-8") as f:
        lines = [l for l in f.read().splitlines() if l.strip()]

    changed = 0
    now = datetime.now(timezone.utc).isoformat()
    out = []
    for l in lines:
        try:
            rec = json.loads(l)
        except Exception:
            out.append(l)
            continue
        is_target = (
            rec.get("path") == "<head>"
            and rec.get("code") == "UNKNOWN"
            and "ETIMEDOUT" in rec.get("error", "")
            and rec.get("state") == "open"
            and not rec.get("acknowledged")
        )
        if is_target:
            rec["state"] = "acknowledged"
            rec["acknowledged"] = True
            rec["acknowledged_at"] = now
            rec["ack_reason"] = (
                "environmental MSYS git spawnSync timeout; root cause fixed "
                "via sync.ts git() retry patch (v0.42.57.1)"
            )
            changed += 1
        out.append(json.dumps(rec, ensure_ascii=False))

    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    open_now = [json.loads(l) for l in out if json.loads(l).get("state") == "open"]
    print(f"acknowledged={changed}  remaining_open={len(open_now)}")
    for r in open_now:
        print("  STILL OPEN:", r.get("source_id"), r.get("path"), r.get("code"))


if __name__ == "__main__":
    main()
