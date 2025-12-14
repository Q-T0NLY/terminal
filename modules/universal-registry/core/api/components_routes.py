"""
Registry Components API Routes
Infrastructure components: cache, database, queue, storage, proxy
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/components", tags=["components"])

# ==================== DATA MODELS ====================

class ComponentType(str, Enum):
    CACHE = "cache"
    DATABASE = "database"
    QUEUE = "queue"
    STORAGE = "storage"
    PROXY = "proxy"
    LOADBALANCER = "loadbalancer"
    GATEWAY = "gateway"

class ComponentStatus(str, Enum):
    REGISTERED = "registered"
    ENABLED = "enabled"
    DISABLED = "disabled"
    DEGRADED = "degraded"
    FAILED = "failed"

class Provider(str, Enum):
    REDIS = "redis"
    MEMCACHED = "memcached"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    MYSQL = "mysql"
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"
    SQS = "sqs"
    S3 = "s3"
    MINIO = "minio"
    NGINX = "nginx"
    HAPROXY = "haproxy"
    ENVOY = "envoy"

class ComponentInfo(BaseModel):
    id: str
    name: str
    type: ComponentType
    provider: Provider
    description: Optional[str] = None
    endpoint: Optional[str] = None
    port: Optional[int] = None
    connection_string: Optional[str] = None
    capacity: Optional[Dict[str, Any]] = {}
    replication: Optional[Dict[str, Any]] = {}
    metadata: Dict[str, Any] = {}

class ComponentCreate(BaseModel):
    name: str
    type: ComponentType
    provider: Provider
    description: Optional[str] = None
    endpoint: Optional[str] = None
    port: Optional[int] = None
    connection_string: Optional[str] = None
    capacity: Optional[Dict[str, Any]] = {}
    replication: Optional[Dict[str, Any]] = {}

class ComponentUpdate(BaseModel):
    endpoint: Optional[str] = None
    port: Optional[int] = None
    capacity: Optional[Dict[str, Any]] = None
    replication: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

# ==================== REGISTRY ====================

components_registry: Dict[str, Dict[str, Any]] = {}
component_logs: Dict[str, List[Dict[str, Any]]] = {}
component_stats: Dict[str, Dict[str, Any]] = {}

def log_component_event(component_id: str, level: str, message: str):
    """Log component events"""
    if component_id not in component_logs:
        component_logs[component_id] = []
    
    component_logs[component_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(component_logs[component_id]) > 1000:
        component_logs[component_id] = component_logs[component_id][-1000:]

# ==================== CRUD OPERATIONS ====================

@router.get("/", summary="List all components")
async def list_components(
    type: Optional[ComponentType] = Query(None),
    status: Optional[ComponentStatus] = Query(None),
    provider: Optional[Provider] = Query(None)
):
    """List all registry components"""
    result = list(components_registry.values())
    
    if type:
        result = [c for c in result if c.get("type") == type.value]
    if status:
        result = [c for c in result if c.get("status") == status.value]
    if provider:
        result = [c for c in result if c.get("provider") == provider.value]
    
    return {
        "total": len(result),
        "components": result
    }

@router.post("/", summary="Add new component")
async def add_component(component: ComponentCreate):
    """Register a new infrastructure component"""
    component_id = f"comp_{component.name.lower().replace(' ', '-')}"
    
    if component_id in components_registry:
        raise HTTPException(status_code=409, detail="Component already exists")
    
    component_data = component.dict()
    component_data["id"] = component_id
    component_data["status"] = ComponentStatus.REGISTERED.value
    component_data["created_at"] = datetime.utcnow().isoformat()
    component_data["health"] = "unknown"
    component_data["metadata"] = {}
    
    # Initialize stats
    component_stats[component_id] = {
        "connections": 0,
        "operations": 0,
        "errors": 0,
        "uptime": 0
    }
    
    components_registry[component_id] = component_data
    log_component_event(component_id, "INFO", f"Component registered: {component.name}")
    
    return {
        "message": "Component added successfully",
        "component_id": component_id,
        "component": component_data
    }

@router.get("/{component_id}", summary="Get component details")
async def get_component(component_id: str):
    """Get detailed component information"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return components_registry[component_id]

@router.post("/{component_id}/enable", summary="Enable component")
async def enable_component(component_id: str):
    """Enable infrastructure component"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    component = components_registry[component_id]
    
    if component["status"] == ComponentStatus.ENABLED.value:
        return {"message": "Component already enabled", "component": component}
    
    log_component_event(component_id, "INFO", "Enabling component")
    
    component["status"] = ComponentStatus.ENABLED.value
    component["enabled_at"] = datetime.utcnow().isoformat()
    component["health"] = "healthy"
    
    log_component_event(component_id, "INFO", "Component enabled")
    
    return {
        "message": "Component enabled",
        "component": component
    }

@router.post("/{component_id}/disable", summary="Disable component")
async def disable_component(component_id: str):
    """Disable infrastructure component"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    component = components_registry[component_id]
    
    if component["status"] != ComponentStatus.ENABLED.value:
        raise HTTPException(status_code=400, detail="Component is not enabled")
    
    log_component_event(component_id, "INFO", "Disabling component")
    
    component["status"] = ComponentStatus.DISABLED.value
    component["disabled_at"] = datetime.utcnow().isoformat()
    component["health"] = "stopped"
    
    log_component_event(component_id, "INFO", "Component disabled")
    
    return {
        "message": "Component disabled",
        "component": component
    }

@router.delete("/{component_id}", summary="Remove component")
async def remove_component(component_id: str):
    """Remove component from registry"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    component = components_registry[component_id]
    
    if component["status"] == ComponentStatus.ENABLED.value:
        await disable_component(component_id)
    
    log_component_event(component_id, "WARNING", "Removing component")
    
    del components_registry[component_id]
    
    return {
        "message": "Component removed successfully",
        "component_id": component_id
    }

@router.put("/{component_id}", summary="Update component")
async def update_component(component_id: str, update: ComponentUpdate):
    """Update component configuration"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    component = components_registry[component_id]
    
    if update.endpoint:
        component["endpoint"] = update.endpoint
    if update.port:
        component["port"] = update.port
    if update.capacity:
        component["capacity"].update(update.capacity)
    if update.replication:
        component["replication"].update(update.replication)
    if update.metadata:
        component["metadata"].update(update.metadata)
    
    component["updated_at"] = datetime.utcnow().isoformat()
    
    log_component_event(component_id, "INFO", "Component updated")
    
    return {
        "message": "Component updated",
        "component": component
    }

# ==================== MONITORING ====================

@router.get("/{component_id}/health", summary="Component health check")
async def check_component_health(component_id: str):
    """Get component health status"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    component = components_registry[component_id]
    stats = component_stats.get(component_id, {})
    
    return {
        "component_id": component_id,
        "status": component["status"],
        "health": component.get("health", "unknown"),
        "type": component["type"],
        "provider": component["provider"],
        "stats": stats
    }

@router.get("/{component_id}/stats", summary="Get component statistics")
async def get_component_stats(component_id: str):
    """Get detailed component statistics"""
    if component_id not in components_registry:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return {
        "component_id": component_id,
        "stats": component_stats.get(component_id, {})
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Components statistics")
async def get_components_overview():
    """Get comprehensive components statistics"""
    stats = {
        "total_components": len(components_registry),
        "by_type": {},
        "by_status": {},
        "by_provider": {}
    }
    
    for component in components_registry.values():
        ctype = component.get("type", "unknown")
        stats["by_type"][ctype] = stats["by_type"].get(ctype, 0) + 1
        
        status = component.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        provider = component.get("provider", "unknown")
        stats["by_provider"][provider] = stats["by_provider"].get(provider, 0) + 1
    
    return stats
