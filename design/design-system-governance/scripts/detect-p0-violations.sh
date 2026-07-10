#!/usr/bin/env bash
# detect-p0-violations.sh
# Part of design-system-governance skill
# Run from project root. Returns non-zero exit code if any P0 violations found.

set -euo pipefail

PROJECT_ROOT="${1:-.}"
SRC_DIR="$PROJECT_ROOT/src"

echo "🔍 Design System P0 Violation Detection"
echo "Project: $PROJECT_ROOT"
echo ""

VIOLATIONS=0

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

check() {
    local name="$1"
    local pattern="$2"
    local files="${3:-$SRC_DIR}"
    local exclude="${4:-}"

    echo -n "Checking $name... "
    local cmd="grep -rn \"$pattern\" $files --include=\"*.tsx\" --include=\"*.ts\""
    if [ -n "$exclude" ]; then
        cmd="$cmd | grep -v \"$exclude\""
    fi
    local results
    results=$(eval "$cmd" 2>/dev/null || true)
    if [ -n "$results" ]; then
        echo -e "${RED}VIOLATIONS FOUND${NC}"
        echo "$results" | head -20
        echo "..."
        VIOLATIONS=$((VIOLATIONS + 1))
    else
        echo -e "${GREEN}CLEAN${NC}"
    fi
}

# P0-HS: Hardcoded font sizes
check "P0-HS: Hardcoded font sizes (text-[Npx])" "text-\[[0-9]px\]"

# P0-HP: Hardcoded padding
check "P0-HP: Hardcoded padding (p-[N])" "p-\[[0-9]"

# P0-HR: Hardcoded border radius
check "P0-HR: Hardcoded border radius (rounded-[N])" "rounded-\[[0-9]"

# P0-GC: Generic Tailwind colors
check "P0-GC: Generic Tailwind colors (slate/zinc/gray/neutral/stone)" "slate-\|zinc-\|gray-\|neutral-\|stone-" "$SRC_DIR" "var(--color"

# P0-RX: Raw hex in components (exclude design token files)
check "P0-RX: Raw hex in components" "#[0-9a-fA-F]\{6\}" "$SRC_DIR" "tokens.json\|tailwind.theme.json\|DESIGN.md"

echo ""
echo "🔍 Signature Element Checks (manual - in src/index.css)"

for elem in ".accent-bar" ".curve-glow" ".stagger-in" ".pulse-brass"; do
    echo -n "Checking $elem... "
    if grep -q "$elem" "$SRC_DIR/index.css" 2>/dev/null; then
        echo -e "${GREEN}FOUND${NC}"
    else
        echo -e "${RED}MISSING${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

echo ""
echo -n "Checking prefers-reduced-motion... "
if grep -q "prefers-reduced-motion" "$SRC_DIR/index.css" 2>/dev/null; then
    echo -e "${GREEN}FOUND${NC}"
else
    echo -e "${RED}MISSING${NC}"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

echo ""
echo "================================="
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL P0 CHECKS PASSED${NC}"
    echo "Environment can proceed with feature work."
    exit 0
else
    echo -e "${RED}❌ $VIOLATIONS P0 VIOLATION CATEGORIES FOUND${NC}"
    echo "STOP: Remediate P0 before any feature work (Three-Layer Method invariant)."
    exit 1
fi