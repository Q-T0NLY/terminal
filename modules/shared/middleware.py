"""
🔒 Shared Middleware for All OSE Services
Production-grade middleware components
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
import hashlib
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== Authentication Middleware ====================

security = HTTPBearer(auto_error=False)

class APIKeyAuth:
    """API Key Authentication"""
    
    # In production, store these in database/secrets manager
    VALID_API_KEYS = {
        "ose_prod_key_123": {"name": "Production", "tier": "premium"},
        "ose_dev_key_456": {"name": "Development", "tier": "standard"},
        "ose_test_key_789": {"name": "Testing", "tier": "basic"}
    }
    
    @staticmethod
    async def verify_api_key(api_key: str) -> Optional[Dict]:
        """Verify API key and return user info"""
        return APIKeyAuth.VALID_API_KEYS.get(api_key)
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = None):
        """Get current authenticated user"""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials"
            )
        
        user = await APIKeyAuth.verify_api_key(credentials.credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return user


# ==================== Rate Limiting Middleware ====================

class RateLimiter:
    """In-memory rate limiter (use Redis in production)"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
        self.limits = {
            "basic": {"requests": 100, "window": 3600},      # 100/hour
            "standard": {"requests": 1000, "window": 3600},  # 1000/hour
            "premium": {"requests": 10000, "window": 3600}   # 10000/hour
        }
    
    def is_allowed(self, key: str, tier: str = "basic") -> bool:
        """Check if request is allowed"""
        now = time.time()
        limit_config = self.limits.get(tier, self.limits["basic"])
        
        # Clean old requests
        if key in self.requests:
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if now - req_time < limit_config["window"]
            ]
        else:
            self.requests[key] = []
        
        # Check limit
        if len(self.requests[key]) >= limit_config["requests"]:
            return False
        
        # Add new request
        self.requests[key].append(now)
        return True
    
    def get_reset_time(self, key: str, tier: str = "basic") -> int:
        """Get time until rate limit resets"""
        if key not in self.requests or not self.requests[key]:
            return 0
        
        limit_config = self.limits.get(tier, self.limits["basic"])
        oldest_request = min(self.requests[key])
        reset_time = oldest_request + limit_config["window"]
        return int(reset_time - time.time())


rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier
        client_ip = request.client.host
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        client_id = api_key or client_ip
        
        # Determine tier
        tier = "basic"
        if api_key and api_key in APIKeyAuth.VALID_API_KEYS:
            tier = APIKeyAuth.VALID_API_KEYS[api_key].get("tier", "basic")
        
        # Check rate limit
        if not rate_limiter.is_allowed(client_id, tier):
            reset_time = rate_limiter.get_reset_time(client_id, tier)
            return Response(
                content=json.dumps({
                    "error": "Rate limit exceeded",
                    "reset_in_seconds": reset_time
                }),
                status_code=429,
                headers={
                    "X-RateLimit-Limit": str(rate_limiter.limits[tier]["requests"]),
                    "X-RateLimit-Reset": str(reset_time),
                    "Content-Type": "application/json"
                }
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.limits[tier]["requests"])
        response.headers["X-RateLimit-Remaining"] = str(
            rate_limiter.limits[tier]["requests"] - len(rate_limiter.requests.get(client_id, []))
        )
        
        return response


# ==================== Logging Middleware ====================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Request/response logging middleware"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = hashlib.md5(
            f"{time.time()}{request.client.host}".encode()
        ).hexdigest()[:8]
        
        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host}"
        )
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"[{request_id}] Status: {response.status_code} "
                f"Duration: {process_time:.3f}s"
            )
            
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] Error: {str(e)} "
                f"Duration: {process_time:.3f}s"
            )
            raise


# ==================== CORS Middleware ====================

def get_cors_config():
    """Get CORS configuration"""
    return {
        "allow_origins": ["*"],  # In production, specify exact origins
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": ["X-Request-ID", "X-Process-Time", "X-RateLimit-Limit"]
    }


# ==================== Error Handler ====================

async def handle_errors(request: Request, call_next):
    """Global error handler"""
    try:
        return await call_next(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unhandled error: {str(e)}")
        return Response(
            content=json.dumps({
                "error": "Internal server error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }),
            status_code=500,
            media_type="application/json"
        )
