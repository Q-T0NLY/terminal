# 🏗️ OSE Microservices Architecture

## Vision: Ultra-Modern Containerized System Management Platform

OSE is now architected as a **cloud-native, containerized microservices platform** where each feature runs independently as a Docker container with its own API, database, and UI.

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Kong/Traefik)               │
│                   Port 8000 - Load Balancer                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Discovery   │      │Factory Reset │      │Reinstallation│
│  Service     │      │  Service     │      │  Service     │
│  Port 8001   │      │  Port 8002   │      │  Port 8003   │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│Optimization  │      │Terminal Config│     │   Message    │
│  Service     │      │  Service     │      │    Queue     │
│  Port 8004   │      │  Port 8005   │      │  (RabbitMQ)  │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────┐
│              Shared Storage (PostgreSQL + Redis)          │
│           TimescaleDB for Metrics & Event Store           │
└──────────────────────────────────────────────────────────┘
```

---

## 📦 Microservices

### 1. Discovery Service (Port 8001)
**Purpose:** Ultra-Advanced System-Wide Discovery, Scanning, and Detection

**Features:**
- Real-time hardware detection (CPU, GPU, RAM, Disk, Network)
- OS and package detection (distro, kernel, packages)
- Application discovery (installed apps, versions, dependencies)
- Network topology mapping
- Cloud provider detection (AWS, GCP, Azure)
- Container runtime detection (Docker, Podman, K8s)
- Database detection (PostgreSQL, MySQL, MongoDB, Redis)
- Service discovery (systemd, init.d, supervisord)
- Security audit (open ports, CVEs, misconfigurations)
- Performance profiling (CPU/RAM/Disk usage patterns)

**Tech Stack:**
- FastAPI (Python)
- PostgreSQL (metadata storage)
- Redis (caching)
- Prometheus (metrics)
- Grafana (visualization)

**API Endpoints:**
```
GET  /api/v1/discover/hardware
GET  /api/v1/discover/software
GET  /api/v1/discover/network
GET  /api/v1/discover/security
POST /api/v1/scan/full
POST /api/v1/scan/quick
GET  /api/v1/reports/{scan_id}
```

**Standalone Usage:**
```bash
docker run -p 8001:8001 ose/discovery
curl http://localhost:8001/api/v1/scan/full
```

---

### 2. Factory Reset Service (Port 8002)
**Purpose:** Ultra-Advanced Factory Reset with Dynamic User Customizations

**Features:**
- **Dynamic Selection UI** - Interactive web UI for selecting what to reset
- **Granular Control** - Package-by-package, file-by-file selection
- **Smart Classification** - AI-powered categorization (System, User, App)
- **Preview Mode** - See exactly what will be removed before execution
- **Rollback Points** - Automatic snapshots before each operation
- **Selective Reset** - Reset only selected components
- **Factory Profiles** - Pre-configured reset profiles (Light, Medium, Deep, Nuclear)
- **Custom Workflows** - User-defined reset sequences
- **Dry-Run Mode** - Simulate without changes
- **Recovery Console** - Emergency recovery if system breaks

**Tech Stack:**
- FastAPI (Python backend)
- React + TypeScript (frontend)
- PostgreSQL (state tracking)
- Redis (session management)
- NATS (event streaming)

**API Endpoints:**
```
GET  /api/v1/reset/analyze
POST /api/v1/reset/preview
POST /api/v1/reset/execute
GET  /api/v1/reset/profiles
POST /api/v1/reset/custom
POST /api/v1/reset/rollback
GET  /api/v1/reset/status/{job_id}
```

**Reset Profiles:**
```yaml
profiles:
  light:
    - Clean caches
    - Remove temp files
    - Clear logs
    
  medium:
    - Light +
    - Remove user-installed packages
    - Reset user configs
    
  deep:
    - Medium +
    - Purge application data
    - Reset system configs
    
  nuclear:
    - Deep +
    - Wipe user data
    - Reinstall package managers
    - Full system reset
```

**Web UI:**
```
http://localhost:8002/ui
- Interactive file tree
- Checkboxes for selection
- Size/impact visualization
- Before/after preview
- One-click rollback
```

---

### 3. Reinstallation Service (Port 8003)
**Purpose:** Ultra-Advanced Reinstallation & Auto-Config Regeneration

**Features:**
- **Package Reinstallation** - Reinstall packages with fresh configs
- **Config Regeneration** - Auto-generate optimal configurations
- **Dependency Resolution** - Smart dependency handling
- **Version Selection** - Choose specific package versions
- **Batch Operations** - Reinstall multiple packages at once
- **Config Templates** - Pre-built config templates
- **Environment Detection** - Auto-configure based on hardware
- **Migration Tools** - Migrate configs between systems
- **Backup Integration** - Auto-backup before reinstall
- **Health Checks** - Post-install validation

**Tech Stack:**
- FastAPI (Python)
- Ansible (automation)
- Jinja2 (config templates)
- PostgreSQL (package metadata)

**API Endpoints:**
```
POST /api/v1/reinstall/package
POST /api/v1/reinstall/batch
POST /api/v1/config/generate
GET  /api/v1/config/templates
POST /api/v1/config/apply
POST /api/v1/migrate/export
POST /api/v1/migrate/import
```

**Config Templates:**
```
- nginx.conf.j2 (optimized for hardware)
- postgresql.conf.j2 (tuned for RAM/CPU)
- sysctl.conf.j2 (kernel params)
- limits.conf.j2 (resource limits)
- zshrc.j2 (shell config)
```

---

### 4. Optimization Service (Port 8004)
**Purpose:** Ultra-Advanced System/Terminal/Specs Optimizations

**Features:**
- **Hardware Profiling** - Detect CPU, RAM, Disk capabilities
- **Auto-Tuning** - Automatically optimize based on hardware
- **Benchmark Suite** - Measure before/after performance
- **Kernel Optimization** - Tune kernel parameters
- **Memory Management** - Optimize swap, cache, buffers
- **Disk Optimization** - Tune I/O schedulers, filesystems
- **Network Optimization** - TCP/IP stack tuning
- **Terminal Optimization** - Shell, prompt, completions
- **Application Tuning** - Database, web server, cache tuning
- **Power Management** - Battery/performance profiles

**Tech Stack:**
- FastAPI (Python)
- Go (performance-critical operations)
- eBPF (kernel tracing)
- PostgreSQL (optimization history)

**API Endpoints:**
```
POST /api/v1/optimize/auto
POST /api/v1/optimize/kernel
POST /api/v1/optimize/memory
POST /api/v1/optimize/disk
POST /api/v1/optimize/network
POST /api/v1/optimize/terminal
GET  /api/v1/benchmark/run
GET  /api/v1/profiles
```

**Optimization Profiles:**
```yaml
profiles:
  laptop_battery:
    cpu_governor: powersave
    swappiness: 10
    disk_scheduler: noop
    
  desktop_performance:
    cpu_governor: performance
    swappiness: 1
    disk_scheduler: kyber
    tcp_congestion: bbr
    
  server_production:
    cpu_governor: performance
    swappiness: 0
    disk_scheduler: none
    tcp_congestion: cubic
    file_max: 2097152
```

---

### 5. Terminal Config Service (Port 8005)
**Purpose:** Enterprise ZShrc Configuration Management

**Features:**
- **Config Generation** - Generate optimal ZSH configs
- **Theme Management** - Install/manage ZSH themes
- **Plugin Management** - Oh-My-Zsh, Prezto, Antigen support
- **Alias Registry** - Central alias management
- **Completion System** - Auto-completion configuration
- **Prompt Engineering** - Custom prompt builders
- **Performance Tuning** - Fast startup optimization
- **Cloud Sync** - Sync configs across machines
- **Version Control** - Config versioning and rollback
- **Templates** - Pre-built config templates

**Tech Stack:**
- FastAPI (Python)
- Git (version control)
- S3/MinIO (cloud storage)
- PostgreSQL (config metadata)

**API Endpoints:**
```
POST /api/v1/config/generate
GET  /api/v1/themes
POST /api/v1/themes/install
GET  /api/v1/plugins
POST /api/v1/plugins/install
POST /api/v1/aliases/import
POST /api/v1/sync/push
POST /api/v1/sync/pull
```

---

## 🔧 Infrastructure Services

### API Gateway (Port 8000)
- **Kong** or **Traefik**
- Rate limiting
- Authentication/Authorization (OAuth2, JWT)
- Load balancing
- Service discovery
- API versioning

### Message Queue
- **RabbitMQ** or **NATS**
- Async task processing
- Event streaming
- Pub/Sub messaging

### Databases
- **PostgreSQL** - Primary data store
- **TimescaleDB** - Metrics and time-series
- **Redis** - Caching and sessions

### Monitoring
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Loki** - Log aggregation
- **Jaeger** - Distributed tracing

---

## 🐳 Docker Architecture

### Base Images
```dockerfile
FROM python:3.11-alpine AS base
# Minimal base with Python

FROM base AS discovery
# Discovery service specific deps

FROM base AS factory-reset
# Factory reset service specific deps

# etc...
```

### Multi-Stage Builds
- **Stage 1:** Dependencies installation
- **Stage 2:** Application build
- **Stage 3:** Runtime image (minimal)

### Image Sizes
- Base: ~50MB
- Discovery Service: ~120MB
- Factory Reset Service: ~150MB
- Optimization Service: ~100MB
- Terminal Config: ~80MB

---

## 🚀 Deployment

### Development
```bash
docker-compose up
```

### Production (Kubernetes)
```bash
kubectl apply -f k8s/
```

### Standalone Service
```bash
docker run -p 8001:8001 ose/discovery
```

---

## 📊 Communication Patterns

### Synchronous (REST API)
- User interactions
- Real-time queries
- Simple operations

### Asynchronous (Message Queue)
- Long-running tasks
- Batch operations
- Event notifications

### Streaming (WebSocket)
- Real-time updates
- Progress tracking
- Live logs

---

## 🔐 Security

- **Service-to-Service Auth:** mTLS
- **User Auth:** OAuth2 + JWT
- **Secrets Management:** Vault
- **Network Policies:** Zero-trust
- **API Rate Limiting:** Redis-based
- **Audit Logging:** All operations logged

---

## 📈 Scalability

Each service can scale independently:
```yaml
services:
  discovery:
    replicas: 3
  factory-reset:
    replicas: 2
  optimization:
    replicas: 5
```

---

## 🎯 Next Steps

1. **Phase 1:** Containerize existing modules
2. **Phase 2:** Build microservices APIs
3. **Phase 3:** Create web UIs
4. **Phase 4:** Add orchestration
5. **Phase 5:** Deploy to production

**Status:** Architecture Designed ✅ | Implementation Starting 🚧
