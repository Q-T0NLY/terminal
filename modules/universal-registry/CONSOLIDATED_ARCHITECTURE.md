# Universal Registry - Consolidated Architecture

## 🎯 Architecture Overview

The platform is now fully consolidated into a **unified, non-redundant architecture** with clear separation of concerns.

---

## 📁 Consolidated Structure

```
/workspaces/terminal/
│
├── bin/
│   ├── ose-cli                      ← ✅ MAIN TUI CLI (ALL system features)
│   └── universal-registry-cli        ← ✅ REGISTRY CLI (plugins/services only)
│
└── modules/universal-registry/
    ├── hyper_registry.py              ← ✅ Main API Gateway
    │
    ├── core/
    │   ├── gateway/
    │   │   └── api_gateway.py         ← ✅ Unified Gateway + Key Rotation
    │   │
    │   ├── api/
    │   │   ├── metrics_routes.py      ← ✅ ALL metrics & monitoring
    │   │   ├── plugins_routes.py      ← ✅ Plugin management
    │   │   └── microservices_routes.py← ✅ Service management
    │   │
    │   ├── advanced/
    │   │   ├── semantic_search.py     ← Search engine
    │   │   └── stream_propagation.py  ← Event streams
    │   │
    │   └── integrations/
    │       └── webhooks.py            ← Webhook system
    │
    └── plugins/
        └── plugin_registry.py         ← Plugin database
```

---

## 🔑 Key Consolidations

### 1. **API Gateway** (NEW)
**File**: `core/gateway/api_gateway.py`

**Features**:
- ✅ Unified authentication for ALL routes
- ✅ API key management with rotation
- ✅ JWT token support
- ✅ Permission-based access control
- ✅ Rate limiting
- ✅ Key expiration & grace periods
- ✅ Usage statistics

**Key Types**:
- `api_key` - Standard API keys
- `jwt_token` - JWT tokens
- `service_key` - Service-to-service auth
- `admin_key` - Admin access

**Permissions**:
- Read: `read:plugins`, `read:services`, `read:metrics`, `read:streams`
- Write: `write:plugins`, `write:services`, `write:config`
- Admin: `admin:keys`, `admin:users`, `admin:system`

### 2. **Metrics System** (Already exists - Enhanced)
**File**: `core/api/metrics_routes.py`

**Consolidates ALL metrics**:
- ✅ System metrics (CPU, memory, disk, network)
- ✅ Plugin metrics
- ✅ Service metrics
- ✅ Registry metrics
- ✅ Performance metrics
- ✅ Alert system
- ✅ Real-time monitoring

### 3. **CLI Consolidation**

#### `ose-cli` - Main Interactive TUI
**Purpose**: Complete system management

**Features**:
- Interactive TUI menu
- All system features
- Docker service management
- Configuration management
- Metrics & monitoring
- System health checks
- Service discovery
- Logs & diagnostics

**Usage**:
```bash
ose-cli          # Launch interactive menu
```

#### `universal-registry-cli` - Registry Management
**Purpose**: Registry, plugins, service mesh only

**Features**:
- Plugin lifecycle (register, install, activate, deactivate, uninstall)
- Service mesh management
- Microservices control
- Code injection & monitoring
- Event streams
- Webhooks

**Usage**:
```bash
universal-registry-cli plugin list
universal-registry-cli service start my-service
universal-registry-cli stream subscribe
```

---

## 🌐 API Routes Organization

### Gateway Routes (`/api/v1/gateway`)
```
POST   /gateway/keys              - Create API key
GET    /gateway/keys              - List API keys
GET    /gateway/keys/{id}         - Get key details
POST   /gateway/keys/{id}/rotate  - Rotate key
DELETE /gateway/keys/{id}         - Revoke key
POST   /gateway/tokens            - Create JWT token
GET    /gateway/stats             - Gateway statistics
GET    /gateway/permissions       - List permissions
```

### Plugin Routes (`/api/v1/plugins`)
```
GET    /plugins/                  - List plugins
POST   /plugins/register          - Register plugin
GET    /plugins/{id}              - Get plugin
POST   /plugins/{id}/install      - Install plugin
POST   /plugins/{id}/activate     - Activate plugin
POST   /plugins/{id}/deactivate   - Deactivate plugin
DELETE /plugins/{id}              - Uninstall plugin
PUT    /plugins/{id}              - Update plugin
GET    /plugins/{id}/health       - Plugin health
GET    /plugins/{id}/logs         - Plugin logs
GET    /plugins/{id}/config       - Get config
PUT    /plugins/{id}/config       - Update config
GET    /plugins/{id}/dependencies - Dependencies
GET    /plugins/stats/overview    - Statistics
```

### Service Routes (`/api/v1/services`)
```
GET    /services                  - List services
POST   /services/register         - Register service
POST   /services/{id}/start       - Start service
POST   /services/{id}/stop        - Stop service
POST   /services/{id}/restart     - Restart service
GET    /services/{id}/logs        - Service logs
GET    /services/{id}/health      - Service health
```

### Metrics Routes (`/api/v1/metrics`)
```
GET    /metrics/system            - System metrics
GET    /metrics/system/processes  - Top processes
GET    /metrics/plugins           - Plugin metrics
GET    /metrics/services          - Service metrics
GET    /metrics/registry          - Registry metrics
GET    /metrics/performance       - Performance metrics
GET    /metrics/alerts            - Active alerts
POST   /metrics/alerts/configure  - Configure alerts
GET    /metrics/history           - Historical data
POST   /metrics/export            - Export metrics
GET    /metrics/dashboard         - Dashboard data
```

### Stream Routes (`/api/v1/streams`)
```
GET    /streams/stats             - Stream statistics
GET    /streams/subscribe         - Subscribe (SSE)
POST   /streams/publish           - Publish event
```

### Webhook Routes (`/api/v1/webhooks`)
```
GET    /webhooks                  - List webhooks
POST   /webhooks                  - Register webhook
DELETE /webhooks/{id}             - Delete webhook
POST   /webhooks/{id}/test        - Test webhook
```

---

## 🔐 Authentication Flow

### 1. Get Admin Key (First time)
```bash
# Start registry - admin key shown in logs
python3 hyper_registry.py
# Save the admin key shown at startup
```

### 2. Create API Keys
```bash
curl -X POST http://localhost:8080/api/v1/gateway/keys \
  -H "X-API-Key: admin_xxxx..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Application",
    "key_type": "api_key",
    "permissions": ["read:plugins", "write:plugins"],
    "expires_in_days": 90,
    "rate_limit": 1000
  }'
```

### 3. Use API Key
```bash
curl http://localhost:8080/api/v1/plugins/ \
  -H "X-API-Key: ureg_xxxx..."
```

### 4. Or Use JWT Token
```bash
# Get token
curl -X POST http://localhost:8080/api/v1/gateway/tokens \
  -H "X-API-Key: admin_xxxx..." \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "user@example.com",
    "permissions": ["read:plugins", "read:services"],
    "expires_in_minutes": 60
  }'

# Use token
curl http://localhost:8080/api/v1/plugins/ \
  -H "Authorization: Bearer eyJhbGc..."
```

---

## 📊 Metrics Collection

### System Metrics
```python
# Collected automatically every 5 seconds
- CPU usage (total, per core)
- Memory (used, available, cached)
- Disk (usage, I/O)
- Network (bytes sent/received)
- Load average
```

### Plugin Metrics
```python
- Total plugins
- By status (active, installed, failed)
- By feature category
- Installation times
- Activation times
- Error rates
```

### Service Metrics
```python
- Total services
- Active/inactive count
- Request rates
- Response times
- Error rates
- Uptime
```

### Performance Metrics
```python
- Request latency (p50, p95, p99)
- Throughput (requests/sec)
- Error rate
- Cache hit rate
- Database query times
```

---

## 🚨 Alert System

### Alert Types
- `WARNING` - Attention needed
- `CRITICAL` - Immediate action required
- `INFO` - Informational

### Alert Triggers
```python
# CPU
WARNING: > 75%
CRITICAL: > 90%

# Memory
WARNING: > 75%
CRITICAL: > 90%

# Disk
WARNING: > 80%
CRITICAL: > 90%

# Error Rate
WARNING: > 5%
CRITICAL: > 10%

# Latency
WARNING: > 500ms
CRITICAL: > 1000ms
```

---

## 🎯 Usage Examples

### Example 1: Full System Setup

```bash
# 1. Start registry
python3 modules/universal-registry/hyper_registry.py

# 2. Launch interactive TUI
ose-cli

# 3. Or use registry CLI directly
universal-registry-cli plugin list
```

### Example 2: API with Authentication

```bash
# Create admin API key for automation
curl -X POST http://localhost:8080/api/v1/gateway/keys \
  -H "X-API-Key: $ADMIN_KEY" \
  -d '{
    "name": "Automation Bot",
    "key_type": "service_key",
    "permissions": ["read:plugins", "write:services", "read:metrics"]
  }'

# Use service key
export SERVICE_KEY="svc_xxxx..."

# List plugins
curl http://localhost:8080/api/v1/plugins/ \
  -H "X-API-Key: $SERVICE_KEY"

# Get metrics
curl http://localhost:8080/api/v1/metrics/system \
  -H "X-API-Key: $SERVICE_KEY"
```

### Example 3: Key Rotation

```bash
# Rotate key with 24h grace period
curl -X POST http://localhost:8080/api/v1/gateway/keys/key_abc123/rotate \
  -H "X-API-Key: $ADMIN_KEY" \
  -d '{"key_id": "key_abc123", "grace_period_hours": 24}'

# Response includes new key
# {
#   "new_key_id": "key_def456",
#   "new_api_key": "ureg_new_key...",
#   "grace_period_end": "2025-12-15T12:00:00"
# }

# Old key works for 24 hours
# Update apps to use new key before grace period ends
```

---

## 🔄 Migration from Old Structure

### CLI Migration

**Before**:
```bash
microservices-cli services list
universal-registry-cli plugin list
ose_tui.py  # Separate TUI
```

**After**:
```bash
ose-cli                              # All system features (interactive)
universal-registry-cli plugin list   # Registry/plugins only
universal-registry-cli service list  # Services via registry
```

### API Migration

**Before**:
```bash
# No unified auth
curl http://localhost:8080/api/v1/plugins/
curl http://localhost:8080/api/v1/services/
curl http://localhost:8080/api/v1/metrics/system
```

**After**:
```bash
# All routes require authentication
curl http://localhost:8080/api/v1/plugins/ \
  -H "X-API-Key: ureg_xxxx..."

curl http://localhost:8080/api/v1/metrics/system \
  -H "X-API-Key: ureg_xxxx..."
```

---

## 📚 Documentation

1. **[PLATFORM_COMPLETE.md](PLATFORM_COMPLETE.md)** - Quick start guide
2. **[UNIFIED_CONTROL.md](UNIFIED_CONTROL.md)** - Complete API reference
3. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details
4. **[CONSOLIDATED_ARCHITECTURE.md](CONSOLIDATED_ARCHITECTURE.md)** - This document

---

## ✅ Summary

### What Was Consolidated

✅ **API Gateway**: One unified gateway with key rotation  
✅ **Metrics**: All metrics in `metrics_routes.py`  
✅ **CLIs**: Two focused tools instead of many fragmented ones  
✅ **Authentication**: Unified auth for all routes  
✅ **Monitoring**: Centralized metrics collection  

### What Was Removed

❌ Multiple redundant CLI tools  
❌ Fragmented authentication  
❌ Duplicate metrics collection  
❌ Scattered route files  

### Core Principles

1. **ONE Gateway** - All routes through unified gateway
2. **ONE Auth System** - Consistent authentication everywhere
3. **ONE Metrics System** - Centralized monitoring
4. **TWO CLIs** - Clear separation: system vs registry
5. **ZERO Redundancy** - Each component has one purpose

---

**Universal Registry v∞.9 - Fully Consolidated Architecture** ✅
