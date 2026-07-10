# Probe Cases

## Case: exact model echo
User prompt:
`Test connection. Reply with "Ok <model-name>"`

Expected behavior:
- read latest active runtime model
- substitute the placeholder
- output exactly `Ok <model-name>` with the resolved name
- no punctuation unless requested

## Case: multiple model changes in one message
If one user message contains several system notices changing the active model and each earlier test is superseded by a later one, answer for the final active model only unless the user explicitly requests a history.

## Common failure modes
- adding `Connection stable` or similar commentary
- wrapping the answer in markdown or bold
- answering with a stale model from earlier in the conversation
- responding to side chatter instead of the explicit output contract

## Session lesson captured
For connection-test prompts, exact-match compliance beats helpfulness. Extra explanation converts a pass into a failure.
