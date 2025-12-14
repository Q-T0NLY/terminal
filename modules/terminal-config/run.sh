#!/bin/bash
# Build and run Terminal Config Service

set -e

SERVICE_NAME="terminal-config"
PORT=8005

echo "🔨 Building ${SERVICE_NAME} service..."
docker build -t ose/${SERVICE_NAME}:latest .

echo "🚀 Running ${SERVICE_NAME} service..."
docker run -d \
  --name ose-${SERVICE_NAME} \
  -p ${PORT}:${PORT} \
  ose/${SERVICE_NAME}:latest

echo "✅ ${SERVICE_NAME} service started!"
echo "📊 Access at: http://localhost:${PORT}"
echo "📖 API docs: http://localhost:${PORT}/docs"
echo ""
echo "View logs: docker logs -f ose-${SERVICE_NAME}"
echo "Stop service: docker stop ose-${SERVICE_NAME}"
echo "Remove container: docker rm ose-${SERVICE_NAME}"
