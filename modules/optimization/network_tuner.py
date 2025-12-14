"""
🌐 Network Tuner
Optimize network stack and TCP/IP parameters
"""

import subprocess
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class NetworkInfo:
    """Network interface information"""
    interface: str
    state: str
    mtu: int
    speed: str
    driver: str
    

class NetworkTuner:
    """
    Optimize network performance
    
    Features:
    - TCP/IP stack tuning
    - Network buffer optimization
    - Congestion control algorithms
    - DNS optimization
    - Interface optimization
    
    Tuning areas:
    - TCP window sizes
    - Connection backlog
    - Keepalive settings
    - Congestion control (BBR, CUBIC, etc.)
    - Network buffers
    """
    
    PROFILES = {
        "low_latency": {
            "description": "Optimized for low latency (gaming, VoIP)",
            "params": {
                "net.ipv4.tcp_low_latency": "1",
                "net.ipv4.tcp_fastopen": "3",
                "net.core.netdev_max_backlog": "5000",
                "net.ipv4.tcp_no_metrics_save": "1",
                "net.ipv4.tcp_timestamps": "1",
                "net.ipv4.tcp_sack": "1",
                "net.ipv4.tcp_congestion_control": "bbr",  # If available
            }
        },
        
        "high_throughput": {
            "description": "Optimized for high bandwidth (downloads, streaming)",
            "params": {
                "net.core.rmem_max": "134217728",  # 128MB
                "net.core.wmem_max": "134217728",
                "net.ipv4.tcp_rmem": "4096 87380 67108864",  # min default max
                "net.ipv4.tcp_wmem": "4096 65536 67108864",
                "net.core.netdev_max_backlog": "250000",
                "net.ipv4.tcp_congestion_control": "cubic",
                "net.ipv4.tcp_mtu_probing": "1",
            }
        },
        
        "server": {
            "description": "Optimized for server workloads",
            "params": {
                "net.core.somaxconn": "4096",
                "net.core.netdev_max_backlog": "10000",
                "net.ipv4.tcp_max_syn_backlog": "8192",
                "net.ipv4.tcp_tw_reuse": "1",
                "net.ipv4.tcp_fin_timeout": "15",
                "net.ipv4.ip_local_port_range": "1024 65535",
                "net.ipv4.tcp_keepalive_time": "300",
                "net.ipv4.tcp_keepalive_probes": "5",
                "net.ipv4.tcp_keepalive_intvl": "15",
            }
        },
        
        "wifi": {
            "description": "Optimized for WiFi connections",
            "params": {
                "net.ipv4.tcp_congestion_control": "bbr",
                "net.ipv4.tcp_fastopen": "3",
                "net.ipv4.tcp_mtu_probing": "1",
                "net.core.default_qdisc": "fq",  # Fair queuing
            }
        }
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Network Tuner
        
        Args:
            dry_run: If True, simulate changes
        """
        self.dry_run = dry_run
        
    def get_network_info(self) -> List[NetworkInfo]:
        """
        Get information about network interfaces
        
        Returns:
            List of NetworkInfo objects
        """
        interfaces = []
        
        try:
            # Get interface list
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True,
                check=True
            )
            
            current_iface = None
            
            for line in result.stdout.split('\n'):
                # New interface
                if line and not line.startswith(' '):
                    parts = line.split(':')
                    
                    if len(parts) >= 2:
                        iface_name = parts[1].strip()
                        state = "DOWN"
                        
                        if "state UP" in line:
                            state = "UP"
                        elif "state DOWN" in line:
                            state = "DOWN"
                            
                        # Get MTU
                        mtu = 1500
                        mtu_match = line.split("mtu ")
                        
                        if len(mtu_match) > 1:
                            try:
                                mtu = int(mtu_match[1].split()[0])
                            except ValueError:
                                pass
                                
                        current_iface = NetworkInfo(
                            interface=iface_name,
                            state=state,
                            mtu=mtu,
                            speed="",
                            driver=""
                        )
                        
                        interfaces.append(current_iface)
                        
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        return interfaces
        
    def get_current_settings(self) -> Dict[str, str]:
        """
        Get current network tuning settings
        
        Returns:
            Dict of parameter: value
        """
        settings = {}
        
        # Common parameters to check
        params = [
            "net.ipv4.tcp_congestion_control",
            "net.core.rmem_max",
            "net.core.wmem_max",
            "net.core.somaxconn",
            "net.ipv4.tcp_fastopen",
            "net.ipv4.tcp_tw_reuse",
        ]
        
        for param in params:
            try:
                result = subprocess.run(
                    ["sysctl", "-n", param],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                settings[param] = result.stdout.strip()
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                settings[param] = "unknown"
                
        return settings
        
    def apply_profile(self, profile: str = "low_latency") -> Dict[str, any]:
        """
        Apply network tuning profile
        
        Args:
            profile: Profile name (low_latency, high_throughput, server, wifi)
            
        Returns:
            Dict with results
        """
        if profile not in self.PROFILES:
            return {
                "success": False,
                "error": f"Unknown profile: {profile}"
            }
            
        profile_config = self.PROFILES[profile]
        params = profile_config["params"]
        
        applied = []
        failed = []
        
        for param, value in params.items():
            if self._set_parameter(param, value):
                applied.append(param)
            else:
                failed.append(param)
                
        return {
            "success": len(failed) == 0,
            "profile": profile,
            "description": profile_config["description"],
            "applied": applied,
            "failed": failed
        }
        
    def optimize_dns(self) -> Dict[str, any]:
        """
        Optimize DNS settings
        
        Returns:
            Dict with optimization results
        """
        # Common DNS optimizations
        recommendations = []
        
        # Check current DNS servers
        try:
            result = subprocess.run(
                ["cat", "/etc/resolv.conf"],
                capture_output=True,
                text=True
            )
            
            current_dns = []
            
            for line in result.stdout.split('\n'):
                if line.startswith('nameserver'):
                    dns = line.split()[1]
                    current_dns.append(dns)
                    
            recommendations.append({
                "current_dns": current_dns,
                "suggestion": "Consider using fast DNS servers like 1.1.1.1 (Cloudflare) or 8.8.8.8 (Google)"
            })
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        # Check if systemd-resolved is running
        try:
            subprocess.run(
                ["systemctl", "is-active", "systemd-resolved"],
                check=True,
                capture_output=True
            )
            
            recommendations.append({
                "systemd_resolved": "active",
                "suggestion": "systemd-resolved is active. Consider enabling DNS caching and DNSSEC."
            })
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            recommendations.append({
                "systemd_resolved": "inactive",
                "suggestion": "Consider enabling systemd-resolved for DNS caching."
            })
            
        return {
            "recommendations": recommendations
        }
        
    def test_latency(self, host: str = "8.8.8.8") -> Dict[str, any]:
        """
        Test network latency
        
        Args:
            host: Host to ping
            
        Returns:
            Dict with latency results
        """
        try:
            result = subprocess.run(
                ["ping", "-c", "10", host],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse statistics
            stats = {}
            
            for line in result.stdout.split('\n'):
                if "rtt min/avg/max/mdev" in line:
                    parts = line.split('=')[1].strip().split('/')
                    
                    if len(parts) >= 4:
                        stats = {
                            "min": float(parts[0]),
                            "avg": float(parts[1]),
                            "max": float(parts[2]),
                            "mdev": parts[3].split()[0]
                        }
                        
            return {
                "success": True,
                "host": host,
                "stats": stats
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return {
                "success": False,
                "host": host,
                "error": "Failed to ping host"
            }
            
    def get_congestion_algorithms(self) -> List[str]:
        """
        Get available TCP congestion control algorithms
        
        Returns:
            List of available algorithms
        """
        try:
            result = subprocess.run(
                ["sysctl", "-n", "net.ipv4.tcp_available_congestion_control"],
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip().split()
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
            
    def set_congestion_algorithm(self, algorithm: str) -> Dict[str, any]:
        """
        Set TCP congestion control algorithm
        
        Args:
            algorithm: Algorithm name (bbr, cubic, reno, etc.)
            
        Returns:
            Dict with results
        """
        available = self.get_congestion_algorithms()
        
        if algorithm not in available:
            return {
                "success": False,
                "error": f"Algorithm '{algorithm}' not available. Available: {', '.join(available)}"
            }
            
        if self._set_parameter("net.ipv4.tcp_congestion_control", algorithm):
            return {
                "success": True,
                "algorithm": algorithm
            }
        else:
            return {
                "success": False,
                "error": "Failed to set congestion algorithm"
            }
            
    def optimize_interface(
        self,
        interface: str,
        mtu: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Optimize network interface
        
        Args:
            interface: Interface name (e.g., eth0, wlan0)
            mtu: MTU size (or None for auto)
            
        Returns:
            Dict with results
        """
        if self.dry_run:
            return {
                "success": True,
                "interface": interface
            }
            
        # Set MTU if specified
        if mtu:
            try:
                subprocess.run(
                    ["sudo", "ip", "link", "set", interface, "mtu", str(mtu)],
                    check=True,
                    capture_output=True
                )
                
                return {
                    "success": True,
                    "interface": interface,
                    "mtu": mtu
                }
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                return {
                    "success": False,
                    "interface": interface,
                    "error": "Failed to set MTU"
                }
                
        return {
            "success": True,
            "interface": interface
        }
        
    # ==================== Private Helper Methods ====================
    
    def _set_parameter(self, param: str, value: str) -> bool:
        """Set network parameter via sysctl"""
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
