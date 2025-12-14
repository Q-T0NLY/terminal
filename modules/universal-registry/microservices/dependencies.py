"""
Service Dependency Mapping and Relationship Management
Tracks dependencies between services and generates visual relationship graphs
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class DependencyType(Enum):
    """Types of service dependencies"""
    HARD = "hard"  # Service cannot function without this dependency
    SOFT = "soft"  # Service can function with degraded performance
    OPTIONAL = "optional"  # Service can function normally without this
    CIRCULAR = "circular"  # Circular dependency detected


class RelationshipType(Enum):
    """Types of service relationships"""
    SYNC_API = "sync_api"  # Synchronous API calls
    ASYNC_EVENT = "async_event"  # Event-driven communication
    MESSAGE_QUEUE = "message_queue"  # Message queue communication
    DATABASE = "database"  # Shared database
    CACHE = "cache"  # Shared cache
    FILE_SYSTEM = "file_system"  # Shared file system
    SERVICE_MESH = "service_mesh"  # Service mesh communication


@dataclass
class ServiceDependency:
    """Represents a dependency between two services"""
    source_service: str
    target_service: str
    dependency_type: DependencyType
    relationship_type: RelationshipType
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0  # Importance weight (0.0 - 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "source": self.source_service,
            "target": self.target_service,
            "dependency_type": self.dependency_type.value,
            "relationship_type": self.relationship_type.value,
            "description": self.description,
            "metadata": self.metadata,
            "weight": self.weight
        }


@dataclass
class ServiceNode:
    """Represents a service in the dependency graph"""
    service_id: str
    service_name: str
    service_type: str  # "core", "integration", "utility", etc.
    port: int
    dependencies_out: Set[str] = field(default_factory=set)  # Services this depends on
    dependencies_in: Set[str] = field(default_factory=set)  # Services that depend on this
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def dependency_count(self) -> int:
        """Total number of dependencies (in + out)"""
        return len(self.dependencies_out) + len(self.dependencies_in)
    
    def is_hub(self) -> bool:
        """Check if this is a hub (many dependencies)"""
        return self.dependency_count() > 3
    
    def is_isolated(self) -> bool:
        """Check if service has no dependencies"""
        return self.dependency_count() == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "service_type": self.service_type,
            "port": self.port,
            "dependencies_out": list(self.dependencies_out),
            "dependencies_in": list(self.dependencies_in),
            "dependency_count": self.dependency_count(),
            "is_hub": self.is_hub(),
            "is_isolated": self.is_isolated(),
            "metadata": self.metadata
        }


class DependencyGraph:
    """Manages service dependency relationships"""
    
    def __init__(self):
        self.nodes: Dict[str, ServiceNode] = {}
        self.edges: List[ServiceDependency] = []
        self.clusters: Dict[str, List[str]] = {}  # Logical groupings
    
    def add_service(
        self,
        service_id: str,
        service_name: str,
        service_type: str,
        port: int,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a service node to the graph"""
        self.nodes[service_id] = ServiceNode(
            service_id=service_id,
            service_name=service_name,
            service_type=service_type,
            port=port,
            metadata=metadata or {}
        )
    
    def add_dependency(
        self,
        source: str,
        target: str,
        dependency_type: DependencyType,
        relationship_type: RelationshipType,
        description: str = "",
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a dependency edge between services"""
        # Ensure both services exist
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Both services must be registered: {source}, {target}")
        
        # Create dependency
        dep = ServiceDependency(
            source_service=source,
            target_service=target,
            dependency_type=dependency_type,
            relationship_type=relationship_type,
            description=description,
            weight=weight,
            metadata=metadata or {}
        )
        
        self.edges.append(dep)
        
        # Update node dependencies
        self.nodes[source].dependencies_out.add(target)
        self.nodes[target].dependencies_in.add(source)
    
    def get_dependencies(self, service_id: str, direction: str = "both") -> List[str]:
        """Get dependencies for a service"""
        if service_id not in self.nodes:
            return []
        
        node = self.nodes[service_id]
        
        if direction == "out":
            return list(node.dependencies_out)
        elif direction == "in":
            return list(node.dependencies_in)
        else:  # both
            return list(node.dependencies_out | node.dependencies_in)
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the graph"""
        circular_deps = []
        visited = set()
        rec_stack = set()
        
        def dfs(node_id: str, path: List[str]) -> bool:
            """DFS to detect cycles"""
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)
            
            # Check all dependencies
            for dep in self.nodes[node_id].dependencies_out:
                if dep not in visited:
                    if dfs(dep, path.copy()):
                        return True
                elif dep in rec_stack:
                    # Circular dependency found
                    cycle_start = path.index(dep)
                    circular_deps.append(path[cycle_start:] + [dep])
                    return True
            
            rec_stack.remove(node_id)
            return False
        
        # Check all nodes
        for node_id in self.nodes:
            if node_id not in visited:
                dfs(node_id, [])
        
        return circular_deps
    
    def get_critical_path(self) -> List[str]:
        """Get the critical dependency path (longest path)"""
        # Simple implementation: DFS to find longest path
        max_path = []
        
        def dfs(node_id: str, path: List[str], visited: Set[str]):
            nonlocal max_path
            
            if len(path) > len(max_path):
                max_path = path.copy()
            
            for dep in self.nodes[node_id].dependencies_out:
                if dep not in visited:
                    visited.add(dep)
                    dfs(dep, path + [dep], visited)
                    visited.remove(dep)
        
        # Start from nodes with no incoming dependencies
        for node_id in self.nodes:
            if not self.nodes[node_id].dependencies_in:
                dfs(node_id, [node_id], {node_id})
        
        return max_path
    
    def cluster_services(self) -> Dict[str, List[str]]:
        """Group services into logical clusters"""
        clusters = {}
        
        # Cluster by service type
        for node in self.nodes.values():
            cluster_name = node.service_type
            if cluster_name not in clusters:
                clusters[cluster_name] = []
            clusters[cluster_name].append(node.service_id)
        
        self.clusters = clusters
        return clusters
    
    def get_hub_services(self, threshold: int = 3) -> List[str]:
        """Get services with many dependencies (hubs)"""
        return [
            node_id for node_id, node in self.nodes.items()
            if node.dependency_count() >= threshold
        ]
    
    def get_isolated_services(self) -> List[str]:
        """Get services with no dependencies"""
        return [
            node_id for node_id, node in self.nodes.items()
            if node.is_isolated()
        ]
    
    def to_cytoscape_json(self) -> Dict[str, Any]:
        """Export graph in Cytoscape.js format for visualization"""
        elements = []
        
        # Add nodes
        for node in self.nodes.values():
            elements.append({
                "data": {
                    "id": node.service_id,
                    "label": node.service_name,
                    "type": node.service_type,
                    "port": node.port,
                    "dependency_count": node.dependency_count(),
                    "is_hub": node.is_hub()
                },
                "group": "nodes"
            })
        
        # Add edges
        for edge in self.edges:
            elements.append({
                "data": {
                    "id": f"{edge.source_service}-{edge.target_service}",
                    "source": edge.source_service,
                    "target": edge.target_service,
                    "dependency_type": edge.dependency_type.value,
                    "relationship_type": edge.relationship_type.value,
                    "weight": edge.weight,
                    "description": edge.description
                },
                "group": "edges"
            })
        
        return {"elements": elements}
    
    def to_d3_json(self) -> Dict[str, Any]:
        """Export graph in D3.js force-directed graph format"""
        nodes = []
        links = []
        
        # Add nodes
        for node in self.nodes.values():
            nodes.append({
                "id": node.service_id,
                "name": node.service_name,
                "type": node.service_type,
                "port": node.port,
                "group": node.service_type,
                "dependency_count": node.dependency_count()
            })
        
        # Add links
        for edge in self.edges:
            links.append({
                "source": edge.source_service,
                "target": edge.target_service,
                "type": edge.relationship_type.value,
                "value": edge.weight
            })
        
        return {"nodes": nodes, "links": links}
    
    def to_mermaid(self) -> str:
        """Export graph as Mermaid diagram syntax"""
        lines = ["graph TD"]
        
        # Add nodes with styling
        for node in self.nodes.values():
            style = "rounded" if node.is_hub() else "default"
            lines.append(f"    {node.service_id}[{node.service_name}]")
        
        # Add edges
        for edge in self.edges:
            arrow = "==>" if edge.dependency_type == DependencyType.HARD else "-->"
            label = edge.relationship_type.value
            lines.append(f"    {edge.source_service} {arrow}|{label}| {edge.target_service}")
        
        return "\n".join(lines)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get graph summary statistics"""
        return {
            "total_services": len(self.nodes),
            "total_dependencies": len(self.edges),
            "hub_services": self.get_hub_services(),
            "isolated_services": self.get_isolated_services(),
            "circular_dependencies": self.detect_circular_dependencies(),
            "critical_path": self.get_critical_path(),
            "clusters": self.cluster_services(),
            "average_dependencies": round(
                sum(node.dependency_count() for node in self.nodes.values()) / len(self.nodes)
                if self.nodes else 0,
                2
            )
        }


# Global dependency graph instance
dependency_graph = DependencyGraph()


def initialize_ose_dependencies():
    """Initialize dependencies for all OSE services"""
    
    # Register all services
    services = [
        ("service-mesh", "Service Mesh", "core", 8000),
        ("discovery", "Discovery Service", "core", 8001),
        ("factory-reset", "Factory Reset Service", "utility", 8002),
        ("reinstallation", "Reinstallation Service", "utility", 8003),
        ("optimization", "Optimization Service", "core", 8004),
        ("terminal-config", "Terminal Config Service", "configuration", 8005),
        ("metrics-collector", "Metrics Collector", "monitoring", 8006),
        ("rabbitmq", "RabbitMQ", "infrastructure", 5672),
        ("redis", "Redis Cache", "infrastructure", 6379),
        ("postgres", "PostgreSQL", "infrastructure", 5432),
        ("prometheus", "Prometheus", "monitoring", 9090),
        ("grafana", "Grafana", "monitoring", 3000),
    ]
    
    for service_id, name, stype, port in services:
        dependency_graph.add_service(service_id, name, stype, port)
    
    # Define dependencies
    deps = [
        # Service Mesh dependencies (hub)
        ("service-mesh", "discovery", DependencyType.HARD, RelationshipType.SYNC_API),
        ("service-mesh", "factory-reset", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("service-mesh", "reinstallation", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("service-mesh", "optimization", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("service-mesh", "terminal-config", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("service-mesh", "metrics-collector", DependencyType.HARD, RelationshipType.SYNC_API),
        ("service-mesh", "rabbitmq", DependencyType.HARD, RelationshipType.MESSAGE_QUEUE),
        ("service-mesh", "redis", DependencyType.HARD, RelationshipType.CACHE),
        ("service-mesh", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Discovery Service dependencies
        ("discovery", "rabbitmq", DependencyType.SOFT, RelationshipType.MESSAGE_QUEUE),
        ("discovery", "redis", DependencyType.SOFT, RelationshipType.CACHE),
        ("discovery", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Factory Reset dependencies
        ("factory-reset", "discovery", DependencyType.HARD, RelationshipType.SYNC_API),
        ("factory-reset", "rabbitmq", DependencyType.SOFT, RelationshipType.MESSAGE_QUEUE),
        ("factory-reset", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Reinstallation dependencies
        ("reinstallation", "discovery", DependencyType.HARD, RelationshipType.SYNC_API),
        ("reinstallation", "rabbitmq", DependencyType.SOFT, RelationshipType.MESSAGE_QUEUE),
        ("reinstallation", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Optimization dependencies
        ("optimization", "discovery", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("optimization", "metrics-collector", DependencyType.HARD, RelationshipType.SYNC_API),
        ("optimization", "rabbitmq", DependencyType.SOFT, RelationshipType.MESSAGE_QUEUE),
        ("optimization", "redis", DependencyType.HARD, RelationshipType.CACHE),
        ("optimization", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Terminal Config dependencies
        ("terminal-config", "discovery", DependencyType.SOFT, RelationshipType.SYNC_API),
        ("terminal-config", "redis", DependencyType.SOFT, RelationshipType.CACHE),
        ("terminal-config", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Metrics Collector dependencies
        ("metrics-collector", "prometheus", DependencyType.HARD, RelationshipType.SYNC_API),
        ("metrics-collector", "rabbitmq", DependencyType.SOFT, RelationshipType.MESSAGE_QUEUE),
        ("metrics-collector", "redis", DependencyType.HARD, RelationshipType.CACHE),
        ("metrics-collector", "postgres", DependencyType.HARD, RelationshipType.DATABASE),
        
        # Monitoring dependencies
        ("grafana", "prometheus", DependencyType.HARD, RelationshipType.SYNC_API),
        ("prometheus", "metrics-collector", DependencyType.SOFT, RelationshipType.SYNC_API),
    ]
    
    for source, target, dep_type, rel_type in deps:
        dependency_graph.add_dependency(source, target, dep_type, rel_type)
    
    return dependency_graph
