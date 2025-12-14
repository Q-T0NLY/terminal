# 🚀 Universal Registry - START HERE

## Your Platform is Ready!

The Universal Registry has been **completely consolidated** into a unified, enterprise-grade architecture.

---

## ✅ What You Have Now

### 1. **API Gateway with Key Rotation** 
[core/gateway/api_gateway.py](core/gateway/api_gateway.py)

### 2. **Three Management CLIs**
- **[universal-registry-cli](../../bin/universal-registry-cli)** - 🆕 Complete CRUD operations (80+ commands) ⭐
- **[ose-cli](../../bin/ose-cli)** - Interactive TUI for all system features
- **[microservices-cli](../../bin/microservices-cli)** - Microservices mesh management

### 3. **Unified Metrics System**
[core/api/metrics_routes.py](core/api/metrics_routes.py)

---

## 🎯 Quick Start (3 Steps)

### Step 1: Start the Registry
```bash
cd /workspaces/terminal/modules/universal-registry
python3 hyper_registry.py
```

**Expected output**:
```
🔐 Initial admin API key generated: ureg_admin_xxxxxxxx
📊 Metrics API: http://localhost:8080/api/v1/metrics/
🔑 Gateway API: http://localhost:8080/api/v1/gateway/
```

⚠️ **SAVE THE ADMIN KEY** - you'll need it!

---

### Step 2: Launch Interactive TUI
```bash
ose-cli
```

**You'll see**:
```
╔══════════════════════════════════════╗
║  Universal Hyper Registry - OSE      ║
║  v∞.9 - Enterprise Edition           ║
╚══════════════════════════════════════╝

Main Menu:
  1. System Status & Health
  2. Universal Registry Management
  3. Plugin Management
  4. Microservices Management
  5. Metrics & Monitoring
  6. Service Mesh Configuration
  7. Event Streams
  8. Webhooks
  9. Search & Discovery
  10. System Configuration
  11. Docker Services
  12. Logs & Diagnostics
```

---

### Step 3: Use the Management CLI

**Enhanced: `universal-registry-cli` - Complete CRUD Operations CLI** ⭐

```bash
# Full CRUD operations (80+ commands)
universal-registry-cli plugin add              # Add new plugin
universal-registry-cli plugin install <id>     # Install plugin
universal-registry-cli plugin enable <id>      # Enable plugin
universal-registry-cli plugin list             # List all plugins

universal-registry-cli service add             # Add new service
universal-registry-cli service enable <id>     # Start service

universal-registry-cli engine add              # Add compute engine
universal-registry-cli grid add                # Add grid node
universal-registry-cli config show             # Show configuration

# See all commands
universal-registry-cli help
```

**Additional Features:**
```bash
universal-registry-cli component list          # Registry components
universal-registry-cli registry add            # Sub-registries
universal-registry-cli mesh list-routes        # Service mesh
```

---

## 🔐 Authentication Examples

### Create an API Key
```bash
# Using the admin key from Step 1
curl -X POST http://localhost:8080/api/v1/gateway/keys \
  -H "X-API-Key: ureg_admin_xxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Application",
    "key_type": "api_key",
    "permissions": [
      "read:plugins",
      "read:services",
      "write:plugins"
    ],
    "rate_limit": 1000,
    "expires_in_days": 90
  }'
```

**Response**:
```json
{
  "key_id": "key_abc123",
  "api_key": "ureg_app_xyz789...",
  "name": "My Application",
  "permissions": ["read:plugins", "read:services", "write:plugins"],
  "rate_limit": 1000,
  "expires_at": "2026-03-15T12:00:00Z"
}
```

### Use the API Key
```bash
# List plugins
curl http://localhost:8080/api/v1/plugins/ \
  -H "X-API-Key: ureg_app_xyz789..."

# Get metrics
curl http://localhost:8080/api/v1/metrics/system \
  -H "X-API-Key: ureg_app_xyz789..."
```

### Rotate a Key
```bash
# Rotate with 24-hour grace period
curl -X POST http://localhost:8080/api/v1/gateway/keys/key_abc123/rotate \
  -H "X-API-Key: ureg_admin_xxxxxxxx" \
  -d '{"grace_period_hours": 24}'
```

---

## 📊 View Metrics

### Via CLI
```bash
ose-cli

# Select: 5. Metrics & Monitoring
# Then choose:
#   - System Metrics
#   - Plugin Metrics
#   - Service Metrics
#   - Performance Dashboard
```

### Via API
```bash
# System health
curl http://localhost:8080/api/v1/metrics/system \
  -H "X-API-Key: $API_KEY"

# Plugin statistics
curl http://localhost:8080/api/v1/metrics/plugins \
  -H "X-API-Key: $API_KEY"

# Performance metrics
curl http://localhost:8080/api/v1/metrics/performance \
  -H "X-API-Key: $API_KEY"

# All metrics dashboard
curl http://localhost:8080/api/v1/metrics/dashboard \
  -H "X-API-Key: $API_KEY"
```

---

## 🔍 Common Tasks

### Plugin Management
```bash
# Using TUI
ose-cli
→ 3. Plugin Management
→ List Plugins / Install Plugin / Activate Plugin

# Using CLI
universal-registry-cli plugin list
universal-registry-cli plugin install my-plugin
universal-registry-cli plugin activate my-plugin
```

### Service Management
```bash
# Using TUI
ose-cli
→ 4. Microservices Management
→ List Services / Start Service / Stop Service

# Using CLI
universal-registry-cli service list
universal-registry-cli service start my-service
universal-registry-cli service health my-service
```

### Monitoring
```bash
# Using TUI
ose-cli
→ 5. Metrics & Monitoring
→ Real-time Dashboard / Alerts / Historical Data

# Using CLI
universal-registry-cli system stats
universal-registry-cli system health
```

---

## 📁 Architecture Overview

```
┌─────────────────────────────────────────┐
│         API Gateway (Port 8080)         │
│  ┌───────────────────────────────────┐  │
│  │ Authentication & Key Rotation     │  │
│  │ Rate Limiting & Permissions       │  │
│  │ Usage Tracking & Monitoring       │  │
│  └───────────────────────────────────┘  │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼─────┐    ┌─────▼─────────┐
│  Plugins  │    │  Microservices│
│  Routes   │    │  Routes       │
└─────┬─────┘    └─────┬─────────┘
      │                │
      └────────┬────────┘
               │
        ┌──────▼──────┐
        │   Metrics   │
        │  Collector  │
        └─────────────┘
```

---

## 🎯 Key Features

### Unified API Gateway ✅
- API key management with rotation
- JWT token support
- Permission-based access control
- Rate limiting per key
- Usage statistics

### Consolidated Metrics ✅
- System metrics (CPU, memory, disk, network)
- Plugin metrics (installs, activations, usage)
- Service metrics (requests, errors, latency)
- Performance metrics (p50, p95, p99)
- Alert system with thresholds

### Two Focused CLIs ✅
- **ose-cli**: Interactive TUI for all system features
- **universal-registry-cli**: Registry, plugins, service mesh

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [START_HERE.md](START_HERE.md) | Quick start guide (this file) |
| [CONSOLIDATION_SUMMARY.md](CONSOLIDATION_SUMMARY.md) | Complete consolidation details |
| [CONSOLIDATED_ARCHITECTURE.md](CONSOLIDATED_ARCHITECTURE.md) | Architecture documentation |
| [UNIFIED_CONTROL.md](UNIFIED_CONTROL.md) | API reference |
| [PLATFORM_COMPLETE.md](PLATFORM_COMPLETE.md) | Platform overview |

---

## 🔄 Migration from Old Tools

If you have existing code using the old microservices-cli or separate tools:

### Replace This:
```bash
# OLD - fragmented tools
microservices-cli service start my-service
./some-other-cli plugin install my-plugin
```

### With This:
```bash
# NEW - consolidated
universal-registry-cli service start my-service
universal-registry-cli plugin install my-plugin

# OR use interactive TUI
ose-cli
```

### Update API Calls:
```bash
# OLD - no authentication
curl http://localhost:8080/api/v1/plugins/

# NEW - with API key
curl http://localhost:8080/api/v1/plugins/ \
  -H "X-API-Key: ureg_app_xyz..."
```

---

## ⚠️ Important Notes

### Security
- **Admin key**: Generated on first start, save it securely
- **Key rotation**: Set up automatic rotation for production
- **Permissions**: Use least-privilege principle
- **Rate limits**: Adjust based on your needs

### Performance
- **Rate limiting**: Default 1,000 req/hour per key
- **Metrics collection**: Every 60 seconds
- **Alert checking**: Every 30 seconds
- **Database**: SQLite for keys (consider PostgreSQL for production)

### Production
- Set environment variables:
  - `REGISTRY_ENV=production`
  - `SECRET_KEY=your-secret-key`
  - `DATABASE_URL=postgresql://...`
- Configure HTTPS with valid certificates
- Set up log rotation
- Configure backup strategy

---

## 🆘 Troubleshooting

### Can't start registry
```bash
# Check if port 8080 is in use
lsof -i :8080

# Kill existing process if needed
kill $(lsof -t -i:8080)

# Start with debug logging
DEBUG=1 python3 hyper_registry.py
```

### Can't authenticate
```bash
# Verify admin key exists
ls -la /var/lib/ose/api_keys.db

# Check logs for admin key
grep "Initial admin API key" /var/log/ose/registry.log

# Or generate new admin key
curl -X POST http://localhost:8080/api/v1/gateway/keys/bootstrap
```

### CLI not found
```bash
# Make CLIs executable
chmod +x /workspaces/terminal/bin/ose-cli
chmod +x /workspaces/terminal/bin/universal-registry-cli

# Add to PATH
export PATH="/workspaces/terminal/bin:$PATH"
```

---

## 🎉 You're Ready!

The platform is fully consolidated and ready to use:

1. ✅ **API Gateway** - with key rotation and auth
2. ✅ **Unified Metrics** - all monitoring in one place
3. ✅ **Two CLIs** - focused and powerful
4. ✅ **Complete Docs** - everything documented
5. ✅ **Zero Redundancy** - clean architecture

### Next Steps:

```bash
# 1. Start the registry
cd /workspaces/terminal/modules/universal-registry
python3 hyper_registry.py

# 2. Save the admin key shown in output

# 3. Launch the TUI
ose-cli

# 4. Explore!
```

---

**Universal Registry v∞.9 - Consolidation Complete** 🚀

Need help? Check:
- [CONSOLIDATION_SUMMARY.md](CONSOLIDATION_SUMMARY.md) - Complete details
- [CONSOLIDATED_ARCHITECTURE.md](CONSOLIDATED_ARCHITECTURE.md) - Technical architecture
- [UNIFIED_CONTROL.md](UNIFIED_CONTROL.md) - API reference
