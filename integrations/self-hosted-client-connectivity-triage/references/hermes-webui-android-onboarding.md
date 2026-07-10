# Hermes WebUI Android onboarding vs browser reachability

## Pattern
A user could reach Hermes WebUI over Tailscale after binding to `0.0.0.0`, but the Android app still timed out during first-run connect.

## Useful separation
- Remote `GET /health` succeeded.
- Remote `GET /login` returned the Hermes sign-in page.
- Remote `GET /api/status` returned `401` rather than timing out or refusing the connection.
- Therefore the network path and WebUI bind were already good.
- Remaining issue space narrowed to Android client onboarding/readiness behavior and auth handshake expectations.

## Log pattern worth recognizing
If access logs show the remote phone/Tailscale IP hitting all three of these:
- `GET /health` → `200`
- `GET /api/status` → `401`
- `GET /login` → `200`

then stop treating the problem as "server did not start". The phone is reaching the app; the remaining problem is the client's auth/protocol path.

## Durable lesson
When a self-hosted UI is reachable by browser but not by native client:
1. confirm remote health endpoint
2. confirm remote login/root page renders
3. inspect client release/version skew
4. treat app onboarding logic as a separate compatibility surface

## Hermes-specific note
For Hermes WebUI, phone-browser access to the login page can prove Tailscale/browser usability even when the Android client build is lagging current releases.

## Cleanup lesson
If you explore speculative compatibility patches in the server repo but do not verify them as the real fix, revert them before closeout and report the true blocker plainly.
