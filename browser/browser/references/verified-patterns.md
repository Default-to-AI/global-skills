# Verified Automation Patterns (2026-06-06)

These patterns were tested end-to-end on Windows with local Chrome (remote debugging enabled) and Browser Use cloud.

## Local Chrome Attach — Prerequisites

1. User enables `chrome://inspect/#remote-debugging` → "Allow remote debugging for this browser instance" → click "Allow"/"זה בסדר"
2. `browser-harness --doctor` shows:
   ```
   [ok  ] chrome running
   [ok  ] daemon alive
   [ok  ] active browser connections — 1
   ```

## Core Pattern: Coordinate Click + JS (Works Through Iframes/Shadow DOM)

```python
# 1. Get element center via JS
coords = js("""
const el = document.querySelector('your-selector');
if (el) {
  const r = el.getBoundingClientRect();
  return {x: r.left + r.width/2, y: r.top + r.height/2};
}
return null;
""")

# 2. Click at coordinates → wait → screenshot
if coords:
    click_at_xy(coords['x'], coords['y'])
    wait_for_load()
    capture_screenshot("after_click.png")
```

**Why this works**: `Input.dispatchMouseEvent` at compositor level passes through iframes, shadow DOM, cross-origin — no selector brittleness.

---

## Verified Demo Patterns

### Pattern 1: Wikipedia Search & Navigation
```python
new_tab("https://en.wikipedia.org/wiki/Main_Page")
wait_for_load()

# Search box
coords = js("""const el = document.querySelector('#searchInput');
if (el) { const r = el.getBoundingClientRect(); return {x: r.left + r.width/2, y: r.top + r.height/2}; } return null;""")
click_at_xy(coords['x'], coords['y'])
type_text("Browser automation")
press_key("Enter")
wait_for_load()

# Click first result
first = js("""const el = document.querySelector('#mw-content-text .mw-search-result-heading a');
if (el) { const r = el.getBoundingClientRect(); return {x: r.left + r.width/2, y: r.top + r.height/2}; } return null;""")
click_at_xy(first['x'], first['y'])
wait_for_load()
capture_screenshot("wiki_article.png")
```

**Result**: Main Page → Search Results → "Browser automation" article page. Tab shows 🐴 prefix.

### Pattern 2: Form Fill (httpbin.org/forms/post)
```python
new_tab("https://httpbin.org/forms/post")
wait_for_load()

# Get all form field coordinates
fields = js("""
const inputs = document.querySelectorAll('input, textarea, select');
const result = {};
inputs.forEach((el, i) => {
  const r = el.getBoundingClientRect();
  result[el.name || el.id || `field_${i}`] = {x: r.left + r.width/2, y: r.top + r.height/2};
});
return result;
""")

# Fill each field by coordinate
for name, coord in fields.items():
    click_at_xy(coord['x'], coord['y'])
    type_text(test_data[name])  # your test data dict
```

### Pattern 3: Example.com Link Click
```python
new_tab("https://example.com")
wait_for_load()
link = js("""const a = document.querySelector('a');
if (a) { const r = a.getBoundingClientRect(); return {x: r.left + r.width/2, y: r.top + r.height/2}; } return null;""")
click_at_xy(link['x'], link['y'])
wait_for_load()
# Page title changes from "Example Domain" to "Example Domains"
```

---

## Cloud Browser Use (BU_AUTOSPAWN)

```bash
BU_AUTOSPAWN=1 browser-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
stop_remote_daemon()
PY
```

**Conditions**: `BROWSER_USE_API_KEY` set + `BU_AUTOSPAWN=1` + no local Chrome CDP on 9222/9223.

**Verification**: Returns `page_info()` with `url: https://example.com/`, title "Example Domain".

---

## Diagnosis: browser-harness --doctor

Single source of truth for "is it working?"

| Mode | Expected Output |
|------|-----------------|
| Local Chrome | `[ok] chrome running`, `[ok] daemon alive`, `[ok] active browser connections — 1` |
| Cloud | `[ok] chrome running`, `[ok] daemon alive`, `[ok] active browser connections — 1` (shows cloud browser) |
| Neither | `[FAIL] daemon alive`, `[FAIL] active browser connections — 0` |

---

## Windows-Specific Notes

- `chrome://` protocol links **cannot** be opened programmatically on Windows — user must manually paste `chrome://inspect/#remote-debugging` in omnibox
- The "Could not find Chrome application" error when clicking Allow is a Windows protocol handler issue, not a browser-harness failure
- Hebrew UI: "זה בסדר" = "OK", "ביטול" = "Cancel"

---

## Visual Indicators of Success

- Tab title prefixed with 🐴 (horse emoji) = agent controls this tab
- Chrome shows "Automated testing software performs a check on Chrome" banner
- Screenshots capture actual browser viewport
- `page_info()` returns real URL/title from your Chrome tab