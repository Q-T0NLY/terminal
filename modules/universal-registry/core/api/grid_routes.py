"""
Distributed Grid API Routes
Grid node management with load balancing and auto-discovery
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/grid", tags=["grid"])

# ==================== DATA MODELS ====================

class NodeType(str, Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    GATEWAY = "gateway"
    WORKER = "worker"
    COORDINATOR = "coordinator"

class NodeStatus(str, Enum):
    JOINING = "joining"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAINING = "draining"
    FAILED = "failed"

class LoadBalancingStrategy(str, Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    RANDOM = "random"
    CONSISTENT_HASH = "consistent_hash"

class NodeHealth(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class NodeInfo(BaseModel):
    id: str
    name: str
    type: NodeType
    host: str
    port: int
    region: Optional[str] = None
    zone: Optional[str] = None
    capacity: Optional[Dict[str, Any]] = {}
    tags: List[str] = []
    metadata: Dict[str, Any] = {}

class NodeCreate(BaseModel):
    name: str
    type: NodeType
    host: str
    port: int
    region: Optional[str] = None
    zone: Optional[str] = None
    capacity: Optional[Dict[str, Any]] = {}
    tags: List[str] = []

class NodeUpdate(BaseModel):
    capacity: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class AffinityRule(BaseModel):
    key: str
    operator: str  # eq, ne, in, exists
    value: Optional[Any] = None

# ==================== REGISTRY ====================

grid_registry: Dict[str, Dict[str, Any]] = {}
node_logs: Dict[str, List[Dict[str, Any]]] = {}
node_metrics: Dict[str, Dict[str, Any]] = {}
grid_config: Dict[str, Any] = {
    "load_balancing_strategy": LoadBalancingStrategy.ROUND_ROBIN.value,
    "auto_discovery": True,
    "health_check_interval": 30
}

def log_node_event(node_id: str, level: str, message: str):
    """Log node events"""
    if node_id not in node_logs:
        node_logs[node_id] = []
    
    node_logs[node_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(node_logs[node_id]) > 1000:
        node_logs[node_id] = node_logs[node_id][-1000:]

def get_active_nodes(node_type: Optional[NodeType] = None) -> List[Dict[str, Any]]:
    """Get all active nodes"""
    nodes = [n for n in grid_registry.values() if n.get("status") == NodeStatus.ACTIVE.value]
    if node_type:
        nodes = [n for n in nodes if n.get("type") == node_type.value]
    return nodes

def select_node_with_strategy(nodes: List[Dict], strategy: str) -> Optional[Dict]:
    """Select a node based on load balancing strategy"""
    if not nodes:
        return None
    
    if strategy == LoadBalancingStrategy.ROUND_ROBIN.value:
        # Simple rotation (in production, maintain state)
        return nodes[0]
    elif strategy == LoadBalancingStrategy.LEAST_CONNECTIONS.value:
        return min(nodes, key=lambda n: node_metrics.get(n["id"], {}).get("connections", 0))
    elif strategy == LoadBalancingStrategy.WEIGHTED.value:
        # Weight by capacity (simplified)
        return max(nodes, key=lambda n: n.get("capacity", {}).get("weight", 1))
    elif strategy == LoadBalancingStrategy.RANDOM.value:
        import random
        return random.choice(nodes)
    else:  # ROUND_ROBIN default
        return nodes[0]

# ==================== CRUD OPERATIONS ====================

@router.get("/nodes", summary="List all grid nodes")
async def list_nodes(
    type: Optional[NodeType] = Query(None),
    status: Optional[NodeStatus] = Query(None),
    region: Optional[str] = Query(None)
):
    """List all grid nodes"""
    result = list(grid_registry.values())
    
    if type:
        result = [n for n in result if n.get("type") == type.value]
    if status:
        result = [n for n in result if n.get("status") == status.value]
    if region:
        result = [n for n in result if n.get("region") == region]
    
    return {
        "total": len(result),
        "nodes": result
    }

@router.post("/nodes", summary="Add grid node")
async def add_node(node: NodeCreate):
    """Register a new grid node"""
    node_id = f"node_{node.name.lower().replace(' ', '-')}"
    
    if node_id in grid_registry:
        raise HTTPException(status_code=409, detail="Node already exists")
    
    node_data = node.dict()
    node_data["id"] = node_id
    node_data["status"] = NodeStatus.JOINING.value
    node_data["health"] = NodeHealth.HEALTHY.value
    node_data["joined_at"] = datetime.utcnow().isoformat()
    node_data["metadata"] = {}
    
    # Initialize metrics
    node_metrics[node_id] = {
        "connections": 0,
        "requests": 0,
        "cpu_usage": 0.0,
        "memory_usage": 0.0,
        "uptime": 0
    }
    
    grid_registry[node_id] = node_data
    log_node_event(node_id, "INFO", f"Node joining grid: {node.name}")
    
    # Auto-activate if auto-discovery enabled
    if grid_config.get("auto_discovery"):
        node_data["status"] = NodeStatus.ACTIVE.value
        node_data["activated_at"] = datetime.utcnow().isoformat()
        log_node_event(node_id, "INFO", "Node activated (auto-discovery)")
    
    return {
        "message": "Node added to grid",
        "node_id": node_id,
        "node": node_data
    }

@router.get("/nodes/{node_id}", summary="Get node details")
async def get_node(node_id: str):
    """Get detailed node information"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id].copy()
    node["metrics"] = node_metrics.get(node_id, {})
    
    return node

@router.put("/nodes/{node_id}", summary="Update node")
async def update_node(node_id: str, update: NodeUpdate):
    """Update node configuration"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id]
    
    if update.capacity:
        node["capacity"].update(update.capacity)
    if update.tags:
        node["tags"] = update.tags
    if update.metadata:
        node["metadata"].update(update.metadata)
    
    node["updated_at"] = datetime.utcnow().isoformat()
    
    log_node_event(node_id, "INFO", "Node updated")
    
    return {
        "message": "Node updated",
        "node": node
    }

@router.delete("/nodes/{node_id}", summary="Remove node")
async def remove_node(node_id: str, drain: bool = Query(False)):
    """Remove node from grid"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id]
    
    if drain and node.get("status") == NodeStatus.ACTIVE.value:
        # Drain connections first
        node["status"] = NodeStatus.DRAINING.value
        log_node_event(node_id, "INFO", "Node draining")
        
        # In production, wait for connections to drain
        node["drained_at"] = datetime.utcnow().isoformat()
    
    log_node_event(node_id, "WARNING", "Node removed from grid")
    del grid_registry[node_id]
    
    return {
        "message": "Node removed from grid",
        "node_id": node_id
    }

# ==================== NODE OPERATIONS ====================

@router.post("/nodes/{node_id}/activate", summary="Activate node")
async def activate_node(node_id: str):
    """Activate a grid node"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id]
    
    if node["status"] == NodeStatus.ACTIVE.value:
        return {"message": "Node already active", "node": node}
    
    node["status"] = NodeStatus.ACTIVE.value
    node["activated_at"] = datetime.utcnow().isoformat()
    
    log_node_event(node_id, "INFO", "Node activated")
    
    return {
        "message": "Node activated",
        "node": node
    }

@router.post("/nodes/{node_id}/deactivate", summary="Deactivate node")
async def deactivate_node(node_id: str):
    """Deactivate a grid node"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id]
    
    if node["status"] != NodeStatus.ACTIVE.value:
        raise HTTPException(status_code=400, detail="Node is not active")
    
    node["status"] = NodeStatus.INACTIVE.value
    node["deactivated_at"] = datetime.utcnow().isoformat()
    
    log_node_event(node_id, "INFO", "Node deactivated")
    
    return {
        "message": "Node deactivated",
        "node": node
    }

@router.get("/nodes/{node_id}/health", summary="Check node health")
async def check_node_health(node_id: str):
    """Get node health status"""
    if node_id not in grid_registry:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = grid_registry[node_id]
    metrics = node_metrics.get(node_id, {})
    
    # Determine health based on metrics
    health = NodeHealth.HEALTHY.value
    if metrics.get("cpu_usage", 0) > 90 or metrics.get("memory_usage", 0) > 90:
        health = NodeHealth.DEGRADED.value
    if metrics.get("cpu_usage", 0) > 98 or metrics.get("memory_usage", 0) > 98:
        health = NodeHealth.UNHEALTHY.value
    
    node["health"] = health
    
    return {
        "node_id": node_id,
        "status": node["status"],
        "health": health,
        "metrics": metrics
    }

# ==================== LOAD BALANCING ====================

@router.post("/balance", summary="Get balanced node")
async def get_balanced_node(
    type: Optional[NodeType] = Query(None),
    affinity: Optional[List[AffinityRule]] = None
):
    """Get a node based on load balancing strategy"""
    nodes = get_active_nodes(type)
    
    if not nodes:
        raise HTTPException(status_code=404, detail="No active nodes available")
    
    # Apply affinity rules if provided
    if affinity:
        for rule in affinity:
            if rule.operator == "eq":
                nodes = [n for n in nodes if n.get("metadata", {}).get(rule.key) == rule.value]
            elif rule.operator == "ne":
                nodes = [n for n in nodes if n.get("metadata", {}).get(rule.key) != rule.value]
            elif rule.operator == "in":
                nodes = [n for n in nodes if n.get("metadata", {}).get(rule.key) in rule.value]
            elif rule.operator == "exists":
                nodes = [n for n in nodes if rule.key in n.get("metadata", {})]
    
    if not nodes:
        raise HTTPException(status_code=404, detail="No nodes match affinity rules")
    
    strategy = grid_config.get("load_balancing_strategy", LoadBalancingStrategy.ROUND_ROBIN.value)
    selected_node = select_node_with_strategy(nodes, strategy)
    
    if not selected_node:
        raise HTTPException(status_code=500, detail="Failed to select node")
    
    # Increment connection counter
    node_id = selected_node["id"]
    node_metrics[node_id]["connections"] = node_metrics[node_id].get("connections", 0) + 1
    
    return {
        "node": selected_node,
        "strategy": strategy,
        "total_candidates": len(nodes)
    }

@router.put("/config/load-balancing", summary="Configure load balancing")
async def configure_load_balancing(strategy: LoadBalancingStrategy):
    """Configure grid load balancing strategy"""
    grid_config["load_balancing_strategy"] = strategy.value
    
    return {
        "message": "Load balancing strategy updated",
        "strategy": strategy.value
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Grid statistics")
async def get_grid_overview():
    """Get comprehensive grid statistics"""
    stats = {
        "total_nodes": len(grid_registry),
        "active_nodes": 0,
        "by_type": {},
        "by_region": {},
        "total_connections": 0,
        "total_requests": 0
    }
    
    for node in grid_registry.values():
        if node.get("status") == NodeStatus.ACTIVE.value:
            stats["active_nodes"] += 1
        
        ntype = node.get("type", "unknown")
        stats["by_type"][ntype] = stats["by_type"].get(ntype, 0) + 1
        
        region = node.get("region", "default")
        stats["by_region"][region] = stats["by_region"].get(region, 0) + 1
        
        metrics = node_metrics.get(node["id"], {})
        stats["total_connections"] += metrics.get("connections", 0)
        stats["total_requests"] += metrics.get("requests", 0)
    
    stats["load_balancing_strategy"] = grid_config.get("load_balancing_strategy")
    
    return stats
