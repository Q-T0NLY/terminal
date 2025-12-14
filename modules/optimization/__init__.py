"""
⚡ OSE Optimization Module
System and terminal optimization with integrated modules

Includes:
- Optimization Service (4 profiles: conservative, balanced, aggressive, extreme)
- CPU Governor (frequency scaling, affinity, governor settings)
- Memory Optimizer (swappiness, cache pressure, huge pages)
- Network Tuner (TCP tuning, buffers, congestion control)
- Kernel Tuner (sysctl parameters, kernel modules)
- Startup Manager (boot time analysis, service optimization)
- Service Analyzer (unnecessary services, resource hogs)
"""

from cpu_governor import CPUGovernor
from memory_optimizer import MemoryOptimizer
from network_tuner import NetworkTuner
from kernel_tuner import KernelTuner
from startup_manager import StartupManager
from service_analyzer import ServiceAnalyzer

__all__ = [
    "CPUGovernor",
    "MemoryOptimizer",
    "NetworkTuner",
    "KernelTuner",
    "StartupManager",
    "ServiceAnalyzer",
]
