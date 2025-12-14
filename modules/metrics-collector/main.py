"""
📊 OSE Metrics Collector Service
Real-time system metrics collection and monitoring

Features:
- Real-time metric collection
- Prometheus integration
- System performance monitoring
- Resource usage tracking
- Alert management
- Historical data storage
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import psutil
import platform
from pathlib import Path
import json

app = FastAPI(
    title="OSE Metrics Collector Service",
    description="Real-time System Metrics Collection and Monitoring",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Models ====================

class MetricType(str, Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    PROCESS = "process"
    SYSTEM = "system"


class SystemMetrics(BaseModel):
    timestamp: str
    cpu_percent: float
    cpu_count: int
    cpu_freq_current: Optional[float]
    memory_total_gb: float
    memory_used_gb: float
    memory_percent: float
    swap_total_gb: float
    swap_used_gb: float
    swap_percent: float
    disk_total_gb: float
    disk_used_gb: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float
    boot_time: str
    uptime_hours: float


class ProcessMetrics(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    num_threads: int


class MetricAlert(BaseModel):
    id: str
    metric_type: MetricType
    threshold: float
    current_value: float
    severity: str  # info, warning, critical
    message: str
    timestamp: str


# ==================== Metrics Collection ====================

def collect_system_metrics() -> SystemMetrics:
    """Collect current system metrics"""
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    cpu_freq_current = cpu_freq.current if cpu_freq else None
    
    # Memory
    mem = psutil.virtual_memory()
    memory_total_gb = mem.total / (1024**3)
    memory_used_gb = mem.used / (1024**3)
    memory_percent = mem.percent
    
    # Swap
    swap = psutil.swap_memory()
    swap_total_gb = swap.total / (1024**3)
    swap_used_gb = swap.used / (1024**3)
    swap_percent = swap.percent
    
    # Disk
    disk = psutil.disk_usage('/')
    disk_total_gb = disk.total / (1024**3)
    disk_used_gb = disk.used / (1024**3)
    disk_percent = disk.percent
    
    # Network
    net_io = psutil.net_io_counters()
    network_sent_mb = net_io.bytes_sent / (1024**2)
    network_recv_mb = net_io.bytes_recv / (1024**2)
    
    # System
    boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()
    uptime_hours = (datetime.now().timestamp() - psutil.boot_time()) / 3600
    
    return SystemMetrics(
        timestamp=datetime.now().isoformat(),
        cpu_percent=cpu_percent,
        cpu_count=cpu_count,
        cpu_freq_current=cpu_freq_current,
        memory_total_gb=round(memory_total_gb, 2),
        memory_used_gb=round(memory_used_gb, 2),
        memory_percent=memory_percent,
        swap_total_gb=round(swap_total_gb, 2),
        swap_used_gb=round(swap_used_gb, 2),
        swap_percent=swap_percent,
        disk_total_gb=round(disk_total_gb, 2),
        disk_used_gb=round(disk_used_gb, 2),
        disk_percent=disk_percent,
        network_sent_mb=round(network_sent_mb, 2),
        network_recv_mb=round(network_recv_mb, 2),
        boot_time=boot_time,
        uptime_hours=round(uptime_hours, 2)
    )


def collect_top_processes(limit: int = 10) -> List[ProcessMetrics]:
    """Collect metrics for top processes by CPU usage"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'status', 'num_threads']):
        try:
            pinfo = proc.info
            processes.append(ProcessMetrics(
                pid=pinfo['pid'],
                name=pinfo['name'],
                cpu_percent=pinfo['cpu_percent'] or 0.0,
                memory_percent=pinfo['memory_percent'] or 0.0,
                memory_mb=round(pinfo['memory_info'].rss / (1024**2), 2) if pinfo['memory_info'] else 0.0,
                status=pinfo['status'],
                num_threads=pinfo['num_threads'] or 0
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x.cpu_percent, reverse=True)
    return processes[:limit]


def check_alerts(metrics: SystemMetrics) -> List[MetricAlert]:
    """Check metrics against thresholds and generate alerts"""
    alerts = []
    
    # CPU alerts
    if metrics.cpu_percent > 90:
        alerts.append(MetricAlert(
            id=f"cpu_{datetime.now().timestamp()}",
            metric_type=MetricType.CPU,
            threshold=90.0,
            current_value=metrics.cpu_percent,
            severity="critical",
            message=f"CPU usage critical: {metrics.cpu_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    elif metrics.cpu_percent > 75:
        alerts.append(MetricAlert(
            id=f"cpu_{datetime.now().timestamp()}",
            metric_type=MetricType.CPU,
            threshold=75.0,
            current_value=metrics.cpu_percent,
            severity="warning",
            message=f"CPU usage high: {metrics.cpu_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    
    # Memory alerts
    if metrics.memory_percent > 90:
        alerts.append(MetricAlert(
            id=f"memory_{datetime.now().timestamp()}",
            metric_type=MetricType.MEMORY,
            threshold=90.0,
            current_value=metrics.memory_percent,
            severity="critical",
            message=f"Memory usage critical: {metrics.memory_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    elif metrics.memory_percent > 75:
        alerts.append(MetricAlert(
            id=f"memory_{datetime.now().timestamp()}",
            metric_type=MetricType.MEMORY,
            threshold=75.0,
            current_value=metrics.memory_percent,
            severity="warning",
            message=f"Memory usage high: {metrics.memory_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    
    # Disk alerts
    if metrics.disk_percent > 90:
        alerts.append(MetricAlert(
            id=f"disk_{datetime.now().timestamp()}",
            metric_type=MetricType.DISK,
            threshold=90.0,
            current_value=metrics.disk_percent,
            severity="critical",
            message=f"Disk usage critical: {metrics.disk_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    elif metrics.disk_percent > 80:
        alerts.append(MetricAlert(
            id=f"disk_{datetime.now().timestamp()}",
            metric_type=MetricType.DISK,
            threshold=80.0,
            current_value=metrics.disk_percent,
            severity="warning",
            message=f"Disk usage high: {metrics.disk_percent}%",
            timestamp=datetime.now().isoformat()
        ))
    
    return alerts


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSE Metrics Collector Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "metrics": "/api/v1/metrics",
            "processes": "/api/v1/metrics/processes",
            "alerts": "/api/v1/metrics/alerts",
            "prometheus": "/metrics",
            "docs": "/docs"
        }
    }


@app.get("/api/v1/metrics", response_model=SystemMetrics)
async def get_metrics():
    """Get current system metrics"""
    return collect_system_metrics()


@app.get("/api/v1/metrics/processes")
async def get_process_metrics(limit: int = 10):
    """Get top processes by CPU usage"""
    processes = collect_top_processes(limit)
    return {
        "timestamp": datetime.now().isoformat(),
        "total_processes": len(list(psutil.process_iter())),
        "top_processes": processes
    }


@app.get("/api/v1/metrics/alerts")
async def get_alerts():
    """Get current metric alerts"""
    metrics = collect_system_metrics()
    alerts = check_alerts(metrics)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "alert_count": len(alerts),
        "alerts": alerts
    }


@app.get("/api/v1/metrics/system-info")
async def get_system_info():
    """Get static system information"""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/v1/metrics/history")
async def get_metrics_history(minutes: int = 60):
    """
    Get metrics history (simulated - in production would query database)
    """
    # This would query a time-series database in production
    # For now, return current metrics as example
    current = collect_system_metrics()
    
    return {
        "time_range_minutes": minutes,
        "data_points": 1,
        "metrics": [current],
        "note": "Historical metrics require time-series database (Prometheus/InfluxDB)"
    }


@app.get("/metrics")
async def prometheus_metrics():
    """
    Prometheus-compatible metrics endpoint
    """
    metrics = collect_system_metrics()
    
    # Prometheus format
    output = f"""# HELP ose_cpu_percent CPU usage percentage
# TYPE ose_cpu_percent gauge
ose_cpu_percent {metrics.cpu_percent}

# HELP ose_memory_percent Memory usage percentage
# TYPE ose_memory_percent gauge
ose_memory_percent {metrics.memory_percent}

# HELP ose_memory_used_gb Memory used in GB
# TYPE ose_memory_used_gb gauge
ose_memory_used_gb {metrics.memory_used_gb}

# HELP ose_disk_percent Disk usage percentage
# TYPE ose_disk_percent gauge
ose_disk_percent {metrics.disk_percent}

# HELP ose_disk_used_gb Disk used in GB
# TYPE ose_disk_used_gb gauge
ose_disk_used_gb {metrics.disk_used_gb}

# HELP ose_network_sent_mb Network sent in MB
# TYPE ose_network_sent_mb counter
ose_network_sent_mb {metrics.network_sent_mb}

# HELP ose_network_recv_mb Network received in MB
# TYPE ose_network_recv_mb counter
ose_network_recv_mb {metrics.network_recv_mb}

# HELP ose_uptime_hours System uptime in hours
# TYPE ose_uptime_hours gauge
ose_uptime_hours {metrics.uptime_hours}
"""
    
    return output


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "metrics-collector"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
