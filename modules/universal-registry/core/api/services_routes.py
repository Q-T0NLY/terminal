"""
Service Management API Routes
Enterprise-grade microservices lifecycle control with advanced features
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/services", tags=["services"])

# ==================== DATA MODELS ====================

class ServiceStatus(str, Enum):
    CREATED = "created"
    INSTALLED = "installed"
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"
    FAILED = "failed"

class ServiceType(str, Enum):
    API = "api"
    WORKER = "worker"
    PROCESSOR = "processor"
    GATEWAY = "gateway"
    MESH = "mesh"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class ServiceInfo(BaseModel):
    id: str
    name: str
    version: str
    type: ServiceType
    description: Optional[str] = None
    port: int
    replicas: int = 1
    image: Optional[str] = None
    environment: Dict[str, str] = {}
    resources: Dict[str, Any] = {}
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}

class ServiceCreate(BaseModel):
    name: str
    type: ServiceType
    port: int
    version: str = "1.0.0"
    description: Optional[str] = None
    replicas: int = 1
    image: Optional[str] = None
    environment: Dict[str, str] = {}
    resources: Dict[str, Any] = {}
    dependencies: List[str] = []

class ServiceUpdate(BaseModel):
    version: Optional[str] = None
    replicas: Optional[int] = None
    environment: Optional[Dict[str, str]] = None
    resources: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class ServiceConfig(BaseModel):
    config: Dict[str, Any]

class BulkImport(BaseModel):
    services: List[ServiceInfo]

# ==================== IN-MEMORY SERVICE REGISTRY ====================

services_registry: Dict[str, Dict[str, Any]] = {}
service_logs: Dict[str, List[Dict[str, Any]]] = {}
service_metrics: Dict[str, Dict[str, Any]] = {}

def log_service_event(service_id: str, level: str, message: str):
    """Log service events"""
    if service_id not in service_logs:
        service_logs[service_id] = []
    
    service_logs[service_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(service_logs[service_id]) > 1000:
        service_logs[service_id] = service_logs[service_id][-1000:]

# ==================== SERVICE LIFECYCLE ROUTES ====================

@router.get("/", summary="List all services")
async def list_services(
    status: Optional[ServiceStatus] = Query(None),
    type: Optional[ServiceType] = Query(None),
    health: Optional[HealthStatus] = Query(None)
):
    """List all services with optional filtering"""
    result = list(services_registry.values())
    
    if status:
        result = [s for s in result if s.get("status") == status.value]
    if type:
        result = [s for s in result if s.get("type") == type.value]
    if health:
        result = [s for s in result if s.get("health") == health.value]
    
    return {
        "total": len(result),
        "services": result
    }

@router.post("/", summary="Create new service")
async def create_service(service: ServiceCreate):
    """Create a new service"""
    service_id = f"svc_{service.name.lower().replace(' ', '-')}_{int(datetime.utcnow().timestamp())}"
    
    if service_id in services_registry:
        raise HTTPException(status_code=409, detail="[❌] Service already exists")
    
    service_data = service.dict()
    service_data["id"] = service_id
    service_data["status"] = ServiceStatus.CREATED.value
    service_data["health"] = HealthStatus.UNKNOWN.value
    service_data["created_at"] = datetime.utcnow().isoformat()
    service_data["metadata"] = {}
    
    services_registry[service_id] = service_data
    log_service_event(service_id, "INFO", f"Service created: {service.name}")
    
    return {
        "message": "[✅] Service created successfully",
        "service_id": service_id,
        "service": service_data
    }

@router.get("/{service_id}", summary="Get service details")
async def get_service(service_id: str):
    """Get detailed service information"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="[❌] Service not found")
    
    return services_registry[service_id]

@router.post("/{service_id}/install", summary="Install service")
async def install_service(service_id: str):
    """Install service (pull image, setup dependencies)"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    if service["status"] == ServiceStatus.INSTALLED.value:
        return {"message": "[ℹ️] Service already installed", "service": service}
    
    log_service_event(service_id, "INFO", "Installing service")
    
    try:
        # Check dependencies
        missing_deps = []
        for dep in service.get("dependencies", []):
            if dep not in services_registry or services_registry[dep]["status"] not in [
                ServiceStatus.RUNNING.value, ServiceStatus.INSTALLED.value
            ]:
                missing_deps.append(dep)
        
        if missing_deps:
            raise HTTPException(
                status_code=424,
                detail=f"[❌] Missing dependencies: {', '.join(missing_deps)}"
            )
        
        await asyncio.sleep(0.1)  # Simulate installation
        
        service["status"] = ServiceStatus.INSTALLED.value
        service["installed_at"] = datetime.utcnow().isoformat()
        service["health"] = HealthStatus.HEALTHY.value
        
        log_service_event(service_id, "INFO", "Service installed successfully")
        
        return {
            "message": "[✅] Service installed successfully",
            "service": service
        }
    
    except Exception as e:
        service["status"] = ServiceStatus.FAILED.value
        service["health"] = HealthStatus.UNHEALTHY.value
        log_service_event(service_id, "ERROR", f"Installation failed: {str(e)}")
        raise

@router.post("/{service_id}/start", summary="Start service")
async def start_service(service_id: str):
    """Start the service"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    if service["status"] == ServiceStatus.RUNNING.value:
        return {"message": "[ℹ️] Service already running", "service": service}
    
    if service["status"] not in [ServiceStatus.INSTALLED.value, ServiceStatus.STOPPED.value]:
        raise HTTPException(
            status_code=400,
            detail=f"[❌] Cannot start service with status: {service['status']}"
        )
    
    log_service_event(service_id, "INFO", "Starting service")
    
    try:
        await asyncio.sleep(0.1)
        
        service["status"] = ServiceStatus.RUNNING.value
        service["started_at"] = datetime.utcnow().isoformat()
        service["health"] = HealthStatus.HEALTHY.value
        
        # Initialize metrics
        service_metrics[service_id] = {
            "requests": 0,
            "errors": 0,
            "uptime": 0,
            "cpu_usage": 0.0,
            "memory_usage": 0.0
        }
        
        log_service_event(service_id, "INFO", "Service started successfully")
        
        return {
            "message": "[🚀] Service started",
            "service": service
        }
    
    except Exception as e:
        service["status"] = ServiceStatus.FAILED.value
        service["health"] = HealthStatus.UNHEALTHY.value
        log_service_event(service_id, "ERROR", f"Start failed: {str(e)}")
        raise

@router.post("/{service_id}/stop", summary="Stop service")
async def stop_service(service_id: str):
    """Stop the service gracefully"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    if service["status"] != ServiceStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="[❌] Service is not running")
    
    log_service_event(service_id, "INFO", "Stopping service")
    
    try:
        await asyncio.sleep(0.1)
        
        service["status"] = ServiceStatus.STOPPED.value
        service["stopped_at"] = datetime.utcnow().isoformat()
        service["health"] = HealthStatus.UNKNOWN.value
        
        log_service_event(service_id, "INFO", "Service stopped")
        
        return {
            "message": "Service stopped",
            "service": service
        }
    
    except Exception as e:
        log_service_event(service_id, "ERROR", f"Stop failed: {str(e)}")
        raise

@router.post("/{service_id}/restart", summary="Restart service")
async def restart_service(service_id: str):
    """Restart the service"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    log_service_event(service_id, "INFO", "Restarting service")
    
    # Stop then start
    await stop_service(service_id)
    await asyncio.sleep(0.2)
    await start_service(service_id)
    
    return {
        "message": "Service restarted",
        "service": services_registry[service_id]
    }

@router.delete("/{service_id}", summary="Remove service")
async def remove_service(service_id: str, force: bool = Query(False)):
    """Remove service from registry"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    # Check dependents
    if not force:
        dependents = [
            s["name"] for s in services_registry.values()
            if service_id in s.get("dependencies", [])
        ]
        if dependents:
            raise HTTPException(
                status_code=409,
                detail=f"Services depend on this: {', '.join(dependents)}"
            )
    
    log_service_event(service_id, "WARNING", "Removing service")
    
    try:
        if service["status"] == ServiceStatus.RUNNING.value:
            await stop_service(service_id)
        
        del services_registry[service_id]
        log_service_event(service_id, "INFO", "Service removed")
        
        return {
            "message": "Service removed successfully",
            "service_id": service_id
        }
    
    except Exception as e:
        log_service_event(service_id, "ERROR", f"Removal failed: {str(e)}")
        raise

@router.post("/{service_id}/uninstall", summary="Uninstall service")
async def uninstall_service(service_id: str):
    """Uninstall service completely"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    log_service_event(service_id, "INFO", "Uninstalling service")
    
    try:
        if service["status"] == ServiceStatus.RUNNING.value:
            await stop_service(service_id)
        
        await asyncio.sleep(0.1)
        
        service["status"] = ServiceStatus.CREATED.value
        service["health"] = HealthStatus.UNKNOWN.value
        
        log_service_event(service_id, "INFO", "Service uninstalled")
        
        return {
            "message": "Service uninstalled",
            "service": service
        }
    
    except Exception as e:
        log_service_event(service_id, "ERROR", f"Uninstall failed: {str(e)}")
        raise

@router.put("/{service_id}", summary="Update service")
async def update_service(service_id: str, update: ServiceUpdate):
    """Update service configuration"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    
    log_service_event(service_id, "INFO", "Updating service")
    
    if update.version:
        service["version"] = update.version
    if update.replicas is not None:
        service["replicas"] = update.replicas
    if update.environment:
        service["environment"].update(update.environment)
    if update.resources:
        service["resources"].update(update.resources)
    if update.metadata:
        service["metadata"].update(update.metadata)
    
    service["updated_at"] = datetime.utcnow().isoformat()
    
    log_service_event(service_id, "INFO", "Service updated")
    
    return {
        "message": "Service updated",
        "service": service
    }

@router.put("/{service_id}/config", summary="Configure service")
async def configure_service(service_id: str, config: ServiceConfig):
    """Update service configuration"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    service["metadata"]["config"] = config.config
    service["config_updated_at"] = datetime.utcnow().isoformat()
    
    log_service_event(service_id, "INFO", "Configuration updated")
    
    return {
        "message": "Configuration updated",
        "config": config.config
    }

# ==================== MONITORING & OPERATIONS ====================

@router.get("/{service_id}/health", summary="Service health check")
async def check_service_health(service_id: str):
    """Get service health status"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service = services_registry[service_id]
    metrics = service_metrics.get(service_id, {})
    
    return {
        "service_id": service_id,
        "status": service["status"],
        "health": service.get("health", "unknown"),
        "version": service["version"],
        "replicas": service["replicas"],
        "metrics": metrics
    }

@router.get("/{service_id}/logs", summary="Get service logs")
async def get_service_logs(
    service_id: str,
    lines: int = Query(100, ge=1, le=10000)
):
    """Retrieve service logs"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    logs = service_logs.get(service_id, [])
    
    return {
        "service_id": service_id,
        "total_logs": len(logs),
        "logs": logs[-lines:]
    }

@router.get("/{service_id}/metrics", summary="Get service metrics")
async def get_service_metrics(service_id: str):
    """Get detailed service metrics"""
    if service_id not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {
        "service_id": service_id,
        "metrics": service_metrics.get(service_id, {})
    }

# ==================== BULK OPERATIONS ====================

@router.post("/import", summary="Bulk import services")
async def import_services(data: BulkImport):
    """Import multiple services from JSON"""
    imported = []
    errors = []
    
    for service_info in data.services:
        try:
            service_create = ServiceCreate(
                name=service_info.name,
                type=service_info.type,
                port=service_info.port,
                version=service_info.version,
                description=service_info.description,
                replicas=service_info.replicas,
                image=service_info.image,
                environment=service_info.environment,
                resources=service_info.resources,
                dependencies=service_info.dependencies
            )
            result = await create_service(service_create)
            imported.append(result["service_id"])
        except Exception as e:
            errors.append({
                "service": service_info.name,
                "error": str(e)
            })
    
    return {
        "imported": len(imported),
        "failed": len(errors),
        "service_ids": imported,
        "errors": errors
    }

@router.get("/export", summary="Bulk export services")
async def export_services():
    """Export all services to JSON"""
    return {
        "total": len(services_registry),
        "services": list(services_registry.values()),
        "exported_at": datetime.utcnow().isoformat()
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Service statistics")
async def get_service_stats():
    """Get comprehensive service statistics"""
    stats = {
        "total_services": len(services_registry),
        "by_status": {},
        "by_type": {},
        "by_health": {}
    }
    
    for service in services_registry.values():
        status = service.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        stype = service.get("type", "unknown")
        stats["by_type"][stype] = stats["by_type"].get(stype, 0) + 1
        
        health = service.get("health", "unknown")
        stats["by_health"][health] = stats["by_health"].get(health, 0) + 1
    
    return stats
