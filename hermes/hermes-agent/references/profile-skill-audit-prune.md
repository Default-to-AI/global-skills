# Profile skill audit/prune notes

## Durable findings

- `default` skill root: `~/.hermes/skills`
- Named profile skill root: `~/.hermes/profiles/<name>/skills`
- Comparing profile skill counts alone is insufficient; always compute extras and missing sets.
- In the audited case, named profiles had many extras absent from `default`; pruning those extras succeeded cleanly after creating a timestamped backup.
- After pruning, named profiles had `extra_vs_default = []` but still lacked several `default`-only operator/meta skills. This means **subset**, not equality.

## Recommended closeout language

- "Removed all named-profile skills absent from `default`."
- "Every named profile now has `extra_vs_default: []`."
- "Named profiles are now a strict subset of `default`, not identical copies, because they still lack `default`-only skills."

## Recovery pattern

Before deletion, create a timestamped archive under `~/.hermes/backups/`, for example:

`~/.hermes/backups/named-profile-skills-<timestamp>.tgz`

Report that path in closeout as the recovery handle.