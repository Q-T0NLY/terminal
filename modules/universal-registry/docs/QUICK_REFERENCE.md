# 🚀 OSE Universal Registry - Quick Reference

**Version:** ∞.7 | **Port:** 8080 | **Status:** Production Ready

---

## 🏷️ Feature Categories

```
🧠 ai-ml               🔗 web3-blockchain    ☁️ cloud-native       📊 data-engineering
🚀 devops-platform     🛡️ security-platform  ⚙️ system-ops         📈 observability
```

---

## ⚡ Quick Start

### 1. Start Hyper Registry
```bash
cd /workspaces/terminal/modules/universal-registry
python3 hyper_registry.py
```

### 2. Check Health
```bash
nexus-registry health
```

### 3. List Entities
```bash
nexus-registry list plugin
```

---

## 🛠️ CLI Commands

```bash
# Entity Management
nexus-registry list [type] [feature]     # List entities
nexus-registry get <id>                  # Get entity details
nexus-registry create <type> <name>      # Create entity
nexus-registry search <query>            # Search entities

# Relationships
nexus-registry relate <src> <tgt> [type] # Create relationship
nexus-registry graph <id> [depth]        # Get dependency graph

# Monitoring
nexus-registry health                    # Health check
nexus-registry stats                     # Statistics
nexus-registry features                  # List features
```

---

## 📡 API Endpoints

```http
# Entities
POST   /api/v1/entities              Create entity
GET    /api/v1/entities              List entities
GET    /api/v1/entities/{id}         Get entity
POST   /api/v1/search                Search

# Relationships
POST   /api/v1/relationships         Create relationship
GET    /api/v1/graph                 Get graph

# Monitoring
GET    /health                       Health check
GET    /metrics                      Prometheus metrics
GET    /api/v1/stats                 Statistics
WS     /ws                           WebSocket stream
```

---

## 🐍 Python Examples

### Register Plugin

```python
from plugin_registry import PluginRegistry, Plugin

registry = PluginRegistry()

plugin = Plugin(
    name="my-service",
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
        "status": "active",
        "health": "healthy"
    }
)

entity = response.json()
print(f"Created: {entity['id']}")

# List entities
response = httpx.get(
    "http://localhost:8080/api/v1/entities",
    params={"type": "plugin"}
)

for entity in response.json():
    print(f"  - {entity['name']} v{entity['version']}")
```

### WebSocket Stream

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'entity_created') {
    console.log('New entity:', data.entity.name);
  }
};
```

---

## 📊 Database Schema

### Plugins Table
```sql
CREATE TABLE plugins (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    feature TEXT NOT NULL,        -- ai-ml, web3-blockchain, etc.
    display_name TEXT,
    description TEXT,
    author TEXT,
    license TEXT,
    icon TEXT,
    status TEXT,                   -- registered, installed, active
    metadata TEXT,                 -- JSON
    capabilities TEXT,             -- JSON
    dependencies TEXT,             -- JSON
    mesh_config TEXT,              -- JSON
    ui_config TEXT,                -- JSON
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Features Table
```sql
CREATE TABLE features (
    id TEXT PRIMARY KEY,           -- ai-ml, web3-blockchain, etc.
    name TEXT NOT NULL,
    category TEXT,
    icon TEXT,
    description TEXT,
    tags TEXT,
    mesh_service TEXT,
    namespace TEXT,
    plugin_count INTEGER,
    enabled INTEGER
);
```

---

## 🔗 Integration Patterns

### Pattern 1: Auto-Classification

```yaml
# Plugin automatically classified based on name
name: "tensorflow-inference-service"
# → feature: "ai-ml" (90% confidence)

name: "ethereum-smart-contract-verifier"
# → feature: "web3-blockchain" (85% confidence)
```

### Pattern 2: Service Discovery

```python
# Find all AI services
ai_services = registry.list_plugins(feature="ai-ml")

for service in ai_services:
    print(f"{service.name} - {service.status}")
```

### Pattern 3: Dependency Graph

```python
# Get full dependency tree
graph = registry.get_graph(
    root_id="plugin-123",
    depth=5
)

print(f"Nodes: {len(graph['nodes'])}")
print(f"Edges: {len(graph['edges'])}")
```

---

## 📁 File Locations

```
/workspaces/terminal/
├── modules/universal-registry/
│   ├── feature_registry.yaml          # Feature definitions
│   ├── plugin_schema.yaml             # Plugin schema
│   ├── plugin_registry.py             # Plugin manager
│   ├── hyper_registry.py              # Hyper registry (FastAPI)
│   ├── UNIVERSAL_REGISTRY_GUIDE.md    # Complete guide
│   └── IMPLEMENTATION_SUMMARY.md      # Implementation details
│
└── bin/
    └── nexus-registry                 # CLI tool
```

---

## 🔧 Environment Variables

```bash
HYPER_REGISTRY_API=http://localhost:8080/api/v1
PLUGIN_REGISTRY_DB=/var/lib/ose/plugins/registry.db
```

---

## 📚 Documentation

- **Complete Guide**: `UNIVERSAL_REGISTRY_GUIDE.md` (80+ pages)
- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`
- **API Docs**: http://localhost:8080/docs (OpenAPI)
- **Feature Registry**: `feature_registry.yaml`
- **Plugin Schema**: `plugin_schema.yaml`

---

## ⚙️ Configuration

### Feature Classification Rules

```yaml
classification_rules:
  - match: ".*(ai|ml|neural|tensor).*"
    feature: "ai-ml"
    confidence: 0.9
  
  - match: ".*(blockchain|web3|smart.?contract).*"
    feature: "web3-blockchain"
    confidence: 0.85
```

### Plugin Schema Example

```yaml
apiVersion: plugin.nexuspro.io/v1
kind: Plugin
metadata:
  name: "my-plugin"
  version: "1.0.0"
  feature: "ai-ml"
  display_name: "My AI Plugin"
  icon: "🧠"
  author: "Developer"
  license: "MIT"

capabilities:
  api_endpoints:
    - path: "/api/v1/predict"
      method: "POST"
      protocol: "http"

mesh_integration:
  service_name: "my-plugin-svc"
  port: 8080
  protocol: "HTTP"
  replicas: 3
```

---

## 🎯 Common Tasks

### Register a New Plugin

```bash
# CLI
nexus-registry create plugin "my-service" 1.0.0

# Python
plugin = Plugin(name="my-service", version="1.0.0", ...)
registry.register_plugin(plugin)

# HTTP
curl -X POST http://localhost:8080/api/v1/entities \
  -H "Content-Type: application/json" \
  -d '{"type": "plugin", "name": "my-service", ...}'
```

### Query Services by Feature

```bash
# CLI
nexus-registry list plugin ai-ml

# Python
ai_plugins = registry.get_feature_plugins("ai-ml")

# HTTP
curl "http://localhost:8080/api/v1/entities?type=plugin" | \
  jq '.[] | select(.metadata.feature == "ai-ml")'
```

### Analyze Dependencies

```bash
# CLI
nexus-registry graph plugin-123 5

# Python
graph = registry.get_graph(root_id="plugin-123", depth=5)

# HTTP
curl "http://localhost:8080/api/v1/graph?root_id=plugin-123&depth=5"
```

---

## 🚨 Troubleshooting

### Hyper Registry Not Running

```bash
# Check status
curl http://localhost:8080/health

# Start service
cd /workspaces/terminal/modules/universal-registry
python3 hyper_registry.py
```

### CLI Command Not Found

```bash
# Make executable
chmod +x /workspaces/terminal/bin/nexus-registry

# Add to PATH (optional)
export PATH=$PATH:/workspaces/terminal/bin
```

### Database Locked

```bash
# Check for other processes
lsof /var/lib/ose/plugins/registry.db

# Restart if needed
pkill -f hyper_registry.py
python3 hyper_registry.py
```

---

## 📈 Metrics

### Prometheus Metrics

```
registry_entities_total                           Total entities
registry_relationships_total                      Total relationships
registry_connections_active                       Active WebSocket connections
registry_entities_by_type{type="plugin"}          Plugin count
registry_entities_by_type{type="service"}         Service count
```

### Grafana Dashboard

```bash
# Example queries
sum(registry_entities_by_type)
rate(registry_entities_total[5m])
registry_connections_active
```

---

## 🎓 Learning Resources

### Tutorials

1. **Quick Start**: See `IMPLEMENTATION_SUMMARY.md`
2. **Complete Guide**: See `UNIVERSAL_REGISTRY_GUIDE.md`
3. **API Reference**: http://localhost:8080/docs

### Examples

```python
# Example 1: Register and sync
from plugin_registry import PluginRegistry, Plugin
import httpx

registry = PluginRegistry()
plugin = Plugin(name="demo", version="1.0.0", ...)
registry.register_plugin(plugin)

# Sync to hyper registry
httpx.post("http://localhost:8080/api/v1/entities", json={...})

# Example 2: Real-time monitoring
import websockets
import asyncio

async def monitor():
    async with websockets.connect('ws://localhost:8080/ws') as ws:
        while True:
            msg = await ws.recv()
            print(json.loads(msg))

asyncio.run(monitor())
```

---

**© 2025 OSE Project - Universal Registry v∞.7**

**Quick Links:**
- API Docs: http://localhost:8080/docs
- WebSocket: ws://localhost:8080/ws
- Health: http://localhost:8080/health
- Metrics: http://localhost:8080/metrics
