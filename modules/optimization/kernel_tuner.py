"""
🔧 Kernel Tuner
Optimize Linux kernel parameters for better performance
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class KernelParam:
    """Represents a kernel parameter"""
    name: str
    current_value: str
    recommended_value: str
    description: str
    category: str  # memory, network, io, security
    

class KernelTuner:
    """
    Optimize Linux kernel parameters via sysctl
    
    Features:
    - Read current kernel parameters
    - Apply recommended optimizations
    - Profile-based tuning (desktop, server, gaming)
    - Persistent configuration
    - Rollback support
    
    ⚠️ WARNING: Kernel tuning requires careful consideration.
    Always test changes and keep backups!
    """
    
    # Recommended kernel parameters for different profiles
    PROFILES = {
        "desktop": {
            "vm.swappiness": "10",  # Reduce swap usage
            "vm.vfs_cache_pressure": "50",  # Keep file cache longer
            "vm.dirty_ratio": "10",  # Write dirty pages at 10%
            "vm.dirty_background_ratio": "5",  # Background writes at 5%
            "net.core.netdev_max_backlog": "5000",
            "net.ipv4.tcp_fastopen": "3",
        },
        
        "server": {
            "vm.swappiness": "1",  # Minimal swap for servers
            "vm.vfs_cache_pressure": "50",
            "net.core.somaxconn": "4096",  # Increase connection queue
            "net.core.netdev_max_backlog": "10000",
            "net.ipv4.tcp_max_syn_backlog": "8192",
            "net.ipv4.tcp_tw_reuse": "1",  # Reuse TIME_WAIT sockets
            "net.ipv4.ip_local_port_range": "1024 65535",
            "fs.file-max": "2097152",  # Increase file descriptors
        },
        
        "gaming": {
            "vm.swappiness": "5",  # Very low swap
            "vm.vfs_cache_pressure": "50",
            "net.ipv4.tcp_low_latency": "1",  # Prioritize latency
            "net.core.netdev_max_backlog": "5000",
            "kernel.sched_latency_ns": "6000000",  # Reduce scheduler latency
            "kernel.sched_min_granularity_ns": "750000",
        }
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Kernel Tuner
        
        Args:
            dry_run: If True, simulate changes without applying
        """
        self.dry_run = dry_run
        self.sysctl_conf = Path("/etc/sysctl.conf")
        self.sysctl_d = Path("/etc/sysctl.d")
        
    def get_current_params(self, params: List[str]) -> Dict[str, str]:
        """
        Get current values of kernel parameters
        
        Args:
            params: List of parameter names
            
        Returns:
            Dict mapping parameter names to current values
        """
        current = {}
        
        for param in params:
            try:
                result = subprocess.run(
                    ["sysctl", "-n", param],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                current[param] = result.stdout.strip()
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                current[param] = "unknown"
                
        return current
        
    def analyze_parameters(
        self,
        profile: str = "desktop"
    ) -> List[KernelParam]:
        """
        Analyze current parameters and recommend changes
        
        Args:
            profile: Tuning profile (desktop, server, gaming)
            
        Returns:
            List of KernelParam objects with recommendations
        """
        if profile not in self.PROFILES:
            profile = "desktop"
            
        recommended = self.PROFILES[profile]
        current_values = self.get_current_params(list(recommended.keys()))
        
        params = []
        
        for name, rec_value in recommended.items():
            current_val = current_values.get(name, "unknown")
            
            params.append(KernelParam(
                name=name,
                current_value=current_val,
                recommended_value=rec_value,
                description=self._get_param_description(name),
                category=self._get_param_category(name)
            ))
            
        return params
        
    def apply_profile(self, profile: str = "desktop") -> Dict[str, any]:
        """
        Apply kernel tuning profile
        
        Args:
            profile: Profile to apply (desktop, server, gaming)
            
        Returns:
            Dict with results
        """
        if profile not in self.PROFILES:
            return {
                "success": False,
                "error": f"Unknown profile: {profile}"
            }
            
        recommended = self.PROFILES[profile]
        applied = []
        failed = []
        
        for param, value in recommended.items():
            if self._set_parameter(param, value):
                applied.append(param)
            else:
                failed.append(param)
                
        # Make persistent
        if not self.dry_run and applied:
            self._write_persistent_config(profile, recommended)
            
        return {
            "success": len(failed) == 0,
            "profile": profile,
            "applied": applied,
            "failed": failed
        }
        
    def apply_custom(
        self,
        params: Dict[str, str],
        make_persistent: bool = True
    ) -> Dict[str, any]:
        """
        Apply custom kernel parameters
        
        Args:
            params: Dict of parameter_name: value
            make_persistent: Whether to write to sysctl.conf
            
        Returns:
            Dict with results
        """
        applied = []
        failed = []
        
        for param, value in params.items():
            if self._set_parameter(param, value):
                applied.append(param)
            else:
                failed.append(param)
                
        # Make persistent
        if not self.dry_run and applied and make_persistent:
            self._write_persistent_config("custom", params)
            
        return {
            "success": len(failed) == 0,
            "applied": applied,
            "failed": failed
        }
        
    def reset_to_defaults(self) -> bool:
        """
        Reset kernel parameters to system defaults
        
        Returns:
            True if successful
        """
        if self.dry_run:
            return True
            
        # Remove OSE config file
        ose_conf = self.sysctl_d / "99-ose.conf"
        
        if ose_conf.exists():
            try:
                ose_conf.unlink()
                
                # Reload sysctl
                subprocess.run(
                    ["sudo", "sysctl", "--system"],
                    check=True,
                    capture_output=True
                )
                
                return True
                
            except (OSError, subprocess.CalledProcessError):
                return False
                
        return True
        
    # ==================== Private Helper Methods ====================
    
    def _set_parameter(self, param: str, value: str) -> bool:
        """Set kernel parameter temporarily"""
        if self.dry_run:
            return True
            
        try:
            subprocess.run(
                ["sudo", "sysctl", "-w", f"{param}={value}"],
                check=True,
                capture_output=True
            )
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _write_persistent_config(
        self,
        profile: str,
        params: Dict[str, str]
    ):
        """Write persistent sysctl configuration"""
        # Create sysctl.d directory if not exists
        if not self.sysctl_d.exists():
            self.sysctl_d.mkdir(parents=True, exist_ok=True)
            
        ose_conf = self.sysctl_d / "99-ose.conf"
        
        try:
            with open(ose_conf, 'w') as f:
                f.write(f"# OSE Kernel Tuning - Profile: {profile}\n")
                f.write(f"# Generated by OmniSystem Enhancer\n\n")
                
                for param, value in params.items():
                    f.write(f"{param} = {value}\n")
                    
        except (OSError, PermissionError):
            # Fallback to sudo tee
            content = f"# OSE Kernel Tuning - Profile: {profile}\n"
            content += "# Generated by OmniSystem Enhancer\n\n"
            
            for param, value in params.items():
                content += f"{param} = {value}\n"
                
            subprocess.run(
                ["sudo", "tee", str(ose_conf)],
                input=content.encode(),
                check=True,
                capture_output=True
            )
            
    def _get_param_description(self, param: str) -> str:
        """Get description of kernel parameter"""
        descriptions = {
            "vm.swappiness": "Controls swap tendency (0-100, lower = less swap)",
            "vm.vfs_cache_pressure": "Tendency to reclaim inode/dentry cache",
            "vm.dirty_ratio": "Percentage of memory for dirty pages before sync writes",
            "vm.dirty_background_ratio": "Percentage for background writes",
            "net.core.somaxconn": "Maximum socket listen() backlog",
            "net.core.netdev_max_backlog": "Maximum network device backlog",
            "net.ipv4.tcp_max_syn_backlog": "Maximum queued TCP SYN requests",
            "net.ipv4.tcp_tw_reuse": "Reuse TIME_WAIT sockets",
            "net.ipv4.tcp_fastopen": "Enable TCP Fast Open",
            "net.ipv4.tcp_low_latency": "Prioritize low latency over throughput",
            "net.ipv4.ip_local_port_range": "Local port range for outgoing connections",
            "fs.file-max": "Maximum number of file handles",
            "kernel.sched_latency_ns": "Scheduler latency target (nanoseconds)",
            "kernel.sched_min_granularity_ns": "Minimum scheduler granularity",
        }
        
        return descriptions.get(param, f"Kernel parameter: {param}")
        
    def _get_param_category(self, param: str) -> str:
        """Get category of kernel parameter"""
        if param.startswith("vm."):
            return "memory"
        elif param.startswith("net."):
            return "network"
        elif param.startswith("fs."):
            return "filesystem"
        elif param.startswith("kernel.sched"):
            return "scheduler"
        else:
            return "other"
