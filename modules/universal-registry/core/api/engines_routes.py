"""
Compute Engine Management API Routes
Advanced processing engines for analytics, AI/ML, compute, and storage workloads
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/engines", tags=["engines"])

# ==================== DATA MODELS ====================

class EngineType(str, Enum):
    PROCESSING = "processing"
    ANALYTICS = "analytics"
    AI_ML = "ai"
    COMPUTE = "compute"
    STORAGE = "storage"
    STREAM = "stream"
    BATCH = "batch"

class EngineStatus(str, Enum):
    REGISTERED = "registered"
    INSTALLED = "installed"
    RUNNING = "running"
    STOPPED = "stopped"
    SCALING = "scaling"
    FAILED = "failed"

class ScalingPolicy(str, Enum):
    MANUAL = "manual"
    AUTO_CPU = "auto_cpu"
    AUTO_MEMORY = "auto_memory"
    AUTO_QUEUE = "auto_queue"
    PREDICTIVE = "predictive"

class EngineInfo(BaseModel):
    id: str
    name: str
    type: EngineType
    version: str
    description: Optional[str] = None
    capacity: int  # Number of workers/threads
    min_capacity: int = 1
    max_capacity: int = 100
    scaling_policy: ScalingPolicy = ScalingPolicy.MANUAL
    gpu_enabled: bool = False
    gpu_count: int = 0
    memory_limit: Optional[str] = None
    cpu_limit: Optional[float] = None
    runtime: Optional[str] = None
    metadata: Dict[str, Any] = {}

class EngineCreate(BaseModel):
    name: str
    type: EngineType
    version: str = "1.0.0"
    description: Optional[str] = None
    capacity: int = 10
    min_capacity: int = 1
    max_capacity: int = 100
    scaling_policy: ScalingPolicy = ScalingPolicy.MANUAL
    gpu_enabled: bool = False
    gpu_count: int = 0
    memory_limit: Optional[str] = "4Gi"
    cpu_limit: Optional[float] = 2.0
    runtime: Optional[str] = None

class EngineUpdate(BaseModel):
    version: Optional[str] = None
    capacity: Optional[int] = None
    min_capacity: Optional[int] = None
    max_capacity: Optional[int] = None
    scaling_policy: Optional[ScalingPolicy] = None
    metadata: Optional[Dict[str, Any]] = None

class ScaleRequest(BaseModel):
    capacity: int

class WorkloadSubmit(BaseModel):
    task_type: str
    data: Dict[str, Any]
    priority: int = 5

# ==================== ENGINE REGISTRY ====================

engines_registry: Dict[str, Dict[str, Any]] = {}
engine_logs: Dict[str, List[Dict[str, Any]]] = {}
engine_workloads: Dict[str, List[Dict[str, Any]]] = {}
engine_metrics: Dict[str, Dict[str, Any]] = {}

def log_engine_event(engine_id: str, level: str, message: str):
    """Log engine events"""
    if engine_id not in engine_logs:
        engine_logs[engine_id] = []
    
    engine_logs[engine_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(engine_logs[engine_id]) > 1000:
        engine_logs[engine_id] = engine_logs[engine_id][-1000:]

# ==================== ENGINE LIFECYCLE ====================

@router.get("/", summary="List all engines")
async def list_engines(
    type: Optional[EngineType] = Query(None),
    status: Optional[EngineStatus] = Query(None),
    gpu_enabled: Optional[bool] = Query(None)
):
    """List all compute engines with filtering"""
    result = list(engines_registry.values())
    
    if type:
        result = [e for e in result if e.get("type") == type.value]
    if status:
        result = [e for e in result if e.get("status") == status.value]
    if gpu_enabled is not None:
        result = [e for e in result if e.get("gpu_enabled") == gpu_enabled]
    
    return {
        "total": len(result),
        "engines": result
    }

@router.post("/", summary="Create new engine")
async def create_engine(engine: EngineCreate):
    """Register a new compute engine"""
    engine_id = f"eng_{engine.name.lower().replace(' ', '-')}_{int(datetime.utcnow().timestamp())}"
    
    if engine_id in engines_registry:
        raise HTTPException(status_code=409, detail="Engine already exists")
    
    engine_data = engine.dict()
    engine_data["id"] = engine_id
    engine_data["status"] = EngineStatus.REGISTERED.value
    engine_data["current_capacity"] = 0
    engine_data["active_tasks"] = 0
    engine_data["completed_tasks"] = 0
    engine_data["failed_tasks"] = 0
    engine_data["created_at"] = datetime.utcnow().isoformat()
    
    engines_registry[engine_id] = engine_data
    log_engine_event(engine_id, "INFO", f"Engine registered: {engine.name}")
    
    return {
        "message": "Engine created successfully",
        "engine_id": engine_id,
        "engine": engine_data
    }

@router.get("/{engine_id}", summary="Get engine details")
async def get_engine(engine_id: str):
    """Get detailed engine information"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    return engines_registry[engine_id]

@router.post("/{engine_id}/install", summary="Install engine")
async def install_engine(engine_id: str):
    """Install and configure the engine"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if engine["status"] == EngineStatus.INSTALLED.value:
        return {"message": "Engine already installed", "engine": engine}
    
    log_engine_event(engine_id, "INFO", "Installing engine")
    
    try:
        await asyncio.sleep(0.1)
        
        engine["status"] = EngineStatus.INSTALLED.value
        engine["installed_at"] = datetime.utcnow().isoformat()
        
        # Initialize metrics
        engine_metrics[engine_id] = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "gpu_usage": 0.0 if engine["gpu_enabled"] else None,
            "throughput": 0,
            "queue_length": 0,
            "avg_task_time": 0.0
        }
        
        log_engine_event(engine_id, "INFO", "Engine installed successfully")
        
        return {
            "message": "Engine installed successfully",
            "engine": engine
        }
    
    except Exception as e:
        engine["status"] = EngineStatus.FAILED.value
        log_engine_event(engine_id, "ERROR", f"Installation failed: {str(e)}")
        raise

@router.post("/{engine_id}/start", summary="Start engine")
async def start_engine(engine_id: str):
    """Start the compute engine"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if engine["status"] == EngineStatus.RUNNING.value:
        return {"message": "Engine already running", "engine": engine}
    
    if engine["status"] not in [EngineStatus.INSTALLED.value, EngineStatus.STOPPED.value]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start engine with status: {engine['status']}"
        )
    
    log_engine_event(engine_id, "INFO", "Starting engine")
    
    try:
        await asyncio.sleep(0.1)
        
        engine["status"] = EngineStatus.RUNNING.value
        engine["started_at"] = datetime.utcnow().isoformat()
        engine["current_capacity"] = engine["capacity"]
        
        # Initialize workload queue
        engine_workloads[engine_id] = []
        
        log_engine_event(engine_id, "INFO", f"Engine started with capacity {engine['capacity']}")
        
        return {
            "message": "Engine started",
            "engine": engine
        }
    
    except Exception as e:
        engine["status"] = EngineStatus.FAILED.value
        log_engine_event(engine_id, "ERROR", f"Start failed: {str(e)}")
        raise

@router.post("/{engine_id}/stop", summary="Stop engine")
async def stop_engine(engine_id: str):
    """Stop the compute engine gracefully"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if engine["status"] != EngineStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Engine is not running")
    
    log_engine_event(engine_id, "INFO", "Stopping engine")
    
    try:
        # Wait for active tasks to complete
        await asyncio.sleep(0.2)
        
        engine["status"] = EngineStatus.STOPPED.value
        engine["stopped_at"] = datetime.utcnow().isoformat()
        engine["current_capacity"] = 0
        
        log_engine_event(engine_id, "INFO", "Engine stopped")
        
        return {
            "message": "Engine stopped",
            "engine": engine
        }
    
    except Exception as e:
        log_engine_event(engine_id, "ERROR", f"Stop failed: {str(e)}")
        raise

@router.delete("/{engine_id}", summary="Remove engine")
async def remove_engine(engine_id: str):
    """Remove engine from registry"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if engine["status"] == EngineStatus.RUNNING.value:
        await stop_engine(engine_id)
    
    log_engine_event(engine_id, "WARNING", "Removing engine")
    
    del engines_registry[engine_id]
    
    return {
        "message": "Engine removed successfully",
        "engine_id": engine_id
    }

@router.put("/{engine_id}", summary="Update engine")
async def update_engine(engine_id: str, update: EngineUpdate):
    """Update engine configuration"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    log_engine_event(engine_id, "INFO", "Updating engine configuration")
    
    if update.version:
        engine["version"] = update.version
    if update.capacity is not None:
        engine["capacity"] = update.capacity
    if update.min_capacity is not None:
        engine["min_capacity"] = update.min_capacity
    if update.max_capacity is not None:
        engine["max_capacity"] = update.max_capacity
    if update.scaling_policy:
        engine["scaling_policy"] = update.scaling_policy.value
    if update.metadata:
        engine["metadata"].update(update.metadata)
    
    engine["updated_at"] = datetime.utcnow().isoformat()
    
    log_engine_event(engine_id, "INFO", "Engine updated")
    
    return {
        "message": "Engine updated",
        "engine": engine
    }

# ==================== SCALING OPERATIONS ====================

@router.post("/{engine_id}/scale", summary="Scale engine capacity")
async def scale_engine(engine_id: str, request: ScaleRequest):
    """Manually scale engine capacity"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if request.capacity < engine["min_capacity"] or request.capacity > engine["max_capacity"]:
        raise HTTPException(
            status_code=400,
            detail=f"Capacity must be between {engine['min_capacity']} and {engine['max_capacity']}"
        )
    
    log_engine_event(engine_id, "INFO", f"Scaling from {engine['current_capacity']} to {request.capacity}")
    
    engine["status"] = EngineStatus.SCALING.value
    await asyncio.sleep(0.1)
    
    engine["current_capacity"] = request.capacity
    engine["status"] = EngineStatus.RUNNING.value
    engine["scaled_at"] = datetime.utcnow().isoformat()
    
    log_engine_event(engine_id, "INFO", f"Scaled to {request.capacity} workers")
    
    return {
        "message": "Engine scaled successfully",
        "old_capacity": engine.get("capacity"),
        "new_capacity": request.capacity,
        "engine": engine
    }

# ==================== WORKLOAD MANAGEMENT ====================

@router.post("/{engine_id}/submit", summary="Submit workload")
async def submit_workload(engine_id: str, workload: WorkloadSubmit):
    """Submit a task to the engine"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    
    if engine["status"] != EngineStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Engine is not running")
    
    task = {
        "id": f"task_{int(datetime.utcnow().timestamp())}",
        "type": workload.task_type,
        "data": workload.data,
        "priority": workload.priority,
        "submitted_at": datetime.utcnow().isoformat(),
        "status": "queued"
    }
    
    engine_workloads[engine_id].append(task)
    engine["active_tasks"] += 1
    
    log_engine_event(engine_id, "INFO", f"Task submitted: {task['id']}")
    
    return {
        "message": "Task submitted",
        "task": task,
        "queue_position": len(engine_workloads[engine_id])
    }

@router.get("/{engine_id}/workloads", summary="Get engine workloads")
async def get_workloads(engine_id: str):
    """Get all workloads for an engine"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    workloads = engine_workloads.get(engine_id, [])
    
    return {
        "engine_id": engine_id,
        "total_workloads": len(workloads),
        "workloads": workloads
    }

# ==================== MONITORING ====================

@router.get("/{engine_id}/metrics", summary="Get engine metrics")
async def get_engine_metrics(engine_id: str):
    """Get real-time engine metrics"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    engine = engines_registry[engine_id]
    metrics = engine_metrics.get(engine_id, {})
    
    return {
        "engine_id": engine_id,
        "status": engine["status"],
        "capacity": {
            "current": engine.get("current_capacity", 0),
            "min": engine["min_capacity"],
            "max": engine["max_capacity"],
            "target": engine["capacity"]
        },
        "tasks": {
            "active": engine.get("active_tasks", 0),
            "completed": engine.get("completed_tasks", 0),
            "failed": engine.get("failed_tasks", 0)
        },
        "resources": metrics,
        "gpu": {
            "enabled": engine["gpu_enabled"],
            "count": engine["gpu_count"]
        } if engine["gpu_enabled"] else None
    }

@router.get("/{engine_id}/logs", summary="Get engine logs")
async def get_engine_logs(
    engine_id: str,
    lines: int = Query(100, ge=1, le=10000)
):
    """Retrieve engine logs"""
    if engine_id not in engines_registry:
        raise HTTPException(status_code=404, detail="Engine not found")
    
    logs = engine_logs.get(engine_id, [])
    
    return {
        "engine_id": engine_id,
        "total_logs": len(logs),
        "logs": logs[-lines:]
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Engine statistics")
async def get_engine_stats():
    """Get comprehensive engine statistics"""
    stats = {
        "total_engines": len(engines_registry),
        "by_type": {},
        "by_status": {},
        "total_capacity": 0,
        "active_capacity": 0,
        "gpu_engines": 0
    }
    
    for engine in engines_registry.values():
        etype = engine.get("type", "unknown")
        stats["by_type"][etype] = stats["by_type"].get(etype, 0) + 1
        
        status = engine.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        stats["total_capacity"] += engine.get("capacity", 0)
        if engine.get("status") == EngineStatus.RUNNING.value:
            stats["active_capacity"] += engine.get("current_capacity", 0)
        
        if engine.get("gpu_enabled"):
            stats["gpu_engines"] += 1
    
    return stats
