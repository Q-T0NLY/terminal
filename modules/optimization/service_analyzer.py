"""
⚙️ Service Analyzer
Analyze system services for resource usage and optimization opportunities
"""

import subprocess
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ServiceInfo:
    """Information about a system service"""
    name: str
    status: str  # active, inactive, failed
    enabled: bool
    cpu_usage: float = 0.0  # percent
    memory_usage: int = 0  # bytes
    tasks: int = 0
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    required_by: List[str] = field(default_factory=list)
    optimization_score: int = 0  # 0-100, higher = more optimization potential
    

class ServiceAnalyzer:
    """
    Analyze system services for optimization
    
    Features:
    - List all systemd services
    - Analyze resource usage (CPU, memory)
    - Identify unnecessary services
    - Suggest services to disable
    - Dependency analysis
    - Failed service detection
    """
    
    # Services generally safe to disable on desktop systems
    DESKTOP_SAFE_TO_DISABLE = [
        "bluetooth.service",  # If no Bluetooth devices
        "ModemManager.service",  # If no modem
        "cups.service",  # If no printer
        "cups-browsed.service",  # Printer discovery
        "avahi-daemon.service",  # mDNS/zeroconf
        "kerneloops.service",  # Kernel error reporting
        "speech-dispatcher.service",  # Speech synthesis
        "whoopsie.service",  # Ubuntu error reporting
        "apport.service",  # Crash reporting
        "tracker-miner-fs.service",  # GNOME file indexing
        "tracker-store.service",
    ]
    
    # Services that should NEVER be disabled
    ESSENTIAL_SERVICES = [
        "systemd-journald.service",
        "systemd-logind.service",
        "systemd-udevd.service",
        "dbus.service",
        "NetworkManager.service",
        "network.service",
        "ssh.service",
        "sshd.service",
        "cron.service",
        "crond.service",
    ]
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Service Analyzer
        
        Args:
            dry_run: If True, simulate changes
        """
        self.dry_run = dry_run
        
    def list_all_services(self) -> List[ServiceInfo]:
        """
        List all systemd services
        
        Returns:
            List of ServiceInfo objects
        """
        services = []
        
        try:
            # Get all services
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--all", "--no-pager"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if not line.strip() or line.startswith('●'):
                    continue
                    
                # Parse service line
                match = re.match(r'\s*([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+(.*)', line)
                
                if match:
                    name = match.group(1)
                    status = match.group(3)  # active, inactive, failed
                    
                    # Get enabled status
                    enabled = self._is_service_enabled(name)
                    
                    # Get resource usage
                    cpu, memory, tasks = self._get_service_resources(name)
                    
                    # Get description
                    description = self._get_service_description(name)
                    
                    service = ServiceInfo(
                        name=name,
                        status=status,
                        enabled=enabled,
                        cpu_usage=cpu,
                        memory_usage=memory,
                        tasks=tasks,
                        description=description
                    )
                    
                    services.append(service)
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return services
        
    def analyze_services(self) -> Dict[str, any]:
        """
        Analyze all services and provide recommendations
        
        Returns:
            Dict with analysis results
        """
        services = self.list_all_services()
        
        # Categorize services
        active = [s for s in services if s.status == "active"]
        inactive = [s for s in services if s.status == "inactive"]
        failed = [s for s in services if s.status == "failed"]
        
        # High resource usage
        high_cpu = [s for s in active if s.cpu_usage > 5.0]
        high_memory = [s for s in active if s.memory_usage > 100 * 1024 * 1024]  # >100MB
        
        # Safe to disable (enabled but inactive)
        safe_to_disable = [
            s for s in services
            if s.enabled and
            s.status != "active" and
            s.name in self.DESKTOP_SAFE_TO_DISABLE
        ]
        
        # Could be disabled (active but low priority)
        could_disable = [
            s for s in active
            if s.name in self.DESKTOP_SAFE_TO_DISABLE
        ]
        
        return {
            "total_services": len(services),
            "active": len(active),
            "inactive": len(inactive),
            "failed": len(failed),
            "high_cpu": high_cpu,
            "high_memory": high_memory,
            "safe_to_disable": safe_to_disable,
            "could_disable": could_disable,
            "recommendations": self._generate_recommendations(
                failed, high_cpu, high_memory, safe_to_disable, could_disable
            )
        }
        
    def get_failed_services(self) -> List[ServiceInfo]:
        """
        Get list of failed services
        
        Returns:
            List of failed services
        """
        services = self.list_all_services()
        return [s for s in services if s.status == "failed"]
        
    def get_resource_hogs(
        self,
        top_n: int = 10
    ) -> Dict[str, List[ServiceInfo]]:
        """
        Get top resource-consuming services
        
        Args:
            top_n: Number of top services to return
            
        Returns:
            Dict with top CPU and memory consumers
        """
        services = self.list_all_services()
        active = [s for s in services if s.status == "active"]
        
        # Sort by CPU
        by_cpu = sorted(active, key=lambda s: s.cpu_usage, reverse=True)[:top_n]
        
        # Sort by memory
        by_memory = sorted(active, key=lambda s: s.memory_usage, reverse=True)[:top_n]
        
        return {
            "top_cpu": by_cpu,
            "top_memory": by_memory
        }
        
    def optimize_services(
        self,
        disable_unnecessary: bool = True,
        stop_failed: bool = True
    ) -> Dict[str, any]:
        """
        Automatically optimize services
        
        Args:
            disable_unnecessary: Disable unnecessary services
            stop_failed: Stop failed services
            
        Returns:
            Dict with optimization results
        """
        disabled = []
        stopped = []
        
        analysis = self.analyze_services()
        
        # Disable unnecessary services
        if disable_unnecessary:
            for service in analysis["safe_to_disable"]:
                if self._disable_service(service.name):
                    disabled.append(service.name)
                    
        # Stop failed services
        if stop_failed:
            for service in analysis["failed"]:
                if service.name not in self.ESSENTIAL_SERVICES:
                    if self._stop_service(service.name):
                        stopped.append(service.name)
                        
        return {
            "success": True,
            "disabled": disabled,
            "stopped": stopped
        }
        
    # ==================== Private Helper Methods ====================
    
    def _is_service_enabled(self, service: str) -> bool:
        """Check if service is enabled"""
        try:
            result = subprocess.run(
                ["systemctl", "is-enabled", service],
                capture_output=True,
                text=True
            )
            
            return result.stdout.strip() == "enabled"
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _get_service_resources(
        self,
        service: str
    ) -> tuple[float, int, int]:
        """Get service resource usage (CPU%, memory bytes, tasks)"""
        try:
            result = subprocess.run(
                ["systemctl", "show", service, "--property=CPUUsageNSec,MemoryCurrent,TasksCurrent"],
                capture_output=True,
                text=True,
                check=True
            )
            
            cpu = 0.0
            memory = 0
            tasks = 0
            
            for line in result.stdout.split('\n'):
                if line.startswith('MemoryCurrent='):
                    try:
                        memory = int(line.split('=')[1])
                    except ValueError:
                        pass
                elif line.startswith('TasksCurrent='):
                    try:
                        tasks = int(line.split('=')[1])
                    except ValueError:
                        pass
                        
            return cpu, memory, tasks
            
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return 0.0, 0, 0
            
    def _get_service_description(self, service: str) -> str:
        """Get service description"""
        try:
            result = subprocess.run(
                ["systemctl", "show", service, "--property=Description"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if line.startswith('Description='):
                    return line.split('=', 1)[1]
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return ""
        
    def _disable_service(self, service: str) -> bool:
        """Disable a service"""
        if self.dry_run:
            return True
            
        try:
            subprocess.run(
                ["sudo", "systemctl", "disable", service],
                check=True,
                capture_output=True
            )
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _stop_service(self, service: str) -> bool:
        """Stop a service"""
        if self.dry_run:
            return True
            
        try:
            subprocess.run(
                ["sudo", "systemctl", "stop", service],
                check=True,
                capture_output=True
            )
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _generate_recommendations(
        self,
        failed: List[ServiceInfo],
        high_cpu: List[ServiceInfo],
        high_memory: List[ServiceInfo],
        safe_to_disable: List[ServiceInfo],
        could_disable: List[ServiceInfo]
    ) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        if failed:
            recommendations.append(
                f"⚠️ {len(failed)} failed service(s) detected. Consider investigating or disabling them."
            )
            
        if high_cpu:
            recommendations.append(
                f"🔥 {len(high_cpu)} service(s) with high CPU usage. Check for performance issues."
            )
            
        if high_memory:
            recommendations.append(
                f"💾 {len(high_memory)} service(s) with high memory usage (>100MB)."
            )
            
        if safe_to_disable:
            recommendations.append(
                f"✅ {len(safe_to_disable)} unnecessary service(s) can be safely disabled."
            )
            
        if could_disable:
            recommendations.append(
                f"💡 {len(could_disable)} service(s) running that you may not need."
            )
            
        if not recommendations:
            recommendations.append("✨ All services are optimally configured!")
            
        return recommendations
