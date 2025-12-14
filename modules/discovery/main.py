"""
🔍 OSE Discovery Service
Ultra-Advanced System-Wide Discovery, Scanning, and Detection

Standalone microservice for comprehensive system analysis.
"""

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import psutil
import platform
import subprocess
import json
import sys
from pathlib import Path

# Add parent directory to path for shared imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.event_bus_client import EventBusClient, MessagePriority

app = FastAPI(
    title="OSE Discovery Service",
    description="Ultra-Advanced System-Wide Discovery and Detection",
    version="1.0.0"
)

# Initialize Event Bus Client
event_bus = EventBusClient("discovery", "http://localhost:8000")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Lifecycle Events ====================

@app.on_event("startup")
async def startup_event():
    """Service startup - publish lifecycle event"""
    await event_bus.publish_lifecycle_event(
        event="started",
        version="1.0.0",
        additional_data={
            "port": 8001,
            "endpoints": 40,
            "features": ["hardware_scan", "software_scan", "network_scan", "deep_scan"]
        }
    )
    print("🔍 Discovery Service started - event published to message bus")

@app.on_event("shutdown")
async def shutdown_event():
    """Service shutdown - publish lifecycle event"""
    await event_bus.publish_lifecycle_event(
        event="stopped",
        version="1.0.0"
    )
    print("🔍 Discovery Service stopped - event published to message bus")

# ==================== Models ====================

class HardwareInfo(BaseModel):
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk: Dict[str, Any]
    network: Dict[str, Any]
    gpu: Optional[Dict[str, Any]] = None


class SoftwareInfo(BaseModel):
    os: Dict[str, str]
    packages: List[Dict[str, str]]
    applications: List[Dict[str, str]]
    services: List[Dict[str, Any]]


class NetworkInfo(BaseModel):
    interfaces: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]
    open_ports: List[int]
    routing_table: List[Dict[str, str]]


class SecurityInfo(BaseModel):
    open_ports: List[int]
    firewall_status: str
    selinux_status: Optional[str]
    ssh_keys: List[str]
    sudo_users: List[str]


class ScanRequest(BaseModel):
    scan_type: str = "full"  # full, quick, custom
    components: Optional[List[str]] = None


class ScanResult(BaseModel):
    scan_id: str
    timestamp: str
    scan_type: str
    hardware: Optional[HardwareInfo] = None
    software: Optional[SoftwareInfo] = None
    network: Optional[NetworkInfo] = None
    security: Optional[SecurityInfo] = None
    metadata: Dict[str, Any]


# ==================== Discovery Functions ====================

async def discover_hardware() -> HardwareInfo:
    """Discover hardware specifications"""
    
    # CPU
    cpu_info = {
        "model": platform.processor(),
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else 0,
        "usage_percent": psutil.cpu_percent(interval=1),
        "architecture": platform.machine(),
    }
    
    # Memory
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    memory_info = {
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "percent_used": mem.percent,
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_gb": round(swap.used / (1024**3), 2),
    }
    
    # Disk
    disk_partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_partitions.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": usage.percent,
            })
        except PermissionError:
            continue
    
    disk_info = {
        "partitions": disk_partitions,
        "io_counters": dict(psutil.disk_io_counters()._asdict()) if psutil.disk_io_counters() else {}
    }
    
    # Network
    net_io = psutil.net_io_counters()
    network_info = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
        "interfaces_count": len(psutil.net_if_addrs()),
    }
    
    # GPU (basic detection)
    gpu_info = None
    try:
        lspci = subprocess.run(
            ["lspci"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        gpu_lines = [l for l in lspci.stdout.split('\n') if 'VGA' in l or 'Display' in l]
        if gpu_lines:
            gpu_info = {"devices": gpu_lines}
    except:
        pass
    
    return HardwareInfo(
        cpu=cpu_info,
        memory=memory_info,
        disk=disk_info,
        network=network_info,
        gpu=gpu_info
    )


async def discover_software() -> SoftwareInfo:
    """Discover installed software"""
    
    # OS Info
    os_info = {
        "name": platform.system(),
        "version": platform.release(),
        "distribution": platform.platform(),
        "hostname": platform.node(),
        "architecture": platform.machine(),
    }
    
    # Try to get more detailed distro info
    try:
        if Path("/etc/os-release").exists():
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        os_info["pretty_name"] = line.split("=")[1].strip().strip('"')
    except:
        pass
    
    # Packages (detect package manager and list packages)
    packages = []
    
    # APT (Debian/Ubuntu)
    try:
        result = subprocess.run(
            ["dpkg", "-l"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n')[5:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        packages.append({
                            "name": parts[1],
                            "version": parts[2],
                            "manager": "apt"
                        })
    except:
        pass
    
    # DNF/YUM (Fedora/RHEL)
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
                    packages.append({
                        "name": name,
                        "version": version,
                        "manager": "dnf"
                    })
    except:
        pass
    
    # Applications (common application directories)
    applications = []
    app_dirs = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        Path.home() / ".local/share/applications"
    ]
    
    for app_dir in app_dirs:
        app_path = Path(app_dir)
        if app_path.exists():
            for desktop_file in app_path.glob("*.desktop"):
                try:
                    with open(desktop_file) as f:
                        name = None
                        exec_path = None
                        for line in f:
                            if line.startswith("Name="):
                                name = line.split("=", 1)[1].strip()
                            elif line.startswith("Exec="):
                                exec_path = line.split("=", 1)[1].strip()
                        
                        if name:
                            applications.append({
                                "name": name,
                                "exec": exec_path,
                                "desktop_file": str(desktop_file)
                            })
                except:
                    continue
    
    # Services (systemd)
    services = []
    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--all", "--no-pager"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if line.strip() and 'service' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        services.append({
                            "name": parts[0],
                            "load": parts[1],
                            "active": parts[2],
                            "sub": parts[3]
                        })
    except:
        pass
    
    return SoftwareInfo(
        os=os_info,
        packages=packages[:100],  # Limit to first 100
        applications=applications[:50],  # Limit to first 50
        services=services[:50]  # Limit to first 50
    )


async def discover_network() -> NetworkInfo:
    """Discover network configuration"""
    
    # Network interfaces
    interfaces = []
    for iface_name, iface_addrs in psutil.net_if_addrs().items():
        addrs = []
        for addr in iface_addrs:
            addrs.append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast,
            })
        
        interfaces.append({
            "name": iface_name,
            "addresses": addrs
        })
    
    # Active connections
    connections = []
    try:
        for conn in psutil.net_connections(kind='inet')[:50]:  # Limit to 50
            connections.append({
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "laddr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                "raddr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                "status": conn.status,
                "pid": conn.pid
            })
    except:
        pass
    
    # Open ports (listening)
    open_ports = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN' and conn.laddr:
                open_ports.append(conn.laddr.port)
    except:
        pass
    
    open_ports = sorted(list(set(open_ports)))
    
    # Routing table (basic)
    routing_table = []
    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.strip():
                    routing_table.append({"route": line.strip()})
    except:
        pass
    
    return NetworkInfo(
        interfaces=interfaces,
        connections=connections,
        open_ports=open_ports,
        routing_table=routing_table
    )


async def discover_security() -> SecurityInfo:
    """Discover security configuration"""
    
    # Open ports (from network discovery)
    open_ports = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN' and conn.laddr:
                open_ports.append(conn.laddr.port)
    except:
        pass
    
    # Firewall status
    firewall_status = "unknown"
    try:
        # Check UFW
        result = subprocess.run(
            ["ufw", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            if "active" in result.stdout.lower():
                firewall_status = "ufw:active"
            else:
                firewall_status = "ufw:inactive"
    except:
        # Check firewalld
        try:
            result = subprocess.run(
                ["firewall-cmd", "--state"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                firewall_status = f"firewalld:{result.stdout.strip()}"
        except:
            pass
    
    # SELinux status (if available)
    selinux_status = None
    try:
        result = subprocess.run(
            ["getenforce"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            selinux_status = result.stdout.strip()
    except:
        pass
    
    # SSH keys
    ssh_keys = []
    ssh_dir = Path.home() / ".ssh"
    if ssh_dir.exists():
        for key_file in ssh_dir.glob("*.pub"):
            ssh_keys.append(str(key_file))
    
    # Sudo users
    sudo_users = []
    try:
        sudo_group_file = Path("/etc/group")
        if sudo_group_file.exists():
            with open(sudo_group_file) as f:
                for line in f:
                    if line.startswith("sudo:") or line.startswith("wheel:"):
                        parts = line.split(":")
                        if len(parts) >= 4:
                            users = parts[3].strip().split(",")
                            sudo_users.extend(users)
    except:
        pass
    
    return SecurityInfo(
        open_ports=sorted(list(set(open_ports))),
        firewall_status=firewall_status,
        selinux_status=selinux_status,
        ssh_keys=ssh_keys,
        sudo_users=list(set(sudo_users))
    )


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSE Discovery Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "hardware": "/api/v1/discover/hardware",
            "software": "/api/v1/discover/software",
            "network": "/api/v1/discover/network",
            "security": "/api/v1/discover/security",
            "scan": "/api/v1/scan",
            "docs": "/docs"
        }
    }


@app.get("/api/v1/discover/hardware", response_model=HardwareInfo)
async def get_hardware():
    """Discover hardware specifications"""
    return await discover_hardware()


@app.get("/api/v1/discover/software", response_model=SoftwareInfo)
async def get_software():
    """Discover installed software"""
    return await discover_software()


@app.get("/api/v1/discover/network", response_model=NetworkInfo)
async def get_network():
    """Discover network configuration"""
    return await discover_network()


@app.get("/api/v1/discover/security", response_model=SecurityInfo)
async def get_security():
    """Discover security configuration"""
    return await discover_security()


@app.post("/api/v1/scan", response_model=ScanResult)
async def run_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Run comprehensive system scan
    
    Scan types:
    - full: All components
    - quick: Hardware + OS only
    - custom: Specific components
    """
    scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    result = ScanResult(
        scan_id=scan_id,
        timestamp=datetime.now().isoformat(),
        scan_type=request.scan_type,
        metadata={
            "requested_components": request.components or [],
            "duration_seconds": 0
        }
    )
    
    # Determine what to scan
    scan_all = request.scan_type == "full"
    scan_quick = request.scan_type == "quick"
    custom_components = request.components or []
    
    # Run scans
    if scan_all or scan_quick or "hardware" in custom_components:
        result.hardware = await discover_hardware()
    
    if scan_all or scan_quick or "software" in custom_components:
        result.software = await discover_software()
    
    if scan_all or "network" in custom_components:
        result.network = await discover_network()
    
    if scan_all or "security" in custom_components:
        result.security = await discover_security()
    
    # Publish scan completion event
    await event_bus.publish_event(
        event_type="discovery.scan.completed",
        payload={
            "scan_id": scan_id,
            "scan_type": request.scan_type,
            "components_scanned": [
                comp for comp, data in [
                    ("hardware", result.hardware),
                    ("software", result.software),
                    ("network", result.network),
                    ("security", result.security)
                ] if data is not None
            ],
            "timestamp": result.timestamp
        },
        priority=MessagePriority.NORMAL
    )
    
    return result


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "discovery"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
