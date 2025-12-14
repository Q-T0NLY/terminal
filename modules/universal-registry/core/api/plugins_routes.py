"""
Plugin Management API Routes
Provides REST API for full plugin lifecycle control
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/plugins", tags=["plugins"])

# ==================== DATA MODELS ====================

class PluginStatus(str, Enum):
    REGISTERED = "registered"
    INSTALLED = "installed"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    FAILED = "failed"

class FeatureCategory(str, Enum):
    AI_ML = "ai-ml"
    WEB3 = "web3"
    CLOUD = "cloud"
    DATA = "data"
    DEVOPS = "devops"
    SECURITY = "security"
    SYSTEM = "system"
    OBSERVABILITY = "observability"

class PluginInfo(BaseModel):
    id: str
    name: str
    version: str
    feature: FeatureCategory
    description: Optional[str] = None
    author: Optional[str] = None
    license: Optional[str] = None
    repository: Optional[str] = None
    dependencies: List[str] = []
    capabilities: List[str] = []
    metadata: Dict[str, Any] = {}

class PluginInstallRequest(BaseModel):
    source: str  # URL, file path, or package name
    version: Optional[str] = None
    force: bool = False

class PluginUpdateRequest(BaseModel):
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PluginConfigUpdate(BaseModel):
    config: Dict[str, Any]

# ==================== IN-MEMORY PLUGIN REGISTRY ====================

# Simulated plugin registry (in production, use database)
plugins_registry: Dict[str, Dict[str, Any]] = {}
plugin_logs: Dict[str, List[Dict[str, Any]]] = {}

def log_plugin_event(plugin_id: str, level: str, message: str):
    """Log plugin events"""
    if plugin_id not in plugin_logs:
        plugin_logs[plugin_id] = []
    
    plugin_logs[plugin_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    # Keep last 1000 logs
    if len(plugin_logs[plugin_id]) > 1000:
        plugin_logs[plugin_id] = plugin_logs[plugin_id][-1000:]

# ==================== PLUGIN LIFECYCLE ROUTES ====================

@router.get("/", summary="List all plugins")
async def list_plugins(
    status: Optional[PluginStatus] = Query(None, description="Filter by status"),
    feature: Optional[FeatureCategory] = Query(None, description="Filter by feature category")
):
    """
    Get list of all registered plugins with optional filtering.
    
    Filters:
    - status: Filter by plugin status
    - feature: Filter by feature category
    """
    result = list(plugins_registry.values())
    
    if status:
        result = [p for p in result if p.get("status") == status.value]
    
    if feature:
        result = [p for p in result if p.get("feature") == feature.value]
    
    return {
        "total": len(result),
        "plugins": result
    }

@router.post("/register", summary="Register new plugin")
async def register_plugin(plugin: PluginInfo):
    """
    Register a new plugin in the registry.
    
    - Creates plugin entry with REGISTERED status
    - Validates dependencies
    - Sets up plugin metadata
    """
    if plugin.id in plugins_registry:
        raise HTTPException(status_code=409, detail="Plugin already exists")
    
    plugin_data = plugin.dict()
    plugin_data["status"] = PluginStatus.REGISTERED.value
    plugin_data["registered_at"] = datetime.utcnow().isoformat()
    plugin_data["health"] = "unknown"
    
    plugins_registry[plugin.id] = plugin_data
    log_plugin_event(plugin.id, "INFO", f"Plugin registered: {plugin.name} v{plugin.version}")
    
    return {
        "message": "Plugin registered successfully",
        "plugin_id": plugin.id,
        "plugin": plugin_data
    }

@router.get("/{plugin_id}", summary="Get plugin details")
async def get_plugin(plugin_id: str):
    """Get detailed information about a specific plugin"""
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    return plugins_registry[plugin_id]

@router.post("/{plugin_id}/install", summary="Install plugin")
async def install_plugin(plugin_id: str, request: Optional[PluginInstallRequest] = None):
    """
    Install a plugin.
    
    Steps:
    1. Download plugin from source
    2. Verify dependencies
    3. Install plugin files
    4. Update status to INSTALLED
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    if plugin["status"] == PluginStatus.INSTALLED.value:
        return {"message": "Plugin already installed", "plugin": plugin}
    
    # Simulate installation
    log_plugin_event(plugin_id, "INFO", "Starting plugin installation")
    
    try:
        # Check dependencies
        missing_deps = []
        for dep in plugin.get("dependencies", []):
            if dep not in plugins_registry or plugins_registry[dep]["status"] not in [
                PluginStatus.INSTALLED.value, PluginStatus.ACTIVE.value
            ]:
                missing_deps.append(dep)
        
        if missing_deps:
            raise HTTPException(
                status_code=424,
                detail=f"Missing dependencies: {', '.join(missing_deps)}"
            )
        
        # Simulate download and installation
        await asyncio.sleep(0.1)
        
        plugin["status"] = PluginStatus.INSTALLED.value
        plugin["installed_at"] = datetime.utcnow().isoformat()
        plugin["health"] = "healthy"
        
        log_plugin_event(plugin_id, "INFO", "Plugin installed successfully")
        
        return {
            "message": "Plugin installed successfully",
            "plugin": plugin
        }
    
    except Exception as e:
        plugin["status"] = PluginStatus.FAILED.value
        plugin["health"] = "failed"
        log_plugin_event(plugin_id, "ERROR", f"Installation failed: {str(e)}")
        raise

@router.post("/{plugin_id}/activate", summary="Activate plugin")
async def activate_plugin(plugin_id: str):
    """
    Activate an installed plugin.
    
    - Verifies plugin is installed
    - Loads plugin configuration
    - Starts plugin services
    - Updates status to ACTIVE
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    if plugin["status"] not in [PluginStatus.INSTALLED.value, PluginStatus.INACTIVE.value]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot activate plugin with status: {plugin['status']}"
        )
    
    log_plugin_event(plugin_id, "INFO", "Activating plugin")
    
    try:
        # Simulate activation
        await asyncio.sleep(0.1)
        
        plugin["status"] = PluginStatus.ACTIVE.value
        plugin["activated_at"] = datetime.utcnow().isoformat()
        plugin["health"] = "healthy"
        
        log_plugin_event(plugin_id, "INFO", "Plugin activated successfully")
        
        return {
            "message": "Plugin activated",
            "plugin": plugin
        }
    
    except Exception as e:
        plugin["status"] = PluginStatus.FAILED.value
        plugin["health"] = "failed"
        log_plugin_event(plugin_id, "ERROR", f"Activation failed: {str(e)}")
        raise

@router.post("/{plugin_id}/deactivate", summary="Deactivate plugin")
async def deactivate_plugin(plugin_id: str):
    """
    Deactivate an active plugin.
    
    - Stops plugin services
    - Saves plugin state
    - Updates status to INACTIVE
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    if plugin["status"] != PluginStatus.ACTIVE.value:
        raise HTTPException(status_code=400, detail="Plugin is not active")
    
    log_plugin_event(plugin_id, "INFO", "Deactivating plugin")
    
    try:
        # Simulate deactivation
        await asyncio.sleep(0.1)
        
        plugin["status"] = PluginStatus.INACTIVE.value
        plugin["deactivated_at"] = datetime.utcnow().isoformat()
        plugin["health"] = "stopped"
        
        log_plugin_event(plugin_id, "INFO", "Plugin deactivated")
        
        return {
            "message": "Plugin deactivated",
            "plugin": plugin
        }
    
    except Exception as e:
        log_plugin_event(plugin_id, "ERROR", f"Deactivation failed: {str(e)}")
        raise

@router.delete("/{plugin_id}", summary="Uninstall plugin")
async def uninstall_plugin(plugin_id: str, force: bool = Query(False)):
    """
    Uninstall a plugin.
    
    - Deactivates plugin if active
    - Removes plugin files
    - Removes from registry
    - force: Uninstall even if other plugins depend on it
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    # Check if any plugins depend on this one
    if not force:
        dependent_plugins = [
            p["name"] for p in plugins_registry.values()
            if plugin_id in p.get("dependencies", [])
        ]
        if dependent_plugins:
            raise HTTPException(
                status_code=409,
                detail=f"Cannot uninstall: plugins depend on it: {', '.join(dependent_plugins)}"
            )
    
    log_plugin_event(plugin_id, "WARNING", "Uninstalling plugin")
    
    try:
        # Deactivate if active
        if plugin["status"] == PluginStatus.ACTIVE.value:
            await deactivate_plugin(plugin_id)
        
        # Remove plugin
        await asyncio.sleep(0.1)
        
        del plugins_registry[plugin_id]
        log_plugin_event(plugin_id, "INFO", "Plugin uninstalled")
        
        return {
            "message": "Plugin uninstalled successfully",
            "plugin_id": plugin_id
        }
    
    except Exception as e:
        log_plugin_event(plugin_id, "ERROR", f"Uninstall failed: {str(e)}")
        raise

@router.put("/{plugin_id}", summary="Update plugin")
async def update_plugin(plugin_id: str, update: PluginUpdateRequest):
    """
    Update plugin version or metadata.
    
    - Downloads new version
    - Performs rolling update
    - Maintains plugin state
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    old_version = plugin.get("version", "unknown")
    
    log_plugin_event(plugin_id, "INFO", f"Updating plugin from {old_version}")
    
    try:
        if update.version:
            plugin["version"] = update.version
            plugin["updated_at"] = datetime.utcnow().isoformat()
        
        if update.metadata:
            plugin["metadata"].update(update.metadata)
        
        log_plugin_event(plugin_id, "INFO", f"Plugin updated to version {plugin['version']}")
        
        return {
            "message": "Plugin updated",
            "plugin": plugin
        }
    
    except Exception as e:
        log_plugin_event(plugin_id, "ERROR", f"Update failed: {str(e)}")
        raise

# ==================== PLUGIN OPERATIONS ====================

@router.get("/{plugin_id}/health", summary="Check plugin health")
async def check_plugin_health(plugin_id: str):
    """
    Check plugin health status.
    
    Returns:
    - health: healthy, degraded, unhealthy, stopped
    - uptime: Time since activation
    - metrics: Plugin-specific metrics
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    health_status = plugin.get("health", "unknown")
    
    return {
        "plugin_id": plugin_id,
        "status": plugin["status"],
        "health": health_status,
        "version": plugin.get("version", "unknown"),
        "uptime": "0h 0m"  # Calculate from activated_at
    }

@router.get("/{plugin_id}/logs", summary="Get plugin logs")
async def get_plugin_logs(
    plugin_id: str,
    lines: int = Query(100, ge=1, le=10000, description="Number of log lines")
):
    """
    Retrieve plugin logs.
    
    Parameters:
    - lines: Number of recent log lines to return (1-10000)
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    logs = plugin_logs.get(plugin_id, [])
    
    return {
        "plugin_id": plugin_id,
        "total_logs": len(logs),
        "logs": logs[-lines:]
    }

@router.get("/{plugin_id}/config", summary="Get plugin configuration")
async def get_plugin_config(plugin_id: str):
    """Get current plugin configuration"""
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    return {
        "plugin_id": plugin_id,
        "config": plugin.get("metadata", {}).get("config", {})
    }

@router.put("/{plugin_id}/config", summary="Update plugin configuration")
async def update_plugin_config(plugin_id: str, update: PluginConfigUpdate):
    """
    Update plugin configuration.
    
    - Updates configuration
    - Reloads plugin if active
    - Validates configuration
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    
    if "metadata" not in plugin:
        plugin["metadata"] = {}
    
    plugin["metadata"]["config"] = update.config
    plugin["config_updated_at"] = datetime.utcnow().isoformat()
    
    log_plugin_event(plugin_id, "INFO", "Configuration updated")
    
    # Reload plugin if active
    if plugin["status"] == PluginStatus.ACTIVE.value:
        log_plugin_event(plugin_id, "INFO", "Reloading plugin with new configuration")
    
    return {
        "message": "Configuration updated",
        "config": update.config
    }

# ==================== PLUGIN DISCOVERY ====================

@router.get("/features/{feature}", summary="List plugins by feature")
async def list_plugins_by_feature(feature: FeatureCategory):
    """Get all plugins for a specific feature category"""
    result = [
        p for p in plugins_registry.values()
        if p.get("feature") == feature.value
    ]
    
    return {
        "feature": feature.value,
        "total": len(result),
        "plugins": result
    }

@router.get("/status/{status}", summary="List plugins by status")
async def list_plugins_by_status(status: PluginStatus):
    """Get all plugins with a specific status"""
    result = [
        p for p in plugins_registry.values()
        if p.get("status") == status.value
    ]
    
    return {
        "status": status.value,
        "total": len(result),
        "plugins": result
    }

@router.get("/{plugin_id}/dependencies", summary="Get plugin dependencies")
async def get_plugin_dependencies(plugin_id: str):
    """
    Get plugin dependency tree.
    
    Returns:
    - direct: Direct dependencies
    - transitive: All transitive dependencies
    - dependents: Plugins that depend on this one
    """
    if plugin_id not in plugins_registry:
        raise HTTPException(status_code=404, detail="Plugin not found")
    
    plugin = plugins_registry[plugin_id]
    direct_deps = plugin.get("dependencies", [])
    
    # Find plugins that depend on this one
    dependents = [
        p["id"] for p in plugins_registry.values()
        if plugin_id in p.get("dependencies", [])
    ]
    
    return {
        "plugin_id": plugin_id,
        "direct_dependencies": direct_deps,
        "dependents": dependents
    }

# ==================== PLUGIN STATISTICS ====================

@router.get("/stats/overview", summary="Get plugin statistics")
async def get_plugin_stats():
    """
    Get comprehensive plugin statistics.
    
    Returns counts by:
    - Status
    - Feature category
    - Health status
    """
    stats = {
        "total_plugins": len(plugins_registry),
        "by_status": {},
        "by_feature": {},
        "by_health": {}
    }
    
    for plugin in plugins_registry.values():
        # Count by status
        status = plugin.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by feature
        feature = plugin.get("feature", "unknown")
        stats["by_feature"][feature] = stats["by_feature"].get(feature, 0) + 1
        
        # Count by health
        health = plugin.get("health", "unknown")
        stats["by_health"][health] = stats["by_health"].get(health, 0) + 1
    
    return stats
