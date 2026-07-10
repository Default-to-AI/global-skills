#!/usr/bin/env python3
"""
Verify skill synchronization across all Hermes profiles.

Run after configuring shared-skills to confirm all profiles
see identical skill sets from the canonical source.

Usage:
    python verify-skill-sync.py
    python verify-skill-sync.py --hermes-root /custom/path
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set


def run_hermes_skills_list(profile: str, hermes_root: Path) -> List[str]:
    """Run `hermes skills list --profile <name>` and return skill names."""
    env = dict(**__import__("os").environ)
    env["HERMES_HOME"] = str(hermes_root / "profiles" / profile)
    try:
        result = subprocess.run(
            ["hermes", "skills", "list", "--profile", profile],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        if result.returncode != 0:
            return [f"ERROR: {result.stderr.strip()}"]
        # Parse output — skill list format varies, extract skill names
        lines = result.stdout.strip().split("\n")
        skills = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith("=") and not line.startswith("total"):
                # Format: "skill-name  description"
                parts = line.split(None, 1)
                if parts:
                    skills.append(parts[0])
        return skills
    except Exception as e:
        return [f"EXCEPTION: {e}"]


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Verify Hermes skill sync across profiles")
    parser.add_argument(
        "--hermes-root",
        default="/c/Users/Tiger/AppData/Local/hermes",
        help="Hermes root directory (default: %(default)s)",
    )
    parser.add_argument(
        "--profiles",
        nargs="+",
        default=["vault", "engineer", "reviewer", "strategist", "writer"],
        help="Profiles to check (default: all known)",
    )
    parser.add_argument(
        "--canonical",
        default="/c/Users/Tiger/AppData/Local/hermes/shared-skills",
        help="Canonical shared skills directory",
    )
    args = parser.parse_args()

    hermes_root = Path(args.hermes_root)
    profiles = args.profiles
    canonical = Path(args.canonical)

    print(f"Hermes root: {hermes_root}")
    print(f"Canonical skills: {canonical}")
    print(f"Profiles: {profiles}")
    print()

    # Get canonical skill names from filesystem
    canonical_skills: Set[str] = set()
    if canonical.exists():
        for skill_dir in canonical.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    canonical_skills.add(skill_dir.name)
    print(f"Canonical skills ({len(canonical_skills)}): {sorted(canonical_skills)}")
    print()

    # Check each profile
    profile_skills: Dict[str, Set[str]] = {}
    for profile in profiles:
        skills = run_hermes_skills_list(profile, hermes_root)
        skill_set = set(s for s in skills if not s.startswith("ERROR") and not s.startswith("EXCEPTION"))
        profile_skills[profile] = skill_set
        status = "OK" if skill_set == canonical_skills else "MISMATCH"
        print(f"  {profile:12} : {len(skill_set):3} skills — {status}")
        if skill_set != canonical_skills:
            missing = canonical_skills - skill_set
            extra = skill_set - canonical_skills
            if missing:
                print(f"    MISSING: {sorted(missing)}")
            if extra:
                print(f"    EXTRA  : {sorted(extra)}")

    print()

    # Summary
    all_match = all(s == canonical_skills for s in profile_skills.values())
    if all_match:
        print("✅ ALL PROFILES SYNCED — skill sets match canonical source")
        sys.exit(0)
    else:
        print("❌ SYNC FAILURE — at least one profile diverges")
        sys.exit(1)


if __name__ == "__main__":
    main()