"""
🚀 OmniSystem Enhancer (OSE)
The All-in-One System Optimization & Factory Reset Suite

Version: 1.0.0-alpha
Author: OSE Development Team
License: MIT
"""

__version__ = "1.0.0-alpha"
__author__ = "OSE Development Team"
__description__ = "The All-in-One System Optimization & Factory Reset Suite"

# Core modules
from ose.core import orchestrator, state_manager, config_loader

# Feature modules
from ose import factory_reset, pkg_manager, quantum_backup, visual

__all__ = [
    "orchestrator",
    "state_manager", 
    "config_loader",
    "factory_reset",
    "pkg_manager",
    "quantum_backup",
    "visual",
]
