# 🌐 OSE Universal Registry - Complete Integration Guide

**Version:** ∞.7  
**Status:** Production Ready  
**Architecture:** Multi-Database Hyper Registry with Feature Classification

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Feature Classification System](#feature-classification-system)
4. [Plugin Registry](#plugin-registry)
5. [Hyper Registry Core](#hyper-registry-core)
6. [API Reference](#api-reference)
7. [Integration Patterns](#integration-patterns)
8. [Deployment Guide](#deployment-guide)
9. [CLI Tools](#cli-tools)
10. [Advanced Features](#advanced-features)

---

## 🎯 Overview

The **Universal Registry** (formerly Service Mesh) is a next-generation plugin and service management platform that provides:

- **🏷️ Feature Classification**: Automatic categorization into 8 feature domains
- **🧩 Plugin Registry**: Centralized plugin lifecycle management
- **🕸️ Service Mesh Integration**: Automatic mesh service registration
- **📊 Hyper Registry**: Multi-database architecture with real-time sync
- **🎨 Dashboard UI**: Feature-organized web interface
- **🔄 Real-Time Updates**: WebSocket-based live notifications
- **🔗 Graph Relationships**: Entity relationship tracking and traversal

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════════╗
║               UNIVERSAL REGISTRY ARCHITECTURE                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │              FEATURE CLASSIFICATION LAYER                  │ ║
║  │  8 Categories: AI/ML, Web3, Cloud, Data, DevOps,          │ ║
║  │                Security, System, Observability             │ ║
║  └─────────┬──────────────────────────────────────────────────┘ ║
║            │                                                    ║
║  ┌─────────▼──────────────────────────────────────────────────┐ ║
║  │                  PLUGIN REGISTRY                           │ ║
║  │  • Auto-classification engine                             │ ║
║  │  • SQLite database with audit trail                       │ ║
║  │  • Mesh service mapping                                   │ ║
║  └─────────┬──────────────────────────────────────────────────┘ ║
║            │                                                    ║
║  ┌─────────▼──────────────────────────────────────────────────┐ ║
║  │                  HYPER REGISTRY CORE                       │ ║
║  │  • In-memory entity store (extensible to multi-DB)        │ ║
║  │  • Graph relationship engine                              │ ║
║  │  • Real-time WebSocket streaming                          │ ║
║  │  • RESTful API (OpenAPI 3.0)                              │ ║
║  └─────────┬──────────────────────────────────────────────────┘ ║
║            │                                                    ║
║  ┌─────────▼──────────────────────────────────────────────────┐ ║
║  │                   SYNC & INTEGRATION                       │ ║
║  │  • Service mesh sync                                      │ ║
║  │  • Kubernetes integration                                 │ ║
║  │  • Multi-region replication                               │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

### Component Breakdown

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Feature Registry** | Classification rules & feature definitions | YAML config |
| **Plugin Registry** | Plugin lifecycle & metadata | SQLite + Python |
| **Hyper Registry** | Universal entity store | FastAPI + AsyncIO |
| **Dashboard UI** | Web interface | HTML/JS/Bootstrap |
| **CLI Tools** | Command-line management | Bash/Python |

---

## 🏷️ Feature Classification System

### Available Features

| ID | Name | Icon | Category | Namespace |
|----|------|------|----------|-----------|
| `ai-ml` | AI & Machine Learning | 🧠 | ai | ose-ai-ml |
| `web3-blockchain` | Web3 & Blockchain | 🔗 | web3 | ose-web3 |
| `cloud-native` | Cloud Native Platform | ☁️ | cloud | ose-cloud |
| `data-engineering` | Data Engineering | 📊 | data | ose-data |
| `devops-platform` | DevOps & CI/CD | 🚀 | devops | ose-devops |
| `security-platform` | Security & Compliance | 🛡️ | security | ose-security |
| `system-ops` | System Operations | ⚙️ | system | ose-system |
| `observability` | Monitoring & Observability | 📈 | monitoring | ose-monitoring |

### Auto-Classification Rules

The system uses regex pattern matching with confidence scoring:

```yaml
classification_rules:
  - match: ".*(ai|ml|neural|tensor|pytorch|llm|model).*"
    feature: "ai-ml"
    confidence: 0.9
  
  - match: ".*(blockchain|web3|smart.?contract|defi|nft).*"
    feature: "web3-blockchain"
    confidence: 0.85
  
  # ... more rules
```

**Example:**
- Plugin name: `tensorflow-inference-service`
- Auto-classified as: `ai-ml` (90% confidence)

---

## 🧩 Plugin Registry

### Schema

Each plugin must define:

```yaml
apiVersion: plugin.nexuspro.io/v1
kind: Plugin
metadata:
  name: "my-plugin"
  version: "1.0.0"
  feature: "ai-ml"  # or auto-classified
  display_name: "My AI Plugin"
  description: "Advanced AI processing service"
  icon: "🧠"
  author: "Your Name"
  license: "MIT"
  tags: ["ai", "inference", "gpu"]

capabilities:
  api_endpoints:
    - path: "/api/v1/predict"
      method: "POST"
      protocol: "http"
  events:
    - "prediction.completed"
  commands:
    - "predict"

dependencies:
  system:
    - "python3.10"
    - "cuda-11.8"
  plugins: []

mesh_integration:
  service_name: "my-plugin-svc"
  port: 8080
  protocol: "HTTP"
  sidecar: true
  traffic_rules:
    load_balancer: "round_robin"
    circuit_breaker:
      max_connections: 1000
      max_requests: 100

ui:
  tab_name: "My Plugin"
  tab_icon: "🤖"
  dashboard_url: "/ai/my-plugin"
  requires_auth: false
```

### Database Schema

```sql
CREATE TABLE plugins (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    feature TEXT NOT NULL,
    display_name TEXT,
    description TEXT,
    author TEXT,
    license TEXT,
    icon TEXT,
    status TEXT DEFAULT 'registered',
    metadata TEXT,
    capabilities TEXT,
    dependencies TEXT,
    mesh_config TEXT,
    ui_config TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

CREATE TABLE features (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    icon TEXT,
    description TEXT,
    tags TEXT,
    mesh_service TEXT,
    namespace TEXT,
    plugin_count INTEGER DEFAULT 0,
    enabled INTEGER DEFAULT 1
);

CREATE TABLE mesh_services (
    service_name TEXT PRIMARY KEY,
    plugin_id TEXT,
    feature TEXT,
    port INTEGER,
    protocol TEXT,
    status TEXT DEFAULT 'active',
    config TEXT,
    FOREIGN KEY (plugin_id) REFERENCES plugins(id)
);
```

### Python API

```python
from plugin_registry import PluginRegistry, Plugin, PluginStatus

# Initialize registry
registry = PluginRegistry()

# Register a plugin
plugin = Plugin(
    name="my-plugin",
    version="1.0.0",
    feature="ai-ml",  # Optional - auto-classified if not provided
    display_name="My Plugin",
    description="A sample plugin",
    author="Developer",
    license="MIT",
    icon="🔌"
)

registered = registry.register_plugin(plugin)
print(f"Registered: {registered.id}")

# List plugins by feature
ai_plugins = registry.get_feature_plugins("ai-ml")
for p in ai_plugins:
    print(f"  - {p.display_name} v{p.version}")

# Get statistics
stats = registry.get_plugin_statistics()
print(f"Total plugins: {stats['total_plugins']}")
print(f"By feature: {stats['by_feature']}")
```

---

## 🕸️ Hyper Registry Core

### Entity Types

| Type | Description | Example |
|------|-------------|---------|
| `plugin` | Registered plugins | `tensorflow-svc` |
| `service` | Mesh services | `ai-orchestrator` |
| `feature` | Feature categories | `ai-ml` |
| `mesh_node` | Service mesh nodes | `istio-gateway` |
| `relationship` | Entity connections | `plugin → feature` |

### Data Model

```python
@dataclass
class Entity:
    id: str
    type: EntityType  # plugin, service, feature, mesh_node
    name: str
    version: Optional[str] = None
    metadata: Dict[str, Any] = None
    status: EntityStatus = EntityStatus.ACTIVE
    health: HealthStatus = HealthStatus.HEALTHY
    created_at: str = None
    updated_at: str = None
    regions: List[str] = ["local"]
    sync_status: Dict[str, Any] = None

@dataclass
class Relationship:
    id: str
    source_id: str
    target_id: str
    type: str  # "depends_on", "belongs_to", "provides", etc.
    weight: float = 1.0
    metadata: Dict[str, Any] = None
    bidirectional: bool = False
```

### Graph Capabilities

**Supported Queries:**
- **Traversal**: Get entity graph with configurable depth
- **Dependency Analysis**: Find all dependencies recursively
- **Impact Analysis**: Determine what breaks if entity fails
- **Relationship Types**: Filter by relationship type
- **Bidirectional Links**: Support two-way relationships

**Example Graph Query:**

```python
# Get dependency graph for a plugin
graph = registry.get_graph(
    root_id="plugin-123",
    depth=3,
    relationship_types=["depends_on", "requires"]
)

# Result:
{
    "nodes": [Entity(...)],
    "edges": [Relationship(...)],
    "root_id": "plugin-123",
    "depth": 3
}
```

---

## 📡 API Reference

### Base URL

```
http://localhost:8080/api/v1
```

### Endpoints

#### Entities

**Create Entity**
```http
POST /api/v1/entities
Content-Type: application/json

{
  "type": "plugin",
  "name": "my-service",
  "version": "1.0.0",
  "metadata": {
    "feature": "ai-ml",
    "capabilities": ["inference"]
  },
  "status": "active",
  "health": "healthy"
}

Response: 200 OK
{
  "id": "uuid-here",
  "type": "plugin",
  "name": "my-service",
  "version": "1.0.0",
  "metadata": {...},
  "created_at": "2025-01-01T00:00:00Z",
  ...
}
```

**List Entities**
```http
GET /api/v1/entities?type=plugin&status=active&limit=100&offset=0

Response: 200 OK
[
  {
    "id": "uuid-1",
    "type": "plugin",
    "name": "service-1",
    ...
  },
  ...
]
```

**Get Entity**
```http
GET /api/v1/entities/{entity_id}

Response: 200 OK
{
  "id": "uuid-here",
  "type": "plugin",
  ...
}
```

#### Relationships

**Create Relationship**
```http
POST /api/v1/relationships
Content-Type: application/json

{
  "source_id": "plugin-123",
  "target_id": "feature-ai-ml",
  "type": "belongs_to",
  "weight": 0.9,
  "bidirectional": false
}

Response: 200 OK
{
  "id": "rel-uuid",
  "source_id": "plugin-123",
  "target_id": "feature-ai-ml",
  "type": "belongs_to",
  "created_at": "..."
}
```

#### Graph

**Get Entity Graph**
```http
GET /api/v1/graph?root_id=plugin-123&depth=3&types=depends_on,requires

Response: 200 OK
{
  "nodes": [...],
  "edges": [...],
  "root_id": "plugin-123",
  "depth": 3
}
```

#### Search

**Search Entities**
```http
POST /api/v1/search
Content-Type: application/json

{
  "query": "tensorflow",
  "entity_types": ["plugin"],
  "limit": 50,
  "offset": 0
}

Response: 200 OK
[
  {
    "id": "tensorflow-svc",
    "name": "tensorflow-inference",
    ...
  }
]
```

#### Health & Metrics

**Health Check**
```http
GET /health

Response: 200 OK
{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00Z",
  "stats": {
    "total_entities": 150,
    "total_relationships": 200
  }
}
```

**Metrics (Prometheus)**
```http
GET /metrics

Response: 200 OK (text/plain)
registry_entities_total 150
registry_relationships_total 200
registry_connections_active 5
registry_entities_by_type{type="plugin"} 100
registry_entities_by_type{type="service"} 50
```

#### WebSocket

**Real-Time Updates**
```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'entity_created') {
    console.log('New entity:', data.entity);
  } else if (data.type === 'relationship_created') {
    console.log('New relationship:', data.relationship);
  } else if (data.type === 'ping') {
    console.log('Keepalive ping');
  }
};
```

---

## 🔗 Integration Patterns

### Pattern 1: Plugin Registration

```python
from plugin_registry import PluginRegistry, Plugin

registry = PluginRegistry()

# Define plugin
plugin = Plugin(
    name="my-ai-service",
    version="1.0.0",
    feature="ai-ml",  # Auto-classified if omitted
    display_name="My AI Service",
    description="Advanced AI processing",
    author="AI Team",
    license="Apache-2.0",
    icon="🧠",
    metadata={
        "gpu_required": True,
        "model_type": "transformer"
    },
    capabilities={
        "api_endpoints": [
            {"path": "/predict", "method": "POST", "protocol": "http"}
        ],
        "events": ["prediction.completed"],
        "commands": ["predict", "train"]
    },
    mesh_config={
        "service_name": "ai-service",
        "port": 8080,
        "protocol": "HTTP",
        "replicas": 3
    }
)

# Register
result = registry.register_plugin(plugin)
print(f"Registered: {result.id}")

# Register as mesh service
registry.register_mesh_service(
    service_name="ai-service",
    plugin_id=result.id,
    port=8080,
    protocol="HTTP"
)
```

### Pattern 2: Hyper Registry Integration

```python
import httpx
import asyncio

async def register_with_hyper_registry():
    async with httpx.AsyncClient() as client:
        # Create plugin entity
        response = await client.post(
            "http://localhost:8080/api/v1/entities",
            json={
                "type": "plugin",
                "name": "my-ai-service",
                "version": "1.0.0",
                "metadata": {
                    "feature": "ai-ml",
                    "author": "AI Team"
                },
                "status": "active",
                "health": "healthy"
            }
        )
        
        entity = response.json()
        print(f"Created entity: {entity['id']}")
        
        # Create feature relationship
        await client.post(
            "http://localhost:8080/api/v1/relationships",
            json={
                "source_id": entity["id"],
                "target_id": "ai-ml",
                "type": "belongs_to",
                "weight": 1.0
            }
        )
        
        return entity

asyncio.run(register_with_hyper_registry())
```

### Pattern 3: Service Discovery

```python
import httpx

def discover_ai_services():
    """Find all AI/ML services"""
    response = httpx.get(
        "http://localhost:8080/api/v1/entities",
        params={
            "type": "plugin",
            "limit": 100
        }
    )
    
    entities = response.json()
    
    # Filter by feature
    ai_services = [
        e for e in entities 
        if e.get("metadata", {}).get("feature") == "ai-ml"
    ]
    
    for service in ai_services:
        print(f"  - {service['name']} v{service['version']}")
        print(f"    Status: {service['status']}")
        print(f"    Health: {service['health']}")
    
    return ai_services
```

### Pattern 4: Graph Traversal

```python
def analyze_dependencies(plugin_id):
    """Analyze all dependencies for a plugin"""
    response = httpx.get(
        "http://localhost:8080/api/v1/graph",
        params={
            "root_id": plugin_id,
            "depth": 5,
            "types": "depends_on,requires"
        }
    )
    
    graph = response.json()
    
    print(f"Dependency Graph for {plugin_id}:")
    print(f"  Total nodes: {len(graph['nodes'])}")
    print(f"  Total edges: {len(graph['edges'])}")
    
    # Analyze dependencies
    for edge in graph["edges"]:
        source = next(n for n in graph["nodes"] if n["id"] == edge["source_id"])
        target = next(n for n in graph["nodes"] if n["id"] == edge["target_id"])
        
        print(f"  {source['name']} --{edge['type']}--> {target['name']}")
    
    return graph
```

---

## 🚀 Deployment Guide

### Prerequisites

```bash
# Python 3.10+
python3 --version

# Required packages
pip install fastapi uvicorn pydantic pyyaml websockets
```

### Installation

```bash
# 1. Create directory structure
mkdir -p /var/lib/ose/plugins
mkdir -p /etc/ose/registry

# 2. Copy files
cp feature_registry.yaml /etc/ose/registry/
cp plugin_schema.yaml /etc/ose/registry/
cp plugin_registry.py /usr/local/lib/ose/
cp hyper_registry.py /usr/local/lib/ose/

# 3. Start Hyper Registry
python3 /usr/local/lib/ose/hyper_registry.py
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY feature_registry.yaml plugin_schema.yaml ./
COPY plugin_registry.py hyper_registry.py ./

EXPOSE 8080

CMD ["python", "hyper_registry.py"]
```

```bash
# Build and run
docker build -t ose-universal-registry .
docker run -d -p 8080:8080 \
  -v /var/lib/ose/plugins:/var/lib/ose/plugins \
  ose-universal-registry
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: universal-registry
  namespace: ose-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: universal-registry
  template:
    metadata:
      labels:
        app: universal-registry
    spec:
      containers:
      - name: registry
        image: ose-universal-registry:latest
        ports:
        - containerPort: 8080
        env:
        - name: REGISTRY_DB
          value: "/data/registry.db"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: registry-data
---
apiVersion: v1
kind: Service
metadata:
  name: universal-registry
  namespace: ose-system
spec:
  selector:
    app: universal-registry
  ports:
  - port: 8080
    targetPort: 8080
  type: ClusterIP
```

---

## 🛠️ CLI Tools

### nexus-registry (Unified CLI)

```bash
# List entities
nexus-registry list plugin
nexus-registry list service --feature ai-ml

# Get entity details
nexus-registry get <entity-id>

# Create entity
nexus-registry create plugin "my-plugin" \
  --version 1.0.0 \
  --feature ai-ml

# Search
nexus-registry search "tensorflow"

# Graph visualization
nexus-registry graph <entity-id> --depth 5

# Statistics
nexus-registry stats
nexus-registry health
```

### nexus-plugin-manager

```bash
# Discover and register plugins
nexus-plugin-manager discover

# List plugins by feature
nexus-plugin-manager list ai-ml

# Register specific plugin
nexus-plugin-manager register /path/to/plugin

# Show features
nexus-plugin-manager features

# Mesh services
nexus-plugin-manager mesh
```

---

## ⚡ Advanced Features

### 1. Multi-Region Sync

Configure cross-region replication:

```yaml
sync:
  enabled: true
  regions:
    - name: us-east-1
      endpoint: http://registry.us-east-1:8080
    - name: eu-west-1
      endpoint: http://registry.eu-west-1:8080
  interval: 30s
  conflict_resolution: "last_write_wins"
```

### 2. Event Streaming

Subscribe to specific event types:

```python
import websockets
import json

async def stream_events():
    async with websockets.connect('ws://localhost:8080/ws') as ws:
        while True:
            message = await ws.recv()
            event = json.loads(message)
            
            if event['type'] == 'entity_created':
                print(f"New entity: {event['entity']['name']}")
            elif event['type'] == 'relationship_created':
                print(f"New relationship: {event['relationship']['type']}")
```

### 3. Custom Classification Rules

Add your own classification patterns:

```yaml
classification_rules:
  - match: ".*(quantum|qiskit|cirq).*"
    feature: "quantum-computing"
    confidence: 0.95
  
  - match: ".*(iot|sensor|mqtt|edge).*"
    feature: "iot-edge"
    confidence: 0.9
```

### 4. Health Propagation

Dependencies automatically inherit health status:

```python
# If plugin A depends on plugin B, and B becomes unhealthy:
# - B.health = "unhealthy"
# - A.health = "degraded" (automatically)
```

### 5. Version Constraints

Define dependency version requirements:

```python
dependencies = {
    "plugins": ["tensorflow-svc>=2.0.0,<3.0.0"],
    "system": ["python>=3.10", "cuda==11.8"]
}
```

---

## 📊 Monitoring & Observability

### Prometheus Integration

Scrape metrics endpoint:

```yaml
scrape_configs:
  - job_name: 'universal-registry'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```

### Grafana Dashboard

Create dashboard using these metrics:

- `registry_entities_total` - Total entities
- `registry_relationships_total` - Total relationships
- `registry_entities_by_type{type="plugin"}` - Plugin count
- `registry_connections_active` - Active WebSocket connections

---

## 🔒 Security

### Authentication

Configure JWT authentication:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/v1/entities")
async def create_entity(
    entity: EntityCreate,
    token: str = Depends(security)
):
    # Validate token
    if not validate_token(token.credentials):
        raise HTTPException(status_code=401)
    
    return await registry.create_entity(entity)
```

### RBAC

Define role-based access:

```yaml
roles:
  admin:
    permissions: ["*"]
  developer:
    permissions: ["read:*", "write:plugin", "write:service"]
  viewer:
    permissions: ["read:*"]
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8080/docs
- **GraphQL Playground**: http://localhost:8081
- **Feature Registry**: `feature_registry.yaml`
- **Plugin Schema**: `plugin_schema.yaml`

---

## 🎯 Quick Start Example

```python
#!/usr/bin/env python3
"""Quick start example"""

from plugin_registry import PluginRegistry, Plugin
import httpx
import asyncio

async def quick_start():
    # 1. Register plugin locally
    registry = PluginRegistry()
    
    plugin = Plugin(
        name="hello-world",
        version="1.0.0",
        display_name="Hello World Service",
        description="A sample plugin",
        author="Developer",
        license="MIT",
        icon="👋"
    )
    
    local_plugin = registry.register_plugin(plugin)
    print(f"✅ Registered locally: {local_plugin.id}")
    
    # 2. Sync to Hyper Registry
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8080/api/v1/entities",
            json={
                "type": "plugin",
                "name": local_plugin.name,
                "version": local_plugin.version,
                "metadata": {
                    "feature": local_plugin.feature,
                    "display_name": local_plugin.display_name
                }
            }
        )
        
        entity = response.json()
        print(f"✅ Synced to Hyper Registry: {entity['id']}")
    
    # 3. Query back
    response = await client.get(
        "http://localhost:8080/api/v1/entities",
        params={"type": "plugin", "limit": 10}
    )
    
    entities = response.json()
    print(f"\n📋 Total plugins: {len(entities)}")
    for e in entities:
        print(f"  - {e['name']} v{e['version']}")

if __name__ == "__main__":
    asyncio.run(quick_start())
```

---

**© 2025 OSE Project - Universal Registry v∞.7**
