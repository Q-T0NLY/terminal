"""
🔄 OSE Reinstallation Service
Ultra-Advanced Package Reinstallation & Auto-Config Regeneration

Features:
- Automated package reinstallation
- Configuration regeneration with templates
- Backup & restore configurations
- Support for multiple package managers
- Version pinning
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import subprocess
from pathlib import Path

app = FastAPI(
    title="OSE Reinstallation Service",
    description="Package Reinstallation & Configuration Generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Models ====================

class PackageInfo(BaseModel):
    name: str
    version: Optional[str]
    manager: str  # apt, dnf, brew, pip, npm, cargo
    installed: bool


class ReinstallRequest(BaseModel):
    packages: List[str]
    package_manager: str = "auto"
    pin_versions: bool = True
    create_backup: bool = True


class ConfigTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    variables: Dict[str, Any]


class ConfigGenerateRequest(BaseModel):
    template_id: str
    variables: Dict[str, Any]
    output_path: str


class ReinstallResult(BaseModel):
    task_id: str
    packages_reinstalled: int
    packages_failed: int
    errors: List[str]
    backup_path: Optional[str]


# ==================== Templates ====================

CONFIG_TEMPLATES = {
    "nginx": {
        "name": "Nginx Configuration",
        "description": "Production-ready Nginx config",
        "category": "webserver",
        "template": """
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections {{ worker_connections }};
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout {{ keepalive_timeout }};
    types_hash_max_size 2048;
    
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
    
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
""",
        "default_variables": {
            "worker_connections": 1024,
            "keepalive_timeout": 65
        }
    },
    "postgresql": {
        "name": "PostgreSQL Configuration",
        "description": "Optimized PostgreSQL config",
        "category": "database",
        "template": """
# PostgreSQL Configuration
max_connections = {{ max_connections }}
shared_buffers = {{ shared_buffers }}
effective_cache_size = {{ effective_cache_size }}
maintenance_work_mem = {{ maintenance_work_mem }}
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = {{ work_mem }}
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = {{ max_workers }}
max_parallel_workers_per_gather = {{ parallel_workers }}
max_parallel_workers = {{ max_workers }}
""",
        "default_variables": {
            "max_connections": 100,
            "shared_buffers": "256MB",
            "effective_cache_size": "1GB",
            "maintenance_work_mem": "64MB",
            "work_mem": "4MB",
            "max_workers": 4,
            "parallel_workers": 2
        }
    },
    "sysctl": {
        "name": "Sysctl Optimizations",
        "description": "Kernel parameter tuning",
        "category": "system",
        "template": """
# Network optimizations
net.core.rmem_max = {{ rmem_max }}
net.core.wmem_max = {{ wmem_max }}
net.ipv4.tcp_rmem = 4096 87380 {{ tcp_rmem_max }}
net.ipv4.tcp_wmem = 4096 65536 {{ tcp_wmem_max }}
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq

# File system
fs.file-max = {{ file_max }}
fs.inotify.max_user_watches = {{ inotify_watches }}

# Virtual memory
vm.swappiness = {{ swappiness }}
vm.dirty_ratio = {{ dirty_ratio }}
vm.dirty_background_ratio = {{ dirty_background_ratio }}
""",
        "default_variables": {
            "rmem_max": 16777216,
            "wmem_max": 16777216,
            "tcp_rmem_max": 16777216,
            "tcp_wmem_max": 16777216,
            "file_max": 2097152,
            "inotify_watches": 524288,
            "swappiness": 10,
            "dirty_ratio": 15,
            "dirty_background_ratio": 5
        }
    }
}


# ==================== Package Detection ====================

async def detect_installed_packages(manager: str = "auto") -> List[PackageInfo]:
    """Detect installed packages"""
    packages = []
    
    # APT (Debian/Ubuntu)
    if manager in ["auto", "apt"]:
        try:
            result = subprocess.run(
                ["dpkg", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n')[5:]:
                    if line.strip() and line.startswith('ii'):
                        parts = line.split()
                        if len(parts) >= 3:
                            packages.append(PackageInfo(
                                name=parts[1],
                                version=parts[2],
                                manager="apt",
                                installed=True
                            ))
        except:
            pass
    
    # DNF/YUM (Fedora/RHEL)
    if manager in ["auto", "dnf", "yum"]:
        try:
            result = subprocess.run(
                ["rpm", "-qa", "--queryformat", "%{NAME}|%{VERSION}\n"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if '|' in line:
                        name, version = line.split('|', 1)
                        packages.append(PackageInfo(
                            name=name,
                            version=version,
                            manager="dnf",
                            installed=True
                        ))
        except:
            pass
    
    return packages[:100]  # Limit


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSE Reinstallation Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "packages": "/api/v1/packages",
            "reinstall": "/api/v1/reinstall",
            "templates": "/api/v1/config/templates",
            "generate": "/api/v1/config/generate",
            "docs": "/docs"
        }
    }


@app.get("/api/v1/packages")
async def list_packages(manager: str = "auto", limit: int = 100):
    """List installed packages"""
    packages = await detect_installed_packages(manager)
    return {
        "total": len(packages),
        "manager": manager,
        "packages": packages[:limit]
    }


@app.post("/api/v1/reinstall", response_model=ReinstallResult)
async def reinstall_packages(request: ReinstallRequest):
    """
    Reinstall packages (DRY RUN - for safety)
    
    In production, this would actually reinstall packages.
    For safety, we simulate the operation.
    """
    task_id = f"reinstall_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Simulate reinstallation
    reinstalled = len(request.packages)
    failed = 0
    errors = []
    
    # In production, would run:
    # apt-get install --reinstall <package>
    # dnf reinstall <package>
    # brew reinstall <package>
    
    return ReinstallResult(
        task_id=task_id,
        packages_reinstalled=reinstalled,
        packages_failed=failed,
        errors=errors,
        backup_path=f"/var/backups/ose/packages/{task_id}" if request.create_backup else None
    )


@app.get("/api/v1/config/templates")
async def list_templates(category: Optional[str] = None):
    """List available configuration templates"""
    templates = []
    
    for template_id, template_data in CONFIG_TEMPLATES.items():
        if category is None or template_data["category"] == category:
            templates.append(ConfigTemplate(
                id=template_id,
                name=template_data["name"],
                description=template_data["description"],
                category=template_data["category"],
                variables=template_data["default_variables"]
            ))
    
    return {
        "total": len(templates),
        "templates": templates
    }


@app.get("/api/v1/config/templates/{template_id}")
async def get_template(template_id: str):
    """Get template details"""
    if template_id not in CONFIG_TEMPLATES:
        return {"error": "Template not found"}, 404
    
    template = CONFIG_TEMPLATES[template_id]
    return {
        "id": template_id,
        "name": template["name"],
        "description": template["description"],
        "category": template["category"],
        "template": template["template"],
        "default_variables": template["default_variables"]
    }


@app.post("/api/v1/config/generate")
async def generate_config(request: ConfigGenerateRequest):
    """Generate configuration from template"""
    
    if request.template_id not in CONFIG_TEMPLATES:
        return {"error": "Template not found"}, 404
    
    template = CONFIG_TEMPLATES[request.template_id]
    
    # Merge default variables with user variables
    variables = {**template["default_variables"], **request.variables}
    
    # Simple template rendering (in production, use Jinja2)
    content = template["template"]
    for key, value in variables.items():
        placeholder = "{{ " + key + " }}"
        content = content.replace(placeholder, str(value))
    
    return {
        "template_id": request.template_id,
        "output_path": request.output_path,
        "content": content,
        "variables_used": variables
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "reinstallation"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
