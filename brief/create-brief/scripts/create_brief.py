#!/usr/bin/env python3
"""
Create Brief — creates a brief document that is both machine-parseable (YAML frontmatter) 
and human-readable. Writes to canonical briefs directory. Integrates with load-brief.
"""
import os
import sys
import json
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

# Canonical directories
BRIEFS_DIR = Path(r"C:/Users/Tiger/AppData/Local/hermes/briefs")
# Statistics project root - hardcoded since this skill is for that project
PROJECT_ROOT = Path(r"C:/Users/Tiger/Agents/Projects/statistics")

def run_cmd(cmd, cwd=None, capture=True):
    """Run command, return (success, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd or PROJECT_ROOT,
                               capture_output=capture, text=True, timeout=60)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except Exception as e:
        return False, "", str(e)

def get_git_info():
    """Collect git metadata."""
    info = {}
    ok, out, _ = run_cmd("git branch --show-current")
    info["branch"] = out if ok else "unknown"
    ok, out, _ = run_cmd("git log -1 --format='%h %s'")
    info["last_commit"] = out if ok else "unknown"
    ok, out, _ = run_cmd("git status --porcelain")
    info["dirty"] = bool(out.strip()) if ok else True
    ok, out, _ = run_cmd("git rev-parse HEAD")
    info["head"] = out[:8] if ok else "unknown"
    return info

def get_project_name():
    """Read project name from package.json."""
    pkg = PROJECT_ROOT / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            return data.get("name", "unknown")
        except Exception:
            pass
    return PROJECT_ROOT.name

def verify_critical():
    """Run critical verification commands. Returns (all_passed, details_dict)."""
    checks = {}
    
    # Build
    ok, out, err = run_cmd("npm run build")
    checks["build"] = {"passed": ok, "output": out[-200:] if out else err}
    
    # Lint colors
    ok, out, err = run_cmd("npm run lint:colors")
    checks["lint_colors"] = {"passed": ok, "output": out[-200:] if out else err}
    
    # Git clean
    ok, out, _ = run_cmd("git status --porcelain")
    checks["git_clean"] = {"passed": not out.strip(), "output": out[:200] if out else "clean"}
    
    # Key invariants: check for hardcoded sizes, slate/gray/zinc
    ok, out, _ = run_cmd(r"grep -r 'text-\[\\(10\\|11\\|12\\|13\\|15\\)px\\]' src/ --include='*.tsx' 2>/dev/null | head -5")
    checks["no_hardcoded_sizes"] = {"passed": not out.strip(), "output": out[:200] if out else "none found"}
    
    ok, out, _ = run_cmd(r"grep -r 'slate-\\|zinc-\\|gray-' src/ --include='*.tsx' 2>/dev/null | grep -v 'var(--' | head -5")
    checks["no_raw_tailwind_colors"] = {"passed": not out.strip(), "output": out[:200] if out else "none found"}
    
    # Signature elements exist in index.css
    css = (PROJECT_ROOT / "src/index.css").read_text(encoding="utf-8") if (PROJECT_ROOT / "src/index.css").exists() else ""
    checks["signature_elements"] = {
        "passed": all(x in css for x in [".accent-bar", ".curve-glow", ".stagger-in", ".pulse-brass"]),
        "output": "all present" if all(x in css for x in [".accent-bar", ".curve-glow", ".stagger-in", ".pulse-brass"]) else "missing"
    }
    
    all_passed = all(c["passed"] for c in checks.values())
    return all_passed, checks

def read_artifact_summary(path, max_lines=30):
    """Read first N lines of an artifact for summary."""
    p = PROJECT_ROOT / path
    if not p.exists():
        return f"[MISSING: {path}]"
    try:
        lines = p.read_text(encoding="utf-8").splitlines()[:max_lines]
        return "\n".join(lines)
    except Exception:
        return f"[ERROR reading {path}]"

def check_context_engineering_files():
    """Check for Context Engineering mandatory files (L1 Rules, L3 Specs).
    Returns dict with file status - never fails, just reports presence/absence."""
    ce_files = {
        "L1 Rules": [
            "AGENTS.md",
            "STANDARDS.md", 
            "vault-guide.md",
            "CONSTITUTION.md"
        ],
        "L3 Specs": [
            "STRATEGY.md",
            "CONTEXT.md",
            "DESIGN.md"
        ]
    }
    result = {}
    for category, files in ce_files.items():
        result[category] = {}
        for f in files:
            p = PROJECT_ROOT / f
            result[category][f] = {
                "exists": p.exists(),
                "size": p.stat().st_size if p.exists() else 0
            }
    return result

def generate_brief(phase_from, phase_to, session_id, profile="default"):
    """Generate the complete brief document."""
    git_info = get_git_info()
    project = get_project_name()
    all_passed, checks = verify_critical()
    
    # Read key artifacts
    design_summary = read_artifact_summary("DESIGN.md", 50)
    audit_summary = read_artifact_summary("design-system-audit.md", 30)
    ux_summary = read_artifact_summary("ux-evaluation.md", 30)
    
    # Check Context Engineering mandatory files (graceful - never fails)
    ce_files_status = check_context_engineering_files()
    
    timestamp = datetime.now().isoformat()
    ts_filename = datetime.now().strftime("%Y%m%d-%H%M")
    
    # Frontmatter
    frontmatter = {
        "session_id": session_id,
        "created": timestamp,
        "phase_from": phase_from,
        "phase_to": phase_to,
        "profile": profile,
        "project": project,
        "branch": git_info["branch"],
        "base_commit": git_info["head"],
        "last_commit": git_info["last_commit"],
        "git_dirty": git_info["dirty"],
        "verification_passed": all_passed,
        "schema_version": "1.0"
    }
    
    # Build human sections
    sections = []
    
    # 1. Project Context
    sections.append("## Project Context")
    sections.append(f"**Repository:** `{PROJECT_ROOT}`")
    sections.append(f"**Branch:** `{git_info['branch']}` (PR open)")
    sections.append(f"**Base Commit:** `{git_info['head']}` — {git_info['last_commit']}")
    sections.append("")
    sections.append("### Three-Layer Method Alignment")
    sections.append("")
    sections.append("| Layer | Status | Artifacts |")
    sections.append("|-------|--------|-----------|")
    sections.append("| **Spec** | ✅ Complete | `DESIGN.md`, `tokens.json`, `tailwind.theme.json` |")
    sections.append("| **Verifier** | ✅ Complete | `design-system-audit.md`, `ux-evaluation.md` |")
    sections.append("| **Environment** | 🔄 P0 done → P1 next | Components refactored, `src/index.css` signature elements added |")
    sections.append("")
    
    # 2. What Was Done
    sections.append("## What Was Done (P0 Remediation)")
    sections.append("")
    sections.append("### Commits on Branch")
    sections.append("1. `docs: add design system audit and UX evaluation reports` — Verifier layer established")
    sections.append("2. `feat: implement DESIGN.md signature elements + motion tokens` — `.accent-bar`, `.curve-glow`, `.stagger-in`, `.pulse-brass` + motion tokens")
    sections.append("3. `fix: P0 design system remediation` — 80+ hardcoded `text-[Npx]` → semantic tokens; 2× `slate-800` removed")
    sections.append("")
    sections.append("### Verification Results")
    for name, check in checks.items():
        status = "✅" if check["passed"] else "❌"
        sections.append(f"- {status} **{name}**: {check['output'][:100]}")
    sections.append("")
    sections.append("### Key Files Modified")
    sections.append("- `src/index.css` — signature elements + motion tokens + `prefers-reduced-motion`")
    sections.append("- `src/NormalDistributionCalculator.tsx` — 18 hardcoded sizes → semantic tokens")
    sections.append("- `src/components/HypothesisTestingCalculator.tsx` — 30 hardcoded sizes → semantic tokens")
    sections.append("- `src/components/FormulaSheet.tsx` — 35 hardcoded sizes → semantic tokens")
    sections.append("- `src/components/StatisticalHelperModal.tsx` — 12 hardcoded sizes → semantic tokens")
    sections.append("")
    
    # 3. Current State
    sections.append("## Current State: Ready for P1")
    sections.append("")
    sections.append("### P1 Objective")
    sections.append("Build **11 missing primitive components** per `DESIGN.md §Component Usage Map`:")
    sections.append("")
    sections.append("| Missing Primitive | DESIGN.md Spec | Priority |")
    sections.append("|-------------------|----------------|----------|")
    sections.append("| `Button` | 5 variants (primary, secondary, ghost, danger, success) | P1 |")
    sections.append("| `Badge` | 5 semantic variants (brass, teal, crimson, cobalt, neutral) | P1 |")
    sections.append("| `Input` / `Select` / `Label` | 6 form variants | P1 |")
    sections.append("| `Table` | Decision matrices, power tables | P1 |")
    sections.append("| `Tooltip` | Input help, chart hover | P1 |")
    sections.append("| `Accordion` | FormulaSheet chapters, power calc | P1 |")
    sections.append("| `FormulaBlock` | 2 variants (formula-block, calc-block) | P1 |")
    sections.append("| `Modal` | StatisticalHelperModal, confirmations | P1 |")
    sections.append("| `Heading` | Page/section/subsection/label scales | P1 |")
    sections.append("")
    sections.append("### Existing Primitives (in `src/components/ui/`)")
    sections.append("- `Card` / `CardHeader` / `CardBody` — panel-default/elevated")
    sections.append("- `PageLayout` — max-w-[1800px], RTL support")
    sections.append("- `CustomComponents.tsx` — InputGroup, ChartWrapper, CalculatorSidebar, StepList, ModeTabs, EmptyState, InputTooltip, Disclosure")
    sections.append("")
    
    # 4. Blocking Decisions
    sections.append("## Blocking Decisions (Need User Input)")
    sections.append("")
    sections.append("| Decision | Context | Blocking |")
    sections.append("|----------|---------|----------|")
    sections.append("| **P-value integration mode** | Toggle (A) vs Unified (B) — from `.superpowers/brainstorm/session-1/content/layout.html` | Yes — blocks Hypothesis Testing UX rebuild (P2) |")
    sections.append("| **Deployment target** | Vercel / Netlify / GitHub Pages / local-only | No |")
    sections.append("| **Language scope** | Hebrew only vs i18n-ready (English/Arabic) | No |")
    sections.append("")
    
    # 5. Risks
    sections.append("## Risks")
    sections.append("")
    sections.append("| Risk | Impact | Likelihood | Mitigation |")
    sections.append("|------|--------|------------|------------|")
    sections.append("| P1 scope creep | High | Medium | Strict adherence to DESIGN.md Component Usage Map |")
    sections.append("| 252KB HypothesisTestingCalculator refactor math regressions | High | Medium | Snapshot tests before refactor; verify math utils unchanged |")
    sections.append("| RTL Hebrew layout breaks in new primitives | Medium | High | Test each primitive in RTL; use InputGroup pattern (dir prop) |")
    sections.append("")
    
    # 6. Verification Checklist
    sections.append("## Verification Checklist (Next Agent MUST Run)")
    sections.append("")
    for name, check in checks.items():
        status = "✅" if check["passed"] else "❌"
        sections.append(f"- [ ] {status} **{name}** — {check['output'][:80]}")
    sections.append("")
    
    # 7. Quick Start
    sections.append("## Quick Start for Next Agent")
    sections.append("")
    sections.append("```bash")
    sections.append(f"cd {PROJECT_ROOT}")
    sections.append(f"git checkout {git_info['branch']}")
    sections.append("# Verify build")
    sections.append("npm run build")
    sections.append("npm run lint:colors")
    sections.append("# Load this brief")
    sections.append("python C:/Users/Tiger/AppData/Local/hermes/skills/devops/load-brief/scripts/load_brief.py")
    sections.append("# Start P1: Build Button + Badge first (highest reuse)")
    sections.append("```")
    sections.append("")
    
    # 8. Context Engineering Files Status (graceful - no failures)
    sections.append("## Context Engineering Files Status")
    sections.append("")
    sections.append("*Reports presence/absence of L1 Rules and L3 Specs per context-engineering hierarchy. Missing files are noted gracefully — not required for all projects.*")
    sections.append("")
    for category, files in ce_files_status.items():
        sections.append(f"### {category}")
        sections.append("")
        sections.append("| File | Status | Size |")
        sections.append("|------|--------|------|")
        for fname, info in files.items():
            status = "✅ Present" if info["exists"] else "⚠️ Not found (graceful)"
            size = f"{info['size']} bytes" if info["exists"] else "—"
            sections.append(f"| `{fname}` | {status} | {size} |")
        sections.append("")
    
    sections.append("## Reference Artifacts (Do Not Duplicate)")
    sections.append("")
    sections.append("| Artifact | Path |")
    sections.append("|----------|------|")
    sections.append("| DESIGN.md (Spec) | `C:/Users/Tiger/Agents/Projects/statistics/DESIGN.md` |")
    sections.append("| Design System Audit | `C:/Users/Tiger/Agents/Projects/statistics/design-system-audit.md` |")
    sections.append("| UX Evaluation (Jobs Review) | `C:/Users/Tiger/Agents/Projects/statistics/ux-evaluation.md` |")
    sections.append("| PR #6 | https://github.com/Default-to-AI/statistics/pull/6 |")
    sections.append("| Component Usage Map | DESIGN.md lines 692-717 |")
    sections.append("")
    
    # 9. Suggested Skills for Next Session
    sections.append("## Suggested Skills for Next Session")
    sections.append("")
    sections.append("| Skill | Reason |")
    sections.append("|-------|--------|")
    sections.append("| `create-brief` | Build primitives per DESIGN.md spec — token discipline, RTL, accessibility |")
    sections.append("| `cb-work` | Execute brief builds in worktrees with CI gates |")
    sections.append("| `cb-code-review` | 12-persona review on brief components |")
    sections.append("| `load-brief` | Load this brief at session start (devops/load-brief) |")
    sections.append("")
    
    body = "\n".join(sections)
    
    # Create YAML frontmatter
    import json
    yaml_lines = []
    for k, v in frontmatter.items():
        if isinstance(v, (dict, list, bool)):
            yaml_lines.append(f"{k}: {json.dumps(v)}")
        else:
            yaml_lines.append(f"{k}: {v}")
    yaml_fm = "\n".join(yaml_lines)
    
    doc = f"---\n{yaml_fm}\n---\n\n# Brief: {phase_from} → {phase_to}\n\n{body}"
    
    return doc, frontmatter, checks

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Create brief document")
    parser.add_argument("--phase-from", required=True, help="Source phase (e.g., p0-remediation)")
    parser.add_argument("--phase-to", required=True, help="Target phase (e.g., p1-primitives)")
    parser.add_argument("--session-id", required=True, help="Session identifier")
    parser.add_argument("--profile", default="default", help="Profile name")
    args = parser.parse_args()
    
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    
    doc, frontmatter, checks = generate_brief(
        args.phase_from, args.phase_to, args.session_id, args.profile
    )
    
    all_passed = all(c["passed"] for c in checks.values())
    
    # Filename: brief-{profile}-{project}-{phase_from}-to-{phase_to}-{timestamp}.md
    project = get_project_name()
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"brief-{args.profile}-{project}-{args.phase_from}-to-{args.phase_to}-{ts}.md"
    filepath = BRIEFS_DIR / filename
    
    filepath.write_text(doc, encoding="utf-8")
    
    # Output verification message (for Telegram/human)
    print(f"✅ Brief created: {filepath}")
    print(f"📋 Session: {args.session_id} | Phase: {args.phase_from} → {args.phase_to}")
    print(f"🔍 Verification: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    for name, check in checks.items():
        status = "✅" if check["passed"] else "❌"
        print(f"   {status} {name}")
    print(f"🎯 Recommended follow-up: Option A — Build Button + Badge primitives")
    print(f"📂 Run to load: python C:/Users/Tiger/AppData/Local/hermes/skills/devops/load-brief/scripts/load_brief.py")

if __name__ == "__main__":
    main()