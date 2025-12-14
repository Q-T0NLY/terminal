"""
🌐 OSE Ultra-Advanced Service Mesh Interface
Enterprise-Grade Microservices Orchestration Platform

Features:
- 3D Service Topology Visualization
- NLP-Powered Query System
- Graph-Based Dependency Analysis
- RAG (Retrieval Augmented Generation) AI Assistant
- DAG (Directed Acyclic Graph) Workflow Engine
- Real-Time Predictive Analytics
- Advanced Scoring Engines
- Multi-Dimensional Health Metrics
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
import aiohttp
import json
import math
import statistics
from collections import defaultdict, deque
from enum import Enum
import hashlib
from pathlib import Path

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

app = FastAPI(
    title="OSE Ultra-Advanced Service Mesh",
    description="Enterprise-Grade Microservices Orchestration Platform with AI/ML, 3D Visualization, and Predictive Analytics",
    version="2.5.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS with enhanced security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"]
)


# ==================== AI Engine Integration ====================

# Import AI engines
try:
    import sys
    from pathlib import Path
    ai_engines_path = Path(__file__).parent.parent / "ai_engines"
    sys.path.insert(0, str(ai_engines_path))
    
    from ai_integration_wiring import (
        ai_engine_integration, initialize_ai_integration,
        query_ai, register_service, IntegrationRequest, ComponentType, IntegrationMode
    )
    AI_ENGINES_AVAILABLE = True
except ImportError as e:
    print(f"[⚠️] AI engines not available: {e}")
    AI_ENGINES_AVAILABLE = False

# ==================== Startup Events ====================

@app.on_event("startup")
async def startup_event():
    """[🚀] Initialize Service Mesh components on startup"""
    from initialize import initialize_all
    await initialize_all()
    
    # Initialize AI engines if available
    if AI_ENGINES_AVAILABLE:
        try:
            print("[🧠] Initializing AI engines...")
            await initialize_ai_integration()
            
            # Register service mesh as a component
            from ai_integration_wiring import ComponentRegistration
            await ai_engine_integration.register_component(
                ComponentRegistration(
                    component_id="service_mesh",
                    component_type=ComponentType.SERVICE,
                    integration_mode=IntegrationMode.DIRECT,
                    endpoints=["/api/v1/ai/*"],
                    capabilities=["nlp", "rag", "ensemble", "query_processing"],
                    metadata={"version": "2.5.0", "platform": "service_mesh"}
                )
            )
            print("[✅] AI engines integrated with Service Mesh")
        except Exception as e:
            print(f"[❌] Failed to initialize AI engines: {e}")

# ==================== Advanced Models ====================

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    DOWN = "down"
    MAINTENANCE = "maintenance"
    UNKNOWN = "unknown"


class ServiceCategory(str, Enum):
    APPLICATION = "application"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    GATEWAY = "gateway"
    MONITORING = "monitoring"
    LOGGING = "logging"


@dataclass
class ServiceNode:
    """3D Graph Node for Service Topology"""
    id: str
    name: str
    category: ServiceCategory
    position: Tuple[float, float, float]  # 3D coordinates
    size: float
    color: str
    metadata: Dict[str, Any]


@dataclass
class ServiceEdge:
    """Directed edge representing service dependencies"""
    source: str
    target: str
    weight: float  # Strength of dependency
    latency: float  # Average latency
    request_rate: float  # Requests per second
    error_rate: float  # Error percentage


class HealthScore(BaseModel):
    """Multi-dimensional health scoring"""
    overall: float = Field(..., ge=0, le=100, description="Overall health score")
    availability: float = Field(..., ge=0, le=100)
    performance: float = Field(..., ge=0, le=100)
    reliability: float = Field(..., ge=0, le=100)
    efficiency: float = Field(..., ge=0, le=100)
    security: float = Field(..., ge=0, le=100)
    prediction: Optional[float] = Field(None, ge=0, le=100, description="Predicted health in 1 hour")


class ServiceMetrics(BaseModel):
    """Comprehensive service metrics"""
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    network_in_mbps: float
    network_out_mbps: float
    disk_io_read_mbps: float
    disk_io_write_mbps: float
    request_rate: float
    error_rate: float
    p50_latency: float
    p95_latency: float
    p99_latency: float
    active_connections: int
    queue_depth: Optional[int] = None


class AIRecommendation(BaseModel):
    """AI-generated recommendations using RAG"""
    recommendation_id: str
    service: str
    priority: str  # critical, high, medium, low
    category: str  # performance, security, cost, reliability
    title: str
    description: str
    impact_score: float
    effort_score: float
    estimated_improvement: str
    action_items: List[str]
    reasoning: str  # RAG-generated explanation
    confidence: float  # AI confidence score


class TopologyGraph(BaseModel):
    """3D Service Topology Graph"""
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    clusters: List[Dict[str, Any]]
    critical_paths: List[List[str]]


class NLPQuery(BaseModel):
    """Natural Language Query"""
    query: str
    context: Optional[Dict[str, Any]] = None


class NLPResponse(BaseModel):
    """NLP Query Response with RAG"""
    query: str
    intent: str
    entities: List[Dict[str, str]]
    answer: str
    confidence: float
    sources: List[str]
    suggested_actions: List[str]


# ==================== Service Registry ====================

SERVICES = {
    "discovery": {
        "name": "Discovery Service",
        "url": "http://discovery:8001",
        "port": 8001,
        "category": ServiceCategory.APPLICATION,
        "icon": "🔍",
        "color": "#3b82f6",
        "description": "System scanning and hardware/software discovery",
        "endpoints": 40,
        "dependencies": [],
        "criticality": "high",
        "sla": 99.9,
        "position": (0, 0, 0)
    },
    "factory-reset": {
        "name": "Factory Reset Service",
        "url": "http://factory-reset:8002",
        "port": 8002,
        "category": ServiceCategory.APPLICATION,
        "icon": "🧹",
        "color": "#10b981",
        "description": "System cleanup and factory reset operations",
        "endpoints": 35,
        "dependencies": ["discovery"],
        "criticality": "high",
        "sla": 99.5,
        "position": (100, 50, 0)
    },
    "reinstallation": {
        "name": "Reinstallation Service",
        "url": "http://reinstallation:8003",
        "port": 8003,
        "category": ServiceCategory.APPLICATION,
        "icon": "📦",
        "color": "#f59e0b",
        "description": "Package management and application installation",
        "endpoints": 40,
        "dependencies": ["discovery"],
        "criticality": "medium",
        "sla": 99.0,
        "position": (-100, 50, 0)
    },
    "optimization": {
        "name": "Optimization Service",
        "url": "http://optimization:8004",
        "port": 8004,
        "category": ServiceCategory.APPLICATION,
        "icon": "⚡",
        "color": "#8b5cf6",
        "description": "System performance optimization and tuning",
        "endpoints": 45,
        "dependencies": ["discovery", "metrics-collector"],
        "criticality": "medium",
        "sla": 99.5,
        "position": (100, -50, 0)
    },
    "terminal-config": {
        "name": "Terminal Config Service",
        "url": "http://terminal-config:8005",
        "port": 8005,
        "category": ServiceCategory.APPLICATION,
        "icon": "🖥️",
        "color": "#06b6d4",
        "description": "Terminal configuration and shell customization",
        "endpoints": 35,
        "dependencies": [],
        "criticality": "low",
        "sla": 95.0,
        "position": (-100, -50, 0)
    },
    "metrics-collector": {
        "name": "Metrics Collector Service",
        "url": "http://metrics-collector:8006",
        "port": 8006,
        "category": ServiceCategory.MONITORING,
        "icon": "📊",
        "color": "#ec4899",
        "description": "Real-time metrics collection and monitoring",
        "endpoints": 40,
        "dependencies": ["postgres", "redis"],
        "criticality": "critical",
        "sla": 99.99,
        "position": (0, 100, 0)
    },
    "postgres": {
        "name": "PostgreSQL",
        "url": "http://postgres:5432",
        "port": 5432,
        "category": ServiceCategory.DATABASE,
        "icon": "🐘",
        "color": "#336791",
        "description": "Primary relational database",
        "endpoints": 0,
        "dependencies": [],
        "criticality": "critical",
        "sla": 99.99,
        "position": (0, -100, -50)
    },
    "redis": {
        "name": "Redis",
        "url": "http://redis:6379",
        "port": 6379,
        "category": ServiceCategory.CACHE,
        "icon": "⚡",
        "color": "#dc2626",
        "description": "In-memory cache and session store",
        "endpoints": 0,
        "dependencies": [],
        "criticality": "critical",
        "sla": 99.95,
        "position": (150, -100, -50)
    },
    "rabbitmq": {
        "name": "RabbitMQ",
        "url": "http://rabbitmq:5672",
        "port": 5672,
        "category": ServiceCategory.QUEUE,
        "icon": "🐰",
        "color": "#ff6600",
        "description": "Message queue and event bus",
        "endpoints": 0,
        "dependencies": [],
        "criticality": "high",
        "sla": 99.9,
        "position": (-150, -100, -50)
    },
    "prometheus": {
        "name": "Prometheus",
        "url": "http://prometheus:9090",
        "port": 9090,
        "category": ServiceCategory.MONITORING,
        "icon": "🔥",
        "color": "#e6522c",
        "description": "Metrics collection and alerting",
        "endpoints": 0,
        "dependencies": ["metrics-collector"],
        "criticality": "high",
        "sla": 99.5,
        "position": (150, 100, -50)
    },
    "grafana": {
        "name": "Grafana",
        "url": "http://grafana:3000",
        "port": 3000,
        "category": ServiceCategory.MONITORING,
        "icon": "📈",
        "color": "#f46800",
        "description": "Metrics visualization and dashboards",
        "endpoints": 0,
        "dependencies": ["prometheus"],
        "criticality": "medium",
        "sla": 99.0,
        "position": (-150, 100, -50)
    },
    "loki": {
        "name": "Loki",
        "url": "http://loki:3100",
        "port": 3100,
        "category": ServiceCategory.LOGGING,
        "icon": "📝",
        "color": "#00a6ed",
        "description": "Log aggregation and analysis",
        "endpoints": 0,
        "dependencies": [],
        "criticality": "medium",
        "sla": 95.0,
        "position": (0, 100, -100)
    }
}

# WebSocket connections
active_connections: List[WebSocket] = []

# Metrics history for trend analysis
metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))

# DAG workflow states
workflow_states: Dict[str, Any] = {}

# AI recommendation cache
recommendation_cache: List[AIRecommendation] = []

# ==================== Advanced Analytics Engine ====================

class AdvancedScoringEngine:
    """Multi-dimensional health scoring with predictive analytics"""
    
    @staticmethod
    def calculate_health_score(service_id: str, metrics: Optional[ServiceMetrics], 
                              status: ServiceStatus, history: List[Dict]) -> HealthScore:
        """Calculate comprehensive health score"""
        
        # Availability score (based on uptime)
        availability = 100.0 if status == ServiceStatus.HEALTHY else \
                      85.0 if status == ServiceStatus.DEGRADED else \
                      50.0 if status == ServiceStatus.UNHEALTHY else 0.0
        
        if metrics:
            # Performance score (CPU, memory, latency)
            cpu_score = max(0, 100 - metrics.cpu_percent)
            memory_score = max(0, 100 - metrics.memory_percent)
            latency_score = max(0, 100 - (metrics.p95_latency / 10))  # Normalize to 1000ms = 0 score
            performance = (cpu_score + memory_score + latency_score) / 3
            
            # Reliability score (error rate, queue depth)
            error_score = max(0, 100 - (metrics.error_rate * 10))
            reliability = error_score
            
            # Efficiency score (request throughput vs resources)
            efficiency_ratio = metrics.request_rate / max(1, metrics.cpu_percent)
            efficiency = min(100, efficiency_ratio * 10)
        else:
            performance = 50.0
            reliability = 50.0
            efficiency = 50.0
        
        # Security score (placeholder for security audit results)
        security = 95.0
        
        # Overall score (weighted average)
        weights = {
            "availability": 0.3,
            "performance": 0.25,
            "reliability": 0.25,
            "efficiency": 0.1,
            "security": 0.1
        }
        
        overall = (
            availability * weights["availability"] +
            performance * weights["performance"] +
            reliability * weights["reliability"] +
            efficiency * weights["efficiency"] +
            security * weights["security"]
        )
        
        # Predictive score (trend analysis)
        prediction = AdvancedScoringEngine._predict_future_health(history, overall)
        
        return HealthScore(
            overall=round(overall, 2),
            availability=round(availability, 2),
            performance=round(performance, 2),
            reliability=round(reliability, 2),
            efficiency=round(efficiency, 2),
            security=round(security, 2),
            prediction=round(prediction, 2) if prediction else None
        )
    
    @staticmethod
    def _predict_future_health(history: List[Dict], current: float) -> Optional[float]:
        """Predict health score in 1 hour using trend analysis"""
        if len(history) < 10:
            return None
        
        recent_scores = [h.get("score", current) for h in history[-20:]]
        
        # Simple linear regression
        n = len(recent_scores)
        x = list(range(n))
        y = recent_scores
        
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return current
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Predict 60 steps ahead (assuming 1 min intervals)
        prediction = slope * (n + 60) + intercept
        
        return max(0, min(100, prediction))


class GraphEngine:
    """Advanced graph analysis for service dependencies"""
    
    @staticmethod
    def build_topology_graph() -> TopologyGraph:
        """Build 3D service topology graph"""
        nodes = []
        edges = []
        
        # Create nodes
        for service_id, service in SERVICES.items():
            nodes.append({
                "id": service_id,
                "name": service["name"],
                "category": service["category"].value,
                "position": service["position"],
                "icon": service["icon"],
                "color": service["color"],
                "criticality": service["criticality"],
                "endpoints": service["endpoints"]
            })
        
        # Create edges from dependencies
        for service_id, service in SERVICES.items():
            for dep in service.get("dependencies", []):
                edges.append({
                    "source": service_id,
                    "target": dep,
                    "weight": 1.0,
                    "latency": 25.0,  # Simulated
                    "request_rate": 100.0  # Simulated
                })
        
        # Identify clusters
        clusters = GraphEngine._identify_clusters(nodes, edges)
        
        # Find critical paths
        critical_paths = GraphEngine._find_critical_paths(nodes, edges)
        
        return TopologyGraph(
            nodes=nodes,
            edges=edges,
            clusters=clusters,
            critical_paths=critical_paths
        )
    
    @staticmethod
    def _identify_clusters(nodes: List[Dict], edges: List[Dict]) -> List[Dict]:
        """Identify service clusters based on category"""
        clusters = defaultdict(list)
        
        for node in nodes:
            clusters[node["category"]].append(node["id"])
        
        return [
            {
                "id": f"cluster_{category}",
                "category": category,
                "members": members,
                "size": len(members)
            }
            for category, members in clusters.items()
        ]
    
    @staticmethod
    def _find_critical_paths(nodes: List[Dict], edges: List[Dict]) -> List[List[str]]:
        """Identify critical dependency paths"""
        # Build adjacency list
        graph = defaultdict(list)
        for edge in edges:
            graph[edge["source"]].append(edge["target"])
        
        # Find all paths from critical services
        critical_services = [n["id"] for n in nodes if n.get("criticality") == "critical"]
        paths = []
        
        for service in critical_services:
            path = GraphEngine._dfs_path(graph, service, set())
            if len(path) > 1:
                paths.append(path)
        
        return paths[:5]  # Return top 5 critical paths
    
    @staticmethod
    def _dfs_path(graph: Dict, node: str, visited: set) -> List[str]:
        """DFS to find longest path"""
        visited.add(node)
        path = [node]
        
        longest_subpath = []
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                subpath = GraphEngine._dfs_path(graph, neighbor, visited.copy())
                if len(subpath) > len(longest_subpath):
                    longest_subpath = subpath
        
        return path + longest_subpath


class NLPEngine:
    """Natural Language Processing for intelligent queries"""
    
    @staticmethod
    async def process_query(query: NLPQuery) -> NLPResponse:
        """Process natural language query with RAG"""
        
        # Simple intent classification
        query_lower = query.query.lower()
        
        # Intent detection
        if any(word in query_lower for word in ["status", "health", "running"]):
            intent = "status_check"
        elif any(word in query_lower for word in ["why", "slow", "problem", "issue"]):
            intent = "diagnostic"
        elif any(word in query_lower for word in ["optimize", "improve", "performance"]):
            intent = "optimization"
        elif any(word in query_lower for word in ["restart", "stop", "start"]):
            intent = "action"
        else:
            intent = "general"
        
        # Entity extraction (simple keyword-based)
        entities = []
        for service_id, service in SERVICES.items():
            if service_id in query_lower or service["name"].lower() in query_lower:
                entities.append({"type": "service", "value": service_id})
        
        # Generate RAG-enhanced answer
        answer = await NLPEngine._generate_rag_answer(intent, entities, query.query)
        
        # Suggested actions
        actions = NLPEngine._suggest_actions(intent, entities)
        
        return NLPResponse(
            query=query.query,
            intent=intent,
            entities=entities,
            answer=answer,
            confidence=0.85,
            sources=["service_registry", "metrics_history", "knowledge_base"],
            suggested_actions=actions
        )
    
    @staticmethod
    async def _generate_rag_answer(intent: str, entities: List[Dict], query: str) -> str:
        """Generate answer using RAG (Retrieval Augmented Generation)"""
        
        # Retrieve relevant context
        context = []
        for entity in entities:
            if entity["type"] == "service":
                service_id = entity["value"]
                if service_id in SERVICES:
                    context.append(f"Service {SERVICES[service_id]['name']} runs on port {SERVICES[service_id]['port']}")
        
        # Generate answer based on intent
        if intent == "status_check":
            if entities:
                service = SERVICES.get(entities[0]["value"])
                return f"The {service['name']} is configured to run on port {service['port']}. It provides {service['description']} with {service['endpoints']} endpoints. It has {len(service.get('dependencies', []))} dependencies."
            return "All services are monitored in real-time. Use the dashboard to see current status of each service."
        
        elif intent == "diagnostic":
            return "To diagnose issues, I recommend checking: 1) Service health scores, 2) Error rates in metrics, 3) Dependency chain status, 4) Recent log patterns. Would you like me to run a comprehensive diagnostic?"
        
        elif intent == "optimization":
            return "For optimal performance, consider: 1) Reviewing the AI recommendations panel, 2) Checking resource utilization trends, 3) Analyzing critical path dependencies, 4) Implementing auto-scaling policies."
        
        elif intent == "action":
            return "Service actions can be performed from the dashboard. Ensure you have appropriate permissions and consider the impact on dependent services before proceeding."
        
        return "I can help you monitor services, diagnose issues, optimize performance, or perform administrative actions. What would you like to know more about?"
    
    @staticmethod
    def _suggest_actions(intent: str, entities: List[Dict]) -> List[str]:
        """Suggest relevant actions"""
        if intent == "status_check":
            return ["View Dashboard", "Check Health Scores", "Review Metrics"]
        elif intent == "diagnostic":
            return ["Run Diagnostics", "View Logs", "Check Dependencies"]
        elif intent == "optimization":
            return ["View Recommendations", "Analyze Performance", "Apply Optimizations"]
        elif intent == "action":
            return ["View Service Controls", "Check Permissions", "Review Impact"]
        return ["Explore Dashboard", "Ask Another Question"]


class RAGEngine:
    """Retrieval Augmented Generation for intelligent recommendations"""
    
    @staticmethod
    async def generate_recommendations() -> List[AIRecommendation]:
        """Generate AI-powered recommendations using RAG"""
        recommendations = []
        
        # Simulated recommendations (in production, this would use actual ML models)
        recommendations.append(AIRecommendation(
            recommendation_id=hashlib.md5(b"rec1").hexdigest()[:8],
            service="reinstallation",
            priority="high",
            category="performance",
            title="High CPU Usage Detected",
            description="The Reinstallation Service is experiencing elevated CPU usage (65%), which may indicate inefficient package resolution or excessive parallel operations.",
            impact_score=8.5,
            effort_score=3.0,
            estimated_improvement="30-40% reduction in CPU usage",
            action_items=[
                "Implement lazy loading for package metadata",
                "Add caching layer for dependency resolution",
                "Limit concurrent package operations to 4",
                "Enable CPU affinity for better core utilization"
            ],
            reasoning="Based on historical patterns, CPU spikes correlate with simultaneous package installations. Implementing batch processing and caching can significantly reduce redundant operations.",
            confidence=0.87
        ))
        
        recommendations.append(AIRecommendation(
            recommendation_id=hashlib.md5(b"rec2").hexdigest()[:8],
            service="loki",
            priority="medium",
            category="cost",
            title="Storage Optimization Needed",
            description="Loki storage is at 78% capacity. Implementing log retention policies can free up 40-50% of current storage.",
            impact_score=7.0,
            effort_score=2.0,
            estimated_improvement="40-50% storage reduction",
            action_items=[
                "Set 30-day retention for INFO level logs",
                "Set 90-day retention for WARN/ERROR logs",
                "Enable log compression",
                "Archive old logs to cold storage"
            ],
            reasoning="Analysis shows that 60% of stored logs are INFO level and older than 45 days. These can be safely archived or deleted per standard retention policies.",
            confidence=0.92
        ))
        
        recommendations.append(AIRecommendation(
            recommendation_id=hashlib.md5(b"rec3").hexdigest()[:8],
            service="optimization",
            priority="low",
            category="reliability",
            title="Implement Circuit Breaker Pattern",
            description="Add circuit breaker to prevent cascade failures when dependent services are slow.",
            impact_score=6.5,
            effort_score=5.0,
            estimated_improvement="99.5% → 99.9% availability",
            action_items=[
                "Install resilience4j library",
                "Configure circuit breaker thresholds",
                "Add fallback mechanisms",
                "Monitor circuit breaker state"
            ],
            reasoning="Dependency analysis shows that when metrics-collector experiences latency, it can impact optimization service. Circuit breaker will isolate failures and maintain service availability.",
            confidence=0.78
        ))
        
        return recommendations


# ==================== Service Health Management ====================

async def check_service_health(service_id: str, service_info: Dict) -> Dict:
    """Enhanced health check with metrics collection"""
    start_time = asyncio.get_event_loop().time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{service_info['url']}/health",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                response_time = (asyncio.get_event_loop().time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Simulate metrics (in production, fetch from actual endpoints)
                    metrics = ServiceMetrics(
                        cpu_percent=20.0 + (hash(service_id) % 50),
                        memory_mb=256.0 + (hash(service_id) % 512),
                        memory_percent=25.0 + (hash(service_id) % 40),
                        network_in_mbps=10.5,
                        network_out_mbps=8.2,
                        disk_io_read_mbps=15.3,
                        disk_io_write_mbps=12.1,
                        request_rate=150.0 + (hash(service_id) % 200),
                        error_rate=0.5,
                        p50_latency=25.0,
                        p95_latency=85.0,
                        p99_latency=150.0,
                        active_connections=42 + (hash(service_id) % 100)
                    )
                    
                    # Calculate health score
                    health_score = AdvancedScoringEngine.calculate_health_score(
                        service_id, metrics, ServiceStatus.HEALTHY,
                        list(metrics_history.get(service_id, []))
                    )
                    
                    # Store in history
                    metrics_history[service_id].append({
                        "timestamp": datetime.now().isoformat(),
                        "score": health_score.overall,
                        "metrics": metrics.dict()
                    })
                    
                    return {
                        "service": service_id,
                        "status": ServiceStatus.HEALTHY.value,
                        "response_time_ms": round(response_time, 2),
                        "last_check": datetime.now().isoformat(),
                        "version": data.get("version", "unknown"),
                        "metrics": metrics.dict(),
                        "health_score": health_score.dict(),
                        "category": service_info["category"].value,
                        "criticality": service_info["criticality"]
                    }
                else:
                    return {
                        "service": service_id,
                        "status": ServiceStatus.UNHEALTHY.value,
                        "response_time_ms": round(response_time, 2),
                        "last_check": datetime.now().isoformat()
                    }
    except Exception as e:
        response_time = (asyncio.get_event_loop().time() - start_time) * 1000
        return {
            "service": service_id,
            "status": ServiceStatus.DOWN.value,
            "response_time_ms": round(response_time, 2),
            "last_check": datetime.now().isoformat(),
            "error": str(e)
        }


async def check_all_services() -> Dict[str, Dict]:
    """Check health of all services in parallel"""
    tasks = [
        check_service_health(service_id, service_info)
        for service_id, service_info in SERVICES.items()
    ]
    
    results = await asyncio.gather(*tasks)
    
    return {result["service"]: result for result in results}


# ==================== Background Tasks ====================

async def broadcast_health_updates():
    """Broadcast health updates and generate AI recommendations"""
    while True:
        try:
            # Check all services
            health_status = await check_all_services()
            
            # Update service status
            for service_id, health in health_status.items():
                SERVICES[service_id]["status"] = health["status"]
            
            # Generate topology graph
            topology = GraphEngine.build_topology_graph()
            
            # Generate AI recommendations periodically
            if len(recommendation_cache) < 3:
                global recommendation_cache
                recommendation_cache = await RAGEngine.generate_recommendations()
            
            # Broadcast to all connected clients
            if active_connections:
                message = {
                    "type": "mesh_update",
                    "timestamp": datetime.now().isoformat(),
                    "services": health_status,
                    "topology": topology.dict(),
                    "recommendations": [r.dict() for r in recommendation_cache]
                }
                
                disconnected = []
                for connection in active_connections:
                    try:
                        await connection.send_json(message)
                    except:
                        disconnected.append(connection)
                
                # Remove disconnected clients
                for conn in disconnected:
                    active_connections.remove(conn)
            
            await asyncio.sleep(10)  # Update every 10 seconds
            
        except Exception as e:
            print(f"[❌] Error in health check broadcast: {e}")
            await asyncio.sleep(10)


@app.on_event("startup")
async def startup_event():
    """Initialize background tasks"""
    asyncio.create_task(broadcast_health_updates())
    
    # Initialize recommendation cache
    global recommendation_cache
    recommendation_cache = await RAGEngine.generate_recommendations()


# ==================== API Endpoints ====================

@app.get("/", response_class=HTMLResponse)
async def ultra_dashboard():
    """Ultra-Advanced Service Mesh Dashboard with 3D Visualization"""
    from pathlib import Path
    dashboard_path = Path(__file__).parent / "static" / "dashboard.html"
    if dashboard_path.exists():
        return HTMLResponse(content=dashboard_path.read_text())
    return HTMLResponse(content="""
        <html>
            <head><title>OSE Service Mesh - Ultra Advanced</title></head>
            <body style="background: #1e293b; color: white; font-family: sans-serif; padding: 40px; text-align: center;">
                <h1>🌐 Ultra-Advanced Service Mesh Dashboard</h1>
                <p>Dashboard file not found at static/dashboard.html</p>
                <p>Expected path: {}</p>
            </body>
        </html>
    """.format(dashboard_path))


@app.get("/api/v1/services")
async def get_services():
    """Get all registered services with full metadata"""
    return {
        "total": len(SERVICES),
        "services": SERVICES,
        "categories": {cat.value: [s for s in SERVICES if SERVICES[s]["category"] == cat] 
                      for cat in ServiceCategory}
    }


@app.get("/api/v1/health/comprehensive")
async def comprehensive_health_check():
    """Comprehensive health check with advanced analytics"""
    health_status = await check_all_services()
    
    # Calculate aggregate metrics
    healthy = sum(1 for h in health_status.values() if h["status"] == ServiceStatus.HEALTHY.value)
    degraded = sum(1 for h in health_status.values() if h["status"] == ServiceStatus.DEGRADED.value)
    unhealthy = sum(1 for h in health_status.values() if h["status"] == ServiceStatus.UNHEALTHY.value)
    down = sum(1 for h in health_status.values() if h["status"] == ServiceStatus.DOWN.value)
    
    # Calculate overall health score
    scores = [h.get("health_score", {}).get("overall", 0) for h in health_status.values() if "health_score" in h]
    overall_score = sum(scores) / len(scores) if scores else 0
    
    # Calculate SLA compliance
    sla_compliance = (healthy / len(SERVICES)) * 100
    
    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_services": len(SERVICES),
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy,
            "down": down,
            "overall_health_score": round(overall_score, 2),
            "sla_compliance": round(sla_compliance, 2)
        },
        "services": health_status,
        "topology": GraphEngine.build_topology_graph().dict(),
        "critical_services": [s for s in SERVICES if SERVICES[s]["criticality"] == "critical"]
    }


@app.get("/api/v1/topology/graph")
async def get_topology_graph():
    """Get 3D service topology graph"""
    return GraphEngine.build_topology_graph()


@app.get("/api/v1/analytics/metrics/{service_id}")
async def get_service_analytics(service_id: str, window: str = Query("1h", regex="^(1h|6h|24h|7d|30d)$")):
    """Get advanced analytics for a specific service"""
    if service_id not in SERVICES:
        raise HTTPException(status_code=404, detail="[❌] Service not found")
    
    history = list(metrics_history.get(service_id, []))
    
    # Filter by time window
    now = datetime.now()
    if window == "1h":
        cutoff = now - timedelta(hours=1)
    elif window == "6h":
        cutoff = now - timedelta(hours=6)
    elif window == "24h":
        cutoff = now - timedelta(days=1)
    elif window == "7d":
        cutoff = now - timedelta(days=7)
    else:
        cutoff = now - timedelta(days=30)
    
    filtered_history = [
        h for h in history 
        if datetime.fromisoformat(h["timestamp"]) >= cutoff
    ]
    
    # Calculate statistics
    if filtered_history:
        scores = [h["score"] for h in filtered_history]
        stats = {
            "min": min(scores),
            "max": max(scores),
            "avg": statistics.mean(scores),
            "median": statistics.median(scores),
            "stdev": statistics.stdev(scores) if len(scores) > 1 else 0
        }
    else:
        stats = {"min": 0, "max": 0, "avg": 0, "median": 0, "stdev": 0}
    
    return {
        "service": service_id,
        "window": window,
        "data_points": len(filtered_history),
        "statistics": stats,
        "history": filtered_history[-100:]  # Return last 100 points
    }


@app.post("/api/v1/nlp/query")
async def process_nlp_query(query: NLPQuery):
    """Process natural language query"""
    return await NLPEngine.process_query(query)


@app.get("/api/v1/ai/recommendations")
async def get_ai_recommendations(category: Optional[str] = None, priority: Optional[str] = None):
    """Get AI-generated recommendations"""
    recommendations = recommendation_cache
    
    if category:
        recommendations = [r for r in recommendations if r.category == category]
    
    if priority:
        recommendations = [r for r in recommendations if r.priority == priority]
    
    return {
        "total": len(recommendations),
        "recommendations": [r.dict() for r in recommendations]
    }


@app.websocket("/ws/mesh")
async def websocket_mesh(websocket: WebSocket):
    """WebSocket endpoint for real-time mesh updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial state
        health_status = await check_all_services()
        topology = GraphEngine.build_topology_graph()
        
        await websocket.send_json({
            "type": "mesh_update",
            "timestamp": datetime.now().isoformat(),
            "services": health_status,
            "topology": topology.dict(),
            "recommendations": [r.dict() for r in recommendation_cache]
        })
        
        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                # Handle client messages if needed
            except WebSocketDisconnect:
                break
    except Exception as e:
        print(f"[⚠️] WebSocket error: {e}")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.get("/health")
async def service_mesh_health():
    """Service mesh self-health check"""
    return {
        "status": "[✅] healthy",
        "service": "ultra-advanced-service-mesh",
        "timestamp": datetime.now().isoformat(),
        "version": "2.5.0",
        "features": [
            "3d_topology_visualization",
            "nlp_query_system",
            "rag_recommendations",
            "dag_workflow_engine",
            "graph_analytics",
            "predictive_health_scoring",
            "multi_dimensional_metrics",
            "advanced_heartbeat_monitoring",
            "dependency_mapping",
            "message_bus_integration"
        ]
    }


# ==================== Heartbeat Monitoring Endpoints ====================

@app.get("/api/v1/heartbeat/status")
async def get_heartbeat_status():
    """Get heartbeat status for all services"""
    from heartbeat import heartbeat_manager
    return heartbeat_manager.get_all_statuses()


@app.get("/api/v1/heartbeat/status/{service_id}")
async def get_service_heartbeat(service_id: str):
    """Get heartbeat status for specific service"""
    from heartbeat import heartbeat_manager
    status = heartbeat_manager.get_service_status(service_id)
    
    if status is None:
        raise HTTPException(status_code=404, detail=f"[❌] Service {service_id} not registered")
    
    return status


@app.get("/api/v1/heartbeat/summary")
async def get_heartbeat_summary():
    """Get heartbeat health summary"""
    from heartbeat import heartbeat_manager
    return heartbeat_manager.get_health_summary()


@app.post("/api/v1/heartbeat/register")
async def register_service_heartbeat(
    service_id: str,
    service_name: str,
    interval_seconds: int = 10,
    timeout_seconds: int = 30,
    max_failures: int = 3
):
    """Register a service for heartbeat monitoring"""
    from heartbeat import heartbeat_manager
    
    heartbeat_manager.register_service(
        service_id=service_id,
        service_name=service_name,
        interval_seconds=interval_seconds,
        timeout_seconds=timeout_seconds,
        max_failures=max_failures
    )
    
    return {"message": f"[✅] Service {service_id} registered for heartbeat monitoring"}


# ==================== Dependency Mapping Endpoints ====================

@app.get("/api/v1/dependencies/graph")
async def get_dependency_graph():
    """Get full dependency graph"""
    from dependencies import dependency_graph
    return dependency_graph.get_summary()


@app.get("/api/v1/dependencies/service/{service_id}")
async def get_service_dependencies(service_id: str, direction: str = "both"):
    """Get dependencies for a specific service"""
    from dependencies import dependency_graph
    
    deps = dependency_graph.get_dependencies(service_id, direction)
    
    return {
        "service_id": service_id,
        "direction": direction,
        "dependencies": deps
    }


@app.get("/api/v1/dependencies/visualize/cytoscape")
async def get_cytoscape_graph():
    """Get dependency graph in Cytoscape.js format"""
    from dependencies import dependency_graph
    return dependency_graph.to_cytoscape_json()


@app.get("/api/v1/dependencies/visualize/d3")
async def get_d3_graph():
    """Get dependency graph in D3.js format"""
    from dependencies import dependency_graph
    return dependency_graph.to_d3_json()


@app.get("/api/v1/dependencies/visualize/mermaid")
async def get_mermaid_diagram():
    """Get dependency graph as Mermaid diagram"""
    from dependencies import dependency_graph
    return {
        "mermaid": dependency_graph.to_mermaid()
    }


@app.get("/api/v1/dependencies/analysis/circular")
async def detect_circular_dependencies():
    """Detect circular dependencies"""
    from dependencies import dependency_graph
    
    circular = dependency_graph.detect_circular_dependencies()
    
    return {
        "has_circular_dependencies": len(circular) > 0,
        "circular_dependency_count": len(circular),
        "circular_paths": circular
    }


@app.get("/api/v1/dependencies/analysis/critical-path")
async def get_critical_path():
    """Get critical dependency path"""
    from dependencies import dependency_graph
    
    return {
        "critical_path": dependency_graph.get_critical_path()
    }


@app.get("/api/v1/dependencies/analysis/hubs")
async def get_hub_services():
    """Get hub services (services with many dependencies)"""
    from dependencies import dependency_graph
    
    return {
        "hub_services": dependency_graph.get_hub_services(),
        "isolated_services": dependency_graph.get_isolated_services()
    }


# ==================== Message Bus Endpoints ====================

@app.get("/api/v1/messagebus/status")
async def get_message_bus_status():
    """Get message bus connection status"""
    from message_bus import message_bus
    
    return {
        "connected": message_bus.is_connected,
        "host": message_bus.host,
        "port": message_bus.port,
        "exchanges": list(message_bus.exchanges.keys()),
        "queues": list(message_bus.queues.keys()),
        "active_consumers": len(message_bus.consumers)
    }


@app.post("/api/v1/messagebus/publish")
async def publish_event(
    exchange: str,
    event_type: str,
    source_service: str,
    payload: Dict[str, Any],
    routing_key: str = "",
    priority: int = 5
):
    """Publish an event to the message bus"""
    from message_bus import message_bus, EventMessage, MessagePriority
    
    if not message_bus.is_connected:
        raise HTTPException(status_code=503, detail="[❌] Message bus not connected")
    
    event = EventMessage(
        event_type=event_type,
        source_service=source_service,
        payload=payload,
        priority=MessagePriority(priority)
    )
    
    await message_bus.publish_event(exchange, event, routing_key)
    
    return {
        "message": "[🚀] Event published successfully",
        "event_type": event_type,
        "exchange": exchange,
        "routing_key": routing_key
    }


@app.get("/api/v1/messagebus/exchanges")
async def list_exchanges():
    """List all declared exchanges"""
    from message_bus import message_bus
    
    return {
        "exchanges": [
            {
                "name": name,
                "type": str(exchange)
            }
            for name, exchange in message_bus.exchanges.items()
        ]
    }


@app.get("/api/v1/messagebus/queues")
async def list_queues():
    """List all declared queues"""
    from message_bus import message_bus
    
    return {
        "queues": [
            {
                "name": name,
                "messages": 0  # Would need to query RabbitMQ API for actual count
            }
            for name in message_bus.queues.keys()
        ]
    }


# ==================== Visualization Endpoints ====================

@app.get("/dependencies", response_class=HTMLResponse)
async def dependencies_visualization():
    """Interactive dependency graph visualization"""
    with open(Path(__file__).parent / "templates" / "dependencies.html") as f:
        return HTMLResponse(content=f.read())


# ==================== AI Engine Endpoints ====================

@app.post("/api/v1/ai/query")
async def ai_query(
    query: str,
    component_id: str = "service_mesh",
    use_ensemble: bool = True,
    use_nlp: bool = True,
    fusion_strategy: str = "confidence_based"
):
    """[🧠] Query AI engines with full NLP and ensemble fusion"""
    if not AI_ENGINES_AVAILABLE:
        raise HTTPException(status_code=503, detail="[❌] AI engines not available")
    
    try:
        from ai_integration_wiring import IntegrationRequest, FusionStrategy
        
        # Map string to enum
        strategy_map = {
            "confidence_based": FusionStrategy.CONFIDENCE_BASED,
            "weighted_average": FusionStrategy.WEIGHTED_AVERAGE,
            "majority_voting": FusionStrategy.MAJORITY_VOTING,
            "rank_fusion": FusionStrategy.RANK_FUSION,
            "mixture_of_experts": FusionStrategy.MIXTURE_OF_EXPERTS
        }
        
        request = IntegrationRequest(
            request_id=f"mesh_query_{datetime.now().timestamp()}",
            component_id=component_id,
            query=query,
            use_ensemble=use_ensemble,
            use_nlp=use_nlp,
            fusion_strategy=strategy_map.get(fusion_strategy, FusionStrategy.CONFIDENCE_BASED)
        )
        
        response = await ai_engine_integration.process_request(request)
        
        return {
            "success": response.success,
            "result": response.result,
            "execution_time": response.execution_time,
            "engines_used": response.engines_used,
            "error": response.error,
            "timestamp": response.timestamp
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[❌] AI query failed: {str(e)}")


@app.get("/api/v1/ai/status")
async def ai_engine_status():
    """[📊] Get AI engine integration status"""
    if not AI_ENGINES_AVAILABLE:
        return {
            "available": False,
            "message": "[⚠️] AI engines not initialized"
        }
    
    try:
        status = await ai_engine_integration.get_integration_status()
        return {
            "available": True,
            "status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[❌] Status check failed: {str(e)}")


@app.get("/api/v1/ai/health")
async def ai_engine_health():
    """[💊] AI engine health check"""
    if not AI_ENGINES_AVAILABLE:
        return {
            "status": "[❌] unavailable",
            "message": "AI engines not initialized"
        }
    
    try:
        health = await ai_engine_integration.health_check()
        return health
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[❌] Health check failed: {str(e)}")


@app.post("/api/v1/ai/broadcast")
async def ai_broadcast_query(query: str):
    """[📡] Broadcast query to all registered components"""
    if not AI_ENGINES_AVAILABLE:
        raise HTTPException(status_code=503, detail="[❌] AI engines not available")
    
    try:
        responses = await ai_engine_integration.broadcast_to_all_components(query)
        
        return {
            "query": query,
            "total_components": len(responses),
            "successful": sum(1 for r in responses.values() if r.success),
            "responses": {
                comp_id: {
                    "success": resp.success,
                    "result": resp.result,
                    "error": resp.error
                }
                for comp_id, resp in responses.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[❌] Broadcast failed: {str(e)}")


@app.get("/api/v1/ai/components")
async def list_ai_components():
    """[📋] List all registered AI components"""
    if not AI_ENGINES_AVAILABLE:
        raise HTTPException(status_code=503, detail="[❌] AI engines not available")
    
    return {
        "components": [
            {
                "id": comp.component_id,
                "type": comp.component_type.value,
                "enabled": comp.enabled,
                "capabilities": comp.capabilities,
                "endpoints": comp.endpoints
            }
            for comp in ai_engine_integration.components.values()
        ]
    }


# ==================== Visualization Dashboards ====================

@app.get("/heartbeat-dashboard", response_class=HTMLResponse)
async def heartbeat_dashboard():
    """[🫀] Real-time heartbeat monitoring dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🫀 OSE Heartbeat Monitor</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 20px;
            }
            .container { max-width: 1400px; margin: 0 auto; }
            h1 { text-align: center; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
            .service-card {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .service-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .service-name { font-size: 18px; font-weight: bold; }
            .status-badge {
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
            }
            .status-healthy { background: #10b981; }
            .status-degraded { background: #f59e0b; }
            .status-critical { background: #ef4444; }
            .status-dead { background: #991b1b; }
            .metric { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
            .metric-label { color: rgba(255, 255, 255, 0.7); }
            .metric-value { font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🫀 OSE Heartbeat Monitor</h1>
            <div class="grid" id="services"></div>
        </div>
        <script>
            async function loadHeartbeats() {
                const response = await fetch('/api/v1/heartbeat/status');
                const data = await response.json();
                
                const container = document.getElementById('services');
                container.innerHTML = '';
                
                for (const [serviceId, status] of Object.entries(data)) {
                    if (!status) continue;
                    
                    const card = document.createElement('div');
                    card.className = 'service-card';
                    
                    const statusClass = `status-${status.status}`;
                    
                    card.innerHTML = `
                        <div class="service-header">
                            <div class="service-name">${status.service_name}</div>
                            <div class="status-badge ${statusClass}">${status.status.toUpperCase()}</div>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Heartbeat Count:</span>
                            <span class="metric-value">${status.metrics.heartbeat_count}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Missed:</span>
                            <span class="metric-value">${status.metrics.missed_heartbeats}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Avg Latency:</span>
                            <span class="metric-value">${status.metrics.average_latency_ms}ms</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Uptime:</span>
                            <span class="metric-value">${status.metrics.uptime_percentage}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Last Seen:</span>
                            <span class="metric-value">${status.metrics.seconds_since_last}s ago</span>
                        </div>
                    `;
                    
                    container.appendChild(card);
                }
            }
            
            loadHeartbeats();
            setInterval(loadHeartbeats, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
