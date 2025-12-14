#!/bin/bash

# OSE TUI Quick Launcher

echo "🎨 OSE TUI - Ultra-Advanced Terminal Interface"
echo ""
echo "Checking dependencies..."

# Check if rich is installed
if ! python3 -c "import rich" 2>/dev/null; then
    echo "⚠️  Installing required packages..."
    pip install rich requests -q
fi

# Check if Service Mesh is running
echo "Checking Service Mesh connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Service Mesh is running on http://localhost:8000"
else
    echo "⚠️  Service Mesh appears to be offline"
    echo "   Start it with: docker-compose up -d service-mesh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Launching TUI..."
echo ""

# Launch TUI
python3 "$(dirname "$0")/ose_tui.py"
