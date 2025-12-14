#!/bin/bash

echo "🌐 Starting OSE Ultra-Advanced Service Mesh Dashboard..."
echo "📊 Dashboard: http://localhost:8000"
echo "🔌 WebSocket: ws://localhost:8000/ws/mesh"
echo "🤖 NLP API: http://localhost:8000/api/v1/nlp/query"
echo "📈 Topology: http://localhost:8000/api/v1/topology/graph"
echo "💡 AI Recs: http://localhost:8000/api/v1/ai/recommendations"
echo ""

uvicorn advanced_main:app --host 0.0.0.0 --port 8000 --reload
