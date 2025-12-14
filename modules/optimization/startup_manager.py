"""
🚀 Startup Manager
Manage startup applications and services for faster boot
"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class StartupType(Enum):
    """Type of startup item"""
    SYSTEMD_SERVICE = "systemd_service"
    SYSTEMD_TIMER = "systemd_timer"
    CRON_JOB = "cron_job"
    AUTOSTART_DESKTOP = "autostart_desktop"
    LAUNCHD_AGENT = "launchd_agent"  # macOS
    LAUNCHD_DAEMON = "launchd_daemon"  # macOS
    

@dataclass
class StartupItem:
    """Represents a startup item"""
    name: str
    type: StartupType
    enabled: bool
    auto_start: bool
    description: str
    path: Optional[Path] = None
    impact: str = "medium"  # low, medium, high
    

class StartupManager:
    """
    Manage system startup applications and services
    
    Features:
    - List all startup items
    - Enable/disable startup items
    - Analyze boot impact
    - Optimize boot sequence
    - Supports systemd, cron, autostart, launchd
    """
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Startup Manager
        
        Args:
            dry_run: If True, simulate changes without applying
        """
        self.dry_run = dry_run
        self.is_systemd = self._has_systemd()
        self.is_macos = os.uname().sysname == "Darwin"
        
    def list_startup_items(self) -> List[StartupItem]:
        """
        List all startup items
        
        Returns:
            List of StartupItem objects
        """
        items = []
        
        if self.is_systemd:
            items.extend(self._list_systemd_services())
            
        if self.is_macos:
            items.extend(self._list_launchd_items())
            
        items.extend(self._list_autostart_apps())
        items.extend(self._list_cron_jobs())
        
        return items
        
    def analyze_boot_time(self) -> Dict[str, any]:
        """
        Analyze boot time and identify slow services
        
        Returns:
            Dict with boot analysis:
            - total_time: Total boot time in seconds
            - kernel_time: Kernel initialization time
            - userspace_time: Userspace initialization time
            - slow_services: List of slow services
        """
        if not self.is_systemd:
            return {
                "total_time": 0,
                "kernel_time": 0,
                "userspace_time": 0,
                "slow_services": []
            }
            
        try:
            # Get boot time
            result = subprocess.run(
                ["systemd-analyze"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output
            output = result.stdout
            lines = output.split('\n')
            
            total_time = 0
            kernel_time = 0
            userspace_time = 0
            
            if lines:
                # Parse: "Startup finished in 2.5s (kernel) + 18.3s (userspace) = 20.8s"
                parts = lines[0].split('=')
                if len(parts) == 2:
                    total_str = parts[1].strip().rstrip('s')
                    try:
                        total_time = float(total_str)
                    except ValueError:
                        pass
                        
            # Get slow services
            slow_services = self._get_slow_services()
            
            return {
                "total_time": total_time,
                "kernel_time": kernel_time,
                "userspace_time": userspace_time,
                "slow_services": slow_services
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "total_time": 0,
                "kernel_time": 0,
                "userspace_time": 0,
                "slow_services": []
            }
            
    def disable_startup_item(self, item: StartupItem) -> bool:
        """
        Disable a startup item
        
        Args:
            item: StartupItem to disable
            
        Returns:
            True if successful
        """
        if self.dry_run:
            return True
            
        if item.type == StartupType.SYSTEMD_SERVICE:
            return self._disable_systemd_service(item.name)
            
        elif item.type == StartupType.AUTOSTART_DESKTOP:
            return self._disable_autostart_app(item.path)
            
        elif item.type == StartupType.LAUNCHD_AGENT:
            return self._disable_launchd_item(item.path)
            
        return False
        
    def enable_startup_item(self, item: StartupItem) -> bool:
        """
        Enable a startup item
        
        Args:
            item: StartupItem to enable
            
        Returns:
            True if successful
        """
        if self.dry_run:
            return True
            
        if item.type == StartupType.SYSTEMD_SERVICE:
            return self._enable_systemd_service(item.name)
            
        elif item.type == StartupType.AUTOSTART_DESKTOP:
            return self._enable_autostart_app(item.path)
            
        elif item.type == StartupType.LAUNCHD_AGENT:
            return self._enable_launchd_item(item.path)
            
        return False
        
    def optimize_boot(self, target_time: int = 15) -> Dict[str, any]:
        """
        Optimize boot time by disabling unnecessary startup items
        
        Args:
            target_time: Target boot time in seconds
            
        Returns:
            Dict with optimization results
        """
        current_boot = self.analyze_boot_time()
        current_time = current_boot["total_time"]
        
        if current_time <= target_time:
            return {
                "optimized": False,
                "reason": "Boot time already optimal",
                "current_time": current_time,
                "target_time": target_time
            }
            
        # Get all startup items
        items = self.list_startup_items()
        
        # Sort by impact (high impact first)
        high_impact = [i for i in items if i.impact == "high" and i.enabled]
        
        disabled_items = []
        
        # Disable high-impact non-essential services
        for item in high_impact:
            if not self._is_essential(item):
                if self.disable_startup_item(item):
                    disabled_items.append(item.name)
                    
        return {
            "optimized": True,
            "disabled_count": len(disabled_items),
            "disabled_items": disabled_items,
            "current_time": current_time,
            "target_time": target_time,
            "estimated_improvement": len(disabled_items) * 0.5  # Rough estimate
        }
        
    # ==================== Private Helper Methods ====================
    
    def _has_systemd(self) -> bool:
        """Check if system uses systemd"""
        return Path("/run/systemd/system").exists()
        
    def _list_systemd_services(self) -> List[StartupItem]:
        """List systemd services"""
        items = []
        
        try:
            result = subprocess.run(
                ["systemctl", "list-unit-files", "--type=service", "--state=enabled"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if not line.strip() or 'UNIT FILE' in line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    service_name = parts[0]
                    state = parts[1]
                    
                    items.append(StartupItem(
                        name=service_name,
                        type=StartupType.SYSTEMD_SERVICE,
                        enabled=state == "enabled",
                        auto_start=True,
                        description=self._get_service_description(service_name),
                        impact=self._estimate_service_impact(service_name)
                    ))
                    
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return items
        
    def _list_launchd_items(self) -> List[StartupItem]:
        """List macOS launchd items"""
        items = []
        
        launchd_paths = [
            Path.home() / "Library" / "LaunchAgents",
            Path("/Library/LaunchAgents"),
            Path("/Library/LaunchDaemons"),
            Path("/System/Library/LaunchAgents"),
            Path("/System/Library/LaunchDaemons")
        ]
        
        for launchd_dir in launchd_paths:
            if not launchd_dir.exists():
                continue
                
            for plist_file in launchd_dir.glob("*.plist"):
                is_daemon = "LaunchDaemons" in str(launchd_dir)
                
                items.append(StartupItem(
                    name=plist_file.stem,
                    type=StartupType.LAUNCHD_DAEMON if is_daemon else StartupType.LAUNCHD_AGENT,
                    enabled=True,  # Assume enabled if file exists
                    auto_start=True,
                    description=f"launchd item: {plist_file.stem}",
                    path=plist_file,
                    impact="medium"
                ))
                
        return items
        
    def _list_autostart_apps(self) -> List[StartupItem]:
        """List autostart desktop applications"""
        items = []
        
        autostart_dirs = [
            Path.home() / ".config" / "autostart",
            Path("/etc/xdg/autostart")
        ]
        
        for autostart_dir in autostart_dirs:
            if not autostart_dir.exists():
                continue
                
            for desktop_file in autostart_dir.glob("*.desktop"):
                # Read desktop file to get name and enabled status
                enabled = True
                name = desktop_file.stem
                description = ""
                
                try:
                    with open(desktop_file, 'r') as f:
                        content = f.read()
                        
                        # Check if disabled
                        if "Hidden=true" in content or "X-GNOME-Autostart-enabled=false" in content:
                            enabled = False
                            
                        # Extract name
                        for line in content.split('\n'):
                            if line.startswith("Name="):
                                name = line.split('=', 1)[1].strip()
                            elif line.startswith("Comment="):
                                description = line.split('=', 1)[1].strip()
                                
                except (IOError, UnicodeDecodeError):
                    pass
                    
                items.append(StartupItem(
                    name=name,
                    type=StartupType.AUTOSTART_DESKTOP,
                    enabled=enabled,
                    auto_start=enabled,
                    description=description,
                    path=desktop_file,
                    impact="low"
                ))
                
        return items
        
    def _list_cron_jobs(self) -> List[StartupItem]:
        """List cron jobs (not truly startup, but run regularly)"""
        items = []
        
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse cron line
                        parts = line.split(None, 5)
                        if len(parts) >= 6:
                            command = parts[5]
                            
                            items.append(StartupItem(
                                name=f"cron: {command[:30]}...",
                                type=StartupType.CRON_JOB,
                                enabled=True,
                                auto_start=True,
                                description=f"Cron job: {command}",
                                impact="low"
                            ))
                            
        except FileNotFoundError:
            pass
            
        return items
        
    def _get_slow_services(self) -> List[Tuple[str, float]]:
        """Get list of slow systemd services"""
        slow_services = []
        
        try:
            result = subprocess.run(
                ["systemd-analyze", "blame"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n')[:10]:  # Top 10 slowest
                if not line.strip():
                    continue
                    
                parts = line.split(None, 1)
                if len(parts) == 2:
                    time_str = parts[0]
                    service_name = parts[1]
                    
                    # Parse time (e.g., "2.5s", "500ms")
                    try:
                        if 's' in time_str:
                            time_val = float(time_str.rstrip('s'))
                        elif 'ms' in time_str:
                            time_val = float(time_str.rstrip('ms')) / 1000
                        else:
                            time_val = 0
                            
                        slow_services.append((service_name, time_val))
                        
                    except ValueError:
                        continue
                        
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return slow_services
        
    def _get_service_description(self, service_name: str) -> str:
        """Get description of systemd service"""
        try:
            result = subprocess.run(
                ["systemctl", "show", service_name, "--property=Description"],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout.strip()
            if output.startswith("Description="):
                return output.split('=', 1)[1]
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return f"Service: {service_name}"
        
    def _estimate_service_impact(self, service_name: str) -> str:
        """Estimate boot impact of service"""
        # High impact services (databases, servers, heavy apps)
        high_impact = [
            "mysql", "postgresql", "mongodb", "redis",
            "apache2", "nginx", "docker",
            "snapd", "bluetooth"
        ]
        
        # Low impact services
        low_impact = [
            "cron", "rsyslog", "ssh",
            "networking", "systemd"
        ]
        
        service_lower = service_name.lower()
        
        for high in high_impact:
            if high in service_lower:
                return "high"
                
        for low in low_impact:
            if low in service_lower:
                return "low"
                
        return "medium"
        
    def _is_essential(self, item: StartupItem) -> bool:
        """Check if startup item is essential"""
        essential_services = [
            "network", "ssh", "cron", "systemd",
            "dbus", "udev", "getty"
        ]
        
        name_lower = item.name.lower()
        
        return any(essential in name_lower for essential in essential_services)
        
    def _disable_systemd_service(self, service_name: str) -> bool:
        """Disable systemd service"""
        try:
            subprocess.run(
                ["sudo", "systemctl", "disable", service_name],
                check=True,
                capture_output=True
            )
            return True
            
        except subprocess.CalledProcessError:
            return False
            
    def _enable_systemd_service(self, service_name: str) -> bool:
        """Enable systemd service"""
        try:
            subprocess.run(
                ["sudo", "systemctl", "enable", service_name],
                check=True,
                capture_output=True
            )
            return True
            
        except subprocess.CalledProcessError:
            return False
            
    def _disable_autostart_app(self, desktop_file: Path) -> bool:
        """Disable autostart desktop application"""
        try:
            content = desktop_file.read_text()
            
            # Add Hidden=true if not present
            if "Hidden=true" not in content:
                content += "\nHidden=true\n"
                desktop_file.write_text(content)
                
            return True
            
        except (IOError, UnicodeDecodeError):
            return False
            
    def _enable_autostart_app(self, desktop_file: Path) -> bool:
        """Enable autostart desktop application"""
        try:
            content = desktop_file.read_text()
            
            # Remove Hidden=true
            content = content.replace("Hidden=true", "")
            content = content.replace("X-GNOME-Autostart-enabled=false", "")
            
            desktop_file.write_text(content)
            
            return True
            
        except (IOError, UnicodeDecodeError):
            return False
            
    def _disable_launchd_item(self, plist_file: Path) -> bool:
        """Disable macOS launchd item"""
        try:
            subprocess.run(
                ["launchctl", "unload", str(plist_file)],
                check=True,
                capture_output=True
            )
            return True
            
        except subprocess.CalledProcessError:
            return False
            
    def _enable_launchd_item(self, plist_file: Path) -> bool:
        """Enable macOS launchd item"""
        try:
            subprocess.run(
                ["launchctl", "load", str(plist_file)],
                check=True,
                capture_output=True
            )
            return True
            
        except subprocess.CalledProcessError:
            return False
