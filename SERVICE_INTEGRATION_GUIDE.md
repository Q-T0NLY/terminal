# Service Integration Guide

This guide shows how to integrate the **Event Bus** and **Heartbeat Monitoring** into any OSE service.

## Quick Start

### 1. Install Dependencies

Add to your service's `requirements.txt`:
```txt
httpx==0.27.0
```

### 2. Import Event Bus Client

```python
import sys
from pathlib import Path

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.event_bus_client import EventBusClient, MessagePriority
```

### 3. Initialize Client

```python
from fastapi import FastAPI

app = FastAPI(title="My Service")

# Create event bus client
event_bus = EventBusClient("my-service", "http://localhost:8000")
```

### 4. Add Lifecycle Events

```python
@app.on_event("startup")
async def startup_event():
    """Publish service startup event"""
    await event_bus.publish_lifecycle_event(
        event="started",
        version="1.0.0",
        additional_data={
            "port": 8001,
            "endpoints": 25,
            "features": ["feature1", "feature2"]
        }
    )
    print("✅ Service started - event published")

@app.on_event("shutdown")
async def shutdown_event():
    """Publish service shutdown event"""
    await event_bus.publish_lifecycle_event(
        event="stopped",
        version="1.0.0"
    )
    print("🛑 Service stopped - event published")
```

### 5. Ensure Health Endpoint Exists

```python
@app.get("/health")
async def health_check():
    """Health check endpoint for heartbeat monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "my-service",
        "version": "1.0.0"
    }
```

### 6. Publish Events from Endpoints

```python
@app.post("/api/v1/process")
async def process_data(data: dict):
    """Process data and publish completion event"""
    
    # Do processing...
    result = do_processing(data)
    
    # Publish event
    await event_bus.publish_event(
        event_type="my-service.process.completed",
        payload={
            "items_processed": len(result),
            "duration_ms": 1234,
            "status": "success"
        },
        priority=MessagePriority.NORMAL
    )
    
    return {"status": "success", "result": result}
```

## Complete Integration Example

Here's a complete example integrating all features:

```python
"""
My OSE Service with full event bus integration
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys
from pathlib import Path

# Import event bus client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.event_bus_client import EventBusClient, MessagePriority

app = FastAPI(
    title="My Service",
    description="Example OSE service with event bus",
    version="1.0.0"
)

# Initialize Event Bus
event_bus = EventBusClient("my-service", "http://localhost:8000")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Lifecycle Events ====================

@app.on_event("startup")
async def startup_event():
    """Service startup"""
    await event_bus.publish_lifecycle_event(
        event="started",
        version="1.0.0",
        additional_data={
            "port": 8001,
            "endpoints": 10,
            "features": ["processing", "analysis"]
        }
    )
    print("✅ My Service started")

@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown"""
    await event_bus.publish_lifecycle_event(
        event="stopped",
        version="1.0.0"
    )
    print("🛑 My Service stopped")

# ==================== Endpoints ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "my-service",
        "version": "1.0.0"
    }

@app.post("/api/v1/process")
async def process_data(data: dict):
    """Process data with event publishing"""
    start_time = datetime.now()
    
    # Publish start event
    await event_bus.publish_event(
        event_type="my-service.process.started",
        payload={"data_size": len(data)},
        priority=MessagePriority.NORMAL
    )
    
    try:
        # Do actual processing
        result = {"processed": True, "items": 42}
        
        # Publish success event
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        await event_bus.publish_event(
            event_type="my-service.process.completed",
            payload={
                "status": "success",
                "items_processed": 42,
                "duration_ms": duration_ms
            },
            priority=MessagePriority.NORMAL
        )
        
        return {"status": "success", "result": result}
        
    except Exception as e:
        # Publish error event
        await event_bus.publish_error(
            error_type="ProcessingError",
            error_message=str(e),
            context={"data_size": len(data)}
        )
        raise

@app.post("/api/v1/metrics")
async def report_metrics():
    """Report custom metrics"""
    await event_bus.publish_metric(
        metric_name="requests_processed",
        value=42.0,
        unit="count",
        tags={"endpoint": "process", "status": "success"}
    )
    
    return {"status": "metric_published"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Event Types

### Lifecycle Events

Use `publish_lifecycle_event()` for standard lifecycle:

- `started` - Service has started
- `ready` - Service is ready to accept requests
- `stopping` - Service is shutting down
- `stopped` - Service has stopped
- `error` - Critical service error

```python
await event_bus.publish_lifecycle_event(
    event="started",
    version="1.0.0",
    additional_data={"port": 8001}
)
```

### Custom Events

Use `publish_event()` for custom business events:

```python
await event_bus.publish_event(
    event_type="my-service.task.completed",
    payload={
        "task_id": "task_123",
        "result": "success",
        "duration_ms": 1234
    },
    priority=MessagePriority.HIGH
)
```

### Error Events

Use `publish_error()` for errors:

```python
await event_bus.publish_error(
    error_type="DatabaseError",
    error_message="Connection failed",
    stack_trace=traceback.format_exc(),
    context={"database": "postgres", "retry_count": 3}
)
```

### Metric Events

Use `publish_metric()` for metrics:

```python
await event_bus.publish_metric(
    metric_name="response_time",
    value=125.5,
    unit="ms",
    tags={"endpoint": "/api/v1/process", "status": "success"}
)
```

## Message Priorities

Choose appropriate priority for each event:

- **LOW**: Metrics, logs, non-critical updates
- **NORMAL**: Standard business events, task completions
- **HIGH**: Important state changes, lifecycle events
- **CRITICAL**: Errors, failures, alerts

```python
from shared.event_bus_client import MessagePriority

await event_bus.publish_event(
    event_type="critical.alert",
    payload={"alert": "disk_full"},
    priority=MessagePriority.CRITICAL
)
```

## Event Naming Convention

Follow this pattern: `<service>.<domain>.<action>`

Examples:
- `discovery.scan.started`
- `discovery.scan.completed`
- `discovery.error`
- `optimization.analysis.completed`
- `factory-reset.cleanup.started`

## Testing Event Publishing

### Manual Testing

```bash
# Check message bus status
curl http://localhost:8000/api/v1/messagebus/status

# Start your service (events will be published)
python main.py

# Check service mesh logs to see events
curl http://localhost:8000/api/v1/heartbeat/status
```

### TUI Testing

```bash
# Launch TUI
python3 cli/ose_tui.py

# Navigate to Service Mesh
Press: 1

# View message bus
Press: bus

# Publish test event
Press: p
```

## Graceful Degradation

The event bus client is designed to **never fail your service**:

- If Service Mesh is down, events are silently dropped
- HTTP timeouts are configured (default: 5s)
- All publish methods return `bool` (True/False)
- Exceptions are caught and logged

```python
# Event publishing won't crash your service
success = await event_bus.publish_event(...)
if not success:
    # Service Mesh might be down - continue anyway
    print("Warning: Failed to publish event")
```

## Integration Checklist

For each service, complete these steps:

- [ ] Add `httpx` to requirements.txt
- [ ] Import `EventBusClient` from shared module
- [ ] Create event bus client instance
- [ ] Add `@app.on_event("startup")` handler
- [ ] Add `@app.on_event("shutdown")` handler
- [ ] Ensure `/health` endpoint exists
- [ ] Add event publishing to key endpoints
- [ ] Test with Service Mesh running
- [ ] Test graceful degradation (Service Mesh offline)

## Services Integration Status

### ✅ Completed
- **discovery** - Full integration with scan events

### 🚧 Pending
- **optimization** - Add analysis completion events
- **factory-reset** - Add cleanup events  
- **reinstallation** - Add package installation events
- **terminal-config** - Add configuration change events
- **metrics-collector** - Add metrics collection events

## Monitoring Events

Once integrated, you can monitor all events:

### Web Dashboard
```
http://localhost:8000/heartbeat-dashboard
```

### Terminal UI
```bash
python3 cli/ose_tui.py
# Press: 1 → bus
```

### RabbitMQ Admin
```
http://localhost:15672
# Login: guest/guest
```

---

**For questions or issues, see [ADVANCED_FEATURES.md](modules/service-mesh/ADVANCED_FEATURES.md)**
