"""
Service Mesh API Routes
Advanced traffic management, tracing, and load balancing
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/mesh", tags=["service-mesh"])

# ==================== DATA MODELS ====================

class RouteType(str, Enum):
    HTTP = "http"
    GRPC = "grpc"
    TCP = "tcp"
    WEBSOCKET = "websocket"

class LoadBalancerType(str, Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONN = "least_conn"
    IP_HASH = "ip_hash"
    WEIGHTED = "weighted"
    RANDOM = "random"

class CircuitBreakerState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class TrafficSplitStrategy(str, Enum):
    PERCENTAGE = "percentage"
    HEADER = "header"
    COOKIE = "cookie"
    AB_TEST = "ab_test"

class RouteInfo(BaseModel):
    id: str
    name: str
    type: RouteType
    path: str
    destination: str
    weight: int = 100
    timeout: int = 30
    retries: int = 3
    metadata: Dict[str, Any] = {}

class RouteCreate(BaseModel):
    name: str
    type: RouteType
    path: str
    destination: str
    weight: int = 100
    timeout: int = 30
    retries: int = 3

class LoadBalancerConfig(BaseModel):
    type: LoadBalancerType = LoadBalancerType.ROUND_ROBIN
    health_check_interval: int = 30
    health_check_timeout: int = 10
    health_check_path: str = "/health"

class CircuitBreakerConfig(BaseModel):
    enabled: bool = False
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: int = 60
    half_open_requests: int = 3

class RetryPolicy(BaseModel):
    max_attempts: int = 3
    timeout: int = 30
    backoff_multiplier: float = 2.0
    retryable_status_codes: List[int] = [500, 502, 503, 504]

class TrafficSplit(BaseModel):
    service_a: str
    service_b: str
    percentage_a: int = 50
    percentage_b: int = 50
    strategy: TrafficSplitStrategy = TrafficSplitStrategy.PERCENTAGE

# ==================== REGISTRY ====================

mesh_routes: Dict[str, Dict[str, Any]] = {}
mesh_lb_configs: Dict[str, Dict[str, Any]] = {}
mesh_circuit_breakers: Dict[str, Dict[str, Any]] = {}
mesh_retry_policies: Dict[str, Dict[str, Any]] = {}
mesh_traffic_splits: Dict[str, Dict[str, Any]] = {}
mesh_traces: Dict[str, List[Dict[str, Any]]] = {}
mesh_metrics: Dict[str, Dict[str, Any]] = {}

def log_mesh_event(route_id: str, level: str, message: str):
    """Log mesh events"""
    if route_id not in mesh_traces:
        mesh_traces[route_id] = []
    
    mesh_traces[route_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(mesh_traces[route_id]) > 1000:
        mesh_traces[route_id] = mesh_traces[route_id][-1000:]

# ==================== ROUTE MANAGEMENT ====================

@router.get("/routes", summary="List all routes")
async def list_routes(
    type: Optional[RouteType] = Query(None),
    path_prefix: Optional[str] = Query(None)
):
    """List all mesh routes"""
    result = list(mesh_routes.values())
    
    if type:
        result = [r for r in result if r.get("type") == type.value]
    if path_prefix:
        result = [r for r in result if r.get("path", "").startswith(path_prefix)]
    
    return {
        "total": len(result),
        "routes": result
    }

@router.post("/routes", summary="Add route")
async def add_route(route: RouteCreate):
    """Add a new mesh route"""
    route_id = f"route_{route.name.lower().replace(' ', '-')}"
    
    if route_id in mesh_routes:
        raise HTTPException(status_code=409, detail="Route already exists")
    
    route_data = route.dict()
    route_data["id"] = route_id
    route_data["created_at"] = datetime.utcnow().isoformat()
    route_data["metadata"] = {}
    
    # Initialize metrics
    mesh_metrics[route_id] = {
        "requests": 0,
        "successes": 0,
        "failures": 0,
        "avg_latency": 0.0,
        "total_latency": 0.0
    }
    
    mesh_routes[route_id] = route_data
    log_mesh_event(route_id, "INFO", f"Route added: {route.path} -> {route.destination}")
    
    return {
        "message": "Route added successfully",
        "route_id": route_id,
        "route": route_data
    }

@router.get("/routes/{route_id}", summary="Get route details")
async def get_route(route_id: str):
    """Get detailed route information"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    route = mesh_routes[route_id].copy()
    route["metrics"] = mesh_metrics.get(route_id, {})
    route["lb_config"] = mesh_lb_configs.get(route_id)
    route["circuit_breaker"] = mesh_circuit_breakers.get(route_id)
    route["retry_policy"] = mesh_retry_policies.get(route_id)
    
    return route

@router.delete("/routes/{route_id}", summary="Remove route")
async def remove_route(route_id: str):
    """Remove a mesh route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    log_mesh_event(route_id, "WARNING", "Route removed")
    del mesh_routes[route_id]
    
    # Clean up associated configs
    mesh_lb_configs.pop(route_id, None)
    mesh_circuit_breakers.pop(route_id, None)
    mesh_retry_policies.pop(route_id, None)
    
    return {
        "message": "Route removed successfully",
        "route_id": route_id
    }

# ==================== LOAD BALANCING ====================

@router.put("/routes/{route_id}/load-balancer", summary="Configure load balancer")
async def configure_load_balancer(route_id: str, config: LoadBalancerConfig):
    """Configure load balancer for a route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    lb_config = config.dict()
    lb_config["updated_at"] = datetime.utcnow().isoformat()
    
    mesh_lb_configs[route_id] = lb_config
    log_mesh_event(route_id, "INFO", f"Load balancer configured: {config.type.value}")
    
    return {
        "message": "Load balancer configured",
        "route_id": route_id,
        "config": lb_config
    }

@router.get("/routes/{route_id}/load-balancer", summary="Get load balancer config")
async def get_load_balancer(route_id: str):
    """Get load balancer configuration"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route_id not in mesh_lb_configs:
        raise HTTPException(status_code=404, detail="Load balancer not configured")
    
    return {
        "route_id": route_id,
        "config": mesh_lb_configs[route_id]
    }

# ==================== CIRCUIT BREAKER ====================

@router.put("/routes/{route_id}/circuit-breaker", summary="Configure circuit breaker")
async def configure_circuit_breaker(route_id: str, config: CircuitBreakerConfig):
    """Configure circuit breaker for a route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    cb_config = config.dict()
    cb_config["state"] = CircuitBreakerState.CLOSED.value
    cb_config["failure_count"] = 0
    cb_config["success_count"] = 0
    cb_config["last_failure"] = None
    cb_config["updated_at"] = datetime.utcnow().isoformat()
    
    mesh_circuit_breakers[route_id] = cb_config
    log_mesh_event(route_id, "INFO", "Circuit breaker configured")
    
    return {
        "message": "Circuit breaker configured",
        "route_id": route_id,
        "config": cb_config
    }

@router.get("/routes/{route_id}/circuit-breaker", summary="Get circuit breaker status")
async def get_circuit_breaker(route_id: str):
    """Get circuit breaker status"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route_id not in mesh_circuit_breakers:
        raise HTTPException(status_code=404, detail="Circuit breaker not configured")
    
    return {
        "route_id": route_id,
        "status": mesh_circuit_breakers[route_id]
    }

@router.post("/routes/{route_id}/circuit-breaker/reset", summary="Reset circuit breaker")
async def reset_circuit_breaker(route_id: str):
    """Manually reset circuit breaker"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route_id not in mesh_circuit_breakers:
        raise HTTPException(status_code=404, detail="Circuit breaker not configured")
    
    cb = mesh_circuit_breakers[route_id]
    cb["state"] = CircuitBreakerState.CLOSED.value
    cb["failure_count"] = 0
    cb["success_count"] = 0
    cb["last_failure"] = None
    cb["reset_at"] = datetime.utcnow().isoformat()
    
    log_mesh_event(route_id, "INFO", "Circuit breaker reset")
    
    return {
        "message": "Circuit breaker reset",
        "route_id": route_id,
        "status": cb
    }

# ==================== RETRY POLICIES ====================

@router.put("/routes/{route_id}/retry-policy", summary="Configure retry policy")
async def configure_retry_policy(route_id: str, policy: RetryPolicy):
    """Configure retry policy for a route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    policy_data = policy.dict()
    policy_data["updated_at"] = datetime.utcnow().isoformat()
    
    mesh_retry_policies[route_id] = policy_data
    log_mesh_event(route_id, "INFO", f"Retry policy configured: {policy.max_attempts} attempts")
    
    return {
        "message": "Retry policy configured",
        "route_id": route_id,
        "policy": policy_data
    }

@router.get("/routes/{route_id}/retry-policy", summary="Get retry policy")
async def get_retry_policy(route_id: str):
    """Get retry policy configuration"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route_id not in mesh_retry_policies:
        raise HTTPException(status_code=404, detail="Retry policy not configured")
    
    return {
        "route_id": route_id,
        "policy": mesh_retry_policies[route_id]
    }

# ==================== TRAFFIC SPLITTING ====================

@router.post("/traffic-split", summary="Configure traffic split")
async def configure_traffic_split(split: TrafficSplit):
    """Configure A/B testing or canary deployment"""
    split_id = f"split_{split.service_a}_{split.service_b}"
    
    if split.percentage_a + split.percentage_b != 100:
        raise HTTPException(status_code=400, detail="Percentages must sum to 100")
    
    split_data = split.dict()
    split_data["id"] = split_id
    split_data["created_at"] = datetime.utcnow().isoformat()
    split_data["requests_a"] = 0
    split_data["requests_b"] = 0
    
    mesh_traffic_splits[split_id] = split_data
    
    return {
        "message": "Traffic split configured",
        "split_id": split_id,
        "split": split_data
    }

@router.get("/traffic-split/{split_id}", summary="Get traffic split")
async def get_traffic_split(split_id: str):
    """Get traffic split configuration"""
    if split_id not in mesh_traffic_splits:
        raise HTTPException(status_code=404, detail="Traffic split not found")
    
    return mesh_traffic_splits[split_id]

@router.delete("/traffic-split/{split_id}", summary="Remove traffic split")
async def remove_traffic_split(split_id: str):
    """Remove traffic split configuration"""
    if split_id not in mesh_traffic_splits:
        raise HTTPException(status_code=404, detail="Traffic split not found")
    
    del mesh_traffic_splits[split_id]
    
    return {
        "message": "Traffic split removed",
        "split_id": split_id
    }

# ==================== TRACING ====================

@router.get("/routes/{route_id}/traces", summary="Get route traces")
async def get_route_traces(route_id: str, limit: int = Query(100, ge=1, le=1000)):
    """Get distributed traces for a route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    traces = mesh_traces.get(route_id, [])
    
    return {
        "route_id": route_id,
        "total_traces": len(traces),
        "traces": traces[-limit:]
    }

@router.post("/routes/{route_id}/trace", summary="Add trace")
async def add_trace(route_id: str, trace_data: Dict[str, Any]):
    """Add a distributed trace entry"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    trace = {
        "timestamp": datetime.utcnow().isoformat(),
        "trace_id": trace_data.get("trace_id"),
        "span_id": trace_data.get("span_id"),
        "parent_span_id": trace_data.get("parent_span_id"),
        "duration_ms": trace_data.get("duration_ms", 0),
        "status": trace_data.get("status", "ok"),
        "metadata": trace_data.get("metadata", {})
    }
    
    if route_id not in mesh_traces:
        mesh_traces[route_id] = []
    
    mesh_traces[route_id].append(trace)
    
    # Update metrics
    metrics = mesh_metrics[route_id]
    metrics["requests"] += 1
    
    if trace["status"] == "ok":
        metrics["successes"] += 1
    else:
        metrics["failures"] += 1
    
    duration = trace.get("duration_ms", 0)
    metrics["total_latency"] += duration
    metrics["avg_latency"] = metrics["total_latency"] / metrics["requests"]
    
    return {
        "message": "Trace added",
        "trace": trace
    }

# ==================== METRICS ====================

@router.get("/routes/{route_id}/metrics", summary="Get route metrics")
async def get_route_metrics(route_id: str):
    """Get detailed metrics for a route"""
    if route_id not in mesh_routes:
        raise HTTPException(status_code=404, detail="Route not found")
    
    return {
        "route_id": route_id,
        "metrics": mesh_metrics.get(route_id, {})
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Service mesh statistics")
async def get_mesh_overview():
    """Get comprehensive mesh statistics"""
    stats = {
        "total_routes": len(mesh_routes),
        "total_requests": 0,
        "total_failures": 0,
        "avg_latency": 0.0,
        "routes_with_lb": len(mesh_lb_configs),
        "routes_with_cb": len(mesh_circuit_breakers),
        "active_traffic_splits": len(mesh_traffic_splits),
        "circuit_breakers_open": 0
    }
    
    total_latency = 0.0
    request_count = 0
    
    for route_id, metrics in mesh_metrics.items():
        stats["total_requests"] += metrics.get("requests", 0)
        stats["total_failures"] += metrics.get("failures", 0)
        total_latency += metrics.get("total_latency", 0.0)
        request_count += metrics.get("requests", 0)
    
    if request_count > 0:
        stats["avg_latency"] = total_latency / request_count
    
    # Count open circuit breakers
    for cb in mesh_circuit_breakers.values():
        if cb.get("state") == CircuitBreakerState.OPEN.value:
            stats["circuit_breakers_open"] += 1
    
    return stats
