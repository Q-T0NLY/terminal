# 🌐 OSE Service Mesh Interface

**Enterprise-grade centralized dashboard for monitoring and managing all microservices**

**Version:** 2.5.0

## Features

### 🫀 Advanced Heartbeat Monitoring
- Multi-dimensional health tracking (healthy, degraded, critical, dead, unknown)
- Latency metrics (min/max/avg response times)
- Uptime percentage calculation
- Consecutive failure detection
- Configurable health check intervals
- Real-time health summary dashboard
- Background async monitoring

### 🔗 Service Dependency Mapping
- Complete dependency graph visualization
- Circular dependency detection
- Critical path analysis
- Service clustering (core, utility, infrastructure, monitoring, config)
- Hub service identification
- Multiple export formats (D3.js, Cytoscape, Mermaid)
- Interactive 3D dependency graph
- Relationship type tracking (sync_api, async_event, message_queue, database, etc.)

### 💬 Message Bus Integration
- RabbitMQ-based event-driven architecture
- Topic-based event routing
- Priority message queues (low, normal, high, critical)
- Multiple exchange types (topic, direct, fanout)
- RPC support with correlation IDs
- High-level ServiceEventBus API
- Low-level MessageBus for advanced control
- Standard exchanges: ose.events, ose.tasks, ose.logs

### Real-Time Monitoring
- Live health checks for all services
- WebSocket-based real-time updates
- Service response time tracking
- Automatic reconnection on failures

### Service Discovery
- Automatic service registration
- Service-to-service communication monitoring
- Port and endpoint tracking
- Version management

### Visual Dashboard
- Beautiful web-based interface
- Color-coded service status (healthy/unhealthy/down)
- Real-time metrics and statistics
- Interactive D3.js dependency visualization
- Direct links to service API documentation

## API Endpoints

### Dashboard
- `GET /` - Web-based dashboard interface
- `GET /dependencies` - Interactive dependency graph visualization
- `GET /heartbeat-dashboard` - Real-time heartbeat monitoring dashboard
- `WS /ws/health` - WebSocket for real-time updates

### Heartbeat Monitoring (NEW v2.5.0)
- `GET /api/v1/heartbeat/status` - Get all service heartbeat statuses
- `GET /api/v1/heartbeat/status/{service_id}` - Get specific service heartbeat
- `GET /api/v1/heartbeat/summary` - Get health summary statistics
- `POST /api/v1/heartbeat/register` - Register service for monitoring

### Service Dependencies (NEW v2.5.0)
- `GET /api/v1/dependencies/graph` - Complete dependency graph
- `GET /api/v1/dependencies/service/{service_id}` - Service-specific dependencies
- `GET /api/v1/dependencies/visualize/cytoscape` - Cytoscape.js format
- `GET /api/v1/dependencies/visualize/d3` - D3.js force-directed format
- `GET /api/v1/dependencies/visualize/mermaid` - Mermaid diagram
- `GET /api/v1/dependencies/analysis/circular` - Detect circular dependencies
- `GET /api/v1/dependencies/analysis/critical-path` - Find critical path
- `GET /api/v1/dependencies/analysis/hubs` - Identify hub services

### Message Bus (NEW v2.5.0)
- `GET /api/v1/messagebus/status` - RabbitMQ connection status
- `POST /api/v1/messagebus/publish` - Publish event to message bus
- `GET /api/v1/messagebus/exchanges` - List all exchanges
- `GET /api/v1/messagebus/queues` - List all queues

### Service Management
- `GET /api/v1/services` - List all services
- `GET /api/v1/services/{service_id}/health` - Check specific service
- `GET /api/v1/health/all` - Check all services
- `GET /api/v1/metrics` - Get service mesh metrics

### Health Check
- `GET /health` - Service mesh health

## Usage

### Start Service Mesh
```bash
# With docker-compose (recommended)
docker-compose up -d service-mesh rabbitmq redis postgres

# Initialize components (one-time)
cd modules/service-mesh
python initialize.py

# Standalone
uvicorn advanced_main:app --host 0.0.0.0 --port 8000

# With Docker
docker build -t ose-service-mesh .
docker run -p 8000:8000 ose-service-mesh
```

### Access Dashboard
```bash
# Open web dashboards
http://localhost:8000                    # Main dashboard
http://localhost:8000/dependencies       # Interactive dependency graph
http://localhost:8000/heartbeat-dashboard # Real-time heartbeat monitor
http://localhost:8000/api/docs           # API documentation

# Use Terminal UI
python3 cli/ose_tui.py
# Press: 1 (Service Mesh) → hb/deps/bus

# API Examples
curl http://localhost:8000/api/v1/services
curl http://localhost:8000/api/v1/heartbeat/status
curl http://localhost:8000/api/v1/dependencies/graph
curl http://localhost:8000/api/v1/messagebus/status

# Publish test event
curl -X POST http://localhost:8000/api/v1/messagebus/publish \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "service.started",
    "source_service": "test-service",
    "payload": {"status": "ok"},
    "priority": "normal"
  }'
```

## Monitored Services

### Pre-configured Services (12 Total)

**Core Services:**
1. **Service Mesh (8000)** - Central orchestrator - 15 advanced endpoints
2. **Discovery (8001)** - System scanning - 40 endpoints
3. **Optimization (8004)** - Performance tuning - 45 endpoints

**Utility Services:**
4. **Factory Reset (8002)** - Cleanup operations - 35 endpoints
5. **Reinstallation (8003)** - Package management - 40 endpoints

**Infrastructure Services:**
6. **PostgreSQL (5432)** - Primary database
7. **Redis (6379)** - Cache and session store
8. **RabbitMQ (5672)** - Message broker

**Monitoring Services:**
9. **Metrics Collector (8006)** - Metrics collection - 40 endpoints

**Configuration Services:**
10. **Terminal Config (8005)** - Shell customization - 35 endpoints

**Additional Services:**
11. **API Gateway** - External API routing
12. **Auth Service** - Authentication/authorization

**Total: 12 services with 32 inter-service dependencies**

### Dependency Clusters
- **CORE**: service-mesh, discovery, optimization
- **UTILITY**: factory-reset, reinstallation
- **INFRASTRUCTURE**: postgres, redis, rabbitmq
- **MONITORING**: metrics-collector
- **CONFIGURATION**: terminal-config

### Critical Path
`service-mesh → discovery → postgres`

### Hub Services
- **service-mesh** (highest outbound dependencies)
- **discovery** (highest inbound dependencies)

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│              Service Mesh v2.5.0 (Port 8000)                       │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  Web UI      │  │  WebSocket   │  │  Terminal UI (TUI)     │  │
│  │  Dashboard   │  │  Server      │  │  Integration           │  │
│  └──────────────┘  └──────────────┘  └────────────────────────┘  │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │            Core Monitoring Components                       │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │  │
│  │  │ Heartbeat       │  │ Dependency      │  │ Message    │  │  │
│  │  │ Manager         │  │ Graph Engine    │  │ Bus        │  │  │
│  │  │                 │  │                 │  │ Integration│  │  │
│  │  │ • 7 services    │  │ • 12 services   │  │            │  │  │
│  │  │ • 10s intervals │  │ • 32 deps       │  │ • RabbitMQ │  │  │
│  │  │ • Health states │  │ • Cycle detect  │  │ • 3 exch.  │  │  │
│  │  │ • Latency track │  │ • Critical path │  │ • Topic    │  │  │
│  │  │ • Uptime %      │  │ • Clustering    │  │ • Priority │  │  │
│  │  └─────────────────┘  └─────────────────┘  └────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────▼────┐    ┌─────▼─────┐   ┌───▼────┐
         │RabbitMQ │    │  Redis    │   │Postgres│
         │ (5672)  │    │  (6379)   │   │ (5432) │
         └────┬────┘    └───────────┘   └────────┘
              │
    ┌─────────┼──────────┐
    │         │          │
┌───▼───┐ ┌──▼──┐   ┌───▼────┐
│Service│ │Svc 2│...│Service │
│   1   │ │     │   │   12   │
└───────┘ └─────┘   └────────┘

Event Flow (Message Bus):
  Service → ose.events (topic) → Subscribers
  Service → ose.tasks (direct) → Worker
  Service → ose.logs (fanout) → All Loggers
```

## Features Highlight

### 🫀 Heartbeat Monitoring
- **5 Health States**: Healthy, Degraded, Critical, Dead, Unknown
- **Multi-dimensional Metrics**: Latency (min/max/avg), uptime %, consecutive failures
- **Background Monitoring**: Async checks every 10 seconds
- **Configurable Thresholds**: Per-service health criteria
- **Web Dashboard**: Real-time visualization with charts
- **TUI Integration**: Terminal-based monitoring with `hb` command

### 🔗 Dependency Analysis
- **Graph-based Model**: Directed acyclic graph (DAG) with cycle detection
- **4 Dependency Types**: Hard, soft, optional, circular
- **7 Relationship Types**: sync_api, async_event, message_queue, database, cache, file_system, service_mesh
- **Critical Path Detection**: Identify longest dependency chains
- **Service Clustering**: Automatic grouping by type
- **Hub Identification**: Find services with most dependencies
- **Multiple Export Formats**: D3.js, Cytoscape, Mermaid diagrams
- **Interactive Visualization**: 3D force-directed graph with drag-and-drop
- **TUI Integration**: Terminal-based analysis with `deps` command

### 💬 Message Bus (Event-Driven Architecture)
- **RabbitMQ Integration**: Production-ready message broker
- **3 Standard Exchanges**:
  - `ose.events` (topic) - Service lifecycle events
  - `ose.tasks` (direct) - Background task queue
  - `ose.logs` (fanout) - Centralized logging
- **Priority Queues**: 4 priority levels (low, normal, high, critical)
- **Event Routing**: Topic-based patterns (e.g., `service.event_type`)
- **RPC Support**: Request/reply with correlation IDs and timeout
- **Two-Level API**:
  - `MessageBus` - Low-level control for advanced use cases
  - `ServiceEventBus` - High-level API with `@on_event()` decorator
- **TUI Integration**: Monitor and test with `bus` command

### Live Updates
- WebSocket connections for real-time status
- Auto-reconnect on connection loss
- Broadcast updates to all connected clients

### Service Registry
- Automatic service discovery
- Dynamic port allocation
- Endpoint tracking

### Metrics Collection
- Total services count
- Healthy/unhealthy service count
- Average response times
- Total endpoint tracking
- Dependency metrics (hubs, clusters, circular dependencies)

## Configuration

### Environment Variables
```bash
# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Service Mesh Configuration
SERVICE_MESH_PORT=8000
HEARTBEAT_INTERVAL=10  # seconds
HEALTH_CHECK_TIMEOUT=5 # seconds

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Service Registration

Services are registered in the `SERVICES` dictionary:

```python
SERVICES = {
    "service-id": {
        "name": "Service Name",
        "url": "http://service:port",
        "port": 8001,
        "icon": "🔍",
        "description": "Description",
        "endpoints": 40
    }
}
```

### Dependency Configuration

Define dependencies in `dependencies.py`:

```python
from dependencies import DependencyGraph, DependencyType, RelationshipType

graph = DependencyGraph()

# Add services
graph.add_service("service-mesh", "core", "8000")
graph.add_service("discovery", "core", "8001")

# Add dependencies
graph.add_dependency(
    from_service="service-mesh",
    to_service="discovery",
    dependency_type=DependencyType.HARD,
    relationship_type=RelationshipType.SYNC_API,
    weight=1.0
)
```

### Message Bus Setup

Initialize message bus in your service:

```python
from message_bus import ServiceEventBus, MessagePriority

# High-level API
event_bus = ServiceEventBus("my-service")
await event_bus.initialize()

# Register event handler
@event_bus.on_event("service.started")
async def handle_start(message):
    print(f"Service started: {message.payload}")

# Publish event
await event_bus.emit(
    event_type="my-service.ready",
    payload={"status": "ok"},
    priority=MessagePriority.NORMAL
)
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize components
python initialize.py

# Run in development mode
uvicorn advanced_main:app --reload --host 0.0.0.0 --port 8000

# Run with hot reload
./run.sh

# Access dashboards
open http://localhost:8000              # Main dashboard
open http://localhost:8000/dependencies # Dependency graph
open http://localhost:8000/api/docs     # API documentation

# Terminal UI
python3 cli/ose_tui.py
```

### Testing Advanced Features

```bash
# Test heartbeat monitoring
curl http://localhost:8000/api/v1/heartbeat/status

# Test dependency graph
curl http://localhost:8000/api/v1/dependencies/graph

# Test message bus
curl -X POST http://localhost:8000/api/v1/messagebus/publish \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test.event", "source_service": "test", "payload": {}}'

# View Mermaid diagram
curl http://localhost:8000/api/v1/dependencies/visualize/mermaid
```

## Production Deployment

```bash
# Build for production
docker build -t ose-service-mesh:2.5.0 .

# Run with resource limits
docker run -d \
  --name service-mesh \
  -p 8000:8000 \
  --memory="1024m" \
  --cpus="2.0" \
  -e RABBITMQ_HOST=rabbitmq \
  -e POSTGRES_HOST=postgres \
  -e REDIS_HOST=redis \
  ose-service-mesh:2.5.0

# Or use docker-compose
docker-compose up -d service-mesh rabbitmq redis postgres
```

## Integration

### Docker Compose

Add to your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Service Mesh with all features
  service-mesh:
    build: ./modules/service-mesh
    ports:
      - "8000:8000"
    environment:
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_PORT=5672
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - rabbitmq
      - postgres
      - redis
      - discovery
      - factory-reset
      - reinstallation
      - optimization
    networks:
      - ose-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # RabbitMQ for message bus
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest
    networks:
      - ose-network

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - ose-network

  # PostgreSQL for data persistence
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=ose
      - POSTGRES_PASSWORD=ose123
      - POSTGRES_DB=service_mesh
    networks:
      - ose-network

networks:
  ose-network:
    driver: bridge
```

### Service Integration

Add health endpoint to your services:

```python
# In your service (e.g., discovery, optimization)
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "my-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Message Bus Integration

Connect your service to the message bus:

```python
from message_bus import ServiceEventBus

# Initialize
event_bus = ServiceEventBus("my-service")
await event_bus.initialize()

# Listen for events
@event_bus.on_event("service.command")
async def handle_command(message):
    print(f"Received: {message.payload}")
    
# Publish events
await event_bus.emit(
    event_type="my-service.status",
    payload={"status": "processing"}
)
```

---

## Documentation

- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Complete API documentation and usage guide
- **[TUI_ADVANCED_REFERENCE.md](../../TUI_ADVANCED_REFERENCE.md)** - Terminal UI quick reference
- **[API Documentation](http://localhost:8000/api/docs)** - Interactive Swagger UI

## Quick Links

- 🌐 **Web Dashboard**: http://localhost:8000
- 🔗 **Dependency Graph**: http://localhost:8000/dependencies
- 🫀 **Heartbeat Monitor**: http://localhost:8000/heartbeat-dashboard
- 📚 **API Docs**: http://localhost:8000/api/docs
- 🐰 **RabbitMQ Admin**: http://localhost:15672 (guest/guest)
- 💻 **Terminal UI**: `python3 cli/ose_tui.py` → Press 1

## Version History

**v2.5.0** (Current)
- ✨ Advanced heartbeat monitoring with 5 health states
- ✨ Service dependency mapping and visualization
- ✨ RabbitMQ message bus integration
- ✨ Interactive D3.js dependency graph
- ✨ Complete TUI integration (hb, deps, bus commands)
- ✨ 15 new API endpoints
- ✨ Mermaid diagram export
- ✨ Critical path analysis
- ✨ Circular dependency detection

**v2.4.1** (Previous)
- WebSocket real-time updates
- Basic health checking
- Service discovery
- Web dashboard

---

**Access the dashboard at http://localhost:8000** 🚀

**Terminal UI**: `python3 cli/ose_tui.py` 💻
