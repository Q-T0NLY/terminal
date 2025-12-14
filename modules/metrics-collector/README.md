# 📊 Metrics Collector Service

**Real-time System Metrics Collection and Monitoring**

## Features

### Metrics Collection
- **CPU Metrics** - Usage, frequency, core count
- **Memory Metrics** - RAM, swap, usage percentages
- **Disk Metrics** - Usage, I/O, capacity
- **Network Metrics** - Sent/received data, connections
- **Process Metrics** - Top processes, resource usage
- **System Info** - Platform, uptime, architecture

### Monitoring Integration
- **Prometheus Compatible** - `/metrics` endpoint
- **Real-time Alerts** - Threshold-based alerting
- **Historical Data** - Time-series data (with database)
- **Custom Dashboards** - Grafana/Prometheus integration

## Quick Start

```bash
# Build
docker build -t ose/metrics-collector .

# Run
docker run -p 8006:8006 ose/metrics-collector
```

## API Endpoints

### GET /api/v1/metrics
Get current system metrics

**Response:**
```json
{
  "timestamp": "2025-12-13T23:15:00",
  "cpu_percent": 45.2,
  "cpu_count": 8,
  "memory_total_gb": 16.0,
  "memory_used_gb": 8.5,
  "memory_percent": 53.1,
  "disk_total_gb": 500.0,
  "disk_used_gb": 250.0,
  "disk_percent": 50.0,
  "network_sent_mb": 1024.5,
  "network_recv_mb": 2048.3,
  "uptime_hours": 48.5
}
```

### GET /api/v1/metrics/processes
Get top processes by CPU usage

**Parameters:**
- `limit` (int, default: 10) - Number of processes to return

**Response:**
```json
{
  "timestamp": "2025-12-13T23:15:00",
  "total_processes": 245,
  "top_processes": [
    {
      "pid": 1234,
      "name": "python",
      "cpu_percent": 25.5,
      "memory_percent": 5.2,
      "memory_mb": 850.3,
      "status": "running",
      "num_threads": 4
    }
  ]
}
```

### GET /api/v1/metrics/alerts
Get current metric alerts

**Response:**
```json
{
  "timestamp": "2025-12-13T23:15:00",
  "alert_count": 2,
  "alerts": [
    {
      "id": "cpu_1702507500",
      "metric_type": "cpu",
      "threshold": 75.0,
      "current_value": 85.3,
      "severity": "warning",
      "message": "CPU usage high: 85.3%",
      "timestamp": "2025-12-13T23:15:00"
    }
  ]
}
```

### GET /api/v1/metrics/system-info
Get static system information

**Response:**
```json
{
  "platform": "Linux",
  "platform_release": "6.8.0",
  "architecture": "x86_64",
  "processor": "Intel Core i7",
  "hostname": "server-01",
  "cpu_count_physical": 4,
  "cpu_count_logical": 8
}
```

### GET /metrics
Prometheus-compatible metrics endpoint

Returns metrics in Prometheus exposition format for scraping.

## Alert Thresholds

### CPU Alerts
- **Warning**: > 75% usage
- **Critical**: > 90% usage

### Memory Alerts
- **Warning**: > 75% usage
- **Critical**: > 90% usage

### Disk Alerts
- **Warning**: > 80% usage
- **Critical**: > 90% usage

## Prometheus Integration

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'ose-metrics'
    static_configs:
      - targets: ['metrics-collector:8006']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

## Docker Compose Integration

```yaml
metrics-collector:
  build:
    context: ./modules/metrics-collector
    dockerfile: Dockerfile
  container_name: ose-metrics-collector
  ports:
    - "8006:8006"
  restart: unless-stopped
```

## Usage Examples

```bash
# Get current metrics
curl http://localhost:8006/api/v1/metrics

# Get top 5 processes
curl http://localhost:8006/api/v1/metrics/processes?limit=5

# Check alerts
curl http://localhost:8006/api/v1/metrics/alerts

# Prometheus metrics
curl http://localhost:8006/metrics
```

## Interactive Docs

http://localhost:8006/docs
