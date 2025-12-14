#!/bin/bash
set -e

echo "🚀 Starting OSE Metrics Collector Service..."
echo "📊 Port: 8006"
echo "📚 Docs: http://localhost:8006/docs"
echo "📈 Prometheus: http://localhost:8006/metrics"
echo ""

# Run the service
python main.py
