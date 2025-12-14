#!/bin/bash

# 🚀 OSE Quick Start Script
# Ultra-fast setup and launch

set -e

echo "🚀 OSE Platform - Quick Start"
echo "=============================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker found"
echo ""

# Menu
echo "Select an option:"
echo "1) Start all services"
echo "2) Start core services only (no monitoring)"
echo "3) Start specific service"
echo "4) Stop all services"
echo "5) View logs"
echo "6) Check status"
echo "7) Clean up everything"
echo "8) Run tests"
echo ""
read -p "Enter option (1-8): " option

case $option in
    1)
        echo "🚀 Starting all services..."
        docker-compose up -d
        echo ""
        echo "✅ All services started!"
        echo ""
        echo "📊 Service URLs:"
        echo "  - Discovery:        http://localhost:8001"
        echo "  - Factory Reset:    http://localhost:8002"
        echo "  - Reinstallation:   http://localhost:8003"
        echo "  - Optimization:     http://localhost:8004"
        echo "  - Terminal Config:  http://localhost:8005"
        echo "  - API Gateway:      http://localhost:8000"
        echo "  - Grafana:          http://localhost:3000 (admin/admin)"
        echo "  - Prometheus:       http://localhost:9090"
        echo "  - RabbitMQ:         http://localhost:15672 (ose/ose_queue_password)"
        ;;
    
    2)
        echo "🚀 Starting core services..."
        docker-compose up -d postgres redis rabbitmq discovery factory-reset reinstallation optimization terminal-config
        echo "✅ Core services started!"
        ;;
    
    3)
        echo "Available services:"
        echo "  - discovery"
        echo "  - factory-reset"
        echo "  - reinstallation"
        echo "  - optimization"
        echo "  - terminal-config"
        echo ""
        read -p "Enter service name: " service
        docker-compose up -d $service
        echo "✅ $service started!"
        ;;
    
    4)
        echo "🛑 Stopping all services..."
        docker-compose down
        echo "✅ All services stopped!"
        ;;
    
    5)
        read -p "Enter service name (or 'all'): " service
        if [ "$service" = "all" ]; then
            docker-compose logs -f
        else
            docker-compose logs -f $service
        fi
        ;;
    
    6)
        echo "📊 Service Status:"
        docker-compose ps
        echo ""
        echo "🔍 Health Checks:"
        for port in 8001 8002 8003 8004 8005; do
            status=$(curl -s http://localhost:$port/health 2>/dev/null | grep -o '"status":"[^"]*"' || echo "❌")
            echo "  Port $port: $status"
        done
        ;;
    
    7)
        echo "⚠️  WARNING: This will remove all containers, volumes, and data!"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            echo "🧹 Cleaning up..."
            docker-compose down -v
            docker system prune -f
            echo "✅ Cleanup complete!"
        else
            echo "❌ Cancelled"
        fi
        ;;
    
    8)
        echo "🧪 Running tests..."
        echo ""
        
        echo "Testing Discovery Service..."
        curl -s http://localhost:8001/api/v1/discover/hardware | jq . || echo "❌ Failed"
        
        echo ""
        echo "Testing Factory Reset Service..."
        curl -s http://localhost:8002/api/v1/reset/profiles | jq . || echo "❌ Failed"
        
        echo ""
        echo "Testing Optimization Service..."
        curl -s http://localhost:8004/api/v1/optimize/recommendations | jq . || echo "❌ Failed"
        
        echo ""
        echo "Testing Terminal Config Service..."
        curl -s http://localhost:8005/api/v1/profiles | jq . || echo "❌ Failed"
        
        echo ""
        echo "✅ Tests complete!"
        ;;
    
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✨ Done!"
