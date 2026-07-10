# BB-Terminal UI Patterns for Dashboard Layout

Source: `C:\Users\Tiger\AI Hub\Projects\BB-Terminal` - React/TypeScript terminal-style dashboard with workspace tabs.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  BB-TERMINAL APP (React + Vite + Zustand)                   │
├─────────────────────────────────────────────────────────────┤
│  Layout:                                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ CommandBar (top) - command input, autocomplete      │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ QuickBar       - quick actions, symbols             │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ WorkspaceTabs  - persistent tabs per function       │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ FunctionPanel  - modular content area (flex-1)      │   │
│  │    ├─ CC (Command Center)                          │   │
│  │    ├─ INTEL (symbol)  - intelligence/dashboard     │   │
│  │    ├─ DES (symbol)    - details                    │   │
│  │    ├─ GP (symbol)     - graph/chart                │   │
│  │    └─ ...             - 20+ functions              │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ StatusBar      - connection, mode, info             │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  State: Zustand store with persist middleware               │
│  - Tabs array with id, code, symbol                        │
│  - Active tab tracking                                      │
│  - Persisted to localStorage (bbterminal-workspace)        │
└─────────────────────────────────────────────────────────────┘
```

## Key Patterns for Northstar 2.0 CommandCenter

### 1. Workspace Tabs with Persistent State

```typescript
// From app/src/store/workspaceStore.ts
interface Tab {
  id: string;           // "CC:_" or "INTEL:AAPL"
  code: FunctionCode;   // "CC", "INTEL", "DES", etc.
  symbol?: string;      // "AAPL", "SPY", etc.
}

const useWorkspace = create<WorkspaceState>()(
  persist(
    (set, get) => ({
      tabs: [{ id: "CC:_", code: "CC" }],  // Always keep Command Center
      activeTabId: "CC:_",
      activeSymbol: "AAPL",
      
      openTab: (code, symbol) => { /* ... */ },
      closeTab: (id) => { /* fallback to CC */ },
      setActiveTab: (id) => set({ activeTabId: id }),
      setActiveSymbol: (s) => set({ activeSymbol: s.toUpperCase() }),
    }),
    { name: "bbterminal-workspace" }  // localStorage key
  )
);
```

### 2. Modular Function Panels

```tsx
// From app/src/App.tsx
const SCREENS: Record<string, (symbol?: string) => JSX.Element> = {
  CC: () => <CC />,
  INTEL: (s) => <INTEL symbol={s} />,
  DES: (s) => <DES symbol={s} />,
  GP:  (s) => <GP symbol={s} />,
  // ... 20+ functions
};

function App() {
  const { tabs, activeTabId } = useWorkspace();
  const active = tabs.find((t) => t.id === activeTabId) ?? tabs[0];
  const screen = active && SCREENS[active.code]?.(active.symbol);
  
  return (
    <div className="h-screen flex flex-col">
      <CommandBar />
      <QuickBar />
      <WorkspaceTabs />
      <div className="flex-1 min-h-0 p-1 flex">
        {active && (
          <FunctionPanel code={active.code} symbol={active.symbol}>
            {screen ?? <div>Function not implemented.</div>}
          </FunctionPanel>
        )}
      </div>
      <StatusBar />
    </div>
  );
}
```

### 3. Terminal-Themed Styling

```css
/* Consistent terminal aesthetic */
.terminal-border { border-color: hsl(var(--border)); }
.bg-[#0d0d14] { background: #0d0d14; }  /* Deep dark */
.text-primary { color: hsl(var(--primary)); }
.font-mono { font-family: ui-monospace, monospace; }
.tracking-[0.2em] { letter-spacing: 0.2em; }
.uppercase { text-transform: uppercase; }
```

### 4. Responsive Data Display Patterns

```tsx
// From CommandCenter.tsx - effective patterns
// Fixed-width cards with controlled overflow
<div className="p-4 space-y-4 max-w-[1200px] mx-auto">

// Scrollable sections with max-height
<div className="space-y-2 max-h-[400px] overflow-y-auto">

// Flex-wrap for badges/chips
<div className="flex flex-wrap gap-2">

// Consistent typography scale
.text-xs, .text-sm, .text-[10px]  /* Compact terminal density */
.font-mono                         /* Monospace throughout */
```

## Adapting to Northstar 2.0 CommandCenter

| BB-Terminal Pattern | Northstar 2.0 Application |
|---------------------|---------------------------|
| WorkspaceTabs | Add tabbed views: Briefing, Scanner, Committee, Portfolio, Alerts |
| FunctionPanel | Modular widget system per tab |
| CommandBar | Global command palette (Cmd+K) for quick actions |
| QuickBar | Symbol search, universe switcher |
| StatusBar | Pipeline status, data freshness, connection |
| Persistent layout | Restore tab/symbol on reload |
| Terminal theme | Extend existing `bg-[#0d0d14]` `font-mono` style |

## Actual Changes Applied (session)

```tsx
// BEFORE: Fixed layout, hardcoded dark bg
<div className="p-4 space-y-4 max-w-[1200px] mx-auto">
  <h1 className="text-sm font-mono tracking-[0.2em] uppercase text-primary">Command Center</h1>
  <Card className="rounded-none bg-[#0d0d14] border-border terminal-border overflow-hidden">

// AFTER: Responsive grid, semantic tokens, LIVE indicator
<div className="p-4 space-y-4 max-w-full mx-auto">
  <div className="flex items-center justify-between gap-4 mb-4">
    <h1 className="text-sm font-mono tracking-[0.2em] uppercase text-primary">Command Center</h1>
    <div className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground">
      <span className="flex items-center gap-1">
        <span className="w-2 h-2 rounded-full bg-positive animate-pulse" />
        LIVE
      </span>
      <span className="px-2 py-0.5 bg-muted rounded border border-border">
        {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </span>
    </div>
  </div>
  <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
    <Card className="rounded-none bg-card border-border terminal-border overflow-hidden col-span-1 lg:col-span-2 xl:col-span-2">
    <Card className="rounded-none bg-card border-border terminal-border overflow-hidden col-span-1 lg:col-span-1 xl:col-span-1">
    <Card className="rounded-none bg-card border-border terminal-border overflow-hidden col-span-1 lg:col-span-3 xl:col-span-3">
```

**Result:** Build passes, responsive 3-column grid on XL, semantic theming, live time indicator.

## Implementation Hooks for Overnight Loop

```python
def improve_dashboard_ui():
    """Apply BB-Terminal patterns to CommandCenter.tsx"""
    log("UI: Applying dashboard layout improvements...")
    
    # Priority improvements:
    # 1. Add Zustand workspace store (persist tabs/symbol)
    # 2. Create FunctionPanel wrapper for modular widgets
    # 3. Add WorkspaceTabs component
    # 4. Implement CommandBar (Cmd+K palette)
    # 5. Add StatusBar (pipeline health, data freshness)
    # 6. Ensure all components use terminal theme consistently
    # 7. Responsive grid for multi-panel layouts
    
    # For overnight loop: validate build passes after changes
    pass
```

## Terminal Theme Constants (from BB-Terminal)

```typescript
// Colors used consistently
const TERMINAL_BG = '#0d0d14';
const TERMINAL_BORDER = 'hsl(var(--border))';
const TERMINAL_MUTED = 'hsl(var(--muted-foreground))';
const TERMINAL_PRIMARY = 'hsl(var(--primary))';
const TERMINAL_NEGATIVE = 'hsl(var(--negative))';
const TERMINAL_POSITIVE = 'hsl(var(--positive))';

// Typography
const MONO_FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';
const BASE_SIZE = '13px';
const SMALL_SIZE = '11px';  // Badges, labels
const MICRO_SIZE = '10px';  // Dense data
```