"""
Shared Message Bus Client for OSE Services
===========================================

Lightweight client for services to publish events to the Service Mesh message bus.
This is a simplified version that doesn't require the full message_bus.py module.

Usage:
    from shared.event_bus_client import EventBusClient
    
    # Initialize
    client = EventBusClient("my-service", "http://localhost:8000")
    
    # Publish event
    await client.publish_event(
        event_type="my-service.started",
        payload={"version": "1.0.0", "status": "ready"}
    )
"""

import httpx
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class MessagePriority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventBusClient:
    """
    Lightweight message bus client for services.
    
    Uses HTTP to publish events to the Service Mesh message bus API.
    This avoids direct RabbitMQ dependencies in each service.
    """
    
    def __init__(
        self, 
        service_name: str,
        service_mesh_url: str = "http://localhost:8000",
        timeout: float = 5.0
    ):
        """
        Initialize the event bus client.
        
        Args:
            service_name: Name of the service using this client
            service_mesh_url: URL of the Service Mesh API
            timeout: HTTP request timeout in seconds
        """
        self.service_name = service_name
        self.service_mesh_url = service_mesh_url.rstrip('/')
        self.timeout = timeout
        self.publish_url = f"{self.service_mesh_url}/api/v1/messagebus/publish"
    
    async def publish_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Publish an event to the message bus.
        
        Args:
            event_type: Type of event (e.g., "service.started", "task.completed")
            payload: Event data
            priority: Message priority (LOW, NORMAL, HIGH, CRITICAL)
            correlation_id: Optional correlation ID for tracking
            metadata: Optional metadata
        
        Returns:
            True if published successfully, False otherwise
        """
        event_data = {
            "event_type": event_type,
            "source_service": self.service_name,
            "payload": payload,
            "priority": priority.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if correlation_id:
            event_data["correlation_id"] = correlation_id
        
        if metadata:
            event_data["metadata"] = metadata
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.publish_url,
                    json=event_data
                )
                return response.status_code == 200
        except Exception as e:
            # Graceful degradation - don't fail service if message bus is down
            print(f"[{self.service_name}] Failed to publish event: {e}")
            return False
    
    async def publish_lifecycle_event(
        self,
        event: str,
        version: str = "1.0.0",
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Publish a service lifecycle event.
        
        Common events: "started", "ready", "stopping", "stopped", "error"
        
        Args:
            event: Lifecycle event type (started, ready, stopping, etc.)
            version: Service version
            additional_data: Additional event data
        
        Returns:
            True if published successfully
        """
        payload = {
            "event": event,
            "version": version,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if additional_data:
            payload.update(additional_data)
        
        priority = MessagePriority.HIGH if event in ["error", "stopped"] else MessagePriority.NORMAL
        
        return await self.publish_event(
            event_type=f"{self.service_name}.{event}",
            payload=payload,
            priority=priority
        )
    
    async def publish_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Publish a metric event.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
            tags: Optional tags for grouping/filtering
        
        Returns:
            True if published successfully
        """
        payload = {
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if tags:
            payload["tags"] = tags
        
        return await self.publish_event(
            event_type=f"{self.service_name}.metric",
            payload=payload,
            priority=MessagePriority.LOW
        )
    
    async def publish_error(
        self,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Publish an error event.
        
        Args:
            error_type: Type of error
            error_message: Error message
            stack_trace: Optional stack trace
            context: Optional context data
        
        Returns:
            True if published successfully
        """
        payload = {
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if stack_trace:
            payload["stack_trace"] = stack_trace
        
        if context:
            payload["context"] = context
        
        return await self.publish_event(
            event_type=f"{self.service_name}.error",
            payload=payload,
            priority=MessagePriority.CRITICAL
        )


# Convenience functions for quick usage
async def publish_service_event(
    service_name: str,
    event_type: str,
    payload: Dict[str, Any],
    service_mesh_url: str = "http://localhost:8000"
) -> bool:
    """
    Quick helper to publish a single event without creating a client instance.
    
    Example:
        await publish_service_event(
            "discovery",
            "discovery.scan.completed",
            {"items_found": 42, "duration_ms": 1234}
        )
    """
    client = EventBusClient(service_name, service_mesh_url)
    return await client.publish_event(event_type, payload)
