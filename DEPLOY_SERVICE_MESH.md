# 🚀 Ultra-Advanced Service Mesh - Deployment Guide

## Quick Start (3 Steps)

### Step 1: Start the Service Mesh
```bash
cd /workspaces/terminal
docker-compose up -d service-mesh
```

### Step 2: Verify It's Running
```bash
docker logs -f ose-service-mesh
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Access the Dashboard
Open your browser to: **http://localhost:8000**

---

## Full System Deployment

### Start All Services
```bash
cd /workspaces/terminal
docker-compose up -d
```

### Check Service Status
```bash
docker-compose ps
```

All services should show "Up" status:
- ose-service-mesh (Port 8000) ✅
- ose-discovery (Port 8001)
- ose-factory-reset (Port 8002)
- ose-reinstallation (Port 8003)
- ose-optimization (Port 8004)
- ose-terminal-config (Port 8005)
- ose-metrics-collector (Port 8006)
- ose-postgres (Port 5432)
- ose-redis (Port 6379)
- ose-rabbitmq (Port 5672, 15672)
- ose-prometheus (Port 9090)
- ose-grafana (Port 3000)
- ose-loki (Port 3100)

---

## Testing the Ultra-Advanced Features

### 1. Test Dashboard
```bash
curl http://localhost:8000/
# Should return HTML dashboard
```

### 2. Test Service Registry
```bash
curl http://localhost:8000/api/v1/services | jq
```

### 3. Test Health Check
```bash
curl http://localhost:8000/api/v1/health/comprehensive | jq
```

### 4. Test 3D Topology
```bash
curl http://localhost:8000/api/v1/topology/graph | jq
```

### 5. Test NLP Query
```bash
curl -X POST http://localhost:8000/api/v1/nlp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the status of all services"}'
```

### 6. Test AI Recommendations
```bash
curl http://localhost:8000/api/v1/ai/recommendations | jq
```

### 7. Test WebSocket (using wscat)
```bash
# Install wscat if needed
npm install -g wscat

# Connect to WebSocket
wscat -c ws://localhost:8000/ws/mesh
```

---

## Dashboard Features to Explore

### 1. Header Statistics
- Total services count (should show 12)
- Healthy services indicator
- Total endpoints (235)
- Overall health score

### 2. NLP Query Interface
Try these example queries:
- "Show me service health"
- "Why is the discovery service important?"
- "How can I optimize performance?"
- "What are the critical services?"

### 3. 3D Topology Viewer
- Switch between 3D, 2D, and DAG views
- Hover over nodes to see service details
- View dependency connections
- Identify service clusters

### 4. AI Recommendations
- View priority-sorted suggestions
- Check impact and effort scores
- See confidence levels
- Click for detailed action items

### 5. Service Cards
- Filter by: All, Applications, Infrastructure
- View real-time health scores
- Check performance metrics
- Access API docs, logs, and metrics

---

## Troubleshooting

### Dashboard Not Loading
```bash
# Check if Service Mesh is running
docker ps | grep service-mesh

# Check logs for errors
docker logs ose-service-mesh

# Restart the service
docker-compose restart service-mesh
```

### WebSocket Not Connecting
```bash
# Verify port is accessible
curl http://localhost:8000/health

# Check firewall rules
sudo ufw status

# Test WebSocket endpoint
wscat -c ws://localhost:8000/ws/mesh
```

### Services Not Appearing
```bash
# Ensure all services are running
docker-compose ps

# Check individual service health
curl http://localhost:8001/health  # Discovery
curl http://localhost:8002/health  # Factory Reset
# etc...

# Review Service Mesh logs
docker logs ose-service-mesh | grep ERROR
```

### NLP Not Working
```bash
# Test the endpoint directly
curl -X POST http://localhost:8000/api/v1/nlp/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}' | jq

# Check logs for NLP engine errors
docker logs ose-service-mesh | grep NLP
```

---

## Local Development Mode

### Run Service Mesh Standalone
```bash
cd /workspaces/terminal/modules/service-mesh

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
chmod +x run.sh
./run.sh
```

### Development Features
- Auto-reload on code changes
- Enhanced logging
- Direct file editing
- Faster iteration

---

## Performance Optimization

### Adjust Health Check Interval
Edit `advanced_main.py`:
```python
# Change from 10s to 30s for less frequent checks
asyncio.sleep(30)  # Line ~1020
```

### Reduce Metrics History
Edit `advanced_main.py`:
```python
# Change from 1000 to 100 points
metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
```

### Disable AI Recommendations
Edit `advanced_main.py`:
```python
# Comment out recommendation generation
# recommendations_data = await RAGEngine.generate_recommendations()
```

---

## Production Deployment

### Security Enhancements
1. Add API authentication
2. Enable HTTPS/TLS
3. Implement rate limiting
4. Add CORS restrictions
5. Use secrets management

### Scaling
1. Deploy multiple Service Mesh replicas
2. Use load balancer (already have Traefik)
3. Enable database connection pooling
4. Add Redis cluster for caching
5. Configure horizontal pod autoscaling

### Monitoring
1. Connect to existing Prometheus (Port 9090)
2. Create Grafana dashboards (Port 3000)
3. Configure log aggregation with Loki (Port 3100)
4. Set up alerting rules
5. Enable distributed tracing

---

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Service Mesh | http://localhost:8000 | Ultra-advanced dashboard |
| Discovery | http://localhost:8001/docs | API documentation |
| Factory Reset | http://localhost:8002/docs | API documentation |
| Reinstallation | http://localhost:8003/docs | API documentation |
| Optimization | http://localhost:8004/docs | API documentation |
| Terminal Config | http://localhost:8005/docs | API documentation |
| Metrics Collector | http://localhost:8006/docs | API documentation |
| Traefik | http://localhost:8081 | Gateway dashboard |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| RabbitMQ | http://localhost:15672 | Queue management (ose/ose_queue_password) |

---

## Need Help?

- Check [ADVANCED_README.md](modules/service-mesh/ADVANCED_README.md)
- Review [TUI_INTERFACE.md](docs/TUI_INTERFACE.md)
- See [MICROSERVICES_ARCHITECTURE.md](docs/MICROSERVICES_ARCHITECTURE.md)

---

**🎉 Enjoy your ultra-advanced Service Mesh platform!**
