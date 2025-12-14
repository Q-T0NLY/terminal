"""
🌐 OSE Service Mesh Interface
Centralized dashboard for monitoring all microservices
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import aiohttp
import json

app = FastAPI(
    title="OSE Service Mesh",
    description="Centralized Service Monitoring & Management Dashboard",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Service Registry ====================

SERVICES = {
    "discovery": {
        "name": "Discovery Service",
        "url": "http://discovery:8001",
        "port": 8001,
        "icon": "🔍",
        "description": "System scanning and hardware/software discovery",
        "endpoints": 40,
        "status": "unknown"
    },
    "factory-reset": {
        "name": "Factory Reset Service",
        "url": "http://factory-reset:8002",
        "port": 8002,
        "icon": "🧹",
        "description": "System cleanup and factory reset operations",
        "endpoints": 35,
        "status": "unknown"
    },
    "reinstallation": {
        "name": "Reinstallation Service",
        "url": "http://reinstallation:8003",
        "port": 8003,
        "icon": "📦",
        "description": "Package management and application installation",
        "endpoints": 40,
        "status": "unknown"
    },
    "optimization": {
        "name": "Optimization Service",
        "url": "http://optimization:8004",
        "port": 8004,
        "icon": "⚡",
        "description": "System performance optimization and tuning",
        "endpoints": 45,
        "status": "unknown"
    },
    "terminal-config": {
        "name": "Terminal Config Service",
        "url": "http://terminal-config:8005",
        "port": 8005,
        "icon": "🖥️",
        "description": "Terminal configuration and shell customization",
        "endpoints": 35,
        "status": "unknown"
    },
    "metrics-collector": {
        "name": "Metrics Collector Service",
        "url": "http://metrics-collector:8006",
        "port": 8006,
        "icon": "📊",
        "description": "Real-time metrics collection and monitoring",
        "endpoints": 40,
        "status": "unknown"
    }
}

# WebSocket connections for live updates
active_connections: List[WebSocket] = []

# ==================== Models ====================

class ServiceHealth(BaseModel):
    service: str
    status: str
    response_time_ms: float
    last_check: str
    uptime: Optional[str] = None
    version: Optional[str] = None


class ServiceMetrics(BaseModel):
    total_services: int
    healthy_services: int
    unhealthy_services: int
    total_endpoints: int
    average_response_time: float


# ==================== Service Health Checks ====================

async def check_service_health(service_id: str, service_info: Dict) -> ServiceHealth:
    """Check health of a single service"""
    start_time = asyncio.get_event_loop().time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{service_info['url']}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                response_time = (asyncio.get_event_loop().time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    return ServiceHealth(
                        service=service_id,
                        status="healthy",
                        response_time_ms=round(response_time, 2),
                        last_check=datetime.now().isoformat(),
                        version=data.get("version", "unknown")
                    )
                else:
                    return ServiceHealth(
                        service=service_id,
                        status="unhealthy",
                        response_time_ms=round(response_time, 2),
                        last_check=datetime.now().isoformat()
                    )
    except Exception as e:
        response_time = (asyncio.get_event_loop().time() - start_time) * 1000
        return ServiceHealth(
            service=service_id,
            status="down",
            response_time_ms=round(response_time, 2),
            last_check=datetime.now().isoformat()
        )


async def check_all_services() -> Dict[str, ServiceHealth]:
    """Check health of all services"""
    tasks = [
        check_service_health(service_id, service_info)
        for service_id, service_info in SERVICES.items()
    ]
    
    results = await asyncio.gather(*tasks)
    
    return {
        result.service: result
        for result in results
    }


# ==================== Background Tasks ====================

async def broadcast_health_updates():
    """Broadcast service health updates to all WebSocket clients"""
    while True:
        try:
            health_status = await check_all_services()
            
            # Update service status
            for service_id, health in health_status.items():
                SERVICES[service_id]["status"] = health.status
            
            # Broadcast to all connected clients
            if active_connections:
                message = {
                    "type": "health_update",
                    "timestamp": datetime.now().isoformat(),
                    "services": {k: v.dict() for k, v in health_status.items()}
                }
                
                disconnected = []
                for connection in active_connections:
                    try:
                        await connection.send_json(message)
                    except:
                        disconnected.append(connection)
                
                # Remove disconnected clients
                for conn in disconnected:
                    active_connections.remove(conn)
            
            await asyncio.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            print(f"Error in health check broadcast: {e}")
            await asyncio.sleep(10)


@app.on_event("startup")
async def startup_event():
    """Start background health monitoring"""
    asyncio.create_task(broadcast_health_updates())


# ==================== API Endpoints ====================

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Service Mesh Dashboard"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSE Service Mesh Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 2px solid rgba(255,255,255,0.2);
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .metric-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .metric-card h3 {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-card .value {
            font-size: 2.5em;
            font-weight: bold;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }
        
        .service-card {
            background: rgba(255,255,255,0.95);
            color: #333;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #667eea;
        }
        
        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }
        
        .service-card.healthy {
            border-left-color: #10b981;
        }
        
        .service-card.unhealthy {
            border-left-color: #f59e0b;
        }
        
        .service-card.down {
            border-left-color: #ef4444;
        }
        
        .service-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .service-icon {
            font-size: 2.5em;
            margin-right: 15px;
        }
        
        .service-title {
            flex: 1;
        }
        
        .service-title h3 {
            font-size: 1.3em;
            margin-bottom: 5px;
        }
        
        .service-title p {
            font-size: 0.85em;
            color: #666;
        }
        
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status-badge.healthy {
            background: #10b981;
            color: white;
        }
        
        .status-badge.unhealthy {
            background: #f59e0b;
            color: white;
        }
        
        .status-badge.down {
            background: #ef4444;
            color: white;
        }
        
        .service-stats {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9em;
        }
        
        .stat-label {
            color: #6b7280;
        }
        
        .stat-value {
            font-weight: bold;
            color: #1f2937;
        }
        
        .pulse {
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .connection-status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            background: rgba(0,0,0,0.7);
            border-radius: 25px;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .connection-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10b981;
        }
        
        .connection-dot.disconnected {
            background: #ef4444;
        }
        
        .action-buttons {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-secondary {
            background: #e5e7eb;
            color: #374151;
        }
        
        .btn-secondary:hover {
            background: #d1d5db;
        }
    </style>
</head>
<body>
    <div class="connection-status">
        <div class="connection-dot" id="connectionDot"></div>
        <span id="connectionText">Connecting...</span>
    </div>
    
    <div class="container">
        <header>
            <h1>🌐 OSE Service Mesh</h1>
            <p class="subtitle">Real-Time Microservices Monitoring Dashboard</p>
        </header>
        
        <div class="metrics">
            <div class="metric-card">
                <h3>Total Services</h3>
                <div class="value" id="totalServices">6</div>
            </div>
            <div class="metric-card">
                <h3>Healthy</h3>
                <div class="value" style="color: #10b981;" id="healthyServices">-</div>
            </div>
            <div class="metric-card">
                <h3>Unhealthy</h3>
                <div class="value" style="color: #f59e0b;" id="unhealthyServices">-</div>
            </div>
            <div class="metric-card">
                <h3>Total Endpoints</h3>
                <div class="value" id="totalEndpoints">235</div>
            </div>
        </div>
        
        <div class="services-grid" id="servicesGrid"></div>
    </div>
    
    <script>
        const services = {
            "discovery": {
                name: "Discovery Service",
                icon: "🔍",
                description: "System scanning and hardware/software discovery",
                port: 8001,
                endpoints: 40
            },
            "factory-reset": {
                name: "Factory Reset Service",
                icon: "🧹",
                description: "System cleanup and factory reset operations",
                port: 8002,
                endpoints: 35
            },
            "reinstallation": {
                name: "Reinstallation Service",
                icon: "📦",
                description: "Package management and application installation",
                port: 8003,
                endpoints: 40
            },
            "optimization": {
                name: "Optimization Service",
                icon: "⚡",
                description: "System performance optimization and tuning",
                port: 8004,
                endpoints: 45
            },
            "terminal-config": {
                name: "Terminal Config Service",
                icon: "🖥️",
                description: "Terminal configuration and shell customization",
                port: 8005,
                endpoints: 35
            },
            "metrics-collector": {
                name: "Metrics Collector Service",
                icon: "📊",
                description: "Real-time metrics collection and monitoring",
                port: 8006,
                endpoints: 40
            }
        };
        
        let ws = null;
        let reconnectInterval = null;
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/health`);
            
            ws.onopen = () => {
                console.log('WebSocket connected');
                document.getElementById('connectionDot').classList.remove('disconnected');
                document.getElementById('connectionText').textContent = 'Connected';
                if (reconnectInterval) {
                    clearInterval(reconnectInterval);
                    reconnectInterval = null;
                }
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'health_update') {
                    updateDashboard(data.services);
                }
            };
            
            ws.onclose = () => {
                console.log('WebSocket disconnected');
                document.getElementById('connectionDot').classList.add('disconnected');
                document.getElementById('connectionText').textContent = 'Disconnected';
                
                if (!reconnectInterval) {
                    reconnectInterval = setInterval(() => {
                        console.log('Attempting to reconnect...');
                        connectWebSocket();
                    }, 5000);
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
        
        function updateDashboard(healthData) {
            let healthy = 0;
            let unhealthy = 0;
            
            const grid = document.getElementById('servicesGrid');
            grid.innerHTML = '';
            
            for (const [serviceId, health] of Object.entries(healthData)) {
                const service = services[serviceId];
                if (!service) continue;
                
                if (health.status === 'healthy') healthy++;
                else if (health.status === 'unhealthy') unhealthy++;
                
                const card = document.createElement('div');
                card.className = `service-card ${health.status}`;
                card.innerHTML = `
                    <div class="service-header">
                        <div class="service-icon">${service.icon}</div>
                        <div class="service-title">
                            <h3>${service.name}</h3>
                            <p>${service.description}</p>
                        </div>
                    </div>
                    
                    <div>
                        <span class="status-badge ${health.status}">${health.status}</span>
                    </div>
                    
                    <div class="service-stats">
                        <div class="stat-row">
                            <span class="stat-label">Port:</span>
                            <span class="stat-value">${service.port}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Endpoints:</span>
                            <span class="stat-value">${service.endpoints}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Response Time:</span>
                            <span class="stat-value">${health.response_time_ms}ms</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Last Check:</span>
                            <span class="stat-value">${new Date(health.last_check).toLocaleTimeString()}</span>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="window.open('http://localhost:${service.port}/docs', '_blank')">
                            API Docs
                        </button>
                        <button class="btn btn-secondary" onclick="window.open('http://localhost:${service.port}/health', '_blank')">
                            Health Check
                        </button>
                    </div>
                `;
                
                grid.appendChild(card);
            }
            
            document.getElementById('healthyServices').textContent = healthy;
            document.getElementById('unhealthyServices').textContent = unhealthy;
        }
        
        // Initialize
        connectWebSocket();
    </script>
</body>
</html>
"""


@app.get("/api/v1/services", response_model=Dict[str, Any])
async def get_services():
    """Get all registered services"""
    return {
        "total": len(SERVICES),
        "services": SERVICES
    }


@app.get("/api/v1/services/{service_id}/health", response_model=ServiceHealth)
async def get_service_health(service_id: str):
    """Get health status of a specific service"""
    if service_id not in SERVICES:
        return JSONResponse(
            status_code=404,
            content={"error": f"Service {service_id} not found"}
        )
    
    health = await check_service_health(service_id, SERVICES[service_id])
    return health


@app.get("/api/v1/health/all")
async def get_all_health():
    """Get health status of all services"""
    health_status = await check_all_services()
    
    healthy = sum(1 for h in health_status.values() if h.status == "healthy")
    unhealthy = sum(1 for h in health_status.values() if h.status == "unhealthy")
    down = sum(1 for h in health_status.values() if h.status == "down")
    
    avg_response_time = sum(h.response_time_ms for h in health_status.values()) / len(health_status)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_services": len(SERVICES),
            "healthy": healthy,
            "unhealthy": unhealthy,
            "down": down,
            "average_response_time_ms": round(avg_response_time, 2)
        },
        "services": {k: v.dict() for k, v in health_status.items()}
    }


@app.get("/api/v1/metrics")
async def get_metrics():
    """Get service mesh metrics"""
    health_status = await check_all_services()
    
    healthy = sum(1 for h in health_status.values() if h.status == "healthy")
    total_endpoints = sum(s["endpoints"] for s in SERVICES.values())
    avg_response_time = sum(h.response_time_ms for h in health_status.values()) / len(health_status)
    
    return ServiceMetrics(
        total_services=len(SERVICES),
        healthy_services=healthy,
        unhealthy_services=len(SERVICES) - healthy,
        total_endpoints=total_endpoints,
        average_response_time=round(avg_response_time, 2)
    )


@app.websocket("/ws/health")
async def websocket_health(websocket: WebSocket):
    """WebSocket endpoint for real-time health updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial health status
        health_status = await check_all_services()
        await websocket.send_json({
            "type": "health_update",
            "timestamp": datetime.now().isoformat(),
            "services": {k: v.dict() for k, v in health_status.items()}
        })
        
        # Keep connection alive
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.get("/health")
async def health_check():
    """Service mesh health check"""
    return {
        "status": "healthy",
        "service": "service-mesh",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
