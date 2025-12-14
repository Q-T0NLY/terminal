#!/usr/bin/env python3
"""
Universal Plugin Registry with Feature Classification
Version: ∞.7
"""

import sqlite3
import json
import re
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration
REGISTRY_DB = "/var/lib/ose/plugins/registry.db"
FEATURE_REGISTRY = "/workspaces/terminal/modules/universal-registry/core/feature_registry.yaml"
PLUGIN_SCHEMA = "/workspaces/terminal/modules/universal-registry/plugins/plugin_schema.yaml"


class PluginStatus(str, Enum):
    """Plugin lifecycle status"""
    REGISTERED = "registered"
    INSTALLED = "installed"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    FAILED = "failed"


class FeatureCategory(str, Enum):
    """Feature categories for classification"""
    AI_ML = "ai-ml"
    WEB3 = "web3-blockchain"
    CLOUD = "cloud-native"
    DATA = "data-engineering"
    DEVOPS = "devops-platform"
    SECURITY = "security-platform"
    SYSTEM = "system-ops"
    OBSERVABILITY = "observability"


@dataclass
class Plugin:
    """Plugin entity"""
    id: str
    name: str
    version: str
    feature: str
    display_name: str
    description: str
    author: str
    license: str
    icon: str
    status: str = PluginStatus.REGISTERED
    metadata: Dict[str, Any] = None
    capabilities: Dict[str, Any] = None
    dependencies: Dict[str, List[str]] = None
    mesh_config: Dict[str, Any] = None
    ui_config: Dict[str, Any] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow().isoformat()
        if self.metadata is None:
            self.metadata = {}
        if self.capabilities is None:
            self.capabilities = {}
        if self.dependencies is None:
            self.dependencies = {}
        if self.mesh_config is None:
            self.mesh_config = {}
        if self.ui_config is None:
            self.ui_config = {}


@dataclass
class Feature:
    """Feature category"""
    id: str
    name: str
    category: str
    icon: str
    description: str
    tags: List[str]
    mesh_service: str
    namespace: str
    plugin_count: int = 0
    enabled: bool = True


class PluginRegistry:
    """Central plugin registry with feature classification"""
    
    def __init__(self, db_path: str = REGISTRY_DB):
        self.db_path = db_path
        self.features: Dict[str, Feature] = {}
        self.plugins: Dict[str, Plugin] = {}
        self.classification_rules: List[Dict] = []
        
        # Initialize database
        self._init_database()
        
        # Load feature registry
        self._load_feature_registry()
    
    def _init_database(self):
        """Initialize SQLite database schema"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript("""
            -- Plugins table
            CREATE TABLE IF NOT EXISTS plugins (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                feature TEXT NOT NULL,
                display_name TEXT,
                description TEXT,
                author TEXT,
                license TEXT,
                icon TEXT,
                status TEXT DEFAULT 'registered',
                metadata TEXT,
                capabilities TEXT,
                dependencies TEXT,
                mesh_config TEXT,
                ui_config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, version)
            );
            
            -- Features table
            CREATE TABLE IF NOT EXISTS features (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                icon TEXT,
                description TEXT,
                tags TEXT,
                mesh_service TEXT,
                namespace TEXT,
                plugin_count INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1
            );
            
            -- Plugin dependencies table
            CREATE TABLE IF NOT EXISTS plugin_dependencies (
                plugin_id TEXT,
                dependency_id TEXT,
                dependency_type TEXT,
                required INTEGER DEFAULT 1,
                version_constraint TEXT,
                PRIMARY KEY (plugin_id, dependency_id),
                FOREIGN KEY (plugin_id) REFERENCES plugins(id)
            );
            
            -- Mesh services table
            CREATE TABLE IF NOT EXISTS mesh_services (
                service_name TEXT PRIMARY KEY,
                plugin_id TEXT,
                feature TEXT,
                port INTEGER,
                protocol TEXT,
                replicas INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active',
                config TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins(id)
            );
            
            -- Plugin events table (for audit trail)
            CREATE TABLE IF NOT EXISTS plugin_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plugin_id TEXT,
                event_type TEXT,
                event_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins(id)
            );
            
            -- Create indexes
            CREATE INDEX IF NOT EXISTS idx_plugins_feature ON plugins(feature);
            CREATE INDEX IF NOT EXISTS idx_plugins_status ON plugins(status);
            CREATE INDEX IF NOT EXISTS idx_plugins_name ON plugins(name);
            CREATE INDEX IF NOT EXISTS idx_mesh_services_feature ON mesh_services(feature);
            CREATE INDEX IF NOT EXISTS idx_plugin_events_plugin_id ON plugin_events(plugin_id);
            CREATE INDEX IF NOT EXISTS idx_plugin_events_timestamp ON plugin_events(timestamp);
        """)
        
        conn.commit()
        conn.close()
    
    def _load_feature_registry(self):
        """Load feature definitions from YAML"""
        try:
            with open(FEATURE_REGISTRY, 'r') as f:
                registry = yaml.safe_load(f)
            
            # Load features
            for feature_def in registry['spec']['features']:
                feature = Feature(
                    id=feature_def['id'],
                    name=feature_def['name'],
                    category=feature_def['category'],
                    icon=feature_def['icon'],
                    description=feature_def['description'],
                    tags=feature_def['tags'],
                    mesh_service=feature_def['mesh_service'],
                    namespace=feature_def['namespace']
                )
                self.features[feature.id] = feature
                
                # Store in database
                self._save_feature_to_db(feature)
            
            # Load classification rules
            self.classification_rules = registry['spec']['classification_rules']
            
        except FileNotFoundError:
            print(f"Warning: Feature registry not found at {FEATURE_REGISTRY}")
    
    def _save_feature_to_db(self, feature: Feature):
        """Save feature to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO features 
            (id, name, category, icon, description, tags, mesh_service, namespace, enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            feature.id,
            feature.name,
            feature.category,
            feature.icon,
            feature.description,
            json.dumps(feature.tags),
            feature.mesh_service,
            feature.namespace,
            1 if feature.enabled else 0
        ))
        
        conn.commit()
        conn.close()
    
    def classify_plugin(self, plugin_name: str, metadata: Dict = None) -> str:
        """Auto-classify plugin into feature category"""
        name_lower = plugin_name.lower()
        
        # Try metadata-based classification first
        if metadata and 'feature' in metadata:
            return metadata['feature']
        
        # Apply classification rules
        best_match = None
        best_confidence = 0.0
        
        for rule in self.classification_rules:
            pattern = rule['match']
            confidence = rule['confidence']
            feature = rule['feature']
            
            if re.search(pattern, name_lower):
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = feature
        
        # Default to system-ops if no match
        return best_match or FeatureCategory.SYSTEM
    
    def register_plugin(self, plugin: Plugin) -> Plugin:
        """Register a new plugin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Auto-classify if needed
            if not plugin.feature:
                plugin.feature = self.classify_plugin(plugin.name, plugin.metadata)
            
            # Generate ID
            if not plugin.id:
                plugin.id = f"{plugin.name}-{plugin.version}"
            
            # Insert plugin
            cursor.execute("""
                INSERT INTO plugins 
                (id, name, version, feature, display_name, description, author, 
                 license, icon, status, metadata, capabilities, dependencies, 
                 mesh_config, ui_config, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plugin.id,
                plugin.name,
                plugin.version,
                plugin.feature,
                plugin.display_name,
                plugin.description,
                plugin.author,
                plugin.license,
                plugin.icon,
                plugin.status,
                json.dumps(plugin.metadata),
                json.dumps(plugin.capabilities),
                json.dumps(plugin.dependencies),
                json.dumps(plugin.mesh_config),
                json.dumps(plugin.ui_config),
                plugin.created_at,
                plugin.updated_at
            ))
            
            # Update feature plugin count
            cursor.execute("""
                UPDATE features 
                SET plugin_count = plugin_count + 1
                WHERE id = ?
            """, (plugin.feature,))
            
            # Log event
            self._log_event(cursor, plugin.id, "plugin.registered", {
                "name": plugin.name,
                "version": plugin.version,
                "feature": plugin.feature
            })
            
            conn.commit()
            self.plugins[plugin.id] = plugin
            
            return plugin
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Plugin already exists: {plugin.id}") from e
        finally:
            conn.close()
    
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get plugin by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM plugins WHERE id = ?", (plugin_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_plugin(row)
    
    def list_plugins(self, 
                     feature: Optional[str] = None,
                     status: Optional[str] = None,
                     limit: int = 100,
                     offset: int = 0) -> List[Plugin]:
        """List plugins with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM plugins WHERE 1=1"
        params = []
        
        if feature:
            query += " AND feature = ?"
            params.append(feature)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_plugin(row) for row in rows]
    
    def get_feature_plugins(self, feature_id: str) -> List[Plugin]:
        """Get all plugins for a feature"""
        return self.list_plugins(feature=feature_id)
    
    def update_plugin_status(self, plugin_id: str, status: str) -> bool:
        """Update plugin status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE plugins 
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (status, datetime.utcnow().isoformat(), plugin_id))
        
        # Log event
        self._log_event(cursor, plugin_id, "plugin.status_changed", {
            "new_status": status
        })
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def register_mesh_service(self, 
                             service_name: str,
                             plugin_id: str,
                             port: int,
                             protocol: str = "HTTP",
                             config: Dict = None) -> bool:
        """Register plugin as mesh service"""
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO mesh_services
            (service_name, plugin_id, feature, port, protocol, config)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            service_name,
            plugin_id,
            plugin.feature,
            port,
            protocol,
            json.dumps(config or {})
        ))
        
        # Log event
        self._log_event(cursor, plugin_id, "mesh.service_registered", {
            "service_name": service_name,
            "port": port,
            "protocol": protocol
        })
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_mesh_services(self, feature: Optional[str] = None) -> List[Dict]:
        """Get mesh services, optionally filtered by feature"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM mesh_services"
        params = []
        
        if feature:
            query += " WHERE feature = ?"
            params.append(feature)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_plugin_statistics(self) -> Dict:
        """Get registry statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {
            "total_plugins": 0,
            "by_feature": {},
            "by_status": {},
            "total_features": len(self.features),
            "total_mesh_services": 0
        }
        
        # Total plugins
        cursor.execute("SELECT COUNT(*) FROM plugins")
        stats["total_plugins"] = cursor.fetchone()[0]
        
        # By feature
        cursor.execute("""
            SELECT feature, COUNT(*) as count
            FROM plugins
            GROUP BY feature
        """)
        stats["by_feature"] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM plugins
            GROUP BY status
        """)
        stats["by_status"] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Mesh services
        cursor.execute("SELECT COUNT(*) FROM mesh_services")
        stats["total_mesh_services"] = cursor.fetchone()[0]
        
        conn.close()
        
        return stats
    
    def _row_to_plugin(self, row: sqlite3.Row) -> Plugin:
        """Convert database row to Plugin object"""
        return Plugin(
            id=row['id'],
            name=row['name'],
            version=row['version'],
            feature=row['feature'],
            display_name=row['display_name'],
            description=row['description'],
            author=row['author'],
            license=row['license'],
            icon=row['icon'],
            status=row['status'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {},
            capabilities=json.loads(row['capabilities']) if row['capabilities'] else {},
            dependencies=json.loads(row['dependencies']) if row['dependencies'] else {},
            mesh_config=json.loads(row['mesh_config']) if row['mesh_config'] else {},
            ui_config=json.loads(row['ui_config']) if row['ui_config'] else {},
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
    def _log_event(self, cursor, plugin_id: str, event_type: str, data: Dict):
        """Log plugin event for audit trail"""
        cursor.execute("""
            INSERT INTO plugin_events (plugin_id, event_type, event_data)
            VALUES (?, ?, ?)
        """, (plugin_id, event_type, json.dumps(data)))


# Global registry instance
_registry_instance = None

def get_registry() -> PluginRegistry:
    """Get or create global registry instance"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = PluginRegistry()
    return _registry_instance
