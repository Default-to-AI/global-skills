# Windows verification flow for Browser Use + browser-harness

## Durable install path

Use a stable checkout such as:

```text
C:/Users/<user>/Developer/browser-harness
```

## Config verification

1. Add `BROWSER_USE_API_KEY` to the active Hermes profile `.env`.
2. Set `browser.cloud_provider: browser-use` in Hermes config.
3. Confirm with `hermes status` that Browser Use is recognized.

## Editable install fallback

If plain editable install fails with an `AssertionError: SRE module mismatch`, rerun with the live Hermes/session interpreter:

```bash
uv tool install -e . --python "<live-python-exe>" --no-managed-python --force
```

This is a retry pattern for Windows editable installs using uv, not a reason to abandon the install.

## Positive cloud verification

`browser-harness --doctor` can still show no active browser connection even when install is correct.

**Simplest path (preferred): BU_AUTOSPAWN**

```bash
BU_AUTOSPAWN=1 BROWSER_USE_API_KEY=... browser-harness <<'PY'
new_tab('https://example.com')
wait_for_load()
print(page_info())
PY
```

Expected positive signals:
- Cloud browser provisions (liveUrl printed)
- `page_info()['url'] == 'https://example.com/'`
- Title includes `Example Domain`

**Conditions** (run.py logic): `BROWSER_USE_API_KEY` set + `BU_AUTOSPAWN=1` + no local Chrome CDP on 9222/9223 + no `BU_CDP_URL`/`BU_CDP_WS` override.

---

**Alternative: Python API smoke test** (for finer control)

Use the installed tool environment's Python and run a real cloud-browser smoke test:

```python
from browser_harness.admin import start_remote_daemon, stop_remote_daemon, restart_daemon
from browser_harness.helpers import new_tab, wait_for_load, page_info
```

Recommended test flow:

1. Load `BROWSER_USE_API_KEY` from the active Hermes `.env` into the subprocess environment.
2. Set `BU_NAME` to an isolated value like `verify`.
3. `restart_daemon('verify')`
4. `browser = start_remote_daemon('verify', timeout=1)`
5. `new_tab('https://example.com')`
6. `wait_for_load()`
7. `print(page_info())`
8. `stop_remote_daemon('verify')`

Expected positive signals:

- browser id present
- liveUrl present
- `page_info()['url'] == 'https://example.com/'`
- title includes `Example Domain`
- stop path succeeds

## Interpretation

- Cloud smoke test passes + doctor says Chrome local attach missing -> Browser Use cloud mode works; only local Chrome mode remains unconfigured.
- Cloud smoke test fails -> do not claim integration complete.

## Windows: chrome:// protocol links don't open from external commands

On Windows, `chrome://inspect/#remote-debugging` (and other `chrome://` URLs) **cannot be opened via `start`, `cmd /c start`, or browser automation tools** — Windows has no registered handler for the `chrome://` protocol. The user must manually:

1. Open a new tab in Chrome
2. Paste `chrome://inspect/#remote-debugging` into the omnibox and press Enter
3. Tick **"Allow remote debugging for this browser instance"**
4. Click **"Allow"** (or Hebrew **"זה בסדר"**) on the confirmation popup

**Do not** attempt to automate this step via `browser-harness` or shell commands — it requires user interaction in the Chrome UI. The verification flow should instruct the user to do this manually, then re-run `browser-harness --doctor` to confirm the local attach works.

**Workaround for documentation/scripts**: Provide the full URL as copy-paste text, not as a clickable link or CLI target.

---

## Positive local Chrome verification (verified 2026-06-06)

Once remote debugging is enabled, the local attach works end-to-end:

```bash
# 1. Doctor shows all local checks pass
browser-harness --doctor
# [ok  ] chrome running
# [ok  ] daemon alive
# [ok  ] active browser connections — 1

# 2. Basic harness command works
browser-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
# Returns: {'url': 'https://example.com/', 'title': 'Example Domain', ...}

# 3. Visible automation pattern (coordinate click + JS)
browser-harness <<'PY'
new_tab("https://en.wikipedia.org/wiki/Main_Page")
wait_for_load()
coords = js("""
const el = document.querySelector('#searchInput');
if (el) {
  const r = el.getBoundingClientRect();
  return {x: r.left + r.width/2, y: r.top + r.height/2};
}
return null;
""")
if coords:
    click_at_xy(coords['x'], coords['y'])
    type_text("Browser automation")
    press_key("Enter")
    wait_for_load()
    print(page_info()['title'])
capture_screenshot("wiki_search.png")
PY
```

**Expected positive signals for local mode:**
- `browser-harness --doctor` shows `[ok]` for daemon and active connections
- `page_info()` returns real URL/title from your Chrome tab
- Screenshots capture your actual browser viewport
- Tab shows 🐴 prefix (horse emoji) when agent controls it
- Chrome shows "Automated testing software performs a check on Chrome" banner

**Interpretation:**
- Local doctor all `[ok]` + cloud smoke test passes → **both modes work**, use whichever fits the task
- Local doctor fails → only cloud mode available (set `BU_AUTOSPAWN=1`)
- Cloud smoke test fails + local works → cloud creds/config issue, local still usable
