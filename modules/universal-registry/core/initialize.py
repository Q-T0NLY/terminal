"""
Service Mesh Initialization Script
Initializes heartbeat monitoring, dependency graph, and message bus
"""

import asyncio
import logging
from heartbeat import heartbeat_manager
from dependencies import dependency_graph, initialize_ose_dependencies, DependencyType, RelationshipType
from message_bus import initialize_message_bus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_heartbeat_monitoring():
    """Initialize heartbeat monitoring for all services"""
    logger.info("Initializing heartbeat monitoring...")
    
    # Register all OSE services
    services = [
        ("service-mesh", "Service Mesh", 8000),
        ("discovery", "Discovery Service", 8001),
        ("factory-reset", "Factory Reset Service", 8002),
        ("reinstallation", "Reinstallation Service", 8003),
        ("optimization", "Optimization Service", 8004),
        ("terminal-config", "Terminal Config Service", 8005),
        ("metrics-collector", "Metrics Collector", 8006),
    ]
    
    for service_id, service_name, port in services:
        heartbeat_manager.register_service(
            service_id=service_id,
            service_name=service_name,
            interval_seconds=10,
            timeout_seconds=30,
            max_failures=3,
            metadata={"port": port}
        )
    
    logger.info(f"Registered {len(services)} services for heartbeat monitoring")
    
    # Start background monitoring
    asyncio.create_task(heartbeat_manager.start_monitoring())
    logger.info("Heartbeat monitoring started")


async def initialize_dependency_graph():
    """Initialize service dependency graph"""
    logger.info("Initializing dependency graph...")
    
    # Initialize OSE service dependencies
    initialize_ose_dependencies()
    
    # Get summary
    summary = dependency_graph.get_summary()
    
    logger.info(f"Dependency graph initialized:")
    logger.info(f"  - Total services: {summary['total_services']}")
    logger.info(f"  - Total dependencies: {summary['total_dependencies']}")
    logger.info(f"  - Hub services: {summary['hub_services']}")
    logger.info(f"  - Circular dependencies: {len(summary['circular_dependencies'])}")
    
    if summary['circular_dependencies']:
        logger.warning(f"Found circular dependencies: {summary['circular_dependencies']}")


async def initialize_message_bus_system():
    """Initialize RabbitMQ message bus"""
    logger.info("Initializing message bus...")
    
    try:
        # Connect to RabbitMQ
        await initialize_message_bus(host="localhost", port=5672)
        logger.info("Message bus initialized and connected")
        
    except Exception as e:
        logger.warning(f"Could not connect to message bus: {e}")
        logger.warning("Services will operate without event-driven communication")


async def initialize_all():
    """Initialize all Service Mesh components"""
    logger.info("=" * 80)
    logger.info("OSE Service Mesh - Initializing Components")
    logger.info("=" * 80)
    
    # Initialize dependency graph (synchronous)
    await initialize_dependency_graph()
    
    # Initialize heartbeat monitoring (async background task)
    await initialize_heartbeat_monitoring()
    
    # Initialize message bus (async)
    await initialize_message_bus_system()
    
    logger.info("=" * 80)
    logger.info("Service Mesh Initialization Complete")
    logger.info("=" * 80)
    logger.info("")
    logger.info("Features enabled:")
    logger.info("  ✓ Advanced Heartbeat Monitoring")
    logger.info("  ✓ Dependency Mapping & Visualization")
    logger.info("  ✓ Message/Event/Task Bus")
    logger.info("  ✓ Real-time Service Health Tracking")
    logger.info("  ✓ Circular Dependency Detection")
    logger.info("  ✓ Critical Path Analysis")
    logger.info("")


if __name__ == "__main__":
    # Run initialization
    asyncio.run(initialize_all())
