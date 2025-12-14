"""
Configuration Management API Routes
System-wide settings with validation, encryption, and versioning
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/config", tags=["configuration"])

# ==================== DATA MODELS ====================

class ConfigType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    JSON = "json"
    SECRET = "secret"

class ConfigScope(str, Enum):
    GLOBAL = "global"
    SERVICE = "service"
    ENVIRONMENT = "environment"
    USER = "user"

class ConfigEntry(BaseModel):
    key: str
    value: Any
    type: ConfigType = ConfigType.STRING
    scope: ConfigScope = ConfigScope.GLOBAL
    description: Optional[str] = None
    encrypted: bool = False
    metadata: Dict[str, Any] = {}

class ConfigSet(BaseModel):
    key: str
    value: Any
    type: Optional[ConfigType] = ConfigType.STRING
    scope: Optional[ConfigScope] = ConfigScope.GLOBAL
    description: Optional[str] = None
    encrypt: bool = False

class ConfigValidation(BaseModel):
    required: bool = False
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    allowed_values: Optional[List[Any]] = None
    pattern: Optional[str] = None

# ==================== REGISTRY ====================

config_registry: Dict[str, Dict[str, Any]] = {}
config_history: Dict[str, List[Dict[str, Any]]] = {}
config_schemas: Dict[str, ConfigValidation] = {}

# Default configurations
default_configs = {
    "system.log_level": {"value": "INFO", "type": "string", "scope": "global"},
    "system.max_connections": {"value": 1000, "type": "integer", "scope": "global"},
    "api.rate_limit": {"value": 100, "type": "integer", "scope": "global"},
    "api.timeout": {"value": 30, "type": "integer", "scope": "global"},
    "security.encryption_enabled": {"value": True, "type": "boolean", "scope": "global"}
}

def initialize_defaults():
    """Initialize default configurations"""
    for key, config in default_configs.items():
        if key not in config_registry:
            config_registry[key] = {
                "key": key,
                "value": config["value"],
                "type": config["type"],
                "scope": config["scope"],
                "description": f"Default configuration for {key}",
                "encrypted": False,
                "created_at": datetime.utcnow().isoformat(),
                "metadata": {}
            }

initialize_defaults()

def log_config_change(key: str, old_value: Any, new_value: Any, user: str = "system"):
    """Log configuration changes"""
    if key not in config_history:
        config_history[key] = []
    
    config_history[key].append({
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "old_value": old_value,
        "new_value": new_value
    })
    
    if len(config_history[key]) > 100:
        config_history[key] = config_history[key][-100:]

def validate_config_value(key: str, value: Any) -> bool:
    """Validate configuration value against schema"""
    if key not in config_schemas:
        return True
    
    schema = config_schemas[key]
    
    if schema.required and value is None:
        return False
    
    if schema.min_value is not None and value < schema.min_value:
        return False
    
    if schema.max_value is not None and value > schema.max_value:
        return False
    
    if schema.allowed_values and value not in schema.allowed_values:
        return False
    
    if schema.pattern:
        import re
        if not re.match(schema.pattern, str(value)):
            return False
    
    return True

def encrypt_value(value: Any) -> str:
    """Encrypt sensitive value (simplified - use proper encryption in production)"""
    import base64
    return base64.b64encode(json.dumps(value).encode()).decode()

def decrypt_value(encrypted: str) -> Any:
    """Decrypt encrypted value"""
    import base64
    return json.loads(base64.b64decode(encrypted.encode()).decode())

# ==================== CONFIG OPERATIONS ====================

@router.get("/", summary="List all configurations")
async def list_configs(
    scope: Optional[ConfigScope] = Query(None),
    type: Optional[ConfigType] = Query(None),
    prefix: Optional[str] = Query(None)
):
    """List all configuration entries"""
    result = list(config_registry.values())
    
    if scope:
        result = [c for c in result if c.get("scope") == scope.value]
    if type:
        result = [c for c in result if c.get("type") == type.value]
    if prefix:
        result = [c for c in result if c.get("key", "").startswith(prefix)]
    
    # Mask encrypted values
    for config in result:
        if config.get("encrypted"):
            config["value"] = "***ENCRYPTED***"
    
    return {
        "total": len(result),
        "configs": result
    }

@router.get("/{key:path}", summary="Get configuration value")
async def get_config(key: str, decrypt: bool = Query(False)):
    """Get a specific configuration value"""
    if key not in config_registry:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config = config_registry[key].copy()
    
    if config.get("encrypted"):
        if decrypt:
            config["value"] = decrypt_value(config["value"])
        else:
            config["value"] = "***ENCRYPTED***"
    
    return config

@router.post("/", summary="Set configuration")
async def set_config(config: ConfigSet):
    """Set a configuration value"""
    # Validate value
    if not validate_config_value(config.key, config.value):
        raise HTTPException(status_code=400, detail="Configuration value failed validation")
    
    old_value = None
    if config.key in config_registry:
        old_value = config_registry[config.key].get("value")
    
    value = config.value
    encrypted = config.encrypt
    
    # Encrypt if requested
    if encrypted:
        value = encrypt_value(config.value)
    
    config_data = {
        "key": config.key,
        "value": value,
        "type": config.type.value,
        "scope": config.scope.value,
        "description": config.description or f"Configuration for {config.key}",
        "encrypted": encrypted,
        "updated_at": datetime.utcnow().isoformat(),
        "metadata": {}
    }
    
    if config.key not in config_registry:
        config_data["created_at"] = datetime.utcnow().isoformat()
    
    config_registry[config.key] = config_data
    log_config_change(config.key, old_value, config.value)
    
    return {
        "message": "Configuration set successfully",
        "key": config.key,
        "config": config_data
    }

@router.put("/{key:path}", summary="Update configuration")
async def update_config(key: str, value: Any):
    """Update configuration value"""
    if key not in config_registry:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Validate value
    if not validate_config_value(key, value):
        raise HTTPException(status_code=400, detail="Configuration value failed validation")
    
    config = config_registry[key]
    old_value = config.get("value")
    
    # Encrypt if original was encrypted
    if config.get("encrypted"):
        value = encrypt_value(value)
    
    config["value"] = value
    config["updated_at"] = datetime.utcnow().isoformat()
    
    log_config_change(key, old_value, value)
    
    return {
        "message": "Configuration updated",
        "key": key,
        "config": config
    }

@router.delete("/{key:path}", summary="Delete configuration")
async def delete_config(key: str):
    """Delete a configuration entry"""
    if key not in config_registry:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Prevent deleting default configs
    if key in default_configs:
        raise HTTPException(status_code=400, detail="Cannot delete default configuration")
    
    old_value = config_registry[key].get("value")
    del config_registry[key]
    
    log_config_change(key, old_value, None)
    
    return {
        "message": "Configuration deleted",
        "key": key
    }

@router.post("/{key:path}/reset", summary="Reset to default")
async def reset_config(key: str):
    """Reset configuration to default value"""
    if key not in default_configs:
        raise HTTPException(status_code=404, detail="No default value defined for this configuration")
    
    default = default_configs[key]
    old_value = config_registry.get(key, {}).get("value")
    
    config_registry[key] = {
        "key": key,
        "value": default["value"],
        "type": default["type"],
        "scope": default["scope"],
        "description": f"Default configuration for {key}",
        "encrypted": False,
        "updated_at": datetime.utcnow().isoformat(),
        "metadata": {}
    }
    
    log_config_change(key, old_value, default["value"], "system_reset")
    
    return {
        "message": "Configuration reset to default",
        "key": key,
        "config": config_registry[key]
    }

# ==================== SCHEMA MANAGEMENT ====================

@router.post("/schema/{key:path}", summary="Define configuration schema")
async def set_config_schema(key: str, validation: ConfigValidation):
    """Define validation schema for a configuration key"""
    config_schemas[key] = validation
    
    return {
        "message": "Configuration schema defined",
        "key": key,
        "schema": validation.dict()
    }

@router.get("/schema/{key:path}", summary="Get configuration schema")
async def get_config_schema(key: str):
    """Get validation schema for a configuration key"""
    if key not in config_schemas:
        raise HTTPException(status_code=404, detail="Schema not found")
    
    return {
        "key": key,
        "schema": config_schemas[key].dict()
    }

# ==================== BULK OPERATIONS ====================

@router.post("/import", summary="Import configurations")
async def import_configs(configs: List[ConfigSet]):
    """Bulk import configurations"""
    imported = []
    errors = []
    
    for config in configs:
        try:
            result = await set_config(config)
            imported.append(config.key)
        except Exception as e:
            errors.append({"key": config.key, "error": str(e)})
    
    return {
        "message": f"Imported {len(imported)} configurations",
        "imported": imported,
        "errors": errors
    }

@router.get("/export", summary="Export configurations")
async def export_configs(
    scope: Optional[ConfigScope] = Query(None),
    include_encrypted: bool = Query(False)
):
    """Export all configurations as JSON"""
    result = list(config_registry.values())
    
    if scope:
        result = [c for c in result if c.get("scope") == scope.value]
    
    if not include_encrypted:
        result = [c for c in result if not c.get("encrypted")]
    
    return {
        "total": len(result),
        "configs": result,
        "exported_at": datetime.utcnow().isoformat()
    }

# ==================== HISTORY ====================

@router.get("/{key:path}/history", summary="Get configuration history")
async def get_config_history(key: str, limit: int = Query(10, ge=1, le=100)):
    """Get change history for a configuration key"""
    if key not in config_registry:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    history = config_history.get(key, [])
    
    return {
        "key": key,
        "total_changes": len(history),
        "history": history[-limit:]
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Configuration statistics")
async def get_config_overview():
    """Get comprehensive configuration statistics"""
    stats = {
        "total_configs": len(config_registry),
        "by_scope": {},
        "by_type": {},
        "encrypted_count": 0,
        "total_changes": 0
    }
    
    for config in config_registry.values():
        scope = config.get("scope", "unknown")
        stats["by_scope"][scope] = stats["by_scope"].get(scope, 0) + 1
        
        ctype = config.get("type", "unknown")
        stats["by_type"][ctype] = stats["by_type"].get(ctype, 0) + 1
        
        if config.get("encrypted"):
            stats["encrypted_count"] += 1
    
    for history in config_history.values():
        stats["total_changes"] += len(history)
    
    return stats
