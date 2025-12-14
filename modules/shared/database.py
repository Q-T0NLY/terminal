"""
💾 Shared Database Models and Utilities
Production-grade database layer
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
from contextlib import contextmanager

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ose:ose_secure_password@postgres:5432/ose"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()


# ==================== Database Models ====================

class ScanHistory(Base):
    """Discovery scan history"""
    __tablename__ = "scan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    scan_type = Column(String)  # full, quick, custom
    duration_seconds = Column(Float)
    components_scanned = Column(Integer)
    results = Column(JSON)
    errors = Column(JSON, nullable=True)


class ResetHistory(Base):
    """Factory reset history"""
    __tablename__ = "reset_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    profile = Column(String)  # light, medium, deep, nuclear
    components = Column(JSON)
    freed_space_mb = Column(Float)
    duration_seconds = Column(Float)
    status = Column(String)  # pending, running, completed, failed
    backup_path = Column(String, nullable=True)
    errors = Column(JSON, nullable=True)


class OptimizationHistory(Base):
    """Optimization history"""
    __tablename__ = "optimization_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    profile = Column(String)  # conservative, balanced, aggressive, extreme
    categories = Column(JSON)
    performance_improvement = Column(Float)
    benchmark_before = Column(JSON)
    benchmark_after = Column(JSON)
    status = Column(String)
    rollback_available = Column(Boolean, default=False)


class PackageInstallation(Base):
    """Package installation history"""
    __tablename__ = "package_installations"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    package_manager = Column(String)  # apt, dnf, pacman
    packages = Column(JSON)
    installed_count = Column(Integer)
    failed_count = Column(Integer)
    duration_seconds = Column(Float)
    status = Column(String)
    logs = Column(Text, nullable=True)


class TerminalConfiguration(Base):
    """Terminal configuration history"""
    __tablename__ = "terminal_configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    config_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    profile = Column(String)  # minimal, balanced, power, enterprise
    theme = Column(String)
    plugins = Column(JSON)
    custom_settings = Column(JSON, nullable=True)
    generated_files = Column(JSON)
    status = Column(String)


class MetricsSnapshot(Base):
    """System metrics snapshots"""
    __tablename__ = "metrics_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_percent = Column(Float)
    network_sent_mb = Column(Float)
    network_recv_mb = Column(Float)
    top_processes = Column(JSON)
    alerts = Column(JSON, nullable=True)


class APIRequestLog(Base):
    """API request logging"""
    __tablename__ = "api_request_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    request_id = Column(String, index=True)
    service = Column(String, index=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    duration_ms = Column(Float)
    client_ip = Column(String)
    user_agent = Column(String, nullable=True)
    api_key_hash = Column(String, nullable=True)


# ==================== Database Utilities ====================

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    """Get database session context manager"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session (for FastAPI dependency)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== Repository Pattern ====================

class BaseRepository:
    """Base repository with common operations"""
    
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db
    
    def create(self, **kwargs):
        """Create new record"""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def get_by_id(self, id: int):
        """Get record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100):
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, **kwargs):
        """Update record"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance
    
    def delete(self, id: int):
        """Delete record"""
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
        return instance


# Initialize database on import
init_db()
