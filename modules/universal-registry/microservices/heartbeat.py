"""
Advanced Heartbeat Manager for OSE Services
Monitors service health with sophisticated heartbeat mechanisms
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import json

class HeartbeatStatus(Enum):
    """Heartbeat status states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    DEAD = "dead"
    UNKNOWN = "unknown"

@dataclass
class HeartbeatMetrics:
    """Metrics for heartbeat monitoring"""
    last_heartbeat: float
    heartbeat_count: int = 0
    missed_heartbeats: int = 0
    average_latency: float = 0.0
    max_latency: float = 0.0
    min_latency: float = float('inf')
    consecutive_failures: int = 0
    uptime_start: float = field(default_factory=time.time)
    
    def uptime_seconds(self) -> float:
        """Calculate uptime in seconds"""
        return time.time() - self.uptime_start
    
    def uptime_percentage(self) -> float:
        """Calculate uptime percentage"""
        total_expected = self.heartbeat_count + self.missed_heartbeats
        if total_expected == 0:
            return 100.0
        return (self.heartbeat_count / total_expected) * 100.0

@dataclass
class ServiceHeartbeat:
    """Heartbeat information for a service"""
    service_id: str
    service_name: str
    status: HeartbeatStatus
    metrics: HeartbeatMetrics
    interval_seconds: int = 10
    timeout_seconds: int = 30
    max_failures: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_alive(self) -> bool:
        """Check if service is alive based on heartbeat"""
        time_since_last = time.time() - self.metrics.last_heartbeat
        return time_since_last < self.timeout_seconds
    
    def update_status(self):
        """Update heartbeat status based on metrics"""
        if not self.is_alive():
            self.status = HeartbeatStatus.DEAD
        elif self.metrics.consecutive_failures >= self.max_failures:
            self.status = HeartbeatStatus.CRITICAL
        elif self.metrics.consecutive_failures > 0:
            self.status = HeartbeatStatus.DEGRADED
        else:
            self.status = HeartbeatStatus.HEALTHY
    
    def record_success(self, latency: float):
        """Record successful heartbeat"""
        self.metrics.last_heartbeat = time.time()
        self.metrics.heartbeat_count += 1
        self.metrics.consecutive_failures = 0
        
        # Update latency metrics
        self.metrics.max_latency = max(self.metrics.max_latency, latency)
        self.metrics.min_latency = min(self.metrics.min_latency, latency)
        
        # Calculate rolling average latency
        total = self.metrics.average_latency * (self.metrics.heartbeat_count - 1) + latency
        self.metrics.average_latency = total / self.metrics.heartbeat_count
        
        self.update_status()
    
    def record_failure(self):
        """Record failed heartbeat"""
        self.metrics.missed_heartbeats += 1
        self.metrics.consecutive_failures += 1
        self.update_status()


class HeartbeatManager:
    """Advanced heartbeat monitoring system"""
    
    def __init__(self):
        self.heartbeats: Dict[str, ServiceHeartbeat] = {}
        self.running = False
        self.monitor_task: Optional[asyncio.Task] = None
    
    def register_service(
        self,
        service_id: str,
        service_name: str,
        interval_seconds: int = 10,
        timeout_seconds: int = 30,
        max_failures: int = 3,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Register a service for heartbeat monitoring"""
        self.heartbeats[service_id] = ServiceHeartbeat(
            service_id=service_id,
            service_name=service_name,
            status=HeartbeatStatus.UNKNOWN,
            metrics=HeartbeatMetrics(last_heartbeat=time.time()),
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
            max_failures=max_failures,
            metadata=metadata or {}
        )
    
    def unregister_service(self, service_id: str):
        """Unregister a service from heartbeat monitoring"""
        if service_id in self.heartbeats:
            del self.heartbeats[service_id]
    
    async def check_heartbeat(self, service_id: str, check_url: str) -> bool:
        """Check service heartbeat"""
        import aiohttp
        
        if service_id not in self.heartbeats:
            return False
        
        heartbeat = self.heartbeats[service_id]
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(check_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    latency = time.time() - start_time
                    
                    if response.status == 200:
                        heartbeat.record_success(latency)
                        return True
                    else:
                        heartbeat.record_failure()
                        return False
        except Exception:
            latency = time.time() - start_time
            heartbeat.record_failure()
            return False
    
    def get_service_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a service"""
        if service_id not in self.heartbeats:
            return None
        
        heartbeat = self.heartbeats[service_id]
        
        return {
            "service_id": service_id,
            "service_name": heartbeat.service_name,
            "status": heartbeat.status.value,
            "is_alive": heartbeat.is_alive(),
            "metrics": {
                "heartbeat_count": heartbeat.metrics.heartbeat_count,
                "missed_heartbeats": heartbeat.metrics.missed_heartbeats,
                "consecutive_failures": heartbeat.metrics.consecutive_failures,
                "average_latency_ms": round(heartbeat.metrics.average_latency * 1000, 2),
                "max_latency_ms": round(heartbeat.metrics.max_latency * 1000, 2),
                "min_latency_ms": round(heartbeat.metrics.min_latency * 1000, 2) if heartbeat.metrics.min_latency != float('inf') else 0,
                "uptime_seconds": round(heartbeat.metrics.uptime_seconds(), 2),
                "uptime_percentage": round(heartbeat.metrics.uptime_percentage(), 2),
                "last_heartbeat": datetime.fromtimestamp(heartbeat.metrics.last_heartbeat).isoformat(),
                "seconds_since_last": round(time.time() - heartbeat.metrics.last_heartbeat, 2)
            },
            "config": {
                "interval_seconds": heartbeat.interval_seconds,
                "timeout_seconds": heartbeat.timeout_seconds,
                "max_failures": heartbeat.max_failures
            },
            "metadata": heartbeat.metadata
        }
    
    def get_all_statuses(self) -> Dict[str, Any]:
        """Get status of all monitored services"""
        return {
            service_id: self.get_service_status(service_id)
            for service_id in self.heartbeats.keys()
        }
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get overall health summary"""
        total = len(self.heartbeats)
        healthy = sum(1 for hb in self.heartbeats.values() if hb.status == HeartbeatStatus.HEALTHY)
        degraded = sum(1 for hb in self.heartbeats.values() if hb.status == HeartbeatStatus.DEGRADED)
        critical = sum(1 for hb in self.heartbeats.values() if hb.status == HeartbeatStatus.CRITICAL)
        dead = sum(1 for hb in self.heartbeats.values() if hb.status == HeartbeatStatus.DEAD)
        
        return {
            "total_services": total,
            "healthy": healthy,
            "degraded": degraded,
            "critical": critical,
            "dead": dead,
            "overall_health_percentage": round((healthy / total * 100) if total > 0 else 0, 2)
        }
    
    async def start_monitoring(self):
        """Start continuous heartbeat monitoring"""
        self.running = True
        
        while self.running:
            # Check all heartbeats
            for service_id, heartbeat in self.heartbeats.items():
                # Construct health check URL
                # This would be service-specific in production
                check_url = f"http://{service_id}:{heartbeat.metadata.get('port', 8000)}/health"
                
                # Schedule heartbeat check
                asyncio.create_task(self.check_heartbeat(service_id, check_url))
            
            # Wait for next check interval (use minimum interval)
            min_interval = min(
                (hb.interval_seconds for hb in self.heartbeats.values()),
                default=10
            )
            await asyncio.sleep(min_interval)
    
    async def stop_monitoring(self):
        """Stop heartbeat monitoring"""
        self.running = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass


# Global heartbeat manager instance
heartbeat_manager = HeartbeatManager()
