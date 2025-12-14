"""
Feature Flags API Routes
Advanced feature toggles with gradual rollout and targeting
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/features", tags=["features"])

# ==================== DATA MODELS ====================

class FeatureStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"
    TESTING = "testing"

class RolloutStrategy(str, Enum):
    INSTANT = "instant"
    GRADUAL = "gradual"
    CANARY = "canary"
    BLUE_GREEN = "blue_green"
    AB_TEST = "ab_test"

class TargetingRule(BaseModel):
    attribute: str
    operator: str  # eq, ne, in, contains, gt, lt
    value: Any

class FeatureInfo(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    enabled: bool = False
    rollout_percentage: int = 0
    rollout_strategy: RolloutStrategy = RolloutStrategy.INSTANT
    targeting_rules: List[TargetingRule] = []
    metadata: Dict[str, Any] = {}

class FeatureCreate(BaseModel):
    name: str
    description: Optional[str] = None
    enabled: bool = False
    rollout_percentage: int = 0
    rollout_strategy: RolloutStrategy = RolloutStrategy.INSTANT
    targeting_rules: List[TargetingRule] = []

class FeatureUpdate(BaseModel):
    description: Optional[str] = None
    enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = None
    rollout_strategy: Optional[RolloutStrategy] = None
    targeting_rules: Optional[List[TargetingRule]] = None
    metadata: Optional[Dict[str, Any]] = None

class FeatureEvaluation(BaseModel):
    user_id: Optional[str] = None
    attributes: Dict[str, Any] = {}

# ==================== REGISTRY ====================

features_registry: Dict[str, Dict[str, Any]] = {}
feature_logs: Dict[str, List[Dict[str, Any]]] = {}
feature_stats: Dict[str, Dict[str, Any]] = {}

def log_feature_event(feature_id: str, level: str, message: str):
    """Log feature events"""
    if feature_id not in feature_logs:
        feature_logs[feature_id] = []
    
    feature_logs[feature_id].append({
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message
    })
    
    if len(feature_logs[feature_id]) > 1000:
        feature_logs[feature_id] = feature_logs[feature_id][-1000:]

def evaluate_targeting_rules(rules: List[Dict], attributes: Dict[str, Any]) -> bool:
    """Evaluate targeting rules against user attributes"""
    if not rules:
        return True
    
    for rule in rules:
        attr = rule.get("attribute")
        operator = rule.get("operator")
        value = rule.get("value")
        user_value = attributes.get(attr)
        
        if operator == "eq" and user_value != value:
            return False
        elif operator == "ne" and user_value == value:
            return False
        elif operator == "in" and user_value not in value:
            return False
        elif operator == "contains" and value not in str(user_value):
            return False
        elif operator == "gt" and not (user_value and user_value > value):
            return False
        elif operator == "lt" and not (user_value and user_value < value):
            return False
    
    return True

# ==================== CRUD OPERATIONS ====================

@router.get("/", summary="List all features")
async def list_features(
    enabled: Optional[bool] = Query(None),
    status: Optional[FeatureStatus] = Query(None)
):
    """List all feature flags"""
    result = list(features_registry.values())
    
    if enabled is not None:
        result = [f for f in result if f.get("enabled") == enabled]
    if status:
        result = [f for f in result if f.get("status") == status.value]
    
    return {
        "total": len(result),
        "features": result
    }

@router.post("/", summary="Create feature flag")
async def create_feature(feature: FeatureCreate):
    """Create a new feature flag"""
    feature_id = f"feat_{feature.name.lower().replace(' ', '-')}"
    
    if feature_id in features_registry:
        raise HTTPException(status_code=409, detail="Feature already exists")
    
    feature_data = feature.dict()
    feature_data["id"] = feature_id
    feature_data["status"] = FeatureStatus.DISABLED.value
    feature_data["created_at"] = datetime.utcnow().isoformat()
    feature_data["metadata"] = {}
    
    # Initialize stats
    feature_stats[feature_id] = {
        "evaluations": 0,
        "enabled_count": 0,
        "disabled_count": 0
    }
    
    features_registry[feature_id] = feature_data
    log_feature_event(feature_id, "INFO", f"Feature created: {feature.name}")
    
    return {
        "message": "Feature created successfully",
        "feature_id": feature_id,
        "feature": feature_data
    }

@router.get("/{feature_id}", summary="Get feature details")
async def get_feature(feature_id: str):
    """Get detailed feature information"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    return features_registry[feature_id]

@router.put("/{feature_id}", summary="Update feature")
async def update_feature(feature_id: str, update: FeatureUpdate):
    """Update feature configuration"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature = features_registry[feature_id]
    
    if update.description is not None:
        feature["description"] = update.description
    if update.enabled is not None:
        feature["enabled"] = update.enabled
        feature["status"] = FeatureStatus.ENABLED.value if update.enabled else FeatureStatus.DISABLED.value
    if update.rollout_percentage is not None:
        feature["rollout_percentage"] = max(0, min(100, update.rollout_percentage))
        if 0 < feature["rollout_percentage"] < 100:
            feature["status"] = FeatureStatus.ROLLOUT.value
    if update.rollout_strategy is not None:
        feature["rollout_strategy"] = update.rollout_strategy.value
    if update.targeting_rules is not None:
        feature["targeting_rules"] = [r.dict() for r in update.targeting_rules]
    if update.metadata:
        feature["metadata"].update(update.metadata)
    
    feature["updated_at"] = datetime.utcnow().isoformat()
    
    log_feature_event(feature_id, "INFO", "Feature updated")
    
    return {
        "message": "Feature updated",
        "feature": feature
    }

@router.delete("/{feature_id}", summary="Delete feature")
async def delete_feature(feature_id: str):
    """Delete a feature flag"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    log_feature_event(feature_id, "WARNING", "Feature deleted")
    del features_registry[feature_id]
    
    return {
        "message": "Feature deleted successfully",
        "feature_id": feature_id
    }

# ==================== OPERATIONS ====================

@router.post("/{feature_id}/enable", summary="Enable feature")
async def enable_feature(feature_id: str):
    """Enable a feature flag"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature = features_registry[feature_id]
    feature["enabled"] = True
    feature["status"] = FeatureStatus.ENABLED.value
    feature["enabled_at"] = datetime.utcnow().isoformat()
    
    log_feature_event(feature_id, "INFO", "Feature enabled")
    
    return {
        "message": "Feature enabled",
        "feature": feature
    }

@router.post("/{feature_id}/disable", summary="Disable feature")
async def disable_feature(feature_id: str):
    """Disable a feature flag"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature = features_registry[feature_id]
    feature["enabled"] = False
    feature["status"] = FeatureStatus.DISABLED.value
    feature["disabled_at"] = datetime.utcnow().isoformat()
    
    log_feature_event(feature_id, "INFO", "Feature disabled")
    
    return {
        "message": "Feature disabled",
        "feature": feature
    }

@router.post("/{feature_id}/rollout", summary="Configure rollout")
async def configure_rollout(
    feature_id: str,
    percentage: int = Query(..., ge=0, le=100),
    strategy: RolloutStrategy = RolloutStrategy.GRADUAL
):
    """Configure gradual rollout"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature = features_registry[feature_id]
    feature["rollout_percentage"] = percentage
    feature["rollout_strategy"] = strategy.value
    
    if percentage == 100:
        feature["status"] = FeatureStatus.ENABLED.value
        feature["enabled"] = True
    elif percentage == 0:
        feature["status"] = FeatureStatus.DISABLED.value
        feature["enabled"] = False
    else:
        feature["status"] = FeatureStatus.ROLLOUT.value
    
    log_feature_event(feature_id, "INFO", f"Rollout configured: {percentage}% - {strategy.value}")
    
    return {
        "message": "Rollout configured",
        "feature": feature
    }

@router.post("/{feature_id}/evaluate", summary="Evaluate feature")
async def evaluate_feature(feature_id: str, evaluation: FeatureEvaluation):
    """Evaluate if feature is enabled for user/context"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    feature = features_registry[feature_id]
    stats = feature_stats[feature_id]
    stats["evaluations"] += 1
    
    # Check if feature is globally disabled
    if not feature.get("enabled", False):
        stats["disabled_count"] += 1
        return {
            "feature_id": feature_id,
            "enabled": False,
            "reason": "feature_disabled"
        }
    
    # Check targeting rules
    rules = feature.get("targeting_rules", [])
    if not evaluate_targeting_rules(rules, evaluation.attributes):
        stats["disabled_count"] += 1
        return {
            "feature_id": feature_id,
            "enabled": False,
            "reason": "targeting_rules_not_met"
        }
    
    # Check rollout percentage
    rollout_pct = feature.get("rollout_percentage", 100)
    if rollout_pct < 100:
        # Simple hash-based rollout (in production, use consistent hashing)
        user_id = evaluation.user_id or "anonymous"
        hash_val = hash(user_id) % 100
        if hash_val >= rollout_pct:
            stats["disabled_count"] += 1
            return {
                "feature_id": feature_id,
                "enabled": False,
                "reason": "rollout_percentage",
                "rollout_percentage": rollout_pct
            }
    
    stats["enabled_count"] += 1
    return {
        "feature_id": feature_id,
        "enabled": True,
        "reason": "enabled"
    }

# ==================== STATISTICS ====================

@router.get("/stats/overview", summary="Features statistics")
async def get_features_overview():
    """Get comprehensive features statistics"""
    stats = {
        "total_features": len(features_registry),
        "enabled": 0,
        "disabled": 0,
        "in_rollout": 0,
        "total_evaluations": 0
    }
    
    for feature in features_registry.values():
        status = feature.get("status")
        if status == FeatureStatus.ENABLED.value:
            stats["enabled"] += 1
        elif status == FeatureStatus.DISABLED.value:
            stats["disabled"] += 1
        elif status == FeatureStatus.ROLLOUT.value:
            stats["in_rollout"] += 1
        
        feat_stats = feature_stats.get(feature["id"], {})
        stats["total_evaluations"] += feat_stats.get("evaluations", 0)
    
    return stats

@router.get("/{feature_id}/stats", summary="Get feature statistics")
async def get_feature_stats(feature_id: str):
    """Get detailed feature statistics"""
    if feature_id not in features_registry:
        raise HTTPException(status_code=404, detail="Feature not found")
    
    return {
        "feature_id": feature_id,
        "stats": feature_stats.get(feature_id, {})
    }
