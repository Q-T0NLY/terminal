#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║ 🎯 COMPONENT A: SYSTEM INTEGRITY SCORER                                        ║
║ Real-time health scoring with weighted metrics and adaptive thresholds         ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MetricWeight:
    """Weighted metric configuration"""
    name: str
    weight: float
    threshold_warn: float
    threshold_critical: float
    optimal_range: Tuple[float, float]


@dataclass
class IntegrityScore:
    """System integrity score result"""
    overall_score: float
    grade: str  # A+, A, B, C, D, F
    status: str  # optimal, degraded, critical
    metrics: Dict[str, float]
    issues: List[str]
    recommendations: List[str]
    timestamp: str


class SystemIntegrityScorer:
    """
    🎯 Advanced system integrity scorer with adaptive thresholds
    
    Scoring Formula:
    Overall Score = Σ(metric_value × weight) / Σ(weights)
    
    Where each metric is normalized to 0-100 scale
    """
    
    METRIC_WEIGHTS = [
        MetricWeight("cpu_health", 0.20, 80.0, 95.0, (0, 70)),
        MetricWeight("memory_health", 0.25, 85.0, 95.0, (0, 80)),
        MetricWeight("disk_health", 0.15, 85.0, 95.0, (0, 80)),
        MetricWeight("service_availability", 0.25, 90.0, 95.0, (95, 100)),
        MetricWeight("network_health", 0.10, 80.0, 90.0, (0, 50)),
        MetricWeight("process_health", 0.05, 85.0, 95.0, (0, 100))
    ]
    
    GRADE_THRESHOLDS = {
        95: "A+", 90: "A", 85: "A-",
        80: "B+", 75: "B", 70: "B-",
        65: "C+", 60: "C", 55: "C-",
        50: "D", 0: "F"
    }
    
    def __init__(self):
        self.history: List[IntegrityScore] = []
        self.baseline: Optional[Dict[str, float]] = None
        
    async def collect_metrics(self) -> Dict[str, float]:
        """Collect all system metrics"""
        metrics = {}
        
        # CPU Health (inverted - lower usage = better)
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics['cpu_health'] = max(0, 100 - cpu_percent)
        
        # Memory Health
        mem = psutil.virtual_memory()
        metrics['memory_health'] = max(0, 100 - mem.percent)
        
        # Disk Health
        disk = psutil.disk_usage('/')
        metrics['disk_health'] = max(0, 100 - disk.percent)
        
        # Service Availability (check running services)
        running_services = await self._check_services()
        total_services = len(running_services)
        healthy_services = sum(1 for s in running_services.values() if s)
        metrics['service_availability'] = (healthy_services / total_services * 100) if total_services > 0 else 100
        
        # Network Health (check connectivity)
        network_ok = await self._check_network()
        metrics['network_health'] = 100 if network_ok else 0
        
        # Process Health (zombie/defunct processes)
        zombie_count = len([p for p in psutil.process_iter(['status']) if p.info['status'] == 'zombie'])
        metrics['process_health'] = max(0, 100 - (zombie_count * 10))
        
        return metrics
    
    async def _check_services(self) -> Dict[str, bool]:
        """Check critical service availability"""
        services = {
            'discovery': 8001,
            'optimization': 8002,
            'terminal-config': 8003,
            'universal-registry': 8004
        }
        
        status = {}
        for name, port in services.items():
            try:
                # Quick port check
                proc = await asyncio.create_subprocess_exec(
                    'netstat', '-tuln',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await proc.communicate()
                status[name] = f':{port}' in stdout.decode()
            except:
                status[name] = False
        
        return status
    
    async def _check_network(self) -> bool:
        """Check network connectivity"""
        try:
            proc = await asyncio.create_subprocess_exec(
                'ping', '-c', '1', '-W', '1', '8.8.8.8',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await asyncio.wait_for(proc.communicate(), timeout=2)
            return proc.returncode == 0
        except:
            return False
    
    def calculate_score(self, metrics: Dict[str, float]) -> IntegrityScore:
        """
        Calculate weighted integrity score
        
        Formula: Overall = Σ(metric × weight) / Σ(weights)
        """
        total_score = 0.0
        total_weight = 0.0
        issues = []
        recommendations = []
        
        for metric_def in self.METRIC_WEIGHTS:
            value = metrics.get(metric_def.name, 0)
            weighted_value = value * metric_def.weight
            total_score += weighted_value
            total_weight += metric_def.weight
            
            # Check thresholds
            if value < metric_def.threshold_critical:
                issues.append(f"🔴 CRITICAL: {metric_def.name} at {value:.1f}% (critical threshold: {metric_def.threshold_critical}%)")
                recommendations.append(f"Immediate action required for {metric_def.name}")
            elif value < metric_def.threshold_warn:
                issues.append(f"🟡 WARNING: {metric_def.name} at {value:.1f}% (warning threshold: {metric_def.threshold_warn}%)")
                recommendations.append(f"Monitor {metric_def.name} closely")
        
        # Calculate final score
        overall_score = (total_score / total_weight) if total_weight > 0 else 0
        
        # Determine grade
        grade = "F"
        for threshold, grade_letter in sorted(self.GRADE_THRESHOLDS.items(), reverse=True):
            if overall_score >= threshold:
                grade = grade_letter
                break
        
        # Determine status
        if overall_score >= 90:
            status = "optimal"
        elif overall_score >= 70:
            status = "degraded"
        else:
            status = "critical"
        
        return IntegrityScore(
            overall_score=round(overall_score, 2),
            grade=grade,
            status=status,
            metrics=metrics,
            issues=issues,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )
    
    async def score(self) -> IntegrityScore:
        """Run complete integrity scoring"""
        metrics = await self.collect_metrics()
        score = self.calculate_score(metrics)
        
        # Store in history
        self.history.append(score)
        if len(self.history) > 100:
            self.history.pop(0)
        
        # Update baseline if first run
        if self.baseline is None:
            self.baseline = metrics
        
        return score
    
    def get_trend(self, minutes: int = 30) -> Dict[str, str]:
        """Analyze score trend over time"""
        if len(self.history) < 2:
            return {"trend": "insufficient_data"}
        
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent = [h for h in self.history if datetime.fromisoformat(h.timestamp) > cutoff]
        
        if len(recent) < 2:
            return {"trend": "insufficient_data"}
        
        first_score = recent[0].overall_score
        last_score = recent[-1].overall_score
        delta = last_score - first_score
        
        if delta > 5:
            trend = "improving"
        elif delta < -5:
            trend = "degrading"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "delta": round(delta, 2),
            "first": round(first_score, 2),
            "last": round(last_score, 2)
        }


# ══════════════════════════════════════════════════════════════════════════════
# 🌐 FastAPI Service Endpoint
# ══════════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="System Integrity Scorer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scorer = SystemIntegrityScorer()


@app.get("/")
async def root():
    return {
        "service": "System Integrity Scorer",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/score")
async def get_score():
    """Get current system integrity score"""
    score = await scorer.score()
    return asdict(score)


@app.get("/trend")
async def get_trend(minutes: int = 30):
    """Get score trend analysis"""
    return scorer.get_trend(minutes)


@app.get("/metrics")
async def get_metrics():
    """Get raw metrics only"""
    metrics = await scorer.collect_metrics()
    return {"metrics": metrics, "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
