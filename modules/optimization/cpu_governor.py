"""
⚡ CPU Governor
Manage CPU frequency scaling and power management
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class CPUInfo:
    """CPU information"""
    cpu_id: int
    current_freq: int  # MHz
    min_freq: int  # MHz
    max_freq: int  # MHz
    governor: str
    driver: str
    available_governors: List[str]
    

class CPUGovernor:
    """
    Manage CPU frequency scaling
    
    Features:
    - List available governors
    - Change CPU governor (performance, powersave, ondemand, etc.)
    - Set CPU frequencies
    - Profile-based tuning (performance, balanced, powersave)
    - Per-core configuration
    
    Available governors:
    - performance: Maximum frequency always
    - powersave: Minimum frequency always
    - ondemand: Dynamic scaling based on load
    - conservative: Gradual scaling
    - schedutil: Scheduler-based scaling (modern kernels)
    """
    
    PROFILES = {
        "performance": {
            "governor": "performance",
            "description": "Maximum performance, highest power usage"
        },
        
        "balanced": {
            "governor": "ondemand",  # or schedutil
            "description": "Balance performance and power"
        },
        
        "powersave": {
            "governor": "powersave",
            "description": "Maximum battery life, lower performance"
        },
        
        "gaming": {
            "governor": "performance",
            "description": "Optimized for gaming (high performance)"
        }
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize CPU Governor
        
        Args:
            dry_run: If True, simulate changes
        """
        self.dry_run = dry_run
        self.sysfs_cpu = Path("/sys/devices/system/cpu")
        
    def get_cpu_info(self) -> List[CPUInfo]:
        """
        Get information about all CPUs
        
        Returns:
            List of CPUInfo objects
        """
        cpus = []
        
        # Find all CPU directories
        cpu_dirs = sorted(self.sysfs_cpu.glob("cpu[0-9]*"))
        
        for cpu_dir in cpu_dirs:
            cpu_id = int(cpu_dir.name.replace("cpu", ""))
            
            cpufreq_dir = cpu_dir / "cpufreq"
            
            if not cpufreq_dir.exists():
                continue
                
            try:
                # Read frequency information
                current_freq = self._read_sysfs(cpufreq_dir / "scaling_cur_freq")
                min_freq = self._read_sysfs(cpufreq_dir / "scaling_min_freq")
                max_freq = self._read_sysfs(cpufreq_dir / "scaling_max_freq")
                governor = self._read_sysfs(cpufreq_dir / "scaling_governor", as_int=False).strip()
                driver = self._read_sysfs(cpufreq_dir / "scaling_driver", as_int=False).strip()
                
                # Read available governors
                available_gov_file = cpufreq_dir / "scaling_available_governors"
                available_governors = []
                
                if available_gov_file.exists():
                    available_governors = available_gov_file.read_text().strip().split()
                    
                cpus.append(CPUInfo(
                    cpu_id=cpu_id,
                    current_freq=current_freq // 1000,  # Convert kHz to MHz
                    min_freq=min_freq // 1000,
                    max_freq=max_freq // 1000,
                    governor=governor,
                    driver=driver,
                    available_governors=available_governors
                ))
                
            except (IOError, ValueError):
                continue
                
        return cpus
        
    def set_governor(
        self,
        governor: str,
        cpu_id: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Set CPU governor
        
        Args:
            governor: Governor name (performance, powersave, ondemand, etc.)
            cpu_id: Specific CPU ID, or None for all CPUs
            
        Returns:
            Dict with results
        """
        cpus = self.get_cpu_info()
        
        if not cpus:
            return {
                "success": False,
                "error": "No CPUs found or cpufreq not available"
            }
            
        # Validate governor
        available_governors = cpus[0].available_governors
        
        if governor not in available_governors:
            return {
                "success": False,
                "error": f"Governor '{governor}' not available. Available: {', '.join(available_governors)}"
            }
            
        # Set governor
        if cpu_id is not None:
            # Specific CPU
            result = self._set_cpu_governor(cpu_id, governor)
            
            return {
                "success": result,
                "cpu_id": cpu_id,
                "governor": governor
            }
            
        else:
            # All CPUs
            success_count = 0
            
            for cpu in cpus:
                if self._set_cpu_governor(cpu.cpu_id, governor):
                    success_count += 1
                    
            return {
                "success": success_count == len(cpus),
                "governor": governor,
                "affected_cpus": success_count,
                "total_cpus": len(cpus)
            }
            
    def apply_profile(self, profile: str = "balanced") -> Dict[str, any]:
        """
        Apply CPU tuning profile
        
        Args:
            profile: Profile name (performance, balanced, powersave, gaming)
            
        Returns:
            Dict with results
        """
        if profile not in self.PROFILES:
            return {
                "success": False,
                "error": f"Unknown profile: {profile}. Available: {', '.join(self.PROFILES.keys())}"
            }
            
        profile_config = self.PROFILES[profile]
        governor = profile_config["governor"]
        
        # Check if schedutil is available for balanced mode
        cpus = self.get_cpu_info()
        
        if cpus and profile == "balanced":
            if "schedutil" in cpus[0].available_governors:
                governor = "schedutil"  # Prefer schedutil over ondemand
                
        result = self.set_governor(governor)
        result["profile"] = profile
        result["description"] = profile_config["description"]
        
        return result
        
    def get_current_profile(self) -> Optional[str]:
        """
        Detect current profile based on governor
        
        Returns:
            Profile name or None
        """
        cpus = self.get_cpu_info()
        
        if not cpus:
            return None
            
        current_governor = cpus[0].governor
        
        for profile, config in self.PROFILES.items():
            if config["governor"] == current_governor:
                return profile
                
            # Handle schedutil as balanced
            if current_governor == "schedutil" and profile == "balanced":
                return profile
                
        return None
        
    def benchmark_governors(self) -> Dict[str, any]:
        """
        Benchmark different governors (requires cpufreq-bench)
        
        Returns:
            Dict with benchmark results
        """
        # This is a placeholder - actual benchmarking would require
        # cpufreq-bench or similar tool
        
        return {
            "note": "Governor benchmarking requires additional tools",
            "recommendation": "Use 'cpufreq-bench' for detailed benchmarking"
        }
        
    # ==================== Private Helper Methods ====================
    
    def _read_sysfs(
        self,
        path: Path,
        as_int: bool = True
    ) -> any:
        """Read value from sysfs file"""
        try:
            content = path.read_text().strip()
            
            if as_int:
                return int(content)
            else:
                return content
                
        except (IOError, ValueError):
            return 0 if as_int else ""
            
    def _set_cpu_governor(self, cpu_id: int, governor: str) -> bool:
        """Set governor for specific CPU"""
        if self.dry_run:
            return True
            
        governor_file = self.sysfs_cpu / f"cpu{cpu_id}" / "cpufreq" / "scaling_governor"
        
        try:
            # Try direct write first
            subprocess.run(
                ["sudo", "sh", "-c", f"echo {governor} > {governor_file}"],
                check=True,
                capture_output=True
            )
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try cpufreq-set as fallback
            try:
                subprocess.run(
                    ["sudo", "cpufreq-set", "-c", str(cpu_id), "-g", governor],
                    check=True,
                    capture_output=True
                )
                return True
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
