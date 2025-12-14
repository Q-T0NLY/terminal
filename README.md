# 🚀 OSE - OmniSystem Enhancer Platform

**Ultra-Modern, Professional, Enterprise System Suite with Microservices Architecture**

A comprehensive, containerized microservices platform for system discovery, optimization, factory reset, and terminal configuration.

[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 📚 **Full documentation available in [docs/](docs/) folder** - See [docs/README.md](docs/README.md) for complete documentation index

---

## 🏗️ What is OSE?

OSE (OmniSystem Enhancer) is a next-generation system management platform built with modern microservices architecture. Each feature runs as an independent, containerized service that can be deployed, scaled, and managed separately.

### 🎯 Core Features

🔍 **Discovery Service** - Ultra-advanced system-wide scanning and hardware/software detection  
🧹 **Factory Reset Service** - Dynamic factory reset with granular control and backup  
🔄 **Reinstallation Service** - Automated package reinstallation and config generation  
⚡ **Optimization Service** - System and terminal performance enhancement with ML recommendations  
🔧 **Terminal Config Service** - ZSH configuration management with themes and cloud sync

---

## 🚀 Quick Start (60 seconds)

### Prerequisites

```bash
# Required
- Docker 20.10+
- docker-compose 1.29+
- 4GB RAM minimum
- 10GB disk space
```

### Start the Platform

```bash
# Clone and start
cd /workspaces/terminal

# Option 1: Use quick start script
./start.sh
# Then select: 1) Start all services

# Option 2: Use docker-compose directly
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Access Services (30 seconds later)

| Service | URL | Docs |
|---------|-----|------|
| **Discovery** | http://localhost:8001 | http://localhost:8001/docs |
| **Factory Reset** | http://localhost:8002 | http://localhost:8002/docs |
| **Reinstallation** | http://localhost:8003 | http://localhost:8003/docs |
| **Optimization** | http://localhost:8004 | http://localhost:8004/docs |
| **Terminal Config** | http://localhost:8005 | http://localhost:8005/docs |
| **Grafana** | http://localhost:3000 | Login: admin/admin |
| **Prometheus** | http://localhost:9090 | Metrics & monitoring |
| **RabbitMQ** | http://localhost:15672 | Login: ose/ose_queue_password |
| **Traefik** | http://localhost:8080 | API Gateway dashboard |

---

## 🔍 Try It Now - Quick Examples

### 1. Scan Your System

```bash
curl http://localhost:8001/api/v1/scan \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"scan_type": "quick"}' | jq
```

**Result:**
```json
{
  "scan_id": "scan_20231213_143022",
  "hardware": {
    "cpu": {"cores": 8, "model": "Intel Core i7"},
    "memory": {"total_gb": 16.0, "available_gb": 8.5}
  },
  "software": {
    "os": {"name": "Linux", "version": "5.15.0"},
    "packages": [...]
  }
}
```

### 2. Get Optimization Recommendations

```bash
curl http://localhost:8004/api/v1/optimize/recommendations | jq
```

**Result:**
```json
{
  "total_recommendations": 12,
  "recommendations": [
    {
      "title": "Set CPU Governor to Performance",
      "impact_score": 8,
      "current_value": "powersave",
      "recommended_value": "performance"
    }
  ]
}
```

### 3. Generate ZSH Config

```bash
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "enterprise",
    "theme": "powerlevel10k",
    "plugins": ["zsh-autosuggestions", "zsh-syntax-highlighting"]
  }' | jq
```

### 4. Analyze Factory Reset Options

```bash
curl http://localhost:8002/api/v1/reset/analyze | jq
```

**Result:**
```json
{
  "total_size_mb": 8432.5,
  "components": [
    {"name": "Cache Files", "size_mb": 2340, "risk_level": "low"},
    {"name": "User Configs", "size_mb": 450, "risk_level": "high"}
  ],
  "warnings": ["⚠️  Large amount of data detected"]
}
```

---

## 🧪 Run Integration Tests

```bash
# Install dependencies
pip install requests colorama

# Run comprehensive tests
python test_services.py
```

**Output:**
```
🧪 OSE Platform Integration Tests
============================================================
Health Checks
============================================================
✅ discovery: healthy
✅ factory-reset: healthy
✅ reinstallation: healthy
✅ optimization: healthy
✅ terminal-config: healthy

Health Summary: 5/5 services healthy
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│             API Gateway (Traefik) - Port 8000                    │
│           Load Balancer, Rate Limiting, Authentication           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │Discovery│      │  Factory   │     │ Terminal  │
    │  :8001  │      │  Reset     │     │  Config   │
    │         │      │  :8002     │     │  :8005    │
    └────┬────┘      └─────┬─────┘     └─────┬─────┘
         │                 │                  │
    ┌────▼────┐      ┌────▼──────┐    ┌─────▼─────┐
    │Optimiz. │      │Reinstall  │    │           │
    │  :8004  │      │  :8003    │    │           │
    └────┬────┘      └─────┬─────┘    └───────────┘
         │                 │
         └─────────────────┼─────────────────┐
                           │                 │
         ┌─────────────────┼─────────────────┼──────────┐
         │                 │                 │          │
    ┌────▼────┐      ┌────▼─────┐    ┌─────▼─────┐  ┌─▼───┐
    │Postgres │      │  Redis   │    │ RabbitMQ  │  │ ... │
    │  :5432  │      │  :6379   │    │  :5672    │  └─────┘
    └─────────┘      └──────────┘    └───────────┘
                                             │
         ┌───────────────────────────────────┼──────────┐
         │                                   │          │
    ┌────▼─────┐      ┌──────────┐    ┌────▼──────┐
    │Prometheus│      │ Grafana  │    │   Loki    │
    │  :9090   │      │  :3000   │    │  :3100    │
    └──────────┘      └──────────┘    └───────────┘
```

### Service Responsibilities

| Service | Port | Tech Stack | Purpose |
|---------|------|------------|---------|
| **Discovery** | 8001 | FastAPI, psutil | Hardware/software detection, system scanning |
| **Factory Reset** | 8002 | FastAPI, React | Granular factory reset with 4 profiles |
| **Reinstallation** | 8003 | FastAPI, Jinja2 | Package reinstall, config templates |
| **Optimization** | 8004 | FastAPI, Go | System tuning, benchmarking |
| **Terminal Config** | 8005 | FastAPI | ZSH config generation, themes |
| **PostgreSQL** | 5432 | PostgreSQL 15 | Primary database |
| **Redis** | 6379 | Redis 7 | Cache & sessions |
| **RabbitMQ** | 5672 | RabbitMQ 3 | Message queue |
| **Prometheus** | 9090 | Prometheus | Metrics collection |
| **Grafana** | 3000 | Grafana | Monitoring dashboards |

---

## 📚 Documentation

### Quick Links

- 📘 **[Microservices Guide](README_MICROSERVICES.md)** - Comprehensive platform documentation
- 🏗️ **[Architecture](MICROSERVICES_ARCHITECTURE.md)** - Technical architecture deep dive
- 🔍 **[Discovery Service](modules/discovery/README.md)** - System scanning API
- 🧹 **[Factory Reset Service](modules/factory-reset/README.md)** - Factory reset API

### Legacy Documentation

- **[OSE User Guide](OSE_README.md)** - Original monolithic OSE documentation
- **[Clean Slate Guide](CLEANSLATE_GUIDE.md)** - Terminal configuration guide

---

## 🐳 Docker Commands Reference

### Build & Start

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build discovery

# Build without cache
docker-compose build --no-cache discovery

# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d discovery postgres redis
```

### Manage & Monitor

```bash
# View status
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f discovery

# Restart service
docker-compose restart discovery

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Scale Services

```bash
# Scale discovery service to 3 instances
docker-compose up -d --scale discovery=3

# Scale factory-reset to 2 instances
docker-compose up -d --scale factory-reset=2
```

### Debugging

```bash
# Execute command in container
docker-compose exec discovery /bin/bash

# View container details
docker-compose exec discovery env

# Check resource usage
docker stats

# Inspect network
docker network inspect terminal_ose-network
```

---

## 🔒 Security & Production

### Production Checklist

Before deploying to production:

- [ ] Change all default passwords in `docker-compose.yml`
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure firewall rules (restrict ports)
- [ ] Enable authentication on all services
- [ ] Set up secrets management (HashiCorp Vault)
- [ ] Enable mTLS between services
- [ ] Configure rate limiting in Traefik
- [ ] Set up intrusion detection (fail2ban)
- [ ] Enable audit logging
- [ ] Configure automated backups

### Secure Configuration Example

```yaml
# Enable HTTPS in Traefik
- "--entrypoints.websecure.address=:443"
- "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
- "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"

# Change default passwords
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # From .env file
  REDIS_PASSWORD: ${REDIS_PASSWORD}
  RABBITMQ_PASSWORD: ${RABBITMQ_PASSWORD}
```

---

## 📊 Monitoring & Observability

### Prometheus Metrics

Access metrics at http://localhost:9090

**Useful queries:**
```promql
# CPU usage by service
rate(container_cpu_usage_seconds_total[5m])

# Memory usage
container_memory_usage_bytes

# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

### Grafana Dashboards

1. Open http://localhost:3000
2. Login: admin/admin
3. Import dashboards from `monitoring/grafana/dashboards/`

### Log Aggregation

Loki collects logs from all services:
```bash
# View logs in Grafana
# Add Loki datasource: http://loki:3100
# Query: {container_name="ose-discovery"}
```

---

## 🛠️ Development

### Local Development (Without Docker)

```bash
# Navigate to service
cd modules/discovery

# Install dependencies
pip install -r requirements.txt

# Run service locally
python main.py

# Run with auto-reload
uvicorn main:app --reload --port 8001
```

### Adding a New Service

1. **Create service directory:**
   ```bash
   mkdir -p modules/my-service
   cd modules/my-service
   ```

2. **Create files:**
   ```bash
   touch Dockerfile main.py requirements.txt README.md
   ```

3. **Add to docker-compose.yml:**
   ```yaml
   my-service:
     build:
       context: ./modules/my-service
     ports:
       - "8006:8006"
     environment:
       - DATABASE_URL=postgresql://ose:password@postgres:5432/ose
     networks:
       - ose-network
   ```

4. **Update Prometheus:**
   Add to `monitoring/prometheus.yml`:
   ```yaml
   - job_name: 'my-service'
     static_configs:
       - targets: ['my-service:8006']
   ```

5. **Build and test:**
   ```bash
   docker-compose build my-service
   docker-compose up -d my-service
   curl http://localhost:8006/health
   ```

---

## 🎯 Roadmap

### Completed ✅
- [x] Microservices architecture
- [x] Docker containerization
- [x] 5 core services (Discovery, Factory Reset, Reinstallation, Optimization, Terminal Config)
- [x] Monitoring stack (Prometheus, Grafana, Loki)
- [x] API Gateway (Traefik)
- [x] Message queue (RabbitMQ)
- [x] Database (PostgreSQL, Redis)
- [x] Integration tests
- [x] Interactive API docs (FastAPI)

### In Progress 🚧
- [ ] React frontend dashboard
- [ ] Authentication (OAuth2/JWT)
- [ ] WebSocket real-time updates
- [ ] Kubernetes Helm charts

### Planned 📅
- [ ] GraphQL API
- [ ] Multi-cloud support (AWS, GCP, Azure)
- [ ] CI/CD pipelines (GitHub Actions)
- [ ] AI/ML recommendations
- [ ] Mobile app (React Native)
- [ ] VS Code extension

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request

### Development Guidelines

- Follow PEP 8 for Python code
- Add docstrings to all functions
- Write tests for new features
- Update documentation
- Ensure all services pass health checks

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

Built with:
- **FastAPI** - Modern Python web framework
- **Docker** - Containerization platform
- **Traefik** - Cloud-native API gateway
- **Prometheus & Grafana** - Monitoring stack
- **PostgreSQL & Redis** - Data storage
- **RabbitMQ** - Message broker

Inspired by:
- Kubernetes architecture patterns
- Cloud-native design principles
- Microservices best practices

---

## 📞 Support & Community

### Getting Help

1. **Documentation:** Browse [docs/](docs/) folder or start with [docs/QUICK_START.md](docs/QUICK_START.md)
2. **API Docs:** Visit http://localhost:800X/docs for each service
3. **Architecture:** See [docs/MICROSERVICES_ARCHITECTURE.md](docs/MICROSERVICES_ARCHITECTURE.md)
4. **Issues:** GitHub Issues for bug reports
5. **Discussions:** GitHub Discussions for questions

### Quick Links

- 🐛 [Report Bug](https://github.com/your-repo/issues/new?template=bug_report.md)
- 💡 [Request Feature](https://github.com/your-repo/issues/new?template=feature_request.md)
- 💬 [Join Discussion](https://github.com/your-repo/discussions)
- 📧 [Contact](mailto:support@example.com)

---

<div align="center">

**Built with ❤️ for Modern Infrastructure**

*Microservices • Containerization • Cloud-Native • Enterprise-Ready*

⭐ **Star this repo if you find it useful!** ⭐
docs/README
[Get Started](#-quick-start-60-seconds) • [Documentation](README_MICROSERVICES.md) • [Examples](#-try-it-now---quick-examples) • [Contributing](#-contributing)

</div>
