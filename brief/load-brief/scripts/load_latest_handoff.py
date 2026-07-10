#!/usr/bin/env python3
"""
Load Latest Handoff — consume most recent handoff file from canonical directory.
"""
import os
import sys
import glob
from pathlib import Path
from datetime import datetime

HANDOFFS_DIR = Path(r"C:/Users/Tiger/AppData/Local/hermes/handoffs")

def find_latest_handoff():
    """Return Path to most recent .md file in handoffs dir, or None."""
    files = list(HANDOFFS_DIR.glob("handoff-*.md"))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def parse_handoff(filepath):
    """Extract frontmatter and body. Returns (frontmatter_dict, body_str)."""
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    import yaml
    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return frontmatter, body

def main():
    latest = find_latest_handoff()
    if not latest:
        print("No handoff files found in canonical directory.")
        sys.exit(0)

    # Get creation time from filename timestamp or file mtime
    mtime = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    frontmatter, body = parse_handoff(latest)
    
    # Display to user (injected into session)
    print(f"## Handoff Loaded: {latest.name}")
    print(f"**File:** `{latest}`")
    print(f"**Created:** {mtime}")
    if frontmatter.get("session_id"):
        print(f"**Session ID:** {frontmatter['session_id']}")
    if frontmatter.get("trigger"):
        print(f"**Trigger:** {frontmatter['trigger']}")
    if frontmatter.get("phase_from") and frontmatter.get("phase_to"):
        print(f"**Phase:** {frontmatter['phase_from']} → {frontmatter['phase_to']}")
    print()
    print("---")
    print(body)
    print("---")
    
    # Delete after successful display
    latest.unlink()
    
    # Verification message
    print(f"✅ **Loaded and deleted:** `{latest}` (created {mtime}) — internalized, no longer on disk.")

if __name__ == "__main__":
    main()