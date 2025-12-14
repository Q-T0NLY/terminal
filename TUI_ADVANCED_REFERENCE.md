# OSE TUI - Advanced Features Quick Reference

## 🚀 Accessing New Features

### Launch TUI
```bash
python3 cli/ose_tui.py
```

### Navigate to Service Mesh
```
Main Menu → Press 1
```

## 🎮 Service Mesh Commands

| Command | Feature | Description |
|---------|---------|-------------|
| **1-12** | Service Details | View detailed health breakdown for specific service |
| **r** | Refresh | Reload all service data from API |
| **ai** | AI Recommendations | View top 10 AI-powered optimization suggestions |
| **nlp** | NLP Query | Ask questions in natural language |
| **topo** | Topology | View service clusters and critical paths |
| **hb** | Heartbeat Monitor ⭐ NEW | Real-time health tracking with latency metrics |
| **deps** | Dependencies ⭐ NEW | Service dependency graph and analysis |
| **bus** | Message Bus ⭐ NEW | RabbitMQ status and event publishing |
| **web** | Open Dashboard | Launch web browser to Service Mesh UI |
| **b** | Back | Return to main menu |

## 🫀 Heartbeat Monitor (hb)

### What You See
- **Summary Panel**: Total services, health counts, overall health %
- **Status Table**: Each service with:
  - 🟢 Healthy / 🟡 Degraded / 🔴 Critical / ⚫ Dead
  - Heartbeat count
  - Missed heartbeats
  - Average latency (ms)
  - Uptime percentage
  - Seconds since last heartbeat

### Actions
- `r` - Refresh data
- `web` - Open heartbeat dashboard in browser
- `b` - Back

### Use Cases
- Monitor service health in real-time
- Identify degraded services quickly
- Track uptime and performance
- Detect network issues (high latency)

## 🔗 Dependencies (deps)

### What You See
- **Summary**: Total services, dependencies, clusters, circular warnings
- **Hub Services**: Services with many dependencies
- **Clusters Table**: Services grouped by type (core, utility, infrastructure, etc.)
- **Critical Path**: Longest dependency chain
- **Circular Dependencies**: Warning if any detected
- **Mermaid Diagram**: Copy-paste ready syntax

### Actions
- `r` - Refresh analysis
- `web` - Open interactive 3D graph
- `b` - Back

### Use Cases
- Understand service relationships
- Identify critical services (hubs)
- Detect circular dependencies
- Plan deployment order (critical path)
- Visualize microservices architecture

## 💬 Message Bus (bus)

### What You See
- **Connection Status**: RabbitMQ host, port, connection state
- **Exchanges Table**: Name, type, purpose
  - `ose.events` - Service lifecycle events
  - `ose.tasks` - Background task queue
  - `ose.logs` - Centralized logging
- **Queues Table**: All declared queues
- **Publishing Interface**: Test event capability

### Actions
- `r` - Refresh status
- `p` - Publish test event
- `web` - Open RabbitMQ admin panel (localhost:15672)
- `b` - Back

### Use Cases
- Monitor RabbitMQ connectivity
- View active exchanges and queues
- Test event-driven communication
- Debug message routing issues
- Access RabbitMQ management UI

## 🎯 Quick Workflows

### Health Check Workflow
```
1 → Service Mesh
hb → Heartbeat Monitor
[Check for 🟡 or 🔴 services]
web → Open dashboard for detailed view
```

### Dependency Analysis Workflow
```
1 → Service Mesh
deps → Dependencies
[Review clusters and critical path]
web → Open 3D graph for visualization
```

### Event Publishing Workflow
```
1 → Service Mesh
bus → Message Bus
p → Publish test event
[Verify event sent successfully]
```

### Comprehensive Monitoring
```
1 → Service Mesh
r → Refresh service list
hb → Check heartbeat status
deps → Verify dependencies
bus → Monitor message bus
ai → Review AI recommendations
```

## 🌐 Web Dashboard Integration

All TUI features have corresponding web dashboards:

| TUI Command | Web URL | Description |
|-------------|---------|-------------|
| `hb` then `web` | `http://localhost:8000/heartbeat-dashboard` | Real-time heartbeat monitor |
| `deps` then `web` | `http://localhost:8000/dependencies` | Interactive 3D dependency graph |
| `bus` then `web` | `http://localhost:15672` | RabbitMQ management interface |
| `web` | `http://localhost:8000` | Main Service Mesh dashboard |

## 📊 Status Indicators

### Heartbeat Status
- 🟢 **HEALTHY** - All heartbeats successful, low latency
- 🟡 **DEGRADED** - Some missed heartbeats, higher latency
- 🔴 **CRITICAL** - Multiple consecutive failures
- ⚫ **DEAD** - No response within timeout period
- ⚪ **UNKNOWN** - Not yet monitored

### Service Health Scores
- **90-100** - 🟢 Excellent
- **70-89** - 🟡 Good
- **<70** - 🔴 Needs Attention

## 🔧 Troubleshooting

### "Service Mesh Offline"
```bash
# Start Service Mesh
docker-compose up -d service-mesh

# Wait 10 seconds, then refresh TUI
# Press 'r' in Service Mesh menu
```

### "Heartbeat monitoring not available"
```bash
# Initialize Service Mesh components
cd modules/service-mesh
python initialize.py

# Restart Service Mesh
docker-compose restart service-mesh
```

### "Message bus not available"
```bash
# Start RabbitMQ
docker-compose up -d rabbitmq

# Wait 10 seconds
# Check status with 'bus' command
```

### "Dependencies not showing"
```bash
# Reinitialize dependency graph
cd modules/service-mesh
python initialize.py

# Restart Service Mesh
docker-compose restart service-mesh
```

## 💡 Pro Tips

1. **Use keyboard shortcuts** - All commands are single keys (hb, deps, bus) for fast navigation

2. **Refresh frequently** - Press 'r' in any screen to get latest data

3. **Chain commands** - Use web dashboards for detailed analysis, TUI for quick checks

4. **Monitor during changes** - Keep heartbeat monitor open when deploying updates

5. **Use Mermaid diagrams** - Copy dependency diagrams to documentation

6. **Test events** - Use 'bus' → 'p' to verify message bus is working

7. **Check critical path** - Important for deployment planning and rollback strategies

## 📝 Example Session

```bash
# Launch TUI
python3 cli/ose_tui.py

# Navigate to Service Mesh
> 1

# Check overall health
> r

# Monitor heartbeats
> hb
  [See 6 healthy, 1 degraded]
  
# Check dependencies
> b
> deps
  [See service-mesh depends on discovery]
  
# Verify message bus
> b
> bus
  [RabbitMQ connected, 3 exchanges]
  
# Publish test event
> p
  [Event published successfully]
  
# Open web for detailed view
> web
  [Browser opens to 3D graph]
  
# Return to main menu
> b
> b
```

## 🚀 Next Steps

1. **Explore each feature** - Try all three new commands (hb, deps, bus)
2. **Monitor your services** - Watch heartbeat status during deployments
3. **Analyze dependencies** - Understand your service architecture
4. **Test event publishing** - Verify message bus connectivity
5. **Use web dashboards** - Deep dive with interactive visualizations

---

**Documentation**: See [ADVANCED_FEATURES.md](../ADVANCED_FEATURES.md) for complete API reference

**Support**: All features integrate seamlessly with existing TUI workflow

**Updated**: December 14, 2025
