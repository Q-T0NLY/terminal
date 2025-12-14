"""
💾 Memory Optimizer
Optimize system memory usage and swap configuration
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """System memory information"""
    total: int  # bytes
    available: int  # bytes
    used: int  # bytes
    free: int  # bytes
    cached: int  # bytes
    swap_total: int  # bytes
    swap_used: int  # bytes
    swap_free: int  # bytes
    
    @property
    def usage_percent(self) -> float:
        """Memory usage percentage"""
        return (self.used / self.total) * 100 if self.total > 0 else 0
        
    @property
    def swap_usage_percent(self) -> float:
        """Swap usage percentage"""
        return (self.swap_used / self.swap_total) * 100 if self.swap_total > 0 else 0
        

class MemoryOptimizer:
    """
    Optimize system memory usage
    
    Features:
    - Memory analysis and reporting
    - Clear caches (page cache, dentries, inodes)
    - Swap optimization
    - zram configuration
    - Memory leak detection
    - OOM killer configuration
    """
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Memory Optimizer
        
        Args:
            dry_run: If True, simulate changes
        """
        self.dry_run = dry_run
        
    def get_memory_info(self) -> MemoryInfo:
        """
        Get current memory information
        
        Returns:
            MemoryInfo object
        """
        try:
            with open("/proc/meminfo", 'r') as f:
                meminfo = {}
                
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0].rstrip(':')
                        value = int(parts[1]) * 1024  # Convert KB to bytes
                        meminfo[key] = value
                        
            return MemoryInfo(
                total=meminfo.get('MemTotal', 0),
                available=meminfo.get('MemAvailable', 0),
                used=meminfo.get('MemTotal', 0) - meminfo.get('MemFree', 0) - meminfo.get('Buffers', 0) - meminfo.get('Cached', 0),
                free=meminfo.get('MemFree', 0),
                cached=meminfo.get('Cached', 0),
                swap_total=meminfo.get('SwapTotal', 0),
                swap_used=meminfo.get('SwapTotal', 0) - meminfo.get('SwapFree', 0),
                swap_free=meminfo.get('SwapFree', 0)
            )
            
        except (IOError, ValueError):
            return MemoryInfo(0, 0, 0, 0, 0, 0, 0, 0)
            
    def clear_caches(self, cache_type: str = "all") -> Dict[str, any]:
        """
        Clear system caches
        
        Args:
            cache_type: Type of cache to clear:
                       - "pagecache": Page cache only
                       - "dentries": Dentries and inodes
                       - "all": Everything
                       
        Returns:
            Dict with results
        """
        before = self.get_memory_info()
        
        if self.dry_run:
            return {
                "success": True,
                "cache_type": cache_type,
                "freed": 0
            }
            
        # Sync first to ensure data is written
        try:
            subprocess.run(["sync"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        # Clear caches
        cache_levels = {
            "pagecache": "1",
            "dentries": "2",
            "all": "3"
        }
        
        level = cache_levels.get(cache_type, "3")
        
        try:
            # Write to /proc/sys/vm/drop_caches
            subprocess.run(
                ["sudo", "sh", "-c", f"echo {level} > /proc/sys/vm/drop_caches"],
                check=True,
                capture_output=True
            )
            
            after = self.get_memory_info()
            freed = after.available - before.available
            
            return {
                "success": True,
                "cache_type": cache_type,
                "freed": freed
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "success": False,
                "cache_type": cache_type,
                "freed": 0,
                "error": "Failed to clear caches"
            }
            
    def configure_zram(
        self,
        enable: bool = True,
        size_mb: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Configure zram (compressed RAM swap)
        
        Args:
            enable: Whether to enable zram
            size_mb: Size in MB (defaults to 50% of RAM)
            
        Returns:
            Dict with results
        """
        if self.dry_run:
            return {
                "success": True,
                "enabled": enable,
                "size_mb": size_mb
            }
            
        if enable:
            # Calculate size
            if size_mb is None:
                mem_info = self.get_memory_info()
                size_mb = int((mem_info.total / (1024 * 1024)) * 0.5)
                
            try:
                # Load zram module
                subprocess.run(
                    ["sudo", "modprobe", "zram"],
                    check=True,
                    capture_output=True
                )
                
                # Set zram size
                subprocess.run(
                    ["sudo", "sh", "-c", f"echo {size_mb}M > /sys/block/zram0/disksize"],
                    check=True,
                    capture_output=True
                )
                
                # Format as swap
                subprocess.run(
                    ["sudo", "mkswap", "/dev/zram0"],
                    check=True,
                    capture_output=True
                )
                
                # Enable swap
                subprocess.run(
                    ["sudo", "swapon", "/dev/zram0"],
                    check=True,
                    capture_output=True
                )
                
                return {
                    "success": True,
                    "enabled": True,
                    "size_mb": size_mb
                }
                
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                return {
                    "success": False,
                    "enabled": False,
                    "error": str(e)
                }
                
        else:
            # Disable zram
            try:
                subprocess.run(
                    ["sudo", "swapoff", "/dev/zram0"],
                    check=True,
                    capture_output=True
                )
                
                subprocess.run(
                    ["sudo", "rmmod", "zram"],
                    check=True,
                    capture_output=True
                )
                
                return {
                    "success": True,
                    "enabled": False
                }
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                return {
                    "success": False,
                    "enabled": True,
                    "error": "Failed to disable zram"
                }
                
    def optimize_swap(self) -> Dict[str, any]:
        """
        Optimize swap configuration
        
        Returns:
            Dict with optimization results
        """
        mem_info = self.get_memory_info()
        
        # Recommendations
        recommendations = {
            "swappiness": 10,  # Low swap usage
            "cache_pressure": 50,  # Balanced cache pressure
        }
        
        # If lots of RAM (>16GB), reduce swappiness further
        if mem_info.total > 16 * 1024 * 1024 * 1024:
            recommendations["swappiness"] = 5
            
        # If low RAM (<4GB), increase swappiness
        if mem_info.total < 4 * 1024 * 1024 * 1024:
            recommendations["swappiness"] = 60
            
        applied = []
        
        for param, value in recommendations.items():
            full_param = f"vm.{param}"
            
            if not self.dry_run:
                try:
                    subprocess.run(
                        ["sudo", "sysctl", "-w", f"{full_param}={value}"],
                        check=True,
                        capture_output=True
                    )
                    applied.append(full_param)
                    
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            else:
                applied.append(full_param)
                
        return {
            "success": len(applied) > 0,
            "recommendations": recommendations,
            "applied": applied
        }
        
    def detect_memory_leaks(self) -> Dict[str, any]:
        """
        Detect potential memory leaks
        
        Returns:
            Dict with top memory-consuming processes
        """
        try:
            result = subprocess.run(
                ["ps", "aux", "--sort=-%mem"],
                capture_output=True,
                text=True,
                check=True
            )
            
            processes = []
            
            for line in result.stdout.split('\n')[1:11]:  # Top 10
                if not line.strip():
                    continue
                    
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append({
                        "user": parts[0],
                        "pid": parts[1],
                        "cpu": parts[2],
                        "mem": parts[3],
                        "command": parts[10]
                    })
                    
            return {
                "top_processes": processes
            }
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "top_processes": []
            }
            
    @staticmethod
    def format_bytes(bytes_val: int) -> str:
        """Format bytes into human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"
