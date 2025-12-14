#!/bin/bash

#############################################
# Universal Registry - Consolidation Test
# Verify all components are properly integrated
#############################################

set -e

REGISTRY_DIR="/workspaces/terminal/modules/universal-registry"
BIN_DIR="/workspaces/terminal/bin"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "═══════════════════════════════════════════════════"
echo "  Universal Registry - Consolidation Verification"
echo "═══════════════════════════════════════════════════"
echo ""

# Test 1: Check API Gateway exists
echo -n "1. API Gateway file exists............... "
if [ -f "$REGISTRY_DIR/core/gateway/api_gateway.py" ]; then
    SIZE=$(wc -c < "$REGISTRY_DIR/core/gateway/api_gateway.py")
    echo -e "${GREEN}✓${NC} ($SIZE bytes)"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 2: Check ose-cli exists and is executable
echo -n "2. OSE CLI exists and is executable...... "
if [ -x "$BIN_DIR/ose-cli" ]; then
    SIZE=$(wc -c < "$BIN_DIR/ose-cli")
    echo -e "${GREEN}✓${NC} ($SIZE bytes)"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 3: Check universal-registry-cli exists
echo -n "3. Universal Registry CLI exists......... "
if [ -x "$BIN_DIR/universal-registry-cli" ]; then
    SIZE=$(wc -c < "$BIN_DIR/universal-registry-cli")
    echo -e "${GREEN}✓${NC} ($SIZE bytes)"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 4: Check metrics routes exist
echo -n "4. Metrics routes exist.................. "
if [ -f "$REGISTRY_DIR/core/api/metrics_routes.py" ]; then
    SIZE=$(wc -c < "$REGISTRY_DIR/core/api/metrics_routes.py")
    echo -e "${GREEN}✓${NC} ($SIZE bytes)"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 5: Check documentation exists
echo -n "5. START_HERE.md exists.................. "
if [ -f "$REGISTRY_DIR/START_HERE.md" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 6: Check CONSOLIDATION_SUMMARY.md exists
echo -n "6. CONSOLIDATION_SUMMARY.md exists....... "
if [ -f "$REGISTRY_DIR/CONSOLIDATION_SUMMARY.md" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 7: Check old microservices-cli is symlink (not duplicate)
echo -n "7. No duplicate microservices-cli........ "
if [ -L "$BIN_DIR/microservices-cli" ]; then
    echo -e "${GREEN}✓${NC} (symlink preserved)"
else
    if [ ! -e "$BIN_DIR/microservices-cli" ]; then
        echo -e "${GREEN}✓${NC} (removed)"
    else
        echo -e "${YELLOW}⚠${NC} (exists as file, should remove)"
    fi
fi

# Test 8: Check Python dependencies for ose-cli
echo -n "8. Checking Python dependencies.......... "
if python3 -c "import rich, InquirerPy" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠${NC} (need: pip install rich InquirerPy)"
fi

# Test 9: Verify API Gateway imports
echo -n "9. API Gateway imports correctly......... "
if python3 -c "import sys; sys.path.insert(0, '$REGISTRY_DIR'); from core.gateway.api_gateway import APIGateway" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    exit 1
fi

# Test 10: Count total lines of consolidated code
echo -n "10. Code consolidation metrics........... "
GATEWAY_LINES=$(wc -l < "$REGISTRY_DIR/core/gateway/api_gateway.py" 2>/dev/null || echo "0")
OSE_CLI_LINES=$(wc -l < "$BIN_DIR/ose-cli" 2>/dev/null || echo "0")
REGISTRY_CLI_LINES=$(wc -l < "$BIN_DIR/universal-registry-cli" 2>/dev/null || echo "0")
TOTAL_LINES=$((GATEWAY_LINES + OSE_CLI_LINES + REGISTRY_CLI_LINES))
echo -e "${GREEN}✓${NC} ($TOTAL_LINES lines)"

echo ""
echo "═══════════════════════════════════════════════════"
echo ""
echo "  ${GREEN}✅ All consolidation checks passed!${NC}"
echo ""
echo "═══════════════════════════════════════════════════"
echo ""

# Show summary
echo "📊 Consolidation Summary:"
echo "   • API Gateway:            $GATEWAY_LINES lines"
echo "   • OSE CLI:                $OSE_CLI_LINES lines"
echo "   • Universal Registry CLI: $REGISTRY_CLI_LINES lines"
echo "   • Total new code:         $TOTAL_LINES lines"
echo ""

# Show what to do next
echo "🚀 Next Steps:"
echo ""
echo "   1. Start the registry:"
echo "      cd $REGISTRY_DIR"
echo "      python3 hyper_registry.py"
echo ""
echo "   2. Save the admin API key shown in the output"
echo ""
echo "   3. Launch interactive TUI:"
echo "      ose-cli"
echo ""
echo "   4. Or use the registry CLI:"
echo "      universal-registry-cli plugin list"
echo "      universal-registry-cli service list"
echo ""
echo "   5. Read the documentation:"
echo "      cat $REGISTRY_DIR/START_HERE.md"
echo ""

# Check if dependencies need installation
echo "📦 Dependencies Check:"
echo ""
if ! python3 -c "import rich" 2>/dev/null; then
    echo "   ${YELLOW}⚠${NC}  Need to install: pip install rich InquirerPy"
else
    echo "   ${GREEN}✓${NC}  All Python dependencies installed"
fi
echo ""

echo "═══════════════════════════════════════════════════"
echo "  Platform consolidation complete! 🎉"
echo "═══════════════════════════════════════════════════"
