# 🚀 OSE - Microservices Platform

**Ultra-Modern, Professional, Enterprise System Suite**

## 🏗️ Architecture

### Microservices
- **Discovery Service** (port 8001) - System-wide scanning and detection
- **Factory Reset Service** (port 8002) - Dynamic factory reset with UI
- **Reinstallation Service** (port 8003) - Package reinstallation & config generation
- **Optimization Service** (port 8004) - System/terminal optimization
- **Terminal Config Service** (port 8005) - ZSH configuration management

### Infrastructure
- **API Gateway** (port 8000) - Traefik reverse proxy
- **PostgreSQL** (port 5432) - Primary database
- **Redis** (port 6379) - Cache & sessions
- **RabbitMQ** (ports 5672, 15672) - Message queue
- **Prometheus** (port 9090) - Metrics
- **Grafana** (port 3000) - Dashboards
- **Loki** (port 3100) - Logs

## 🚀 Quick Start

### Start All Services

```bash
# Start the entire platform
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Start Individual Services

```bash
# Start only discovery service
docker-compose up -d discovery

# Start core infrastructure
docker-compose up -d postgres redis rabbitmq

# Start monitoring stack
docker-compose up -d prometheus grafana loki
```

## 🔍 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API Gateway** | http://localhost:8000 | Main entry point |
| **Discovery** | http://localhost:8001 | System discovery |
| **Factory Reset** | http://localhost:8002 | Factory reset |
| **Reinstallation** | http://localhost:8003 | Package reinstall |
| **Optimization** | http://localhost:8004 | System optimization |
| **Terminal Config** | http://localhost:8005 | ZSH config |
| **Traefik Dashboard** | http://localhost:8080 | Gateway dashboard |
| **Grafana** | http://localhost:3000 | Monitoring (admin/admin) |
| **Prometheus** | http://localhost:9090 | Metrics |
| **RabbitMQ** | http://localhost:15672 | Queue (ose/ose_queue_password) |

## 📚 API Documentation

Each service provides interactive API docs at `/docs`:

- http://localhost:8001/docs - Discovery API
- http://localhost:8002/docs - Factory Reset API
- http://localhost:8003/docs - Reinstallation API
- http://localhost:8004/docs - Optimization API
- http://localhost:8005/docs - Terminal Config API

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
# Database
POSTGRES_DB=ose
POSTGRES_USER=ose
POSTGRES_PASSWORD=ose_secure_password

# Redis
REDIS_URL=redis://redis:6379

# RabbitMQ
RABBITMQ_URL=amqp://ose:ose_queue_password@rabbitmq:5672

# Services
DISCOVERY_PORT=8001
FACTORY_RESET_PORT=8002
REINSTALLATION_PORT=8003
OPTIMIZATION_PORT=8004
TERMINAL_CONFIG_PORT=8005
```

## 🐳 Docker Commands

### Build Services

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build discovery

# Build without cache
docker-compose build --no-cache
```

### Manage Services

```bash
# Start all
docker-compose up -d

# Stop all
docker-compose down

# Restart service
docker-compose restart discovery

# View logs
docker-compose logs -f discovery

# Execute command in container
docker-compose exec discovery /bin/bash
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v

# Remove all unused images
docker system prune -a
```

## 📊 Monitoring

### Prometheus Metrics

```bash
# CPU usage by service
rate(container_cpu_usage_seconds_total[5m])

# Memory usage by service
container_memory_usage_bytes

# Request rate
rate(http_requests_total[5m])
```

### Grafana Dashboards

1. Open http://localhost:3000
2. Login: admin/admin
3. Import dashboard from `monitoring/grafana/dashboards/`

## 🔒 Security

### Production Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS with valid certificates
- [ ] Configure firewall rules
- [ ] Enable authentication on all services
- [ ] Set up secrets management (Vault)
- [ ] Enable mTLS between services
- [ ] Configure rate limiting
- [ ] Set up intrusion detection

### Secure Configuration

```yaml
# Enable HTTPS in Traefik
- "--entrypoints.websecure.address=:443"
- "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
- "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
```

## 🧪 Testing

### Health Checks

```bash
# Check all services
for port in 8001 8002 8003 8004 8005; do
  curl -s http://localhost:$port/health | jq
done

# Check infrastructure
curl -s http://localhost:9090/-/healthy  # Prometheus
curl -s http://localhost:3000/api/health # Grafana
```

### Integration Tests

```bash
# Run discovery scan
curl -X POST http://localhost:8001/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"scan_type": "quick"}'

# Get optimization recommendations
curl http://localhost:8004/api/v1/optimize/recommendations

# Generate terminal config
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{"profile": "enterprise", "theme": "powerlevel10k"}'
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# Scale discovery service to 3 instances
docker-compose up -d --scale discovery=3

# Scale factory-reset service
docker-compose up -d --scale factory-reset=2
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# View logs
kubectl logs -f deployment/discovery
```

## 🛠️ Development

### Local Development

```bash
# Install dependencies for a service
cd modules/discovery
pip install -r requirements.txt

# Run service locally
python main.py

# Run with auto-reload
uvicorn main:app --reload --port 8001
```

### Adding a New Service

1. Create service directory: `modules/my-service/`
2. Add `Dockerfile`, `main.py`, `requirements.txt`
3. Add to `docker-compose.yml`
4. Update `monitoring/prometheus.yml`
5. Build and test: `docker-compose up -d my-service`

## 📦 Backup & Restore

### Backup

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U ose ose > backup.sql

# Backup volumes
docker run --rm -v ose_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_data.tar.gz /data
```

### Restore

```bash
# Restore PostgreSQL
docker-compose exec -T postgres psql -U ose ose < backup.sql

# Restore volumes
docker run --rm -v ose_postgres_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/postgres_data.tar.gz -C /
```

## 🐛 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check logs
docker-compose logs discovery

# Check health
docker-compose ps

# Rebuild
docker-compose build --no-cache discovery
docker-compose up -d discovery
```

**Database connection errors:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
docker-compose exec postgres psql -U ose -d ose -c "SELECT 1"
```

**Port already in use:**
```bash
# Find process using port
lsof -i :8001

# Change port in docker-compose.yml
ports:
  - "18001:8001"
```

## 📚 Documentation

- [Architecture Overview](MICROSERVICES_ARCHITECTURE.md)
- [Discovery Service](modules/discovery/README.md)
- [Factory Reset Service](modules/factory-reset/README.md)
- [API Reference](docs/API.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file

## 🎯 Roadmap

- [ ] Add authentication (OAuth2/JWT)
- [ ] Implement WebSocket support
- [ ] Add GraphQL API
- [ ] Create React dashboard
- [ ] Add AI/ML recommendations
- [ ] Kubernetes Helm charts
- [ ] CI/CD pipelines
- [ ] Multi-cloud support
