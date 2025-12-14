"""
Universal API Gateway with Authentication & Key Rotation
Comprehensive gateway management for all API routes
"""

from fastapi import APIRouter, HTTPException, Depends, Header, Security
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import secrets
import hashlib
import jwt
import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
API_KEY_EXPIRE_DAYS = 90

# ==================== DATA MODELS ====================

class KeyType(str, Enum):
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    SERVICE_KEY = "service_key"
    ADMIN_KEY = "admin_key"

class KeyStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    ROTATING = "rotating"

class Permission(str, Enum):
    # Read permissions
    READ_PLUGINS = "read:plugins"
    READ_SERVICES = "read:services"
    READ_METRICS = "read:metrics"
    READ_STREAMS = "read:streams"
    
    # Write permissions
    WRITE_PLUGINS = "write:plugins"
    WRITE_SERVICES = "write:services"
    WRITE_CONFIG = "write:config"
    
    # Admin permissions
    ADMIN_KEYS = "admin:keys"
    ADMIN_USERS = "admin:users"
    ADMIN_SYSTEM = "admin:system"

class APIKey(BaseModel):
    id: str
    name: str
    key_type: KeyType
    key_hash: str
    permissions: List[Permission]
    status: KeyStatus
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    usage_count: int = 0
    rate_limit: int = 1000  # requests per hour
    metadata: Dict[str, Any] = {}

class KeyCreateRequest(BaseModel):
    name: str
    key_type: KeyType
    permissions: List[Permission]
    expires_in_days: Optional[int] = 90
    rate_limit: Optional[int] = 1000
    metadata: Dict[str, Any] = {}

class KeyRotationRequest(BaseModel):
    key_id: str
    grace_period_hours: int = 24

class TokenPayload(BaseModel):
    sub: str  # subject (user/service ID)
    permissions: List[str]
    exp: int  # expiration timestamp
    iat: int  # issued at
    type: str  # token type

# ==================== KEY STORAGE ====================

# In-memory key storage (use Redis/database in production)
api_keys: Dict[str, APIKey] = {}
key_usage_stats: Dict[str, List[float]] = defaultdict(list)  # key_id -> timestamps
rotating_keys: Dict[str, Dict[str, Any]] = {}  # old_key -> rotation info

# Rate limiting
rate_limit_buckets: Dict[str, List[float]] = defaultdict(list)

# ==================== SECURITY FUNCTIONS ====================

def hash_key(key: str) -> str:
    """Hash API key for secure storage"""
    return hashlib.sha256(key.encode()).hexdigest()

def generate_api_key() -> str:
    """Generate secure random API key"""
    return f"ureg_{secrets.token_urlsafe(32)}"

def generate_service_key() -> str:
    """Generate service-specific key"""
    return f"svc_{secrets.token_urlsafe(32)}"

def generate_admin_key() -> str:
    """Generate admin key with enhanced security"""
    return f"admin_{secrets.token_urlsafe(48)}"

def create_jwt_token(payload: TokenPayload) -> str:
    """Create JWT token"""
    return jwt.encode(payload.dict(), SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> TokenPayload:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_rate_limit(key_id: str, limit: int) -> bool:
    """Check if request is within rate limit"""
    now = time.time()
    hour_ago = now - 3600
    
    # Clean old timestamps
    rate_limit_buckets[key_id] = [
        ts for ts in rate_limit_buckets[key_id] if ts > hour_ago
    ]
    
    # Check limit
    if len(rate_limit_buckets[key_id]) >= limit:
        return False
    
    # Add current request
    rate_limit_buckets[key_id].append(now)
    return True

def verify_api_key(key: str) -> APIKey:
    """Verify API key and return key info"""
    key_hash = hash_key(key)
    
    # Find key by hash
    api_key = None
    for k in api_keys.values():
        if k.key_hash == key_hash:
            api_key = k
            break
    
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Check status
    if api_key.status != KeyStatus.ACTIVE:
        raise HTTPException(status_code=401, detail=f"API key is {api_key.status}")
    
    # Check expiration
    if api_key.expires_at and datetime.utcnow() > api_key.expires_at:
        api_key.status = KeyStatus.EXPIRED
        raise HTTPException(status_code=401, detail="API key expired")
    
    # Check rate limit
    if not check_rate_limit(api_key.id, api_key.rate_limit):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Update usage
    api_key.last_used = datetime.utcnow()
    api_key.usage_count += 1
    key_usage_stats[api_key.id].append(time.time())
    
    return api_key

def check_permission(api_key: APIKey, required_permission: Permission) -> bool:
    """Check if API key has required permission"""
    if required_permission in api_key.permissions:
        return True
    
    # Admin keys have all permissions
    if Permission.ADMIN_SYSTEM in api_key.permissions:
        return True
    
    return False

# ==================== DEPENDENCY INJECTION ====================

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)

async def get_api_key(
    api_key: Optional[str] = Security(api_key_header),
    bearer: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme)
) -> APIKey:
    """Extract and verify API key from request"""
    
    # Try API key header first
    if api_key:
        return verify_api_key(api_key)
    
    # Try Bearer token
    if bearer:
        token_payload = verify_jwt_token(bearer.credentials)
        # Convert JWT to APIKey format for consistency
        return APIKey(
            id=token_payload.sub,
            name=f"JWT-{token_payload.sub}",
            key_type=KeyType.JWT_TOKEN,
            key_hash="",
            permissions=[Permission(p) for p in token_payload.permissions],
            status=KeyStatus.ACTIVE,
            created_at=datetime.fromtimestamp(token_payload.iat),
            expires_at=datetime.fromtimestamp(token_payload.exp),
            last_used=datetime.utcnow(),
            usage_count=0,
            rate_limit=1000
        )
    
    raise HTTPException(status_code=401, detail="No valid authentication provided")

def require_permission(permission: Permission):
    """Dependency to require specific permission"""
    async def permission_checker(api_key: APIKey = Depends(get_api_key)) -> APIKey:
        if not check_permission(api_key, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {permission.value} required"
            )
        return api_key
    return permission_checker

# ==================== API ROUTES ====================

router = APIRouter(prefix="/api/v1/gateway", tags=["gateway"])

@router.post("/keys", summary="Create new API key")
async def create_key(
    request: KeyCreateRequest,
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """
    Create new API key with specified permissions.
    Requires ADMIN_KEYS permission.
    """
    
    # Generate key based on type
    if request.key_type == KeyType.ADMIN_KEY:
        raw_key = generate_admin_key()
    elif request.key_type == KeyType.SERVICE_KEY:
        raw_key = generate_service_key()
    else:
        raw_key = generate_api_key()
    
    # Create key object
    key_id = f"key_{secrets.token_hex(8)}"
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)
    
    api_key = APIKey(
        id=key_id,
        name=request.name,
        key_type=request.key_type,
        key_hash=hash_key(raw_key),
        permissions=request.permissions,
        status=KeyStatus.ACTIVE,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        last_used=None,
        usage_count=0,
        rate_limit=request.rate_limit or 1000,
        metadata=request.metadata
    )
    
    api_keys[key_id] = api_key
    
    logger.info(f"Created API key: {key_id} ({request.name})")
    
    return {
        "key_id": key_id,
        "api_key": raw_key,  # Only returned once!
        "name": request.name,
        "key_type": request.key_type,
        "permissions": request.permissions,
        "expires_at": expires_at,
        "rate_limit": api_key.rate_limit,
        "warning": "Save this key securely - it will not be shown again!"
    }

@router.get("/keys", summary="List all API keys")
async def list_keys(
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """List all API keys (without showing actual keys)"""
    return {
        "total": len(api_keys),
        "keys": [
            {
                "id": k.id,
                "name": k.name,
                "key_type": k.key_type,
                "status": k.status,
                "permissions": k.permissions,
                "created_at": k.created_at,
                "expires_at": k.expires_at,
                "last_used": k.last_used,
                "usage_count": k.usage_count,
                "rate_limit": k.rate_limit
            }
            for k in api_keys.values()
        ]
    }

@router.get("/keys/{key_id}", summary="Get key details")
async def get_key_details(
    key_id: str,
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """Get detailed information about a specific key"""
    if key_id not in api_keys:
        raise HTTPException(status_code=404, detail="Key not found")
    
    key = api_keys[key_id]
    usage_history = key_usage_stats.get(key_id, [])
    
    # Calculate usage stats
    now = time.time()
    hour_ago = now - 3600
    day_ago = now - 86400
    
    return {
        "id": key.id,
        "name": key.name,
        "key_type": key.key_type,
        "status": key.status,
        "permissions": key.permissions,
        "created_at": key.created_at,
        "expires_at": key.expires_at,
        "last_used": key.last_used,
        "usage_count": key.usage_count,
        "rate_limit": key.rate_limit,
        "metadata": key.metadata,
        "usage_stats": {
            "last_hour": len([t for t in usage_history if t > hour_ago]),
            "last_day": len([t for t in usage_history if t > day_ago]),
            "total": len(usage_history)
        }
    }

@router.post("/keys/{key_id}/rotate", summary="Rotate API key")
async def rotate_key(
    key_id: str,
    request: KeyRotationRequest,
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """
    Rotate API key with grace period.
    Old key remains valid for grace period.
    """
    if key_id not in api_keys:
        raise HTTPException(status_code=404, detail="Key not found")
    
    old_key = api_keys[key_id]
    
    # Generate new key
    if old_key.key_type == KeyType.ADMIN_KEY:
        new_raw_key = generate_admin_key()
    elif old_key.key_type == KeyType.SERVICE_KEY:
        new_raw_key = generate_service_key()
    else:
        new_raw_key = generate_api_key()
    
    # Create new key with same permissions
    new_key_id = f"key_{secrets.token_hex(8)}"
    new_key = APIKey(
        id=new_key_id,
        name=f"{old_key.name} (rotated)",
        key_type=old_key.key_type,
        key_hash=hash_key(new_raw_key),
        permissions=old_key.permissions,
        status=KeyStatus.ACTIVE,
        created_at=datetime.utcnow(),
        expires_at=old_key.expires_at,
        last_used=None,
        usage_count=0,
        rate_limit=old_key.rate_limit,
        metadata={**old_key.metadata, "rotated_from": key_id}
    )
    
    api_keys[new_key_id] = new_key
    
    # Mark old key as rotating
    old_key.status = KeyStatus.ROTATING
    grace_period_end = datetime.utcnow() + timedelta(hours=request.grace_period_hours)
    
    rotating_keys[key_id] = {
        "new_key_id": new_key_id,
        "grace_period_end": grace_period_end
    }
    
    logger.info(f"Rotated key {key_id} -> {new_key_id} (grace period: {request.grace_period_hours}h)")
    
    return {
        "old_key_id": key_id,
        "new_key_id": new_key_id,
        "new_api_key": new_raw_key,
        "grace_period_hours": request.grace_period_hours,
        "grace_period_end": grace_period_end,
        "warning": "Update your applications to use the new key before grace period ends!"
    }

@router.delete("/keys/{key_id}", summary="Revoke API key")
async def revoke_key(
    key_id: str,
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """Revoke API key immediately"""
    if key_id not in api_keys:
        raise HTTPException(status_code=404, detail="Key not found")
    
    api_keys[key_id].status = KeyStatus.REVOKED
    
    logger.warning(f"Revoked API key: {key_id}")
    
    return {
        "message": "API key revoked",
        "key_id": key_id
    }

@router.post("/tokens", summary="Create JWT token")
async def create_token(
    subject: str,
    permissions: List[Permission],
    expires_in_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    current_key: APIKey = Depends(require_permission(Permission.ADMIN_KEYS))
):
    """Create JWT token for authentication"""
    
    now = int(time.time())
    expires_at = now + (expires_in_minutes * 60)
    
    payload = TokenPayload(
        sub=subject,
        permissions=[p.value for p in permissions],
        exp=expires_at,
        iat=now,
        type="access"
    )
    
    token = create_jwt_token(payload)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in_minutes * 60,
        "expires_at": datetime.fromtimestamp(expires_at)
    }

@router.get("/stats", summary="Gateway statistics")
async def get_gateway_stats(
    current_key: APIKey = Depends(require_permission(Permission.READ_METRICS))
):
    """Get API gateway statistics"""
    
    now = time.time()
    hour_ago = now - 3600
    
    total_requests = sum(len(usage) for usage in key_usage_stats.values())
    active_keys = len([k for k in api_keys.values() if k.status == KeyStatus.ACTIVE])
    
    return {
        "total_keys": len(api_keys),
        "active_keys": active_keys,
        "rotating_keys": len(rotating_keys),
        "total_requests": total_requests,
        "requests_last_hour": sum(
            len([t for t in usage if t > hour_ago])
            for usage in key_usage_stats.values()
        ),
        "keys_by_type": {
            key_type: len([k for k in api_keys.values() if k.key_type == key_type])
            for key_type in KeyType
        },
        "keys_by_status": {
            status: len([k for k in api_keys.values() if k.status == status])
            for status in KeyStatus
        }
    }

@router.get("/permissions", summary="List available permissions")
async def list_permissions():
    """List all available permissions"""
    return {
        "permissions": [
            {
                "name": p.value,
                "category": p.value.split(":")[0],
                "resource": p.value.split(":")[1] if ":" in p.value else "unknown"
            }
            for p in Permission
        ]
    }

# ==================== ADMIN FUNCTIONS ====================

def initialize_admin_key():
    """Create initial admin key on startup"""
    admin_key = generate_admin_key()
    key_id = "admin_initial"
    
    api_key = APIKey(
        id=key_id,
        name="Initial Admin Key",
        key_type=KeyType.ADMIN_KEY,
        key_hash=hash_key(admin_key),
        permissions=list(Permission),  # All permissions
        status=KeyStatus.ACTIVE,
        created_at=datetime.utcnow(),
        expires_at=None,  # Never expires
        last_used=None,
        usage_count=0,
        rate_limit=10000,
        metadata={"initial": True}
    )
    
    api_keys[key_id] = api_key
    
    logger.info(f"="*60)
    logger.info(f"INITIAL ADMIN API KEY (save this securely!):")
    logger.info(f"  {admin_key}")
    logger.info(f"="*60)
    
    return admin_key
