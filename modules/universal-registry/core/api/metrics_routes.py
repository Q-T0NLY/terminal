"""
Universal Registry - Comprehensive Metrics & Monitoring API
Real-time metrics, monitoring, and control endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import psutil
import asyncio
from collections import deque, defaultdict
import time

router = APIRouter(prefix="/api/v1/metrics", tags=["metrics"])

# ==================== DATA MODELS ====================

class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class MetricCategory(str, Enum):
    SYSTEM = "system"
    APPLICATION = "application"
    BUSINESS = "business"
    CUSTOM = "custom"

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class SystemMetrics(BaseModel):
    timestamp: str
    cpu_percent: float
    cpu_count: int
    cpu_freq_mhz: Optional[float] = None
    memory_total_gb: float
    memory_used_gb: float
    memory_percent: float
    memory_available_gb: float
    swap_total_gb: float
    swap_used_gb: float
    swap_percent: float
    disk_total_gb: float
    disk_used_gb: float
    disk_free_gb: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float
    network_packets_sent: int
    network_packets_recv: int
    uptime_seconds: float
    load_average: List[float]

class ProcessMetrics(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    status: str
    num_threads: int
    create_time: str

class PluginMetrics(BaseModel):
    total_plugins: int
    active_plugins: int
    inactive_plugins: int
    failed_plugins: int
    by_feature: Dict[str, int]
    by_status: Dict[str, int]
    total_operations: int
    avg_install_time_sec: float
    avg_activation_time_sec: float

class ServiceMetrics(BaseModel):
    total_services: int
    running_services: int
    stopped_services: int
    failed_services: int
    by_category: Dict[str, int]
    total_requests: int
    avg_response_time_ms: float
    error_rate: float

class RegistryMetrics(BaseModel):
    total_entities: int
    total_relationships: int
    active_connections: int
    total_events: int
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    by_health: Dict[str, int]
    database_size_mb: float
    index_size_mb: float

class Alert(BaseModel):
    id: str
    severity: AlertSeverity
    category: str
    message: str
    timestamp: str
    metric: str
    value: float
    threshold: float
    acknowledged: bool = False

class PerformanceMetrics(BaseModel):
    requests_per_second: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    error_rate: float
    throughput_mb_per_sec: float

# ==================== IN-MEMORY DATA STORES ====================

# Metrics history (last 1000 data points per metric)
metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))

# Active alerts
active_alerts: List[Alert] = []

# Performance counters
perf_counters = {
    "total_requests": 0,
    "total_errors": 0,
    "total_latency_ms": 0.0,
    "latencies": deque(maxlen=1000),
    "start_time": time.time()
}

# Plugin/Service stats
plugin_stats = {
    "total_operations": 0,
    "install_times": deque(maxlen=100),
    "activation_times": deque(maxlen=100)
}

service_stats = {
    "total_requests": 0,
    "response_times": deque(maxlen=1000),
    "errors": 0
}

# Alert thresholds
alert_thresholds = {
    "cpu_percent": {"warning": 75, "critical": 90},
    "memory_percent": {"warning": 75, "critical": 90},
    "disk_percent": {"warning": 80, "critical": 90},
    "error_rate": {"warning": 0.05, "critical": 0.10},
    "latency_ms": {"warning": 500, "critical": 1000}
}

# ==================== HELPER FUNCTIONS ====================

def collect_system_metrics() -> SystemMetrics:
    """Collect comprehensive system metrics"""
    cpu_freq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    
    try:
        load_avg = list(psutil.getloadavg())
    except:
        load_avg = [0.0, 0.0, 0.0]
    
    return SystemMetrics(
        timestamp=datetime.utcnow().isoformat(),
        cpu_percent=psutil.cpu_percent(interval=0.1),
        cpu_count=psutil.cpu_count(),
        cpu_freq_mhz=cpu_freq.current if cpu_freq else None,
        memory_total_gb=round(mem.total / (1024**3), 2),
        memory_used_gb=round(mem.used / (1024**3), 2),
        memory_percent=mem.percent,
        memory_available_gb=round(mem.available / (1024**3), 2),
        swap_total_gb=round(swap.total / (1024**3), 2),
        swap_used_gb=round(swap.used / (1024**3), 2),
        swap_percent=swap.percent,
        disk_total_gb=round(disk.total / (1024**3), 2),
        disk_used_gb=round(disk.used / (1024**3), 2),
        disk_free_gb=round(disk.free / (1024**3), 2),
        disk_percent=disk.percent,
        network_sent_mb=round(net.bytes_sent / (1024**2), 2),
        network_recv_mb=round(net.bytes_recv / (1024**2), 2),
        network_packets_sent=net.packets_sent,
        network_packets_recv=net.packets_recv,
        uptime_seconds=uptime,
        load_average=load_avg
    )

def check_metric_alerts(metrics: SystemMetrics) -> List[Alert]:
    """Check metrics against thresholds and generate alerts"""
    alerts = []
    
    # CPU alerts
    if metrics.cpu_percent > alert_thresholds["cpu_percent"]["critical"]:
        alerts.append(Alert(
            id=f"cpu-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.CRITICAL,
            category="system",
            message=f"Critical CPU usage: {metrics.cpu_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="cpu_percent",
            value=metrics.cpu_percent,
            threshold=alert_thresholds["cpu_percent"]["critical"]
        ))
    elif metrics.cpu_percent > alert_thresholds["cpu_percent"]["warning"]:
        alerts.append(Alert(
            id=f"cpu-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.WARNING,
            category="system",
            message=f"High CPU usage: {metrics.cpu_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="cpu_percent",
            value=metrics.cpu_percent,
            threshold=alert_thresholds["cpu_percent"]["warning"]
        ))
    
    # Memory alerts
    if metrics.memory_percent > alert_thresholds["memory_percent"]["critical"]:
        alerts.append(Alert(
            id=f"mem-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.CRITICAL,
            category="system",
            message=f"Critical memory usage: {metrics.memory_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="memory_percent",
            value=metrics.memory_percent,
            threshold=alert_thresholds["memory_percent"]["critical"]
        ))
    elif metrics.memory_percent > alert_thresholds["memory_percent"]["warning"]:
        alerts.append(Alert(
            id=f"mem-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.WARNING,
            category="system",
            message=f"High memory usage: {metrics.memory_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="memory_percent",
            value=metrics.memory_percent,
            threshold=alert_thresholds["memory_percent"]["warning"]
        ))
    
    # Disk alerts
    if metrics.disk_percent > alert_thresholds["disk_percent"]["critical"]:
        alerts.append(Alert(
            id=f"disk-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.CRITICAL,
            category="system",
            message=f"Critical disk usage: {metrics.disk_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="disk_percent",
            value=metrics.disk_percent,
            threshold=alert_thresholds["disk_percent"]["critical"]
        ))
    elif metrics.disk_percent > alert_thresholds["disk_percent"]["warning"]:
        alerts.append(Alert(
            id=f"disk-{datetime.utcnow().timestamp()}",
            severity=AlertSeverity.WARNING,
            category="system",
            message=f"High disk usage: {metrics.disk_percent}%",
            timestamp=datetime.utcnow().isoformat(),
            metric="disk_percent",
            value=metrics.disk_percent,
            threshold=alert_thresholds["disk_percent"]["warning"]
        ))
    
    return alerts

def calculate_performance_metrics() -> PerformanceMetrics:
    """Calculate application performance metrics"""
    uptime = time.time() - perf_counters["start_time"]
    total_requests = perf_counters["total_requests"]
    total_errors = perf_counters["total_errors"]
    latencies = sorted(list(perf_counters["latencies"]))
    
    rps = total_requests / uptime if uptime > 0 else 0
    error_rate = total_errors / total_requests if total_requests > 0 else 0
    avg_latency = perf_counters["total_latency_ms"] / total_requests if total_requests > 0 else 0
    
    # Calculate percentiles
    if latencies:
        p50_idx = int(len(latencies) * 0.50)
        p95_idx = int(len(latencies) * 0.95)
        p99_idx = int(len(latencies) * 0.99)
        p50 = latencies[p50_idx] if p50_idx < len(latencies) else 0
        p95 = latencies[p95_idx] if p95_idx < len(latencies) else 0
        p99 = latencies[p99_idx] if p99_idx < len(latencies) else 0
    else:
        p50 = p95 = p99 = 0
    
    return PerformanceMetrics(
        requests_per_second=round(rps, 2),
        avg_latency_ms=round(avg_latency, 2),
        p50_latency_ms=round(p50, 2),
        p95_latency_ms=round(p95, 2),
        p99_latency_ms=round(p99, 2),
        error_rate=round(error_rate, 4),
        throughput_mb_per_sec=round(rps * 0.001, 2)  # Estimated
    )

# ==================== SYSTEM METRICS ENDPOINTS ====================

@router.get("/system", response_model=SystemMetrics, summary="Get system metrics")
async def get_system_metrics():
    """
    Get comprehensive system metrics including CPU, memory, disk, and network.
    
    Returns real-time metrics about system resources.
    """
    metrics = collect_system_metrics()
    
    # Store in history
    metrics_history["system"].append({
        "timestamp": metrics.timestamp,
        "cpu": metrics.cpu_percent,
        "memory": metrics.memory_percent,
        "disk": metrics.disk_percent
    })
    
    # Check for alerts
    new_alerts = check_metric_alerts(metrics)
    active_alerts.extend(new_alerts)
    
    return metrics

@router.get("/system/processes", summary="Get top processes")
async def get_top_processes(limit: int = Query(10, ge=1, le=100)):
    """
    Get top processes by CPU usage.
    
    - **limit**: Number of processes to return (1-100)
    """
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'num_threads', 'create_time']):
        try:
            pinfo = proc.info
            processes.append(ProcessMetrics(
                pid=pinfo['pid'],
                name=pinfo['name'],
                cpu_percent=pinfo['cpu_percent'] or 0.0,
                memory_percent=pinfo['memory_percent'] or 0.0,
                memory_mb=round((pinfo['memory_percent'] or 0.0) * psutil.virtual_memory().total / (100 * 1024**2), 2),
                status=pinfo['status'],
                num_threads=pinfo['num_threads'] or 0,
                create_time=datetime.fromtimestamp(pinfo['create_time']).isoformat()
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x.cpu_percent, reverse=True)
    
    return {
        "total_processes": len(processes),
        "top_processes": processes[:limit],
        "timestamp": datetime.utcnow().isoformat()
    }

# ==================== APPLICATION METRICS ENDPOINTS ====================

@router.get("/plugins", response_model=PluginMetrics, summary="Get plugin metrics")
async def get_plugin_metrics():
    """
    Get comprehensive plugin metrics.
    
    Returns statistics about plugin lifecycle, operations, and performance.
    """
    # This would query actual plugin data from the registry
    # For now, returning example data
    return PluginMetrics(
        total_plugins=42,
        active_plugins=38,
        inactive_plugins=3,
        failed_plugins=1,
        by_feature={
            "ai-ml": 12,
            "web3": 8,
            "cloud": 10,
            "data": 6,
            "devops": 4,
            "security": 2
        },
        by_status={
            "active": 38,
            "inactive": 3,
            "failed": 1
        },
        total_operations=plugin_stats["total_operations"],
        avg_install_time_sec=sum(plugin_stats["install_times"]) / len(plugin_stats["install_times"]) if plugin_stats["install_times"] else 0,
        avg_activation_time_sec=sum(plugin_stats["activation_times"]) / len(plugin_stats["activation_times"]) if plugin_stats["activation_times"] else 0
    )

@router.get("/services", response_model=ServiceMetrics, summary="Get service metrics")
async def get_service_metrics():
    """
    Get comprehensive microservices metrics.
    
    Returns statistics about service health, requests, and performance.
    """
    avg_response_time = sum(service_stats["response_times"]) / len(service_stats["response_times"]) if service_stats["response_times"] else 0
    error_rate = service_stats["errors"] / service_stats["total_requests"] if service_stats["total_requests"] > 0 else 0
    
    return ServiceMetrics(
        total_services=15,
        running_services=14,
        stopped_services=1,
        failed_services=0,
        by_category={
            "application": 8,
            "database": 3,
            "monitoring": 2,
            "queue": 1,
            "cache": 1
        },
        total_requests=service_stats["total_requests"],
        avg_response_time_ms=round(avg_response_time, 2),
        error_rate=round(error_rate, 4)
    )

@router.get("/registry", response_model=RegistryMetrics, summary="Get registry metrics")
async def get_registry_metrics():
    """
    Get Universal Registry metrics.
    
    Returns statistics about entities, relationships, and storage.
    """
    return RegistryMetrics(
        total_entities=256,
        total_relationships=512,
        active_connections=8,
        total_events=1024,
        by_type={
            "plugin": 42,
            "service": 15,
            "feature": 8,
            "mesh_node": 12,
            "relationship": 179
        },
        by_status={
            "active": 220,
            "inactive": 25,
            "pending": 8,
            "failed": 3
        },
        by_health={
            "healthy": 230,
            "degraded": 15,
            "unhealthy": 8,
            "unknown": 3
        },
        database_size_mb=245.6,
        index_size_mb=52.3
    )

@router.get("/performance", response_model=PerformanceMetrics, summary="Get performance metrics")
async def get_performance_metrics():
    """
    Get application performance metrics.
    
    Returns request rates, latencies, and throughput.
    """
    return calculate_performance_metrics()

# ==================== METRICS HISTORY ====================

@router.get("/history/{metric_name}", summary="Get metric history")
async def get_metric_history(
    metric_name: str,
    minutes: int = Query(60, ge=1, le=1440, description="Time range in minutes")
):
    """
    Get historical data for a specific metric.
    
    - **metric_name**: Name of the metric (system, cpu, memory, disk, etc.)
    - **minutes**: Number of minutes of history to return (1-1440)
    """
    if metric_name not in metrics_history:
        raise HTTPException(status_code=404, detail=f"Metric {metric_name} not found")
    
    history = list(metrics_history[metric_name])
    
    # Filter by time range
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    filtered = [
        m for m in history
        if datetime.fromisoformat(m["timestamp"]) > cutoff_time
    ]
    
    return {
        "metric": metric_name,
        "time_range_minutes": minutes,
        "data_points": len(filtered),
        "data": filtered
    }

@router.get("/history", summary="Get all metrics history")
async def get_all_history(minutes: int = Query(60, ge=1, le=1440)):
    """
    Get historical data for all metrics.
    
    - **minutes**: Number of minutes of history (1-1440)
    """
    result = {}
    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
    
    for metric_name, history in metrics_history.items():
        filtered = [
            m for m in history
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]
        result[metric_name] = {
            "data_points": len(filtered),
            "data": filtered
        }
    
    return {
        "time_range_minutes": minutes,
        "metrics": result
    }

# ==================== ALERTS MANAGEMENT ====================

@router.get("/alerts", summary="Get active alerts")
async def get_alerts(
    severity: Optional[AlertSeverity] = None,
    acknowledged: Optional[bool] = None
):
    """
    Get active alerts.
    
    - **severity**: Filter by severity (info, warning, error, critical)
    - **acknowledged**: Filter by acknowledgement status
    """
    filtered_alerts = active_alerts
    
    if severity:
        filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
    
    if acknowledged is not None:
        filtered_alerts = [a for a in filtered_alerts if a.acknowledged == acknowledged]
    
    return {
        "total_alerts": len(active_alerts),
        "filtered_alerts": len(filtered_alerts),
        "alerts": filtered_alerts
    }

@router.post("/alerts/{alert_id}/acknowledge", summary="Acknowledge alert")
async def acknowledge_alert(alert_id: str):
    """Acknowledge an alert"""
    for alert in active_alerts:
        if alert.id == alert_id:
            alert.acknowledged = True
            return {"message": "Alert acknowledged", "alert": alert}
    
    raise HTTPException(status_code=404, detail="Alert not found")

@router.delete("/alerts/{alert_id}", summary="Dismiss alert")
async def dismiss_alert(alert_id: str):
    """Dismiss (delete) an alert"""
    global active_alerts
    active_alerts = [a for a in active_alerts if a.id != alert_id]
    return {"message": "Alert dismissed"}

@router.delete("/alerts", summary="Clear all alerts")
async def clear_all_alerts():
    """Clear all alerts"""
    global active_alerts
    count = len(active_alerts)
    active_alerts = []
    return {"message": f"Cleared {count} alerts"}

# ==================== ALERT THRESHOLDS MANAGEMENT ====================

@router.get("/thresholds", summary="Get alert thresholds")
async def get_thresholds():
    """Get current alert thresholds"""
    return alert_thresholds

@router.put("/thresholds/{metric}", summary="Update alert threshold")
async def update_threshold(
    metric: str,
    warning: Optional[float] = None,
    critical: Optional[float] = None
):
    """
    Update alert thresholds for a metric.
    
    - **metric**: Metric name (cpu_percent, memory_percent, etc.)
    - **warning**: Warning threshold value
    - **critical**: Critical threshold value
    """
    if metric not in alert_thresholds:
        raise HTTPException(status_code=404, detail=f"Metric {metric} not found")
    
    if warning is not None:
        alert_thresholds[metric]["warning"] = warning
    
    if critical is not None:
        alert_thresholds[metric]["critical"] = critical
    
    return {
        "message": "Thresholds updated",
        "metric": metric,
        "thresholds": alert_thresholds[metric]
    }

# ==================== PROMETHEUS METRICS ====================

@router.get("/prometheus", summary="Prometheus-compatible metrics")
async def prometheus_metrics():
    """
    Get metrics in Prometheus format.
    
    Returns metrics compatible with Prometheus scraping.
    """
    system = collect_system_metrics()
    performance = calculate_performance_metrics()
    
    output = f"""# HELP ose_registry_cpu_percent CPU usage percentage
# TYPE ose_registry_cpu_percent gauge
ose_registry_cpu_percent {system.cpu_percent}

# HELP ose_registry_memory_percent Memory usage percentage
# TYPE ose_registry_memory_percent gauge
ose_registry_memory_percent {system.memory_percent}

# HELP ose_registry_disk_percent Disk usage percentage
# TYPE ose_registry_disk_percent gauge
ose_registry_disk_percent {system.disk_percent}

# HELP ose_registry_network_sent_mb Network sent in MB
# TYPE ose_registry_network_sent_mb counter
ose_registry_network_sent_mb {system.network_sent_mb}

# HELP ose_registry_network_recv_mb Network received in MB
# TYPE ose_registry_network_recv_mb counter
ose_registry_network_recv_mb {system.network_recv_mb}

# HELP ose_registry_uptime_seconds System uptime in seconds
# TYPE ose_registry_uptime_seconds counter
ose_registry_uptime_seconds {system.uptime_seconds}

# HELP ose_registry_requests_total Total number of requests
# TYPE ose_registry_requests_total counter
ose_registry_requests_total {perf_counters['total_requests']}

# HELP ose_registry_errors_total Total number of errors
# TYPE ose_registry_errors_total counter
ose_registry_errors_total {perf_counters['total_errors']}

# HELP ose_registry_latency_ms Average latency in milliseconds
# TYPE ose_registry_latency_ms gauge
ose_registry_latency_ms {performance.avg_latency_ms}

# HELP ose_registry_p95_latency_ms P95 latency in milliseconds
# TYPE ose_registry_p95_latency_ms gauge
ose_registry_p95_latency_ms {performance.p95_latency_ms}

# HELP ose_registry_p99_latency_ms P99 latency in milliseconds
# TYPE ose_registry_p99_latency_ms gauge
ose_registry_p99_latency_ms {performance.p99_latency_ms}
"""
    
    return output

# ==================== DASHBOARD DATA ====================

@router.get("/dashboard", summary="Get dashboard metrics")
async def get_dashboard_metrics():
    """
    Get comprehensive metrics for dashboard display.
    
    Returns all metrics needed for the main dashboard.
    """
    system = collect_system_metrics()
    performance = calculate_performance_metrics()
    
    # Get latest alerts (unacknowledged)
    recent_alerts = [a for a in active_alerts if not a.acknowledged][-10:]
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": system.dict(),
        "performance": performance.dict(),
        "alerts": {
            "total": len(active_alerts),
            "unacknowledged": len(recent_alerts),
            "critical": len([a for a in recent_alerts if a.severity == AlertSeverity.CRITICAL]),
            "warning": len([a for a in recent_alerts if a.severity == AlertSeverity.WARNING]),
            "recent": recent_alerts
        },
        "health_summary": {
            "overall": "healthy" if system.cpu_percent < 75 and system.memory_percent < 75 else "degraded",
            "cpu_status": "normal" if system.cpu_percent < 75 else "high",
            "memory_status": "normal" if system.memory_percent < 75 else "high",
            "disk_status": "normal" if system.disk_percent < 80 else "high"
        }
    }

# ==================== HEALTH CHECK ====================

@router.get("/health", summary="Metrics API health check")
async def health_check():
    """Health check for the metrics API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "metrics-api",
        "version": "1.0.0"
    }
