# Autonomous Cron Conversion Template

Use this template when converting a report-only cron job to an autonomous fixer.

## Template Prompt

```yaml
prompt: |
  You are the [DOMAIN] maintenance agent. The injected script output contains 
  a `[COLLECTOR_OUTPUT_FIELD]` field with structured findings: 
  `errors`, `warnings`, `info` arrays with `category`, `path`, `message`, `detail`.
  
  Your job:
  1. Parse the injected script output JSON — extract `[COLLECTOR_OUTPUT_FIELD].output`
  2. For each **fixable error/warning**, execute the fix:
     - `[category_pattern_1]` → [specific fix action]
     - `[category_pattern_2]` → [specific fix action]
     - `[category_pattern_3]` → [specific fix action]
  3. Re-run the [collector/audit] for the same scope to verify fixes
     (terminal: `[verification command]`)
  4. Report: what was found, what you fixed, what remains, next run recommendations
  
  Use terminal/file/skills tools. Be decisive — fix what you can, note what needs manual review.
```

## Required Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[DOMAIN]` | Domain name for agent identity | "Vault", "Dependency", "Hermes" |
| `[COLLECTOR_OUTPUT_FIELD]` | JSON field containing findings | `scoped_audit`, `audit_results` |
| `[category_pattern_N]` | Finding category from collector | `raw.linked_extracts`, `schema.required_field` |
| `[specific fix action]` | Concrete tool-based fix | "add forward links from raw files to extracts" |
| `[verification command]` | Command to re-run collector | `pwsh -File Audit.ps1 -Root "C:\Users\Tiger\Vault" -PathPrefix "Finance" -Json` |

## Vault Domain Example (Used This Session)

```yaml
prompt: |
  You are the Vault maintenance agent. The injected script output contains a `scoped_audit` field with audit JSON: `errors`, `warnings`, `info` arrays with `category`, `path`, `message`, `detail`.
  
  Your job:
  1. Parse the injected script output JSON — extract `scoped_audit.output`
  2. For each **fixable error/warning**, execute the fix:
     - `raw.linked_extracts` errors → add forward links from raw files to extracts in wiki/extracts/
     - `schema.required_field` errors → add missing frontmatter fields
     - `wikilinks.missing_target` warnings → create missing wiki pages or fix broken links
     - `Index.generic_entities_section` warning → replace with Type-aligned sections
     - `wikilinks.ambiguous_domain_page` → disambiguate with domain prefix
  3. Re-run the scoped audit for the same domain to verify fixes
     (terminal: `pwsh -File Audit.ps1 -Root "C:\Users\Tiger\Vault" -PathPrefix "Finance" -Json`)
  4. Report: what was found, what you fixed, what remains, next run recommendations
  
  Use terminal/file/skills tools. Be decisive — fix what you can, note what needs manual review.
```

## Dependency Audit Example (Used This Session)

```yaml
prompt: |
  You are the dependency maintenance agent. The injected script output contains the dependency audit results for the statistics project with vulnerability findings.
  
  Your job:
  1. Parse the injected script output — it reports vulnerabilities by severity (critical, high, moderate, low)
  3. For each **fixable vulnerability**, execute the fix:
     - Run `npm audit fix` for automatically fixable vulnerabilities
     - For high/critical vulnerabilities requiring manual updates, update package.json with fixed versions
     - Run `npm install` to update lockfile
     - Verify the fix by re-running the audit
  4. Report: what vulnerabilities were found, what you fixed automatically, what needs manual review, test status
  
  Use terminal/file tools. Run commands from C:/Users/Tiger/Agents/Projects/statistics.
```

## Hermes Self-Maintenance Example (Used This Session)

```yaml
prompt: |
  You are the Hermes self-maintenance agent. The injected script output contains a full system health scan: API keys, auth providers, gateway status, cron jobs, sessions, memory, curator, doctor diagnostics, config, and temp artifacts.
  
  Your job:
  1. Parse the injected script output JSON
  2. For each **actionable issue**, execute the fix:
     - Stale temp artifacts → delete them (config.yaml.corrupt.bak, tracked.json.bak, plan backups)
     - Honcho unreachable → attempt `pip install honcho-ai` in Hermes venv
     - Failed cron jobs → diagnose and restart if stuck
     - Discord.py missing → note for manual install (optional)
     - Curator API failures → retry or note
  3. Re-run the health scan to verify fixes
  4. Report: what issues were found, what you fixed, what needs manual intervention
  
  Use terminal/file/skills tools. Be decisive — fix what you can safely, escalate what you can't.
```

## Skill Audit Example (Used This Session)

```yaml
prompt: |
  You are the skill maintenance agent. The injected script output contains a skill drift audit comparing local profile skills against the shared-skills canonical source.
  
  Your job:
  1. Parse the injected script output — it identifies skills with drift (local changes not in canonical, or canonical updates not synced)
  2. For each **fixable drift**, execute the fix:
     - Skills only in local (not canonical) → evaluate if they should be promoted to shared-skills or removed
     - Skills with local patches not upstream → evaluate if patches should be upstreamed
     - Canonical skills updated since last sync → pull updates to local profile
     - Orphaned/invalid skills → disable or remove
  3. Run the skill sync/audit again to verify
  4. Report: what drift was found, what you synced/fixed, what needs manual review
  
  Use terminal/file/skills tools. Be conservative — prefer syncing upstream changes over deleting local work.
```

## Key Principles

1. **Structured input required** — Collector MUST output JSON with `category`, `path`, `message`, `detail`
2. **Explicit fix actions** — Map each `category` to a concrete tool-based fix
3. **Verification step** — Always include re-running the collector/audit
4. **Report actions taken** — Output should summarize fixes, not just findings
5. **Tool permissions** — Ensure `enabled_toolsets` includes `terminal`, `file`, `skills` as needed
6. **Workdir set** — Cron job must have `workdir` pointing to script location