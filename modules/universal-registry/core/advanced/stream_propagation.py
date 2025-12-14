#!/usr/bin/env python3
"""
Advanced Live Stream Propagation System
Bidirectional real-time data streaming between components
Version: ∞.8
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class StreamType(str, Enum):
    """Stream types"""
    ENTITY_CREATED = "entity.created"
    ENTITY_UPDATED = "entity.updated"
    ENTITY_DELETED = "entity.deleted"
    RELATIONSHIP_CREATED = "relationship.created"
    RELATIONSHIP_DELETED = "relationship.deleted"
    PLUGIN_REGISTERED = "plugin.registered"
    PLUGIN_STATUS_CHANGED = "plugin.status_changed"
    SERVICE_DISCOVERED = "service.discovered"
    HEALTH_CHECK = "health.check"
    METRIC_COLLECTED = "metric.collected"
    ALERT_TRIGGERED = "alert.triggered"
    CONFIGURATION_CHANGED = "config.changed"
    SEARCH_PERFORMED = "search.performed"
    USER_ACTION = "user.action"


class StreamPriority(int, Enum):
    """Stream priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class StreamEvent:
    """Stream event structure"""
    id: str
    type: StreamType
    source: str
    target: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    priority: StreamPriority = StreamPriority.NORMAL
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            **asdict(self),
            "type": self.type.value if isinstance(self.type, Enum) else self.type,
            "priority": self.priority.value if isinstance(self.priority, Enum) else self.priority
        }


@dataclass
class StreamSubscription:
    """Stream subscription"""
    subscriber_id: str
    event_types: Set[StreamType]
    callback: Callable
    filters: Dict[str, Any] = field(default_factory=dict)
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    events_received: int = 0


class StreamHub:
    """Central stream hub for event propagation"""
    
    def __init__(self):
        # Subscriptions by event type
        self.subscriptions: Dict[StreamType, List[StreamSubscription]] = defaultdict(list)
        
        # Event buffer for replay/audit
        self.event_buffer: List[StreamEvent] = []
        self.max_buffer_size = 1000
        
        # Stream statistics
        self.stats = {
            "total_events": 0,
            "events_by_type": defaultdict(int),
            "events_by_priority": defaultdict(int),
            "active_subscriptions": 0,
            "failed_deliveries": 0
        }
        
        # Dead letter queue for failed events
        self.dead_letter_queue: List[StreamEvent] = []
        
    async def publish(self, event: StreamEvent) -> int:
        """Publish event to all matching subscribers"""
        self.stats["total_events"] += 1
        self.stats["events_by_type"][event.type.value] += 1
        self.stats["events_by_priority"][event.priority.value] += 1
        
        # Add to buffer
        self.event_buffer.append(event)
        if len(self.event_buffer) > self.max_buffer_size:
            self.event_buffer.pop(0)
        
        # Find matching subscriptions
        matching_subs = []
        for sub in self.subscriptions.get(event.type, []):
            if sub.active and self._matches_filters(event, sub.filters):
                matching_subs.append(sub)
        
        # Also check wildcard subscriptions
        for sub in self.subscriptions.get("*", []):
            if sub.active and self._matches_filters(event, sub.filters):
                matching_subs.append(sub)
        
        # Deliver to subscribers
        delivered = 0
        for sub in matching_subs:
            try:
                await self._deliver_event(event, sub)
                delivered += 1
                sub.events_received += 1
            except Exception as e:
                logger.error(f"Failed to deliver event to {sub.subscriber_id}: {e}")
                self.stats["failed_deliveries"] += 1
                
                # Add to dead letter queue if critical
                if event.priority == StreamPriority.CRITICAL:
                    self.dead_letter_queue.append(event)
        
        return delivered
    
    async def subscribe(self, 
                       subscriber_id: str, 
                       event_types: List[StreamType],
                       callback: Callable,
                       filters: Optional[Dict[str, Any]] = None) -> StreamSubscription:
        """Subscribe to event stream"""
        subscription = StreamSubscription(
            subscriber_id=subscriber_id,
            event_types=set(event_types),
            callback=callback,
            filters=filters or {}
        )
        
        for event_type in event_types:
            self.subscriptions[event_type].append(subscription)
        
        self.stats["active_subscriptions"] += 1
        
        logger.info(f"Subscriber {subscriber_id} subscribed to {len(event_types)} event types")
        
        return subscription
    
    async def unsubscribe(self, subscription: StreamSubscription):
        """Unsubscribe from stream"""
        subscription.active = False
        
        for event_type in subscription.event_types:
            if subscription in self.subscriptions[event_type]:
                self.subscriptions[event_type].remove(subscription)
        
        self.stats["active_subscriptions"] -= 1
        
        logger.info(f"Subscriber {subscription.subscriber_id} unsubscribed")
    
    async def replay(self, 
                    subscriber_id: str,
                    event_types: Optional[List[StreamType]] = None,
                    since: Optional[str] = None) -> List[StreamEvent]:
        """Replay events from buffer"""
        events = []
        
        for event in self.event_buffer:
            # Filter by type
            if event_types and event.type not in event_types:
                continue
            
            # Filter by timestamp
            if since and event.timestamp < since:
                continue
            
            events.append(event)
        
        return events
    
    async def _deliver_event(self, event: StreamEvent, subscription: StreamSubscription):
        """Deliver event to subscriber"""
        # Call callback
        if asyncio.iscoroutinefunction(subscription.callback):
            await subscription.callback(event)
        else:
            subscription.callback(event)
    
    def _matches_filters(self, event: StreamEvent, filters: Dict[str, Any]) -> bool:
        """Check if event matches filters"""
        if not filters:
            return True
        
        for key, value in filters.items():
            # Check in data
            if key in event.data:
                if isinstance(value, list):
                    if event.data[key] not in value:
                        return False
                elif event.data[key] != value:
                    return False
            # Check in metadata
            elif key in event.metadata:
                if isinstance(value, list):
                    if event.metadata[key] not in value:
                        return False
                elif event.metadata[key] != value:
                    return False
            else:
                return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get stream statistics"""
        return {
            **self.stats,
            "buffer_size": len(self.event_buffer),
            "dead_letter_queue_size": len(self.dead_letter_queue),
            "subscriptions_by_type": {
                k.value: len(v) for k, v in self.subscriptions.items()
            }
        }


class BiDirectionalBridge:
    """Bidirectional bridge between components"""
    
    def __init__(self, component_a: str, component_b: str):
        self.component_a = component_a
        self.component_b = component_b
        self.hub = StreamHub()
        
        # Component-specific queues
        self.queue_a: asyncio.Queue = asyncio.Queue()
        self.queue_b: asyncio.Queue = asyncio.Queue()
        
        # Active status
        self.active = True
        
        # Statistics
        self.stats = {
            "a_to_b": 0,
            "b_to_a": 0,
            "total_transferred": 0
        }
    
    async def propagate_a_to_b(self, event: StreamEvent):
        """Propagate event from A to B"""
        event.source = self.component_a
        event.target = self.component_b
        await self.queue_b.put(event)
        self.stats["a_to_b"] += 1
        self.stats["total_transferred"] += 1
    
    async def propagate_b_to_a(self, event: StreamEvent):
        """Propagate event from B to A"""
        event.source = self.component_b
        event.target = self.component_a
        await self.queue_a.put(event)
        self.stats["b_to_a"] += 1
        self.stats["total_transferred"] += 1
    
    async def start_propagation(self):
        """Start bidirectional propagation"""
        await asyncio.gather(
            self._process_queue_a(),
            self._process_queue_b()
        )
    
    async def _process_queue_a(self):
        """Process queue A"""
        while self.active:
            try:
                event = await asyncio.wait_for(self.queue_a.get(), timeout=1.0)
                await self.hub.publish(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing queue A: {e}")
    
    async def _process_queue_b(self):
        """Process queue B"""
        while self.active:
            try:
                event = await asyncio.wait_for(self.queue_b.get(), timeout=1.0)
                await self.hub.publish(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing queue B: {e}")
    
    async def stop(self):
        """Stop propagation"""
        self.active = False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bridge statistics"""
        return {
            **self.stats,
            "queue_a_size": self.queue_a.qsize(),
            "queue_b_size": self.queue_b.qsize(),
            "active": self.active
        }


class PropagationManager:
    """Manage all stream propagations"""
    
    def __init__(self):
        self.hub = StreamHub()
        self.bridges: Dict[str, BiDirectionalBridge] = {}
        
        # Component registry
        self.components: Dict[str, Dict[str, Any]] = {}
    
    async def register_component(self, component_id: str, metadata: Dict[str, Any]):
        """Register a component"""
        self.components[component_id] = {
            "id": component_id,
            "metadata": metadata,
            "registered_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        logger.info(f"Registered component: {component_id}")
    
    async def create_bridge(self, component_a: str, component_b: str) -> BiDirectionalBridge:
        """Create bidirectional bridge"""
        bridge_id = f"{component_a}<->{component_b}"
        
        if bridge_id in self.bridges:
            return self.bridges[bridge_id]
        
        bridge = BiDirectionalBridge(component_a, component_b)
        self.bridges[bridge_id] = bridge
        
        logger.info(f"Created bridge: {bridge_id}")
        
        return bridge
    
    async def propagate(self, source: str, target: str, event: StreamEvent):
        """Propagate event between components"""
        bridge_id = f"{source}<->{target}"
        
        if bridge_id not in self.bridges:
            # Try reverse
            bridge_id = f"{target}<->{source}"
        
        if bridge_id in self.bridges:
            bridge = self.bridges[bridge_id]
            
            if source == bridge.component_a:
                await bridge.propagate_a_to_b(event)
            else:
                await bridge.propagate_b_to_a(event)
        else:
            # Create new bridge
            bridge = await self.create_bridge(source, target)
            await bridge.propagate_a_to_b(event)
    
    async def broadcast(self, event: StreamEvent):
        """Broadcast event to all components"""
        await self.hub.publish(event)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get propagation statistics"""
        return {
            "hub_stats": self.hub.get_stats(),
            "active_bridges": len(self.bridges),
            "active_components": len([c for c in self.components.values() if c["active"]]),
            "bridge_stats": {
                bridge_id: bridge.get_stats()
                for bridge_id, bridge in self.bridges.items()
            }
        }


# Global propagation manager
propagation_manager = PropagationManager()


# Convenience functions
async def setup_registry_dashboard_bridge():
    """Setup bidirectional bridge between registry and dashboard"""
    await propagation_manager.register_component("universal-registry", {"type": "registry"})
    await propagation_manager.register_component("main-dashboard", {"type": "dashboard"})
    
    bridge = await propagation_manager.create_bridge("universal-registry", "main-dashboard")
    
    # Start propagation
    asyncio.create_task(bridge.start_propagation())
    
    return bridge


async def setup_registry_metrics_bridge():
    """Setup bidirectional bridge between registry and metrics collector"""
    await propagation_manager.register_component("universal-registry", {"type": "registry"})
    await propagation_manager.register_component("metrics-collector", {"type": "metrics"})
    
    bridge = await propagation_manager.create_bridge("universal-registry", "metrics-collector")
    
    # Start propagation
    asyncio.create_task(bridge.start_propagation())
    
    return bridge
