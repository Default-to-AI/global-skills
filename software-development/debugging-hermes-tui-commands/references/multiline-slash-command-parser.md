# Multiline Slash Command Parser Reproduction

## Symptom

Hermes desktop can show `empty slash command` when a valid slash command is pasted with embedded newlines, e.g. a long multiline `/goal` payload.

## Confirmed Behavior

- `/goal short single line` parses normally.
- Multiline input like:
  ```text
  /goal Build the Northstar command center
  and daily morning brief workflow
  ```
  can be treated as an empty slash command by the desktop/frontend flow.

## Investigation Path

Check these files first when debugging this class of issue:

- `web/src/lib/slashExec.ts`
- `apps/desktop/src/lib/chat-runtime.ts`
- `apps/desktop/src/app/session/hooks/use-prompt-actions.ts`
- `cli.py` slash-command handling only after frontend parsing is ruled out

## Practical Operator Guidance

When the issue is user-facing and speed matters more than fixing Hermes immediately:

1. Keep the slash command itself to one short line.
2. Put the detailed specification in the next normal chat message.
3. If needed, use `/goal status` or `/goal clear` as short sanity checks because they avoid multiline paste behavior.

## Lesson

Do not assume a slash command failed because the command is missing from the registry. First separate **registration problems** from **frontend parsing / submit behavior** problems.