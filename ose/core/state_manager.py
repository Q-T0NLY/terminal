"""
📊 OSE State Manager
Tracks system state and operation history
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class OperationStatus(Enum):
    """Status of OSE operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class SystemSnapshot:
    """Represents a point-in-time system state"""
    timestamp: str
    disk_usage: Dict[str, int]
    package_count: int
    health_score: int
    boot_time: float
    memory_usage: int
    
    
@dataclass
class OperationRecord:
    """Record of an OSE operation"""
    id: int
    timestamp: str
    operation_type: str
    modules: List[str]
    status: OperationStatus
    dry_run: bool
    results: Dict[str, Any]
    backup_path: Optional[str] = None


class StateManager:
    """
    Manages OSE system state and operation history
    
    Uses SQLite database to track:
    - System snapshots over time
    - Operation history
    - Backup locations
    - Configuration changes
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize State Manager
        
        Args:
            db_path: Path to SQLite database (uses default if None)
        """
        if db_path is None:
            db_path = Path.home() / ".ose" / "data" / "system_state.db"
            
        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        
        self._init_database()
        
    def _init_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(str(self.db_path))
        cursor = self.conn.cursor()
        
        # System snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                disk_usage TEXT NOT NULL,
                package_count INTEGER,
                health_score INTEGER,
                boot_time REAL,
                memory_usage INTEGER
            )
        """)
        
        # Operations history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                modules TEXT NOT NULL,
                status TEXT NOT NULL,
                dry_run INTEGER NOT NULL,
                results TEXT,
                backup_path TEXT
            )
        """)
        
        # Backups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                path TEXT NOT NULL,
                size INTEGER,
                description TEXT
            )
        """)
        
        self.conn.commit()
        
    def save_snapshot(self, snapshot: SystemSnapshot) -> int:
        """
        Save a system snapshot
        
        Args:
            snapshot: SystemSnapshot to save
            
        Returns:
            Snapshot ID
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO snapshots 
            (timestamp, disk_usage, package_count, health_score, boot_time, memory_usage)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            snapshot.timestamp,
            json.dumps(snapshot.disk_usage),
            snapshot.package_count,
            snapshot.health_score,
            snapshot.boot_time,
            snapshot.memory_usage
        ))
        
        self.conn.commit()
        return cursor.lastrowid
        
    def get_latest_snapshot(self) -> Optional[SystemSnapshot]:
        """Get the most recent system snapshot"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, disk_usage, package_count, health_score, boot_time, memory_usage
            FROM snapshots
            ORDER BY id DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        if row is None:
            return None
            
        return SystemSnapshot(
            timestamp=row[0],
            disk_usage=json.loads(row[1]),
            package_count=row[2],
            health_score=row[3],
            boot_time=row[4],
            memory_usage=row[5]
        )
        
    def save_operation(self, operation: OperationRecord) -> int:
        """
        Save an operation record
        
        Args:
            operation: OperationRecord to save
            
        Returns:
            Operation ID
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO operations
            (timestamp, operation_type, modules, status, dry_run, results, backup_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            operation.timestamp,
            operation.operation_type,
            json.dumps(operation.modules),
            operation.status.value,
            1 if operation.dry_run else 0,
            json.dumps(operation.results),
            operation.backup_path
        ))
        
        self.conn.commit()
        return cursor.lastrowid
        
    def update_operation_status(self, operation_id: int, status: OperationStatus):
        """Update the status of an operation"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE operations
            SET status = ?
            WHERE id = ?
        """, (status.value, operation_id))
        
        self.conn.commit()
        
    def get_operation_history(self, limit: int = 10) -> List[OperationRecord]:
        """
        Get recent operation history
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of OperationRecord objects
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, operation_type, modules, status, dry_run, results, backup_path
            FROM operations
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        
        records = []
        for row in cursor.fetchall():
            records.append(OperationRecord(
                id=row[0],
                timestamp=row[1],
                operation_type=row[2],
                modules=json.loads(row[3]),
                status=OperationStatus(row[4]),
                dry_run=bool(row[5]),
                results=json.loads(row[6]) if row[6] else {},
                backup_path=row[7]
            ))
            
        return records
        
    def get_health_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get health score trend over time
        
        Args:
            days: Number of days to retrieve
            
        Returns:
            List of {timestamp, health_score} dicts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT timestamp, health_score
            FROM snapshots
            WHERE datetime(timestamp) >= datetime('now', ? || ' days')
            ORDER BY timestamp ASC
        """, (f"-{days}",))
        
        return [
            {"timestamp": row[0], "health_score": row[1]}
            for row in cursor.fetchall()
        ]
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
