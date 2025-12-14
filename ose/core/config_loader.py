"""
⚙️ OSE Config Loader
YAML-based configuration management
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CleanupConfig:
    """Cleanup module configuration"""
    enable_cache_cleanup: bool = True
    enable_temp_cleanup: bool = True
    enable_log_cleanup: bool = True
    enable_duplicate_detection: bool = True
    
    cache_max_age_days: int = 30
    log_max_age_days: int = 90
    temp_max_age_hours: int = 24
    
    exclude_patterns: list = None
    
    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = []


@dataclass
class OptimizeConfig:
    """Optimization module configuration"""
    enable_startup_management: bool = True
    enable_kernel_tuning: bool = False  # Requires explicit enable
    enable_memory_optimization: bool = True
    enable_service_management: bool = True
    
    target_boot_time: int = 15  # seconds
    max_startup_apps: int = 5
    
    kernel_params: dict = None
    
    def __post_init__(self):
        if self.kernel_params is None:
            self.kernel_params = {
                "vm.swappiness": 10,
                "vm.vfs_cache_pressure": 50
            }


@dataclass
class FactoryResetConfig:
    """Factory reset module configuration"""
    enable_package_removal: bool = True
    enable_config_purge: bool = True
    enable_user_data_wipe: bool = False  # Requires explicit enable
    
    keep_packages: list = None
    keep_configs: list = None
    
    def __post_init__(self):
        if self.keep_packages is None:
            self.keep_packages = []
        if self.keep_configs is None:
            self.keep_configs = []


@dataclass
class BackupConfig:
    """Quantum Backup configuration"""
    backup_location: str = "~/.ose/backups"
    compression_level: int = 6  # 0-9
    max_backups: int = 5
    enable_cloud_sync: bool = False
    
    
@dataclass
class VisualConfig:
    """Visual interface configuration"""
    enable_3d: bool = True
    enable_animations: bool = True
    enable_particles: bool = True
    
    theme: str = "dark"  # dark, light, neon
    fps_target: int = 60
    

class ConfigLoader:
    """
    Loads and manages OSE configuration from YAML files
    
    Supports:
    - Default configuration
    - User overrides
    - Environment-specific settings
    """
    
    DEFAULT_CONFIG = {
        "cleanup": {
            "enable_cache_cleanup": True,
            "enable_temp_cleanup": True,
            "enable_log_cleanup": True,
            "enable_duplicate_detection": True,
            "cache_max_age_days": 30,
            "log_max_age_days": 90,
            "temp_max_age_hours": 24,
            "exclude_patterns": []
        },
        "optimize": {
            "enable_startup_management": True,
            "enable_kernel_tuning": False,
            "enable_memory_optimization": True,
            "enable_service_management": True,
            "target_boot_time": 15,
            "max_startup_apps": 5,
            "kernel_params": {
                "vm.swappiness": 10,
                "vm.vfs_cache_pressure": 50
            }
        },
        "factory_reset": {
            "enable_package_removal": True,
            "enable_config_purge": True,
            "enable_user_data_wipe": False,
            "keep_packages": [],
            "keep_configs": []
        },
        "backup": {
            "backup_location": "~/.ose/backups",
            "compression_level": 6,
            "max_backups": 5,
            "enable_cloud_sync": False
        },
        "visual": {
            "enable_3d": True,
            "enable_animations": True,
            "enable_particles": True,
            "theme": "dark",
            "fps_target": 60
        },
        "safety": {
            "ultra_paranoid_mode": False,
            "require_confirmation": True,
            "enable_dry_run": True,
            "create_emergency_usb": False
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize Config Loader
        
        Args:
            config_path: Path to config file (uses default if None)
        """
        if config_path is None:
            config_path = Path.home() / ".ose" / "config" / "ose.yaml"
            
        self.config_path = config_path
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        
        # Load user config if exists
        if self.config_path.exists():
            self._load_config()
        else:
            # Create default config file
            self._create_default_config()
            
    def _load_config(self):
        """Load configuration from YAML file"""
        with open(self.config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            
        # Merge with defaults (user config overrides defaults)
        if user_config:
            self._deep_merge(self.config, user_config)
            
    def _create_default_config(self):
        """Create default configuration file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(
                self.DEFAULT_CONFIG,
                f,
                default_flow_style=False,
                sort_keys=False
            )
            
    def _deep_merge(self, base: dict, override: dict):
        """Recursively merge override into base"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
                
    def get_cleanup_config(self) -> CleanupConfig:
        """Get cleanup module configuration"""
        cfg = self.config["cleanup"]
        return CleanupConfig(**cfg)
        
    def get_optimize_config(self) -> OptimizeConfig:
        """Get optimization module configuration"""
        cfg = self.config["optimize"]
        return OptimizeConfig(**cfg)
        
    def get_factory_reset_config(self) -> FactoryResetConfig:
        """Get factory reset module configuration"""
        cfg = self.config["factory_reset"]
        return FactoryResetConfig(**cfg)
        
    def get_backup_config(self) -> BackupConfig:
        """Get backup module configuration"""
        cfg = self.config["backup"]
        return BackupConfig(**cfg)
        
    def get_visual_config(self) -> VisualConfig:
        """Get visual interface configuration"""
        cfg = self.config["visual"]
        return VisualConfig(**cfg)
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key
        
        Example: config.get("cleanup.cache_max_age_days")
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """
        Set configuration value by dot-notation key
        
        Example: config.set("cleanup.cache_max_age_days", 60)
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        
    def save(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(
                self.config,
                f,
                default_flow_style=False,
                sort_keys=False
            )
