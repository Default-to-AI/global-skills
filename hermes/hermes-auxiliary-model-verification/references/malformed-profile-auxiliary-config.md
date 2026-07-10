# Malformed profile-local `auxiliary:` config

Use this note when one Hermes profile behaves differently from the global default after manual config edits.

## Failure pattern

A top-level YAML key is accidentally concatenated onto the previous scalar, e.g.

```yaml
trace: disabledauxiliary:
```

instead of

```yaml
trace: disabled
auxiliary:
```

This usually happens at the boundary between the preceding section and `auxiliary:`.

## Symptoms

- One profile alone ignores expected `auxiliary.*` overrides.
- Global config looks correct, but profile-local behavior is inconsistent.
- A smoke test passes in one profile and fails or silently inherits defaults in another.
- The user reports that they "set up all profiles" but only one profile behaves wrong.

## Repair pattern

1. Inspect the profile-local `config.yaml`, not just `~/.hermes/config.yaml`.
2. Check the line immediately before `auxiliary:` for missing newline or indentation damage.
3. Repair the YAML boundary.
4. Prove the profile parses with a profile-scoped command.
5. Rerun the auxiliary smoke test inside that same profile.

## Success criteria

- Profile-level command returns normally.
- The target route answers through the real task path in that profile.
- Report both the config repair and the positive smoke-test result.
