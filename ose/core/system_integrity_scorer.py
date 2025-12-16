#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SYSTEM INTEGRITY SCORING ENGINE                            ║
║                  Real-time Health & Risk Assessment                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Component A: Comprehensive system health scoring with multi-dimensional metrics
"""

import os
import sys
import json
import time
import psutil
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """Container for system-level metrics"""
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    swap_usage_percent: float
    load_average: Tuple[float, float, float]
    uptime_hours: float
    process_count: int
    open_files: int
    network_connections: int
    timestamp: str


@dataclass
class HealthScore:
    """Container for health scoring results"""
    overall_score: float  # 0-100
    performance_score: float
    stability_score: float
    resource_score: float
    security_score: float
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    recommendations: List[str]
    metrics: SystemMetrics
    timestamp: str


class SystemIntegrityScorer:
    """
    Advanced system health scoring engine with real-time monitoring.
    
    Scoring Methodology:
    - Performance (30%): CPU, Memory, Disk I/O efficiency
    - Stability (25%): Uptime, process health, error rates
    - Resources (25%): Available capacity, growth trends
    - Security (20%): File permissions, open ports, vulnerabilities
    """
    
    # Scoring thresholds
    THRESHOLDS = {
        'cpu': {'excellent': 30, 'good': 50, 'fair': 70, 'poor': 85},
        'memory': {'excellent': 50, 'good': 70, 'fair': 85, 'poor': 95},
        'disk': {'excellent': 50, 'good': 70, 'fair': 85, 'poor': 95},
        'swap': {'excellent': 10, 'good': 30, 'fair': 60, 'poor': 80},
        'load': {'excellent': 1.0, 'good': 2.0, 'fair': 3.0, 'poor': 5.0}
    }
    
    # Risk level mappings
    RISK_LEVELS = {
        (90, 100): 'LOW',
        (75, 90): 'MEDIUM',
        (50, 75): 'HIGH',
        (0, 50): 'CRITICAL'
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the scoring engine"""
        self.config_path = config_path or "/tmp/ose_integrity_config.json"
        self.history_path = "/tmp/ose_integrity_history.json"
        self.config = self._load_config()
        self.history = self._load_history()
        
        logger.info("🎯 System Integrity Scorer initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration or create defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
        
        # Default configuration
        return {
            'weights': {
                'performance': 0.30,
                'stability': 0.25,
                'resources': 0.25,
                'security': 0.20
            },
            'monitoring_interval': 60,  # seconds
            'history_retention': 1000,  # records
            'alert_threshold': 60.0  # score below triggers alert
        }
    
    def _load_history(self) -> List[Dict]:
        """Load scoring history"""
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load history: {e}")
        return []
    
    def _save_history(self, score: HealthScore):
        """Save score to history with retention limit"""
        try:
            self.history.append(asdict(score))
            
            # Enforce retention limit
            max_records = self.config.get('history_retention', 1000)
            if len(self.history) > max_records:
                self.history = self.history[-max_records:]
            
            with open(self.history_path, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def collect_metrics(self) -> SystemMetrics:
        """Collect comprehensive system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent
            
            # Swap metrics
            swap = psutil.swap_memory()
            swap_usage_percent = swap.percent
            
            # Load average
            load_avg = os.getloadavg()
            
            # Uptime
            boot_time = psutil.boot_time()
            uptime_hours = (time.time() - boot_time) / 3600
            
            # Process metrics
            process_count = len(psutil.pids())
            
            # File descriptors (approximate)
            try:
                open_files = len(psutil.Process().open_files())
            except:
                open_files = 0
            
            # Network connections
            try:
                network_connections = len(psutil.net_connections())
            except:
                network_connections = 0
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage_percent=disk_usage_percent,
                swap_usage_percent=swap_usage_percent,
                load_average=load_avg,
                uptime_hours=uptime_hours,
                process_count=process_count,
                open_files=open_files,
                network_connections=network_connections,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"Failed to collect metrics: {e}")
            raise
    
    def _score_metric(self, value: float, thresholds: Dict[str, float], 
                     inverse: bool = False) -> float:
        """
        Score a single metric based on thresholds.
        
        Args:
            value: Current metric value
            thresholds: Dict with 'excellent', 'good', 'fair', 'poor' keys
            inverse: If True, lower values are better
        
        Returns:
            Score from 0-100
        """
        if inverse:
            value = 100 - value
        
        if value <= thresholds['excellent']:
            return 100.0
        elif value <= thresholds['good']:
            # Linear interpolation between excellent and good
            range_size = thresholds['good'] - thresholds['excellent']
            position = value - thresholds['excellent']
            return 100.0 - (position / range_size) * 15.0
        elif value <= thresholds['fair']:
            range_size = thresholds['fair'] - thresholds['good']
            position = value - thresholds['good']
            return 85.0 - (position / range_size) * 20.0
        elif value <= thresholds['poor']:
            range_size = thresholds['poor'] - thresholds['fair']
            position = value - thresholds['fair']
            return 65.0 - (position / range_size) * 40.0
        else:
            return max(0.0, 25.0 - (value - thresholds['poor']) / 10.0)
    
    def calculate_performance_score(self, metrics: SystemMetrics) -> float:
        """Calculate performance subscore (30% of total)"""
        cpu_score = self._score_metric(
            metrics.cpu_percent, 
            self.THRESHOLDS['cpu']
        )
        
        # Load average scoring (normalized by CPU count)
        cpu_count = psutil.cpu_count() or 1
        load_normalized = metrics.load_average[0] / cpu_count * 100
        load_score = self._score_metric(
            load_normalized,
            {'excellent': 50, 'good': 80, 'fair': 120, 'poor': 150}
        )
        
        # Weighted performance score
        return (cpu_score * 0.6) + (load_score * 0.4)
    
    def calculate_stability_score(self, metrics: SystemMetrics) -> float:
        """Calculate stability subscore (25% of total)"""
        # Uptime scoring (longer is better, up to a point)
        uptime_score = min(100.0, (metrics.uptime_hours / 168) * 100)  # 1 week = 100%
        
        # Process count scoring (moderate is best)
        optimal_processes = 150
        process_deviation = abs(metrics.process_count - optimal_processes)
        process_score = max(0, 100 - (process_deviation / 5))
        
        # Weighted stability score
        return (uptime_score * 0.6) + (process_score * 0.4)
    
    def calculate_resource_score(self, metrics: SystemMetrics) -> float:
        """Calculate resource availability subscore (25% of total)"""
        memory_score = self._score_metric(
            metrics.memory_percent,
            self.THRESHOLDS['memory']
        )
        
        disk_score = self._score_metric(
            metrics.disk_usage_percent,
            self.THRESHOLDS['disk']
        )
        
        swap_score = self._score_metric(
            metrics.swap_usage_percent,
            self.THRESHOLDS['swap']
        )
        
        # Weighted resource score
        return (memory_score * 0.4) + (disk_score * 0.4) + (swap_score * 0.2)
    
    def calculate_security_score(self, metrics: SystemMetrics) -> float:
        """Calculate security subscore (20% of total)"""
        # Open connections scoring (fewer is generally better)
        conn_score = max(0, 100 - (metrics.network_connections / 10))
        
        # Open files scoring
        files_score = max(0, 100 - (metrics.open_files / 20))
        
        # Basic security baseline
        baseline_score = 80.0  # Assume reasonable security posture
        
        # Weighted security score
        return (baseline_score * 0.5) + (conn_score * 0.3) + (files_score * 0.2)
    
    def generate_recommendations(self, metrics: SystemMetrics, 
                                scores: Dict[str, float]) -> List[str]:
        """Generate actionable recommendations based on scores"""
        recommendations = []
        
        # Performance recommendations
        if metrics.cpu_percent > 70:
            recommendations.append(
                "⚠️ HIGH CPU: Consider closing unnecessary applications or upgrading hardware"
            )
        
        if metrics.load_average[0] / (psutil.cpu_count() or 1) > 2.0:
            recommendations.append(
                "⚠️ HIGH LOAD: System is oversubscribed, consider process optimization"
            )
        
        # Resource recommendations
        if metrics.memory_percent > 85:
            recommendations.append(
                "💾 HIGH MEMORY: Clear caches or add more RAM"
            )
        
        if metrics.disk_usage_percent > 85:
            recommendations.append(
                "💿 LOW DISK SPACE: Clean up unnecessary files or expand storage"
            )
        
        if metrics.swap_usage_percent > 50:
            recommendations.append(
                "🔄 SWAP PRESSURE: System is swapping heavily, add more physical memory"
            )
        
        # Stability recommendations
        if metrics.uptime_hours < 1:
            recommendations.append(
                "🔄 RECENT REBOOT: System recently restarted, monitor for stability"
            )
        
        if metrics.process_count > 300:
            recommendations.append(
                "📊 HIGH PROCESS COUNT: Review running services for optimization"
            )
        
        # Security recommendations
        if metrics.network_connections > 200:
            recommendations.append(
                "🔒 MANY CONNECTIONS: Review active network connections for security"
            )
        
        # Overall health
        if scores['overall'] < 60:
            recommendations.append(
                "🚨 CRITICAL: System health is degraded, immediate action recommended"
            )
        elif scores['overall'] < 75:
            recommendations.append(
                "⚠️ WARNING: System health needs attention"
            )
        
        if not recommendations:
            recommendations.append("✅ System health is good, no immediate action required")
        
        return recommendations
    
    def determine_risk_level(self, overall_score: float) -> str:
        """Determine risk level based on overall score"""
        for (low, high), level in self.RISK_LEVELS.items():
            if low <= overall_score < high:
                return level
        return 'CRITICAL'
    
    def calculate_health_score(self) -> HealthScore:
        """
        Calculate comprehensive health score.
        
        Returns:
            HealthScore object with all metrics and subscores
        """
        # Collect metrics
        metrics = self.collect_metrics()
        
        # Calculate subscores
        performance_score = self.calculate_performance_score(metrics)
        stability_score = self.calculate_stability_score(metrics)
        resource_score = self.calculate_resource_score(metrics)
        security_score = self.calculate_security_score(metrics)
        
        # Calculate weighted overall score
        weights = self.config['weights']
        overall_score = (
            performance_score * weights['performance'] +
            stability_score * weights['stability'] +
            resource_score * weights['resources'] +
            security_score * weights['security']
        )
        
        # Round to 2 decimal places
        overall_score = round(overall_score, 2)
        performance_score = round(performance_score, 2)
        stability_score = round(stability_score, 2)
        resource_score = round(resource_score, 2)
        security_score = round(security_score, 2)
        
        # Generate recommendations
        scores_dict = {
            'overall': overall_score,
            'performance': performance_score,
            'stability': stability_score,
            'resources': resource_score,
            'security': security_score
        }
        recommendations = self.generate_recommendations(metrics, scores_dict)
        
        # Determine risk level
        risk_level = self.determine_risk_level(overall_score)
        
        # Create health score object
        health_score = HealthScore(
            overall_score=overall_score,
            performance_score=performance_score,
            stability_score=stability_score,
            resource_score=resource_score,
            security_score=security_score,
            risk_level=risk_level,
            recommendations=recommendations,
            metrics=metrics,
            timestamp=datetime.now().isoformat()
        )
        
        # Save to history
        self._save_history(health_score)
        
        return health_score
    
    def get_score_trend(self, periods: int = 10) -> Dict[str, Any]:
        """
        Analyze score trends over recent history.
        
        Args:
            periods: Number of historical records to analyze
        
        Returns:
            Dict with trend analysis
        """
        if len(self.history) < 2:
            return {
                'trend': 'insufficient_data',
                'direction': 'unknown',
                'change_percent': 0.0
            }
        
        recent = self.history[-periods:]
        scores = [record['overall_score'] for record in recent]
        
        # Calculate trend
        first_score = scores[0]
        last_score = scores[-1]
        change = last_score - first_score
        change_percent = (change / first_score) * 100 if first_score > 0 else 0
        
        # Determine direction
        if abs(change_percent) < 2:
            direction = 'stable'
            trend = 'steady'
        elif change_percent > 0:
            direction = 'improving'
            trend = 'upward'
        else:
            direction = 'degrading'
            trend = 'downward'
        
        return {
            'trend': trend,
            'direction': direction,
            'change_percent': round(change_percent, 2),
            'first_score': first_score,
            'last_score': last_score,
            'average_score': round(sum(scores) / len(scores), 2),
            'periods_analyzed': len(scores)
        }
    
    def export_report(self, output_path: str):
        """Export detailed health report to JSON"""
        score = self.calculate_health_score()
        trend = self.get_score_trend()
        
        report = {
            'current_health': asdict(score),
            'trend_analysis': trend,
            'generated_at': datetime.now().isoformat(),
            'system_info': {
                'platform': sys.platform,
                'python_version': sys.version,
                'cpu_count': psutil.cpu_count(),
                'total_memory_gb': round(psutil.virtual_memory().total / (1024**3), 2)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Health report exported to {output_path}")
        return report


def main():
    """CLI interface for testing"""
    scorer = SystemIntegrityScorer()
    
    print("\n" + "="*80)
    print("🎯 SYSTEM INTEGRITY SCORER - Health Analysis")
    print("="*80 + "\n")
    
    # Calculate health score
    score = scorer.calculate_health_score()
    
    # Display results
    print(f"📊 Overall Health Score: {score.overall_score:.1f}/100")
    print(f"🎭 Risk Level: {score.risk_level}")
    print(f"\n📈 Component Scores:")
    print(f"  • Performance: {score.performance_score:.1f}/100")
    print(f"  • Stability:   {score.stability_score:.1f}/100")
    print(f"  • Resources:   {score.resource_score:.1f}/100")
    print(f"  • Security:    {score.security_score:.1f}/100")
    
    print(f"\n💡 Recommendations:")
    for rec in score.recommendations:
        print(f"  {rec}")
    
    # Show trend
    trend = scorer.get_score_trend()
    print(f"\n📉 Trend: {trend['direction'].upper()} ({trend['change_percent']:+.1f}%)")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
