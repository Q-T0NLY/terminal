"""
🔧 Shared Utilities for All OSE Services
Production-grade components
"""

from .middleware import (
    APIKeyAuth,
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    get_cors_config,
    security
)
from .database import (
    get_db,
    get_db_session,
    Base,
    ScanHistory,
    ResetHistory,
    OptimizationHistory,
    PackageInstallation,
    TerminalConfiguration,
    MetricsSnapshot,
    APIRequestLog,
    BaseRepository
)
from .cache import (
    Cache,
    cache_scan_result,
    get_cached_scan,
    cache_optimization_result,
    get_cached_optimization
)

__all__ = [
    # Middleware
    "APIKeyAuth",
    "RateLimitMiddleware",
    "RequestLoggingMiddleware",
    "get_cors_config",
    "security",
    # Database
    "get_db",
    "get_db_session",
    "Base",
    "ScanHistory",
    "ResetHistory",
    "OptimizationHistory",
    "PackageInstallation",
    "TerminalConfiguration",
    "MetricsSnapshot",
    "APIRequestLog",
    "BaseRepository",
    # Cache
    "Cache",
    "cache_scan_result",
    "get_cached_scan",
    "cache_optimization_result",
    "get_cached_optimization",
]
