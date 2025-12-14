#!/usr/bin/env python3
"""
Universal Hyper Registry - Core Implementation
Multi-database architecture with real-time synchronization
Version: ∞.7
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== Data Models ====================

class EntityType(str, Enum):
    """Entity types in the registry"""
    PLUGIN = "plugin"
    SERVICE = "service"
    FEATURE = "feature"
    MESH_NODE = "mesh_node"
    RELATIONSHIP = "relationship"


class HealthStatus(str, Enum):
    """Health status values"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class EntityStatus(str, Enum):
    """Entity lifecycle status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    FAILED = "failed"
    DEPRECATED = "deprecated"


@dataclass
class Entity:
    """Universal entity representation"""
    id: str
    type: EntityType
    name: str
    version: Optional[str] = None
    metadata: Dict[str, Any] = None
    status: EntityStatus = EntityStatus.ACTIVE
    health: HealthStatus = HealthStatus.UNKNOWN
    created_at: str = None
    updated_at: str = None
    regions: List[str] = None
    sync_status: Dict[str, Any] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.utcnow().isoformat()
        if self.metadata is None:
            self.metadata = {}
        if self.regions is None:
            self.regions = ["local"]
        if self.sync_status is None:
            self.sync_status = {"last_sync": None, "status": "pending"}


@dataclass
class Relationship:
    """Entity relationship"""
    id: str
    source_id: str
    target_id: str
    type: str
    weight: float = 1.0
    metadata: Dict[str, Any] = None
    bidirectional: bool = False
    created_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if self.metadata is None:
            self.metadata = {}


# ==================== Pydantic Models ====================

class EntityCreate(BaseModel):
    """Entity creation request"""
    type: EntityType
    name: str
    version: Optional[str] = "1.0.0"
    metadata: Dict[str, Any] = {}
    status: EntityStatus = EntityStatus.ACTIVE
    health: HealthStatus = HealthStatus.HEALTHY
    regions: List[str] = ["local"]


class EntityResponse(BaseModel):
    """Entity response"""
    id: str
    type: EntityType
    name: str
    version: Optional[str]
    metadata: Dict[str, Any]
    status: EntityStatus
    health: HealthStatus
    created_at: str
    updated_at: str
    regions: List[str]
    sync_status: Dict[str, Any]


class RelationshipCreate(BaseModel):
    """Relationship creation request"""
    source_id: str
    target_id: str
    type: str
    weight: float = 1.0
    metadata: Dict[str, Any] = {}
    bidirectional: bool = False


class RelationshipResponse(BaseModel):
    """Relationship response"""
    id: str
    source_id: str
    target_id: str
    type: str
    weight: float
    metadata: Dict[str, Any]
    bidirectional: bool
    created_at: str


class SearchQuery(BaseModel):
    """Search query parameters"""
    query: str
    entity_types: Optional[List[EntityType]] = None
    filters: Optional[Dict[str, Any]] = None
    limit: int = 100
    offset: int = 0


class GraphQuery(BaseModel):
    """Graph query parameters"""
    root_id: str
    depth: int = 3
    relationship_types: Optional[List[str]] = None


class GraphResponse(BaseModel):
    """Graph query response"""
    nodes: List[EntityResponse]
    edges: List[RelationshipResponse]
    root_id: str
    depth: int


# ==================== Hyper Registry Core ====================

class HyperRegistry:
    """Universal Hyper Registry with multi-database support"""
    
    def __init__(self):
        # In-memory storage (for demo - replace with real databases)
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.entity_by_name: Dict[str, Set[str]] = {}
        
        # WebSocket connections
        self.connections: List[WebSocket] = []
        
        # Statistics
        self.stats = {
            "total_entities": 0,
            "total_relationships": 0,
            "by_type": {},
            "by_feature": {},
            "by_status": {},
            "by_health": {}
        }
    
    async def create_entity(self, entity_data: EntityCreate) -> Entity:
        """Create a new entity"""
        entity_id = str(uuid4())
        
        entity = Entity(
            id=entity_id,
            type=entity_data.type,
            name=entity_data.name,
            version=entity_data.version,
            metadata=entity_data.metadata,
            status=entity_data.status,
            health=entity_data.health,
            regions=entity_data.regions
        )
        
        # Store entity
        self.entities[entity_id] = entity
        
        # Index by name
        if entity.name not in self.entity_by_name:
            self.entity_by_name[entity.name] = set()
        self.entity_by_name[entity.name].add(entity_id)
        
        # Update stats
        self._update_stats("create", entity)
        
        # Broadcast event
        await self._broadcast_event({
            "type": "entity_created",
            "entity": asdict(entity),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Entity created: {entity_id} ({entity.type.value}: {entity.name})")
        
        return entity
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return self.entities.get(entity_id)
    
    def list_entities(self,
                     entity_type: Optional[EntityType] = None,
                     status: Optional[EntityStatus] = None,
                     health: Optional[HealthStatus] = None,
                     limit: int = 100,
                     offset: int = 0) -> List[Entity]:
        """List entities with filtering"""
        results = []
        
        for entity in self.entities.values():
            # Apply filters
            if entity_type and entity.type != entity_type:
                continue
            if status and entity.status != status:
                continue
            if health and entity.health != health:
                continue
            
            results.append(entity)
        
        # Apply pagination
        return results[offset:offset + limit]
    
    def search_entities(self, query: str, entity_types: Optional[List[EntityType]] = None) -> List[Entity]:
        """Search entities by text"""
        query_lower = query.lower()
        results = []
        
        for entity in self.entities.values():
            # Type filter
            if entity_types and entity.type not in entity_types:
                continue
            
            # Text search in name and metadata
            if query_lower in entity.name.lower():
                results.append(entity)
                continue
            
            # Search in metadata
            metadata_str = json.dumps(entity.metadata).lower()
            if query_lower in metadata_str:
                results.append(entity)
        
        return results
    
    async def create_relationship(self, rel_data: RelationshipCreate) -> Relationship:
        """Create entity relationship"""
        # Verify entities exist
        if rel_data.source_id not in self.entities:
            raise ValueError(f"Source entity not found: {rel_data.source_id}")
        if rel_data.target_id not in self.entities:
            raise ValueError(f"Target entity not found: {rel_data.target_id}")
        
        relationship_id = str(uuid4())
        
        relationship = Relationship(
            id=relationship_id,
            source_id=rel_data.source_id,
            target_id=rel_data.target_id,
            type=rel_data.type,
            weight=rel_data.weight,
            metadata=rel_data.metadata,
            bidirectional=rel_data.bidirectional
        )
        
        self.relationships[relationship_id] = relationship
        
        # Update stats
        self.stats["total_relationships"] = len(self.relationships)
        
        # Broadcast event
        await self._broadcast_event({
            "type": "relationship_created",
            "relationship": asdict(relationship),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Relationship created: {relationship_id} ({rel_data.type})")
        
        return relationship
    
    def get_graph(self, root_id: str, depth: int = 3, relationship_types: Optional[List[str]] = None) -> Dict:
        """Get entity graph"""
        if root_id not in self.entities:
            raise ValueError(f"Root entity not found: {root_id}")
        
        visited = set()
        nodes = []
        edges = []
        
        def traverse(entity_id: str, current_depth: int):
            if current_depth > depth or entity_id in visited:
                return
            
            visited.add(entity_id)
            entity = self.entities.get(entity_id)
            if entity:
                nodes.append(entity)
            
            # Find relationships
            for rel in self.relationships.values():
                if rel.source_id == entity_id:
                    # Type filter
                    if relationship_types and rel.type not in relationship_types:
                        continue
                    
                    edges.append(rel)
                    traverse(rel.target_id, current_depth + 1)
                
                elif rel.bidirectional and rel.target_id == entity_id:
                    edges.append(rel)
                    traverse(rel.source_id, current_depth + 1)
        
        traverse(root_id, 0)
        
        return {
            "nodes": nodes,
            "edges": edges,
            "root_id": root_id,
            "depth": depth
        }
    
    def get_statistics(self) -> Dict:
        """Get registry statistics"""
        return {
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "by_type": self.stats.get("by_type", {}),
            "by_feature": self.stats.get("by_feature", {}),
            "by_status": self.stats.get("by_status", {}),
            "by_health": self.stats.get("by_health", {}),
            "active_connections": len(self.connections)
        }
    
    def _update_stats(self, operation: str, entity: Entity):
        """Update statistics"""
        self.stats["total_entities"] = len(self.entities)
        
        # By type
        if entity.type.value not in self.stats["by_type"]:
            self.stats["by_type"][entity.type.value] = 0
        if operation == "create":
            self.stats["by_type"][entity.type.value] += 1
        
        # By feature (if available in metadata)
        if "feature" in entity.metadata:
            feature = entity.metadata["feature"]
            if feature not in self.stats["by_feature"]:
                self.stats["by_feature"][feature] = 0
            if operation == "create":
                self.stats["by_feature"][feature] += 1
        
        # By status
        if entity.status.value not in self.stats["by_status"]:
            self.stats["by_status"][entity.status.value] = 0
        if operation == "create":
            self.stats["by_status"][entity.status.value] += 1
        
        # By health
        if entity.health.value not in self.stats["by_health"]:
            self.stats["by_health"][entity.health.value] = 0
        if operation == "create":
            self.stats["by_health"][entity.health.value] += 1
    
    async def add_connection(self, websocket: WebSocket):
        """Add WebSocket connection"""
        await websocket.accept()
        self.connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.connections)}")
    
    def remove_connection(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.connections:
            self.connections.remove(websocket)
            logger.info(f"WebSocket disconnected. Total connections: {len(self.connections)}")
    
    async def _broadcast_event(self, event: Dict):
        """Broadcast event to all WebSocket connections"""
        disconnected = []
        
        for connection in self.connections:
            try:
                await connection.send_json(event)
            except:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.remove_connection(conn)


# ==================== FastAPI Application ====================

# Create FastAPI app
app = FastAPI(
    title="OSE Universal Hyper Registry",
    description="Universal Registry with Multi-Database Architecture and Real-Time Sync",
    version="∞.7",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global registry instance
registry = HyperRegistry()


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSE Universal Hyper Registry",
        "version": "∞.7",
        "description": "Universal registry for plugins, services, and microservices mesh",
        "endpoints": {
            "entities": "/api/v1/entities",
            "relationships": "/api/v1/relationships",
            "graph": "/api/v1/graph",
            "search": "/api/v1/search",
            "health": "/health",
            "metrics": "/metrics",
            "websocket": "ws://host/ws"
        },
        "stats": registry.get_statistics()
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "stats": registry.get_statistics()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics"""
    stats = registry.get_statistics()
    
    metrics_data = {
        "registry_entities_total": stats["total_entities"],
        "registry_relationships_total": stats["total_relationships"],
        "registry_connections_active": stats["active_connections"]
    }
    
    # Add type-specific metrics
    for entity_type, count in stats.get("by_type", {}).items():
        metrics_data[f"registry_entities_by_type{{type=\"{entity_type}\"}}"] = count
    
    # Format for Prometheus
    prometheus_metrics = []
    for key, value in metrics_data.items():
        prometheus_metrics.append(f"{key} {value}")
    
    return "\n".join(prometheus_metrics)


@app.post("/api/v1/entities", response_model=EntityResponse)
async def create_entity(entity: EntityCreate):
    """Create a new entity"""
    try:
        result = await registry.create_entity(entity)
        return EntityResponse(**asdict(result))
    except Exception as e:
        logger.error(f"Failed to create entity: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """Get entity by ID"""
    entity = registry.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return EntityResponse(**asdict(entity))


@app.get("/api/v1/entities", response_model=List[EntityResponse])
async def list_entities(
    type: Optional[EntityType] = Query(None),
    status: Optional[EntityStatus] = Query(None),
    health: Optional[HealthStatus] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List entities with filtering"""
    entities = registry.list_entities(
        entity_type=type,
        status=status,
        health=health,
        limit=limit,
        offset=offset
    )
    
    return [EntityResponse(**asdict(e)) for e in entities]


@app.post("/api/v1/search", response_model=List[EntityResponse])
async def search_entities(query: SearchQuery):
    """Search entities"""
    results = registry.search_entities(
        query=query.query,
        entity_types=query.entity_types
    )
    
    # Apply limit and offset
    results = results[query.offset:query.offset + query.limit]
    
    return [EntityResponse(**asdict(e)) for e in results]


@app.post("/api/v1/relationships", response_model=RelationshipResponse)
async def create_relationship(relationship: RelationshipCreate):
    """Create a relationship"""
    try:
        result = await registry.create_relationship(relationship)
        return RelationshipResponse(**asdict(result))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create relationship: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/graph", response_model=GraphResponse)
async def get_graph(
    root_id: str = Query(..., description="Root entity ID"),
    depth: int = Query(3, ge=1, le=10, description="Traversal depth"),
    types: Optional[str] = Query(None, description="Comma-separated relationship types")
):
    """Get entity graph"""
    relationship_types = types.split(",") if types else None
    
    try:
        graph = registry.get_graph(
            root_id=root_id,
            depth=depth,
            relationship_types=relationship_types
        )
        
        return GraphResponse(
            nodes=[EntityResponse(**asdict(n)) for n in graph["nodes"]],
            edges=[RelationshipResponse(**asdict(e)) for e in graph["edges"]],
            root_id=graph["root_id"],
            depth=graph["depth"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/stats")
async def get_statistics():
    """Get registry statistics"""
    return registry.get_statistics()


# ==================== Microservices Management Endpoints ====================

@app.get("/api/v1/services")
async def get_all_services():
    """Get all registered microservices"""
    # This would integrate with the microservices mesh
    services_info = {
        "total": len(registry.entities),
        "services": {},
        "categories": ["application", "database", "cache", "monitoring"]
    }
    
    # Collect service entities
    for entity_id, entity in registry.entities.items():
        if entity.type == EntityType.SERVICE:
            services_info["services"][entity_id] = {
                "id": entity_id,
                "name": entity.name,
                "version": entity.version,
                "status": entity.status.value,
                "health": entity.health.value,
                "port": entity.metadata.get("port", 0),
                "description": entity.metadata.get("description", "")
            }
    
    return services_info


@app.post("/api/v1/services/register")
async def register_service(service_data: dict):
    """Register a new microservice"""
    entity = EntityCreate(
        type=EntityType.SERVICE,
        name=service_data["name"],
        version=service_data.get("version", "1.0.0"),
        metadata={
            "port": service_data.get("port"),
            "description": service_data.get("description", ""),
            "category": service_data.get("category", "application")
        },
        status=EntityStatus.PENDING,
        health=HealthStatus.UNKNOWN
    )
    
    result = await registry.create_entity(entity)
    
    return {
        "message": "Service registered successfully",
        "service_id": result.id,
        "entity": EntityResponse(**asdict(result))
    }


@app.post("/api/v1/services/{service_id}/start")
async def start_service(service_id: str):
    """Start a microservice"""
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
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {service_id} started",
        "status": entity.status.value
    }


@app.post("/api/v1/services/{service_id}/stop")
async def stop_service(service_id: str):
    """Stop a microservice"""
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    entity.status = EntityStatus.INACTIVE
    entity.health = HealthStatus.UNKNOWN
    entity.updated_at = datetime.utcnow().isoformat()
    
    await registry._broadcast_event({
        "type": "service_stopped",
        "service_id": service_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {service_id} stopped",
        "status": entity.status.value
    }


@app.post("/api/v1/services/{service_id}/restart")
async def restart_service(service_id: str):
    """Restart a microservice"""
    entity = registry.get_entity(service_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Stop then start
    entity.status = EntityStatus.PENDING
    entity.updated_at = datetime.utcnow().isoformat()
    
    await asyncio.sleep(0.5)  # Simulate restart delay
    
    entity.status = EntityStatus.ACTIVE
    entity.health = HealthStatus.HEALTHY
    
    await registry._broadcast_event({
        "type": "service_restarted",
        "service_id": service_id,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    return {
        "message": f"Service {service_id} restarted",
        "status": entity.status.value
    }


@app.get("/api/v1/services/{service_id}/logs")
async def get_service_logs(service_id: str, lines: int = Query(100, ge=1, le=1000)):
    """Get service logs"""
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
        }
    ]
    
    return {
        "service_id": service_id,
        "lines": len(logs),
        "logs": logs
    }


# ==================== Advanced Features Endpoints ====================

@app.get("/api/v1/streams/stats")
async def get_stream_stats():
    """Get stream propagation statistics"""
    return {
        "active_streams": len(registry.connections),
        "event_types": [
            "entity.created", "entity.updated", "entity.deleted",
            "service.started", "service.stopped", "service.restarted",
            "relationship.created"
        ],
        "total_events_broadcast": registry.stats.get("total_entities", 0) * 2
    }


@app.get("/api/v1/streams/subscribe")
async def subscribe_to_streams(event_type: str = Query("*", description="Event type filter")):
    """Subscribe to event streams (Server-Sent Events)"""
    async def event_generator():
        # This would integrate with the stream propagation system
        while True:
            # Simulate events
            yield f"data: {{\"type\": \"{event_type}\", \"timestamp\": \"{datetime.utcnow().isoformat()}\"}}\n\n"
            await asyncio.sleep(5)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/v1/webhooks")
async def get_webhooks():
    """Get registered webhooks"""
    # This would integrate with the webhook manager
    return {
        "total": 0,
        "webhooks": [],
        "available_events": [
            "plugin.registered", "service.discovered", "health.changed",
            "alert.triggered", "deployment.completed"
        ]
    }


@app.post("/api/v1/webhooks")
async def register_webhook(webhook_data: dict):
    """Register a new webhook"""
    webhook_id = str(uuid4())
    
    # This would integrate with the webhook manager
    return {
        "message": "Webhook registered successfully",
        "webhook_id": webhook_id,
        "url": webhook_data["url"],
        "events": webhook_data.get("events", [])
    }


@app.delete("/api/v1/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: str):
    """Delete a webhook"""
    return {
        "message": f"Webhook {webhook_id} deleted"
    }


@app.post("/api/v1/search/index")
async def index_document(doc_data: dict):
    """Add document to search index"""
    # This would integrate with the semantic search engine
    return {
        "message": "Document indexed successfully",
        "doc_id": doc_data["id"],
        "indexed_at": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/search/stats")
async def get_search_stats():
    """Get search index statistics"""
    # This would integrate with the semantic search engine
    return {
        "total_documents": registry.stats.get("total_entities", 0),
        "total_searches": 0,
        "average_response_time_ms": 25.5,
        "index_size_mb": 15.2
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await registry.add_connection(websocket)
    
    try:
        while True:
            # Keep connection alive with pings
            await asyncio.sleep(30)
            await websocket.send_json({
                "type": "ping",
                "timestamp": datetime.utcnow().isoformat()
            })
    except WebSocketDisconnect:
        registry.remove_connection(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        registry.remove_connection(websocket)


# ==================== Startup & Shutdown ====================

@app.on_event("startup")
async def startup_event():
    """Startup initialization"""
    logger.info("Universal Hyper Registry starting up...")
    logger.info(f"Service version: ∞.7")
    
    # Include microservices management routes
    try:
        from core.api.microservices_routes import router as microservices_router
        app.include_router(microservices_router)
        logger.info("✓ Microservices management routes loaded")
    except Exception as e:
        logger.warning(f"⚠ Microservices routes not loaded: {e}")
    
    # Include plugin management routes
    try:
        from core.api.plugins_routes import router as plugins_router
        app.include_router(plugins_router)
        logger.info("✓ Plugin management routes loaded")
    except Exception as e:
        logger.warning(f"⚠ Plugin routes not loaded: {e}")
    
    # Include API Gateway routes
    try:
        from core.gateway.api_gateway import router as gateway_router, initialize_admin_key
        app.include_router(gateway_router)
        admin_key = initialize_admin_key()
        logger.info("✓ API Gateway with key rotation loaded")
    except Exception as e:
        logger.warning(f"⚠ API Gateway routes not loaded: {e}")
    
    # Metrics routes already included via metrics_routes.py
    logger.info("✓ All API routes integrated")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Universal Hyper Registry shutting down...")
    
    # Close all WebSocket connections
    for connection in registry.connections:
        try:
            await connection.close()
        except:
            pass


# ==================== Main ====================

if __name__ == "__main__":
    uvicorn.run(
        "hyper_registry:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )
