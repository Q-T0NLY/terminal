"""
RabbitMQ Message/Event/Task Bus Interface
Provides unified interface for event-driven communication between services
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import aio_pika
from aio_pika import Message, ExchangeType, DeliveryMode
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue, AbstractExchange


logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


class ExchangeTypes(Enum):
    """RabbitMQ exchange types"""
    DIRECT = "direct"
    TOPIC = "topic"
    FANOUT = "fanout"
    HEADERS = "headers"


@dataclass
class EventMessage:
    """Standard event message structure"""
    event_type: str
    source_service: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    priority: MessagePriority = MessagePriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            "event_type": self.event_type,
            "source_service": self.source_service,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp,
            "priority": self.priority.value,
            "metadata": self.metadata
        })
    
    @classmethod
    def from_json(cls, data: str) -> 'EventMessage':
        """Create from JSON string"""
        obj = json.loads(data)
        return cls(
            event_type=obj["event_type"],
            source_service=obj["source_service"],
            payload=obj["payload"],
            correlation_id=obj.get("correlation_id"),
            timestamp=obj.get("timestamp", datetime.utcnow().isoformat()),
            priority=MessagePriority(obj.get("priority", 5)),
            metadata=obj.get("metadata", {})
        )


class MessageBus:
    """RabbitMQ message bus interface"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        virtual_host: str = "/"
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[AbstractChannel] = None
        self.exchanges: Dict[str, AbstractExchange] = {}
        self.queues: Dict[str, AbstractQueue] = {}
        self.consumers: Dict[str, asyncio.Task] = {}
        
        self.is_connected = False
    
    async def connect(self):
        """Connect to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.username,
                password=self.password,
                virtualhost=self.virtual_host
            )
            
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)
            
            self.is_connected = True
            logger.info(f"Connected to RabbitMQ at {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.is_connected = False
            raise
    
    async def disconnect(self):
        """Disconnect from RabbitMQ"""
        # Cancel all consumers
        for task in self.consumers.values():
            task.cancel()
        
        if self.connection:
            await self.connection.close()
        
        self.is_connected = False
        logger.info("Disconnected from RabbitMQ")
    
    async def declare_exchange(
        self,
        name: str,
        exchange_type: ExchangeTypes = ExchangeTypes.TOPIC,
        durable: bool = True
    ) -> AbstractExchange:
        """Declare an exchange"""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        if name in self.exchanges:
            return self.exchanges[name]
        
        exchange = await self.channel.declare_exchange(
            name=name,
            type=ExchangeType[exchange_type.name],
            durable=durable
        )
        
        self.exchanges[name] = exchange
        logger.info(f"Declared exchange: {name} (type: {exchange_type.value})")
        
        return exchange
    
    async def declare_queue(
        self,
        name: str,
        durable: bool = True,
        auto_delete: bool = False,
        arguments: Optional[Dict[str, Any]] = None
    ) -> AbstractQueue:
        """Declare a queue"""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        if name in self.queues:
            return self.queues[name]
        
        queue = await self.channel.declare_queue(
            name=name,
            durable=durable,
            auto_delete=auto_delete,
            arguments=arguments or {}
        )
        
        self.queues[name] = queue
        logger.info(f"Declared queue: {name}")
        
        return queue
    
    async def bind_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str = "#"
    ):
        """Bind a queue to an exchange"""
        if queue_name not in self.queues:
            raise ValueError(f"Queue not declared: {queue_name}")
        
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange not declared: {exchange_name}")
        
        queue = self.queues[queue_name]
        exchange = self.exchanges[exchange_name]
        
        await queue.bind(exchange, routing_key=routing_key)
        logger.info(f"Bound queue {queue_name} to exchange {exchange_name} with routing key {routing_key}")
    
    async def publish_event(
        self,
        exchange_name: str,
        event: EventMessage,
        routing_key: str = ""
    ):
        """Publish an event to an exchange"""
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange not declared: {exchange_name}")
        
        exchange = self.exchanges[exchange_name]
        
        message = Message(
            body=event.to_json().encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            priority=event.priority.value,
            content_type="application/json",
            correlation_id=event.correlation_id,
            timestamp=datetime.utcnow()
        )
        
        await exchange.publish(message, routing_key=routing_key)
        logger.info(f"Published event {event.event_type} to {exchange_name}")
    
    async def consume(
        self,
        queue_name: str,
        callback: Callable[[EventMessage], Any],
        auto_ack: bool = False
    ):
        """Consume messages from a queue"""
        if queue_name not in self.queues:
            raise ValueError(f"Queue not declared: {queue_name}")
        
        queue = self.queues[queue_name]
        
        async def process_message(message: aio_pika.IncomingMessage):
            """Process incoming message"""
            async with message.process(ignore_processed=auto_ack):
                try:
                    # Parse event
                    event = EventMessage.from_json(message.body.decode())
                    
                    # Call callback
                    result = callback(event)
                    if asyncio.iscoroutine(result):
                        await result
                    
                    logger.debug(f"Processed event {event.event_type} from queue {queue_name}")
                    
                except Exception as e:
                    logger.error(f"Error processing message from {queue_name}: {e}")
                    # Message will be requeued if not auto_ack
        
        # Start consuming
        consumer_tag = await queue.consume(process_message)
        logger.info(f"Started consuming from queue: {queue_name}")
        
        return consumer_tag
    
    async def rpc_call(
        self,
        exchange_name: str,
        event: EventMessage,
        routing_key: str,
        timeout: int = 30
    ) -> Optional[EventMessage]:
        """Make an RPC call and wait for response"""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        # Create callback queue
        callback_queue = await self.channel.declare_queue(exclusive=True)
        
        # Create correlation ID
        import uuid
        correlation_id = event.correlation_id or str(uuid.uuid4())
        event.correlation_id = correlation_id
        
        # Response storage
        response_future = asyncio.Future()
        
        async def on_response(message: aio_pika.IncomingMessage):
            """Handle RPC response"""
            if message.correlation_id == correlation_id:
                async with message.process():
                    response = EventMessage.from_json(message.body.decode())
                    response_future.set_result(response)
        
        # Start consuming responses
        await callback_queue.consume(on_response)
        
        # Publish request
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange not declared: {exchange_name}")
        
        exchange = self.exchanges[exchange_name]
        
        message = Message(
            body=event.to_json().encode(),
            correlation_id=correlation_id,
            reply_to=callback_queue.name,
            delivery_mode=DeliveryMode.PERSISTENT
        )
        
        await exchange.publish(message, routing_key=routing_key)
        
        # Wait for response
        try:
            response = await asyncio.wait_for(response_future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.error(f"RPC call timed out after {timeout}s")
            return None
        finally:
            await callback_queue.delete()


class ServiceEventBus:
    """High-level service event bus interface"""
    
    def __init__(self, service_name: str, message_bus: MessageBus):
        self.service_name = service_name
        self.bus = message_bus
        self.event_handlers: Dict[str, List[Callable]] = {}
    
    async def initialize(self):
        """Initialize event bus for this service"""
        # Declare main OSE exchange
        await self.bus.declare_exchange("ose.events", ExchangeTypes.TOPIC)
        
        # Declare service-specific queue
        queue_name = f"ose.{self.service_name}.events"
        await self.bus.declare_queue(queue_name, durable=True)
        
        # Bind to receive all events for this service
        await self.bus.bind_queue(
            queue_name,
            "ose.events",
            routing_key=f"{self.service_name}.#"
        )
        
        # Start consuming
        await self.bus.consume(queue_name, self._handle_event)
    
    async def _handle_event(self, event: EventMessage):
        """Internal event handler"""
        event_type = event.event_type
        
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    result = handler(event)
                    if asyncio.iscoroutine(result):
                        await result
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type}: {e}")
    
    def on_event(self, event_type: str):
        """Decorator to register event handlers"""
        def decorator(func: Callable):
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
            self.event_handlers[event_type].append(func)
            return func
        return decorator
    
    async def emit(
        self,
        event_type: str,
        payload: Dict[str, Any],
        routing_key: Optional[str] = None,
        priority: MessagePriority = MessagePriority.NORMAL
    ):
        """Emit an event"""
        event = EventMessage(
            event_type=event_type,
            source_service=self.service_name,
            payload=payload,
            priority=priority
        )
        
        # Default routing key is service_name.event_type
        if not routing_key:
            routing_key = f"{self.service_name}.{event_type}"
        
        await self.bus.publish_event("ose.events", event, routing_key)
    
    async def broadcast(
        self,
        event_type: str,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ):
        """Broadcast event to all services"""
        await self.emit(event_type, payload, routing_key="broadcast", priority=priority)


# Global message bus instance
message_bus = MessageBus()


async def initialize_message_bus(host: str = "localhost", port: int = 5672):
    """Initialize global message bus"""
    await message_bus.connect()
    
    # Declare standard exchanges
    await message_bus.declare_exchange("ose.events", ExchangeTypes.TOPIC)
    await message_bus.declare_exchange("ose.tasks", ExchangeTypes.DIRECT)
    await message_bus.declare_exchange("ose.logs", ExchangeTypes.FANOUT)
    
    logger.info("Message bus initialized")
    
    return message_bus
