# 🚀 OSE Universal Registry

**Version:** ∞.7 | **Status:** Production Ready

The Universal Registry is a comprehensive platform for managing plugins, services, and microservices mesh with dynamic feature classification, real-time synchronization, and graph-based relationship tracking.

---

## 📁 Directory Structure

```
universal-registry/
├── hyper_registry.py              # 🎯 Main entrypoint - FastAPI server
├── README.md                       # 📖 This file
│
├── core/                           # ⚙️ Core operational files
│   ├── feature_registry.yaml      # Feature classification config
│   ├── requirements.txt           # Python dependencies
│   ├── initialize.py              # Database initialization
│   ├── Dockerfile                 # Container image
│   ├── run.sh                     # Startup script
│   ├── static/                    # Web UI assets
│   ├── templates/                 # HTML templates
│   └── features/                  # Feature-specific configs
│
├── plugins/                        # 🔌 Plugin system
│   ├── plugin_registry.py         # Plugin lifecycle management
│   └── plugin_schema.yaml         # Plugin metadata schema
│
├── microservices/                  # 🌐 Microservices mesh
│   ├── main.py                    # Original service mesh dashboard
│   ├── advanced_main.py           # Extended features
│   ├── heartbeat.py               # Health monitoring
│   ├── dependencies.py            # Dependency tracking
│   ├── message_bus.py             # Event bus integration
│   └── MICROSERVICES_README.md    # Microservices documentation
│
└── docs/                           # 📚 Documentation
    ├── UNIVERSAL_REGISTRY_GUIDE.md    # Complete guide (80+ pages)
    ├── IMPLEMENTATION_SUMMARY.md      # Implementation details
    ├── QUICK_REFERENCE.md             # CLI cheat sheet
    └── ADVANCED_README.md             # Advanced features
```

---

## 🚀 Quick Start

### 1. Start the Registry

```bash
cd /workspaces/terminal/modules/universal-registry
python3 hyper_registry.py
```

The server will start on **http://0.0.0.0:8080**

### 2. Check Health

```bash
nexus-registry health
# OR
curl http://localhost:8080/health
```

### 3. Explore API

Open in browser:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Metrics**: http://localhost:8080/metrics

---

## 🏷️ Feature Categories

The registry organizes all entities into 8 feature categories:

| Icon | Feature | Description |
|------|---------|-------------|
| 🧠 | `ai-ml` | AI & Machine Learning |
| 🔗 | `web3-blockchain` | Web3 & Blockchain |
| ☁️ | `cloud-native` | Cloud Native Platform |
| 📊 | `data-engineering` | Data Engineering |
| 🚀 | `devops-platform` | DevOps & CI/CD |
| 🛡️ | `security-platform` | Security & Compliance |
| ⚙️ | `system-ops` | System Operations |
| 📈 | `observability` | Monitoring & Observability |

---

## 📡 API Endpoints

### Entity Management
```http
POST   /api/v1/entities              # Create entity
GET    /api/v1/entities              # List entities
GET    /api/v1/entities/{id}         # Get entity by ID
POST   /api/v1/search                # Search entities
```

### Relationships
```http
POST   /api/v1/relationships         # Create relationship
GET    /api/v1/graph                 # Get dependency graph
```

### Monitoring
```http
GET    /health                       # Health check
GET    /metrics                      # Prometheus metrics
GET    /api/v1/stats                 # Statistics
WS     /ws                           # WebSocket stream
```

---

## 🛠️ CLI Usage

The `nexus-registry` CLI provides unified management:

```bash
# List entities
nexus-registry list [type] [feature]

# Create entity
nexus-registry create plugin "my-service" 1.0.0

# Search
nexus-registry search "tensorflow"

# Get dependency graph
nexus-registry graph <entity-id> 5

# Health & stats
nexus-registry health
nexus-registry stats
nexus-registry features
```

---

## 🐍 Python API

### Register a Plugin

```python
import sys
sys.path.insert(0, '/workspaces/terminal/modules/universal-registry/plugins')

from plugin_registry import PluginRegistry, Plugin

registry = PluginRegistry()

plugin = Plugin(
    name="my-ai-service",
    version="1.0.0",
    feature="ai-ml",
    display_name="My AI Service",
    description="AI processing service",
    author="Developer",
    license="MIT",
    icon="🧠"
)

result = registry.register_plugin(plugin)
print(f"Registered: {result.id}")
```

### Query Hyper Registry

```python
import httpx

# Create entity
response = httpx.post(
    "http://localhost:8080/api/v1/entities",
    json={
        "type": "plugin",
        "name": "my-service",
        "version": "1.0.0",
        "metadata": {"feature": "ai-ml"},
        "status": "active"
    }
)

# List all plugins
response = httpx.get(
    "http://localhost:8080/api/v1/entities",
    params={"type": "plugin"}
)

for entity in response.json():
    print(f"  - {entity['name']} v{entity['version']}")
```

---

## 🔧 Configuration

### Environment Variables

```bash
export HYPER_REGISTRY_API=http://localhost:8080/api/v1
export PLUGIN_REGISTRY_DB=/var/lib/ose/plugins/registry.db
```

### Feature Classification

Features are auto-classified based on name patterns (see `core/feature_registry.yaml`):

```yaml
classification_rules:
  - match: ".*(ai|ml|neural|tensor).*"
    feature: "ai-ml"
    confidence: 0.9
  
  - match: ".*(blockchain|web3|smart.?contract).*"
    feature: "web3-blockchain"
    confidence: 0.85
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Hyper Registry (FastAPI)               │
│  - Entity Management      - Real-time WebSocket         │
│  - Graph Traversal        - Prometheus Metrics          │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼──────┐    ┌────────▼────────┐
│   Plugin     │    │   Microservices │
│   Registry   │    │      Mesh       │
│  (SQLite)    │    │  (Service Mesh) │
└──────────────┘    └─────────────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Feature Categories │
        │    (8 domains)      │
        └─────────────────────┘
```

---

## 📚 Documentation

- **[Complete Guide](docs/UNIVERSAL_REGISTRY_GUIDE.md)** - 80+ page comprehensive guide
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Technical details & migration guide
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - CLI cheat sheet
- **[Advanced Features](docs/ADVANCED_README.md)** - Extended capabilities
- **[Microservices Mesh](microservices/MICROSERVICES_README.md)** - Service mesh documentation

---

## 🎯 Key Features

✅ **Dynamic Feature Classification** - Auto-classify plugins into 8 categories  
✅ **Plugin Lifecycle Management** - Track status from registration to deprecation  
✅ **Graph Relationships** - Model dependencies and relationships  
✅ **Real-time Updates** - WebSocket streaming for live events  
✅ **Multi-Database Ready** - Extensible to CockroachDB, Neo4j, Elasticsearch  
✅ **REST API** - Full CRUD with OpenAPI documentation  
✅ **CLI Tools** - Unified command-line interface  
✅ **Prometheus Metrics** - Production-ready monitoring  
✅ **Service Mesh Integration** - Auto-registration with Istio  

---

## 🔐 Security

- Environment-based configuration
- API authentication ready (add middleware)
- RBAC support (implement in middleware)
- Audit trail in plugin_events table

---

## 🚢 Deployment

### Local Development
```bash
python3 hyper_registry.py
```

### Docker
```bash
cd core/
docker build -t ose-universal-registry:latest .
docker run -p 8080:8080 ose-universal-registry:latest
```

### Kubernetes
See `docs/UNIVERSAL_REGISTRY_GUIDE.md` for K8s manifests

---

## 📈 Monitoring

### Prometheus Metrics

```
registry_entities_total                      # Total entities
registry_relationships_total                 # Total relationships  
registry_connections_active                  # WebSocket connections
registry_entities_by_type{type="plugin"}     # By entity type
```

### Grafana Dashboard

Import dashboards from `docs/UNIVERSAL_REGISTRY_GUIDE.md`

---

## 🔄 Components

### 🎯 Hyper Registry (Entrypoint)
**File**: `hyper_registry.py`  
**Purpose**: Main FastAPI server providing REST API and WebSocket streaming

### ⚙️ Core
**Folder**: `core/`  
**Purpose**: Configuration files, features, templates, and operational scripts

### 🔌 Plugins
**Folder**: `plugins/`  
**Purpose**: Plugin registry system with SQLite backend and schema validation

### 🌐 Microservices
**Folder**: `microservices/`  
**Purpose**: Original service mesh components (heartbeat, dependencies, message bus)

### 📚 Documentation
**Folder**: `docs/`  
**Purpose**: Comprehensive guides, references, and implementation details

---

## 🤝 Contributing

This is part of the OSE (Operating System Enhancement) project.

---

## 📝 License

MIT License - See LICENSE file

---

## 🆘 Support

- **Documentation**: `docs/` folder
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

---

**© 2025 OSE Project - Universal Registry v∞.7**
