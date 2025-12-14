"""
Sub-Registries API Routes
Hierarchical and domain-based registry management
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/registries", tags=["registries"])

# ==================== DATA MODELS ====================

class RegistryType(str, Enum):
    ROOT = "root"
    DOMAIN = "domain"
    PROJECT = "project"
    ENVIRONMENT = "environment"
    TENANT = "tenant"

class RegistryStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SYNCING = "syncing"
    DEGRADED = "degraded"
    FAILED = "failed"

class SyncMode(str, Enum):
    PULL = "pull"
    PUSH = "push"
    BIDIRECTIONAL = "bidirectional"
    MIRROR = "mirror"

class RegistryInfo(BaseModel):
    id: str
    name: str
    type: RegistryType
    description: Optional[str] = None
    parent_id: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    sync_mode: SyncMode = SyncMode.PULL
    metadata: Dict[str, Any] = {}

class RegistryCreate(BaseModel):
    name: str
    type: RegistryType
    description: Optional[str] = None
    parent_id: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    sync_mode: SyncMode = SyncMode.PULL

class RegistryUpdate(BaseModel):
    description: Optional[str] = None
    url: Optional[str] = None
    sync_mode: Optional[SyncMode] = None
    metadata: Optional[Dict[str, Any]] = None

# ==================== REGISTRY ====================

registries_registry: Dict[str, Dict[str, Any]] = {}
registry_logs: Dict[str, List[Dict[str, Any]]] = {}

def log_registry_event(registry_id: str, level: str, message: str):
    """Log registry events"""
    if registry_id not in registry_logs:
        registry_logs[registry_id] = []
    
    registry_logs[registry_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(registry_logs[registry_id]) > 1000:
        registry_logs[registry_id] = registry_logs[registry_id][-1000:]

def get_registry_hierarchy(registry_id: str) -> List[str]:
    """Get full hierarchy path for a registry"""
    hierarchy = [registry_id]
    current = registries_registry.get(registry_id, {})
    
    while current.get("parent_id"):
        parent_id = current["parent_id"]
        hierarchy.insert(0, parent_id)
        current = registries_registry.get(parent_id, {})
    
    return hierarchy

def get_child_registries(registry_id: str) -> List[str]:
    """Get all child registries"""
    children = []
    for reg_id, reg in registries_registry.items():
        if reg.get("parent_id") == registry_id:
            children.append(reg_id)
            children.extend(get_child_registries(reg_id))
    return children

# ==================== CRUD OPERATIONS ====================

@router.get("/", summary="List all registries")
async def list_registries(
    type: Optional[RegistryType] = Query(None),
    status: Optional[RegistryStatus] = Query(None),
    parent_id: Optional[str] = Query(None)
):
    """List all sub-registries"""
    result = list(registries_registry.values())
    
    if type:
        result = [r for r in result if r.get("type") == type.value]
    if status:
        result = [r for r in result if r.get("status") == status.value]
    if parent_id:
        result = [r for r in result if r.get("parent_id") == parent_id]
    
    return {
        "total": len(result),
        "registries": result
    }

@router.post("/", summary="Create new registry")
async def create_registry(registry: RegistryCreate):
    """Create a new sub-registry"""
    registry_id = f"reg_{registry.name.lower().replace(' ', '-')}"
    
    if registry_id in registries_registry:
        raise HTTPException(status_code=409, detail="Registry already exists")
    
    # Validate parent exists
    if registry.parent_id and registry.parent_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Parent registry not found")
    
    registry_data = registry.dict()
    registry_data["id"] = registry_id
    registry_data["status"] = RegistryStatus.ACTIVE.value
    registry_data["created_at"] = datetime.utcnow().isoformat()
    registry_data["metadata"] = {}
    registry_data["item_count"] = 0
    registry_data["sync_status"] = "idle"
    
    registries_registry[registry_id] = registry_data
    log_registry_event(registry_id, "INFO", f"Registry created: {registry.name}")
    
    return {
        "message": "Registry created successfully",
        "registry_id": registry_id,
        "registry": registry_data
    }

@router.get("/{registry_id}", summary="Get registry details")
async def get_registry(registry_id: str):
    """Get detailed registry information"""
    if registry_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Registry not found")
    
    registry = registries_registry[registry_id].copy()
    registry["hierarchy"] = get_registry_hierarchy(registry_id)
    registry["children"] = get_child_registries(registry_id)
    
    return registry

@router.put("/{registry_id}", summary="Update registry")
async def update_registry(registry_id: str, update: RegistryUpdate):
    """Update registry configuration"""
    if registry_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Registry not found")
    
    registry = registries_registry[registry_id]
    
    if update.description:
        registry["description"] = update.description
    if update.url:
        registry["url"] = update.url
    if update.sync_mode:
        registry["sync_mode"] = update.sync_mode.value
    if update.metadata:
        registry["metadata"].update(update.metadata)
    
    registry["updated_at"] = datetime.utcnow().isoformat()
    
    log_registry_event(registry_id, "INFO", "Registry updated")
    
    return {
        "message": "Registry updated",
        "registry": registry
    }

@router.delete("/{registry_id}", summary="Delete registry")
async def delete_registry(registry_id: str, force: bool = Query(False)):
    """Delete a sub-registry"""
    if registry_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Registry not found")
    
    # Check for children
    children = get_child_registries(registry_id)
    if children and not force:
        raise HTTPException(
            status_code=400,
            detail=f"Registry has {len(children)} child registries. Use force=true to delete"
        )
    
    # Delete children if force
    if force:
        for child_id in children:
            if child_id in registries_registry:
                del registries_registry[child_id]
                log_registry_event(child_id, "WARNING", "Registry deleted (cascaded)")
    
    log_registry_event(registry_id, "WARNING", "Registry deleted")
    del registries_registry[registry_id]
    
    return {
        "message": "Registry deleted successfully",
        "registry_id": registry_id,
        "children_deleted": len(children) if force else 0
    }

# ==================== SYNC OPERATIONS ====================

@router.post("/{registry_id}/sync", summary="Synchronize registry")
async def sync_registry(registry_id: str):
    """Synchronize registry with remote source"""
    if registry_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Registry not found")
    
    registry = registries_registry[registry_id]
    
    if not registry.get("url"):
        raise HTTPException(status_code=400, detail="Registry has no sync URL configured")
    
    log_registry_event(registry_id, "INFO", "Starting sync")
    
    registry["sync_status"] = "syncing"
    registry["status"] = RegistryStatus.SYNCING.value
    registry["last_sync_started"] = datetime.utcnow().isoformat()
    
    # Simulate sync (in production, this would be actual sync)
    registry["sync_status"] = "completed"
    registry["status"] = RegistryStatus.ACTIVE.value
    registry["last_sync_completed"] = datetime.utcnow().isoformat()
    
    log_registry_event(registry_id, "INFO", "Sync completed")
    
    return {
        "message": "Registry synchronized",
        "registry_id": registry_id,
        "sync_mode": registry["sync_mode"]
    }

@router.get("/{registry_id}/hierarchy", summary="Get registry hierarchy")
async def get_hierarchy(registry_id: str):
    """Get full registry hierarchy"""
    if registry_id not in registries_registry:
        raise HTTPException(status_code=404, detail="Registry not found")
    
    hierarchy = get_registry_hierarchy(registry_id)
    children = get_child_registries(registry_id)
    
    return {
        "registry_id": registry_id,
        "hierarchy_path": hierarchy,
        "depth": len(hierarchy),
        "children": children,
        "total_descendants": len(children)
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Registries statistics")
async def get_registries_overview():
    """Get comprehensive registries statistics"""
    stats = {
        "total_registries": len(registries_registry),
        "by_type": {},
        "by_status": {},
        "max_depth": 0,
        "total_items": 0
    }
    
    for registry in registries_registry.values():
        rtype = registry.get("type", "unknown")
        stats["by_type"][rtype] = stats["by_type"].get(rtype, 0) + 1
        
        status = registry.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        hierarchy = get_registry_hierarchy(registry["id"])
        stats["max_depth"] = max(stats["max_depth"], len(hierarchy))
        
        stats["total_items"] += registry.get("item_count", 0)
    
    return stats
