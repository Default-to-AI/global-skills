# Same-target auto-delivery in scheduled research crons

## Durable lesson

In some Hermes scheduled runtimes, the cron system itself auto-delivers the assistant's **final response** to the configured destination. If the agent then tries to send the same content to the **same target** with `hermes send` or `send_message`, Hermes can suppress it with a message equivalent to:

`Skipped send_message to <target>. This cron job will already auto-deliver its final response to that same target.`

This is not a delivery failure. It is a duplicate-delivery guard.

## What to do

1. Keep the saved artifact files as the durable source of truth.
2. Put the intended user-facing report directly in the final assistant response.
3. Do not retry the same-target explicit send after the suppression notice.
4. If the workflow genuinely needs extra notifications, route those to a different target or use a platform-specific explicit-notification path that does not collide with the cron's final delivery target.

## Why this matters for research crons

Research jobs often produce both:
- a saved raw artifact
- a saved synthesis artifact
- a final chat delivery

The pitfall is treating the explicit send step as mandatory even when the runtime already guarantees the final chat delivery. That creates false debugging churn around a system that is behaving correctly.

## Verification

Positive verification is:
- saved files exist at the expected artifact paths
- the runtime states that same-target explicit send was skipped because final response auto-delivery will occur
- the final response contains the actual report intended for the destination

Absence of an explicit `hermes send` success line is not a failure in this mode.
