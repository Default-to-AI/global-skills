# Duplicate Resolution Log

## 2026-06-15: superpowers-* Prefix Cleanup

### Background
`shared-skills/software-development/` contained 13 directories with `superpowers-` prefix where frontmatter `name:` had no prefix:

| Directory | Frontmatter `name:` |
|-----------|---------------------|
| superpowers-brainstorming | brainstorming |
| superpowers-dispatching-parallel-agents | dispatching-parallel-agents |
| superpowers-executing-plans | executing-plans |
| superpowers-finishing-a-development-branch | finishing-a-development-branch |
| superpowers-receiving-code-review | receiving-code-review |
| superpowers-requesting-code-review | requesting-code-review |
| superpowers-subagent-driven-development | subagent-driven-development |
| superpowers-systematic-debugging | systematic-debugging |
| superpowers-test-driven-development | test-driven-development |
| superpowers-using-git-worktrees | using-git-worktrees |
| superpowers-using-superpowers | using-superpowers |
| superpowers-verification-before-completion | verification-before-completion |
| superpowers-writing-plans | writing-plans |
| superpowers-writing-skills | writing-skills |

### Duplicates Found (same frontmatter name, two directories)

| Frontmatter Name | Directories |
|------------------|-------------|
| requesting-code-review | requesting-code-review, superpowers-requesting-code-review |
| systematic-debugging | systematic-debugging, superpowers-systematic-debugging |
| test-driven-development | test-driven-development, superpowers-test-driven-development |

### Resolution
1. Renamed 10 non-duplicate prefixed directories to match frontmatter name (removed `superpowers-`)
2. Deleted 3 duplicate prefixed directories (kept non-prefixed versions which had richer frontmatter with version, author, metadata)
3. Updated frontmatter of `subagent-driven-development` and `writing-plans` to match local profile versions (added version, author, metadata, related_skills)

### Commands Run
```bash
cd /c/Users/Tiger/AppData/Local/hermes/shared-skills/software-development
for dir in superpowers-*; do
  new="${dir#superpowers-}"
  [ "$dir" != "$new" ] && [ ! -d "$new" ] && mv "$dir" "$new"
done
rm -rf superpowers-requesting-code-review superpowers-systematic-debugging superpowers-test-driven-development
```

### Result
- 125 -> 122 unique frontmatter names in shared-skills
- 0 name mismatches between shared and local profiles
- 0 duplicate frontmatter names