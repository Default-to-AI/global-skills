#!/usr/bin/env python3
"""
Skill Audit Collector - Safe Maintenance Cron
Deterministic check for profile skill drift from shared-skills canonical source.
Uses skills_list tool directly for accurate skill names (avoids CLI table truncation).

The collector deliberately separates true drift from expected non-loading skills:
- platform-filtered shared skills are reported under `shared_skills_hidden_by_platform`
- bundled/system local skills are not reported as `extra_skills_in_cli`
- block-style YAML `skills.external_dirs` is detected correctly
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# Import the skills_list tool directly for accurate JSON output
sys.path.insert(0, r"C:\Users\Tiger\AppData\Local\hermes\hermes-agent")
from tools.skills_tool import get_hermes_home, skills_list  # noqa: E402

HERMES_ROOT = Path(r"C:/Users/Tiger/AppData/Local/hermes")
PROFILE_CANDIDATES = ["vault", "librarian", "engineer", "strategist", "reviewer", "writer"]
CURRENT_PLATFORM = "windows"
DEFAULT_SHARED_SKILLS = HERMES_ROOT / "shared-skills"


def read_frontmatter(skill_md: Path) -> dict[str, Any]:
    """Extract simple YAML frontmatter fields needed for skill drift auditing."""
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not content.startswith("---"):
        return {}
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}
    yaml_content = content[3 : end_match.start() + 3]
    data: dict[str, Any] = {}
    for line in yaml_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("name:"):
            data["name"] = stripped.split(":", 1)[1].strip().strip("'\"")
        elif stripped.startswith("platforms:"):
            raw = stripped.split(":", 1)[1].strip()
            if raw.startswith("[") and raw.endswith("]"):
                data["platforms"] = [item.strip().strip("'\"") for item in raw[1:-1].split(",") if item.strip()]
            elif raw:
                data["platforms"] = [raw.strip().strip("'\"")]
        elif stripped.startswith("environments:"):
            raw = stripped.split(":", 1)[1].strip()
            if raw.startswith("[") and raw.endswith("]"):
                data["environments"] = [item.strip().strip("'\"") for item in raw[1:-1].split(",") if item.strip()]
            elif raw:
                data["environments"] = [raw.strip().strip("'\"")]
    return data


def get_skills_with_fm_names(base_dir: Path, include_dot_categories: bool = False) -> dict[str, dict[str, Any]]:
    """Get skills from a base directory, keyed by frontmatter name.

    Supports nested layouts recursively, including patterns like:
    - category/skill/SKILL.md
    - category/subcategory/skill/SKILL.md
    - skill/SKILL.md for uncategorized shared skills
    """
    skills: dict[str, dict[str, Any]] = {}
    if not base_dir.exists():
        return skills

    for skill_md in base_dir.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        try:
            relative_parts = skill_dir.relative_to(base_dir).parts
        except ValueError:
            continue
        if not relative_parts:
            continue
        if not include_dot_categories and any(part.startswith(".") for part in relative_parts):
            continue
        fm = read_frontmatter(skill_md)
        fm_name = fm.get("name")
        if fm_name:
            skills[fm_name] = {
                "directory_name": skill_dir.name,
                "category": relative_parts[0] if len(relative_parts) > 1 else "",
                "platforms": fm.get("platforms"),
                "environments": fm.get("environments"),
                "path": str(skill_md),
            }
    return skills


def parse_external_dirs(config_path: Path) -> list[str]:
    """Parse skills.external_dirs values from a profile config without full YAML dependency."""
    if not config_path.exists():
        return []

    content = config_path.read_text(encoding="utf-8")
    external_dirs: list[str] = []
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^\s*external_dirs\s*:", line):
            continue
        after = line.split(":", 1)[1].strip()
        if after.startswith("[") and after.endswith("]"):
            external_dirs.extend(item.strip().strip("'\"") for item in after[1:-1].split(",") if item.strip())
        base_indent = len(line) - len(line.lstrip())
        for child in lines[index + 1 :]:
            stripped = child.strip()
            if not stripped:
                continue
            child_indent = len(child) - len(child.lstrip())
            if child_indent < base_indent:
                break
            if child_indent == base_indent and not stripped.startswith("-"):
                break
            if stripped.startswith("-"):
                external_dirs.append(stripped[1:].strip().strip("'\""))
    return external_dirs


def discover_canonical_skill_dirs() -> list[Path]:
    """Discover canonical shared skill sources from live profile configs.

    Falls back to ~/.hermes/shared-skills when present, but prefers configured
    external skill directories because they represent the live source of truth.
    """
    discovered: list[Path] = []
    seen: set[str] = set()

    if DEFAULT_SHARED_SKILLS.exists():
        normalized = str(DEFAULT_SHARED_SKILLS).replace("\\", "/").rstrip("/")
        seen.add(normalized)
        discovered.append(DEFAULT_SHARED_SKILLS)

    for profile in [profile for profile in PROFILE_CANDIDATES if (HERMES_ROOT / "profiles" / profile).exists()]:
        config_path = HERMES_ROOT / "profiles" / profile / "config.yaml"
        for raw_dir in parse_external_dirs(config_path):
            normalized = raw_dir.replace("\\", "/").rstrip("/")
            if normalized in seen:
                continue
            path = Path(raw_dir)
            if path.exists():
                seen.add(normalized)
                discovered.append(path)

    return discovered


def platform_allows(skill_meta: dict[str, Any]) -> bool:
    """Return whether a shared skill should be visible on the current host platform."""
    platforms = skill_meta.get("platforms")
    if not platforms:
        return True
    return CURRENT_PLATFORM in {str(platform).lower() for platform in platforms}


def environment_allows(skill_meta: dict[str, Any]) -> bool:
    """Return whether a shared skill is relevant to the current non-kanban cron context."""
    environments = skill_meta.get("environments")
    if not environments:
        return True
    normalized = {str(env).lower().strip() for env in environments}
    # This maintenance cron is not running as a Kanban worker/orchestrator; hide
    # kanban-only offer-surface skills the same way Hermes does.
    if "kanban" in normalized:
        return bool(os.getenv("HERMES_KANBAN_TASK") or os.getenv("HERMES_KANBAN_BOARD"))
    return True


def get_cli_skills_for_profile(profile: str) -> set[str]:
    """
    Get skills visible via CLI for a profile by using skills_list tool directly.
    This avoids CLI table truncation issues.
    """
    original_hermes_home = os.environ.get("HERMES_HOME")
    profile_home = HERMES_ROOT / "profiles" / profile
    os.environ["HERMES_HOME"] = str(profile_home)

    try:
        import tools.skills_tool as skills_tool

        skills_tool.HERMES_HOME = get_hermes_home()
        skills_tool.SKILLS_DIR = skills_tool.HERMES_HOME / "skills"

        result_json = skills_list()
        data = json.loads(result_json)
        if data.get("success"):
            return {skill["name"] for skill in data.get("skills", [])}
        return set()
    except Exception as exc:
        print(f"Error getting skills for {profile}: {exc}", file=sys.stderr)
        return set()
    finally:
        if original_hermes_home:
            os.environ["HERMES_HOME"] = original_hermes_home
        else:
            os.environ.pop("HERMES_HOME", None)


def check_profile_config(profile: str, canonical_dirs: set[str]) -> dict[str, Any]:
    """Check if profile config contains the shared-skills external dir and disabled skills."""
    config_path = HERMES_ROOT / "profiles" / profile / "config.yaml"
    if not config_path.exists():
        return {
            "has_external_dirs": False,
            "external_dirs": None,
            "has_expected_shared_dir": False,
            "disabled_skills": [],
        }

    content = config_path.read_text(encoding="utf-8")
    external_dirs = parse_external_dirs(config_path)
    disabled_skills: list[str] = []
    lines = content.splitlines()
    for index, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line == "disabled:":
            base_indent = len(line) - len(line.lstrip())
            for child in lines[index + 1 :]:
                stripped = child.strip()
                if not stripped:
                    continue
                child_indent = len(child) - len(child.lstrip())
                if child_indent < base_indent:
                    break
                if child_indent == base_indent and not stripped.startswith("-"):
                    break
                if stripped.startswith("-"):
                    disabled_skills.append(stripped[1:].strip().strip("'\""))
    normalized = {entry.replace("\\", "/").rstrip("/") for entry in external_dirs}
    return {
        "has_external_dirs": bool(external_dirs),
        "external_dirs": external_dirs or None,
        "has_expected_shared_dir": bool(normalized & canonical_dirs),
        "disabled_skills": sorted(set(disabled_skills)),
    }


def main() -> int:
    canonical_skill_dirs = discover_canonical_skill_dirs()
    canonical_skill_dir_set = {str(path).replace("\\", "/").rstrip("/") for path in canonical_skill_dirs}
    shared_skills_map: dict[str, dict[str, Any]] = {}
    for skill_dir in canonical_skill_dirs:
        shared_skills_map.update(get_skills_with_fm_names(skill_dir, include_dot_categories=True))
    shared_fm_names = set(shared_skills_map.keys())
    platform_allowed_shared = {name for name, meta in shared_skills_map.items() if platform_allows(meta)}
    environment_allowed_shared = {name for name, meta in shared_skills_map.items() if environment_allows(meta)}
    offer_allowed_shared = platform_allowed_shared & environment_allowed_shared
    platform_hidden_shared = shared_fm_names - platform_allowed_shared
    environment_hidden_shared = shared_fm_names - environment_allowed_shared

    print(f"Shared skills (by frontmatter name): {len(shared_fm_names)}", file=sys.stderr)

    results: dict[str, Any] = {
        "shared_skills_count": len(shared_fm_names),
        "platform_allowed_shared_skills_count": len(platform_allowed_shared),
        "offer_allowed_shared_skills_count": len(offer_allowed_shared),
        "canonical_skill_dirs": sorted(canonical_skill_dir_set),
        "profiles": {},
    }

    profiles = [profile for profile in PROFILE_CANDIDATES if (HERMES_ROOT / "profiles" / profile).exists()]
    for profile in profiles:
        cli_skills = get_cli_skills_for_profile(profile)
        local_skills_all_map = get_skills_with_fm_names(HERMES_ROOT / "profiles" / profile / "skills", include_dot_categories=True)
        local_skills_non_system_map = get_skills_with_fm_names(HERMES_ROOT / "profiles" / profile / "skills", include_dot_categories=False)
        local_all_fm_names = set(local_skills_all_map.keys())
        local_non_system_fm_names = set(local_skills_non_system_map.keys())
        config = check_profile_config(profile, canonical_skill_dir_set)

        disabled_skills = set(config.get("disabled_skills", []))
        expected_visible_shared = offer_allowed_shared - disabled_skills
        missing_from_cli = expected_visible_shared - cli_skills
        hidden_by_platform = sorted(platform_hidden_shared - cli_skills)
        hidden_by_environment = sorted(environment_hidden_shared - cli_skills)
        disabled_shared = sorted((shared_fm_names & disabled_skills) - cli_skills)
        extra_in_cli = cli_skills - shared_fm_names - local_all_fm_names
        local_overrides = local_non_system_fm_names - shared_fm_names

        name_mismatches = []
        for fm_name in shared_fm_names & local_non_system_fm_names:
            shared_dir = shared_skills_map[fm_name]["directory_name"]
            local_dir = local_skills_non_system_map[fm_name]["directory_name"]
            if shared_dir != local_dir:
                name_mismatches.append(
                    {
                        "frontmatter_name": fm_name,
                        "shared_dir": shared_dir,
                        "local_dir": local_dir,
                    }
                )

        results["profiles"][profile] = {
            "cli_skills_count": len(cli_skills),
            "local_skills_count": len(local_non_system_fm_names),
            "local_system_skills_count": len(local_all_fm_names - local_non_system_fm_names),
            "shared_skills_missing_from_cli": sorted(missing_from_cli)[:25],
            "shared_skills_hidden_by_platform": hidden_by_platform[:25],
            "shared_skills_hidden_by_environment": hidden_by_environment[:25],
            "shared_skills_disabled_in_profile": disabled_shared[:25],
            "extra_skills_in_cli": sorted(extra_in_cli)[:25],
            "local_overrides": sorted(local_overrides),
            "name_mismatches": name_mismatches,
            "config_external_dirs": config,
        }

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
