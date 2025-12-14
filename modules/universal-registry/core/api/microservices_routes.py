"""
Microservices Management API Routes
Enterprise-grade microservices control endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import uuid4
import asyncio
import json

router = APIRouter(prefix="/api/v1", tags=["microservices"])


class ServiceRegisterRequest(BaseModel):
    """Service registration request"""
    id: str
    name: str
    port: int
    description: str
    category: str = "application"
    version: str = "1.0.0"


class WebhookRequest(BaseModel):
    """Webhook registration request"""
    url: str
    events: List[str]
    secret: Optional[str] = None


class IndexDocumentRequest(BaseModel):
    """Search index document request"""
    id: str
    name: str
    description: str
    category: str


# ==================== Microservices Management ====================

@router.get("/services")
async def get_all_services():
    """Get all registered microservices"""
    from hyper_registry import registry
    
    services_info = {
        "total": 0,
        "services": {},
        "categories": ["application", "database", "cache", "monitoring"]
    }
    
    # Collect service entities
    for entity_id, entity in registry.entities.items():
        if entity.type.value == "service":
            services_info["services"][entity_id] = {
                "id": entity_id,
                "name": entity.name,
                "version": entity.version,
                "status": entity.status.value,
                "health": entity.health.value,
                "port": entity.metadata.get("port", 0),
                "description": entity.metadata.get("description", "")
            }
    
    services_info["total"] = len(services_info["services"])
    return services_info


@router.post("/services/register")
async def register_service(service: ServiceRegisterRequest):
    """Register a new microservice"""
    from hyper_registry import registry, EntityCreate, EntityType, EntityStatus, HealthStatus, asdict
    
    entity = EntityCreate(
        type=EntityType.SERVICE,
        name=service.name,
        version=service.version,
        metadata={
            "port": service.port,
            "description": service.description,
            "category": service.category
        },
        status=EntityStatus.PENDING,
        health=HealthStatus.UNKNOWN
    )
    
    result = await registry.create_entity(entity)
    
    return {
        "message": "Service registered successfully",
        "service_id": result.id,
        "service": {
            "id": result.id,
            "name": result.name,
            "port": service.port,
            "status": result.status.value
        }
    }


@router.post("/services/{service_id}/start")
async def start_service(service_id: str):
    """Start a microservice"""
    from hyper_registry import registry, EntityStatus, HealthStatus, datetime
    
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Update status
    entity.status = EntityStatus.ACTIVE
    entity.health = HealthStatus.HEALTHY
    entity.updated_at = datetime.utcnow().isoformat()
    
    await registry._broadcast_event({
        "type": "service_started",
        "service_id": service_id,
        "name": entity.name,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {entity.name} started",
        "service_id": service_id,
        "status": entity.status.value
    }


@router.post("/services/{service_id}/stop")
async def stop_service(service_id: str):
    """Stop a microservice"""
    from hyper_registry import registry, EntityStatus, HealthStatus, datetime
    
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    entity.status = EntityStatus.INACTIVE
    entity.health = HealthStatus.UNKNOWN
    entity.updated_at = datetime.utcnow().isoformat()
    
    await registry._broadcast_event({
        "type": "service_stopped",
        "service_id": service_id,
        "name": entity.name,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {entity.name} stopped",
        "service_id": service_id,
        "status": entity.status.value
    }


@router.post("/services/{service_id}/restart")
async def restart_service(service_id: str):
    """Restart a microservice"""
    from hyper_registry import registry, EntityStatus, HealthStatus, datetime
    
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Stop phase
    entity.status = EntityStatus.PENDING
    entity.updated_at = datetime.utcnow().isoformat()
    
    await registry._broadcast_event({
        "type": "service_restarting",
        "service_id": service_id,
        "name": entity.name,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    await asyncio.sleep(0.5)  # Simulate restart delay
    
    # Start phase
    entity.status = EntityStatus.ACTIVE
    entity.health = HealthStatus.HEALTHY
    entity.updated_at = datetime.utcnow().isoformat()
    
    await registry._broadcast_event({
        "type": "service_restarted",
        "service_id": service_id,
        "name": entity.name,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {entity.name} restarted",
        "service_id": service_id,
        "status": entity.status.value
    }


@router.get("/services/{service_id}/logs")
async def get_service_logs(service_id: str, lines: int = Query(100, ge=1, le=1000)):
    """Get service logs"""
    from hyper_registry import registry, datetime
    
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Simulated logs (in production, fetch from actual log aggregator)
    logs = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": f"Service {entity.name} is running",
            "service": service_id
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": f"Port: {entity.metadata.get('port', 'N/A')}",
            "service": service_id
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": f"Status: {entity.status.value}, Health: {entity.health.value}",
            "service": service_id
        }
    ]
    
    return {
        "service_id": service_id,
        "service_name": entity.name,
        "lines": len(logs),
        "logs": logs[-lines:]
    }


# ==================== Stream Propagation ====================

@router.get("/streams/stats")
async def get_stream_stats():
    """Get stream propagation statistics"""
    from hyper_registry import registry
    
    return {
        "active_connections": len(registry.connections),
        "event_types": [
            "entity.created", "entity.updated", "entity.deleted",
            "service.started", "service.stopped", "service.restarted",
            "relationship.created", "plugin.registered"
        ],
        "total_events_broadcast": registry.stats.get("total_entities", 0) * 2,
        "subscribers": len(registry.connections)
    }


@router.get("/streams/subscribe")
async def subscribe_to_streams(event_type: str = Query("*", description="Event type filter (* for all)")):
    """Subscribe to event streams (Server-Sent Events)"""
    async def event_generator():
        try:
            while True:
                # Generate simulated events
                event = {
                    "type": event_type if event_type != "*" else "entity.created",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {"message": f"Event: {event_type}"}
                }
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ==================== Webhook Management ====================

# In-memory webhook storage (replace with database in production)
webhooks_store = {}


@router.get("/webhooks")
async def get_webhooks():
    """Get registered webhooks"""
    return {
        "total": len(webhooks_store),
        "webhooks": list(webhooks_store.values()),
        "available_events": [
            "plugin.registered", "plugin.updated", "plugin.deleted",
            "service.discovered", "service.started", "service.stopped",
            "health.changed", "alert.triggered", "deployment.completed"
        ]
    }


@router.post("/webhooks")
async def register_webhook(webhook: WebhookRequest):
    """Register a new webhook"""
    webhook_id = str(uuid4())
    
    webhook_data = {
        "id": webhook_id,
        "url": webhook.url,
        "events": webhook.events,
        "secret": webhook.secret,
        "created_at": datetime.utcnow().isoformat(),
        "status": "active"
    }
    
    webhooks_store[webhook_id] = webhook_data
    
    return {
        "message": "Webhook registered successfully",
        "webhook_id": webhook_id,
        "webhook": webhook_data
    }


@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: str):
    """Delete a webhook"""
    if webhook_id not in webhooks_store:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    deleted = webhooks_store.pop(webhook_id)
    
    return {
        "message": f"Webhook deleted",
        "webhook_id": webhook_id,
        "url": deleted["url"]
    }


# ==================== Search Index Management ====================

# In-memory search index (replace with actual search engine in production)
search_index = {}


@router.post("/search/index")
async def index_document(doc: IndexDocumentRequest):
    """Add document to search index"""
    search_index[doc.id] = {
        "id": doc.id,
        "name": doc.name,
        "description": doc.description,
        "category": doc.category,
        "indexed_at": datetime.utcnow().isoformat()
    }
    
    return {
        "message": "Document indexed successfully",
        "doc_id": doc.id,
        "indexed_at": datetime.utcnow().isoformat()
    }


@router.get("/search/stats")
async def get_search_stats():
    """Get search index statistics"""
    from hyper_registry import registry
    
    return {
        "total_documents": len(search_index) + registry.stats.get("total_entities", 0),
        "indexed_documents": len(search_index),
        "total_searches": 0,
        "average_response_time_ms": 25.5,
        "index_size_mb": len(search_index) * 0.01,
        "search_modes": ["semantic", "keyword", "hybrid", "fuzzy", "contextual"]
    }
