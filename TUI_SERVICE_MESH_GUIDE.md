# 🎨 TUI Service Mesh Integration Guide

## Overview

The OSE TUI (Terminal User Interface) now has **full integration** with the ultra-advanced Service Mesh backend, providing a beautiful terminal-based interface for monitoring and managing all 12 services.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /workspaces/terminal/cli
pip install -r requirements.txt
```

### 2. Start Service Mesh
```bash
cd /workspaces/terminal
docker-compose up -d service-mesh
```

### 3. Launch TUI
```bash
# Option 1: Direct launch
python3 /workspaces/terminal/cli/ose_tui.py

# Option 2: Quick launcher (checks dependencies)
./cli/launch_tui.sh

# Option 3: Make it global
sudo ln -s /workspaces/terminal/cli/ose_tui.py /usr/local/bin/ose-tui
ose-tui
```

---

## 📋 Features

### Main Menu → Option 1: System Services Mesh

When you select option **1** from the main menu, you enter the ultra-advanced Service Mesh interface with:

#### Real-Time Monitoring
- ✅ Live service status (🟢 UP, 🟡 SLOW, 🔴 DOWN)
- ✅ Health scores (0-100 for each service)
- ✅ CPU & memory metrics
- ✅ Overall system health score
- ✅ Connection status indicator

#### Interactive Commands

| Command | Description |
|---------|-------------|
| **1-12** | View detailed info for specific service |
| **r** | Refresh service status |
| **ai** | View AI-powered recommendations |
| **nlp** | Ask AI questions in natural language |
| **topo** | View service topology & dependencies |
| **web** | Open web dashboard in browser |
| **b** | Back to main menu |

---

## 🤖 AI Features

### 1. AI Recommendations (`ai` command)

Shows top 10 AI-generated recommendations with:
- Priority levels (🔴 Critical, 🟠 High, 🔵 Medium, 🟢 Low)
- Impact scores (0-10)
- Effort scores (0-10)
- Detailed action items

**Example:**
```
Enter your choice: ai

╔══════════════════════════════════════════════════════════╗
║      🤖 AI-Powered Recommendations (5)                   ║
╠═══╤══════════╤═════════════════╤════════════════════╤════╣
║ # │ Priority │ Service         │ Title              │... ║
╠═══╪══════════╪═════════════════╪════════════════════╪════╣
║ 1 │🟠 HIGH   │ reinstallation  │High CPU Usage      │8.5 ║
║ 2 │🔵 MEDIUM │ discovery       │Cache Optimization  │7.2 ║
...

Enter recommendation # for details: 1

┌────────────────────────────────────────────────────────┐
│ High CPU Usage Detected                                │
│                                                        │
│ Description:                                           │
│ The Reinstallation Service is experiencing elevated   │
│ CPU usage (65%), which may indicate inefficient...    │
│                                                        │
│ Action Items:                                          │
│   1. Implement lazy loading for package metadata      │
│   2. Add caching layer for dependency resolution      │
│   3. Limit concurrent package operations to 4         │
└────────────────────────────────────────────────────────┘
```

### 2. NLP Query Interface (`nlp` command)

Ask questions in natural language and get AI-powered answers!

**Example queries:**
- "What is the status of all services?"
- "Why is the discovery service important?"
- "How can I optimize performance?"
- "Show me critical services"
- "What services depend on PostgreSQL?"

**Example session:**
```
Enter your choice: nlp

┌────────────────────────────────────────────────────────┐
│ 🤖 NLP Query Interface                                 │
│                                                        │
│ Ask AI anything about your services!                  │
│                                                        │
│ Example queries:                                       │
│   • 'What is the status of all services?'            │
│   • 'Why is the discovery service important?'        │
│   • 'How can I optimize performance?'                │
└────────────────────────────────────────────────────────┘

Your question: Why is discovery service important?

┌────────────────────────────────────────────────────────┐
│ AI Response                                            │
│                                                        │
│ Intent: status_check (92% confidence)                 │
│                                                        │
│ Answer:                                                │
│ The Discovery Service is critical because it scans    │
│ and catalogs your entire system, providing the        │
│ foundation for other services to operate...           │
│                                                        │
│ Suggested Actions:                                     │
│   • View Discovery Service details                    │
│   • Check recent scan results                         │
│   • Review system inventory                           │
└────────────────────────────────────────────────────────┘

Your question: exit
```

### 3. Topology Visualization (`topo` command)

View service architecture and dependencies:
- Total nodes (services)
- Total edges (dependencies)
- Service clusters by category
- Critical dependency paths

**Example:**
```
Enter your choice: topo

┌────────────────────────────────────────────────────────┐
│ 🔮 3D Service Topology                                 │
│                                                        │
│ Total Nodes: 12                                        │
│ Total Edges: 8                                         │
│ Clusters: 2                                            │
│ Critical Paths: 3                                      │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Service Clusters                                       │
├──────────────┬─────────────────────────────────────────┤
│ Cluster      │ Services                                │
├──────────────┼─────────────────────────────────────────┤
│ application  │ discovery, factory-reset, ...           │
│ database     │ postgres, redis, rabbitmq               │
└──────────────┴─────────────────────────────────────────┘

Critical Dependency Paths:
  Path 1: factory-reset → discovery
  Path 2: reinstallation → discovery
  Path 3: optimization → metrics-collector
```

---

## 📊 Service Details View

Select any service (1-12) to see comprehensive information:

```
Enter your choice: 1

┌────────────────────────────────────────────────────────┐
│ Service Details                                        │
│                                                        │
│ Discovery Service                                      │
│                                                        │
│ Status: HEALTHY                                        │
│ Overall Health: 98/100                                 │
│                                                        │
│ Health Breakdown:                                      │
│   • Availability: 100/100                             │
│   • Performance: 95/100                               │
│   • Reliability: 100/100                              │
│   • Efficiency: 92/100                                │
│   • Security: 100/100                                 │
│   • Predicted (1h): 97/100                            │
│                                                        │
│ Metrics:                                               │
│   • CPU: 15.5%                                        │
│   • Memory: 32.1%                                     │
│   • Latency (P95): 125ms                              │
└────────────────────────────────────────────────────────┘
```

---

## 🎯 Comparison: TUI vs Web Dashboard

### TUI (Terminal Interface)
**Best For:**
- ✅ SSH sessions
- ✅ Remote server management
- ✅ Quick status checks
- ✅ Keyboard-driven workflows
- ✅ Resource-constrained environments
- ✅ Scripting and automation
- ✅ No GUI environments

**Advantages:**
- Fast and lightweight
- No browser required
- Works over SSH
- Keyboard shortcuts
- Low bandwidth usage

### Web Dashboard
**Best For:**
- ✅ Visual monitoring
- ✅ 3D topology visualization
- ✅ Detailed graphs and charts
- ✅ Mouse-driven interaction
- ✅ Real-time WebSocket updates
- ✅ Multiple simultaneous views

**Advantages:**
- Beautiful 3D visualizations
- Animated UI elements
- More detailed metrics
- Real-time updates via WebSocket
- Better for presentations

### Both Interfaces Share:
- ✅ Same backend API
- ✅ Real-time data
- ✅ AI recommendations
- ✅ NLP query capabilities
- ✅ Health scoring
- ✅ Service monitoring

---

## 🔧 Troubleshooting

### "Service Mesh Offline" Message
```bash
# Start Service Mesh
docker-compose up -d service-mesh

# Wait 10 seconds for startup
sleep 10

# Verify it's running
curl http://localhost:8000/health
```

### Import Errors
```bash
# Install required packages
pip install rich requests

# Or use requirements.txt
cd /workspaces/terminal/cli
pip install -r requirements.txt
```

### No Data Showing
- Wait a few seconds after Service Mesh starts
- Press `r` to refresh manually
- Check Service Mesh logs: `docker logs ose-service-mesh`

### Connection Refused
```bash
# Check if Service Mesh container is running
docker ps | grep service-mesh

# Check logs for errors
docker logs ose-service-mesh

# Restart if needed
docker-compose restart service-mesh
```

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- **Number keys (1-12)**: Quick service selection
- **r**: Instant refresh
- **b**: Back to previous menu
- **q**: Quit application
- **h**: Help screen

### Best Practices
1. **Start Service Mesh first** before launching TUI
2. **Use `r` command** to refresh data periodically
3. **Try NLP queries** for quick information
4. **Check AI recommendations** regularly for optimization tips
5. **Use `web` command** to switch to browser view when needed

### Example Workflow
```bash
# 1. Start infrastructure
docker-compose up -d service-mesh

# 2. Launch TUI
python3 cli/ose_tui.py

# 3. In TUI:
#    - Press 1 (Service Mesh)
#    - Press ai (View recommendations)
#    - Press nlp (Ask questions)
#    - Press 1-12 (Check service details)
#    - Press r (Refresh status)
#    - Press b (Back to main menu)
```

---

## 📚 Related Documentation

- [Service Mesh Advanced README](../modules/service-mesh/ADVANCED_README.md)
- [Service Mesh Deployment Guide](../DEPLOY_SERVICE_MESH.md)
- [TUI Interface Documentation](../docs/TUI_INTERFACE.md)
- [Microservices Architecture](../docs/MICROSERVICES_ARCHITECTURE.md)

---

## 🎉 Summary

The TUI Service Mesh integration provides:

1. **Real-time Monitoring** - Live service status, health scores, metrics
2. **AI Features** - Recommendations, NLP queries, intelligent insights
3. **Interactive Commands** - Service details, topology, web integration
4. **Beautiful UI** - Color-coded tables, status badges, panels
5. **Seamless Integration** - Uses same backend API as web dashboard

**Access methods:**
```bash
# Terminal Interface
python3 cli/ose_tui.py

# Web Interface
open http://localhost:8000
```

Both provide the same powerful features in different formats! 🚀
