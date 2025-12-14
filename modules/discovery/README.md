# 🔍 Discovery Service

**Ultra-Advanced System-Wide Discovery, Scanning, and Detection**

## Features

- Real-time hardware detection (CPU, GPU, RAM, Disk, Network)
- OS and package detection (distro, kernel, packages)
- Application discovery (installed apps, versions)
- Network topology mapping
- Security audit (open ports, firewall, SSH keys)
- Service discovery (systemd services)

## Quick Start

### Docker

```bash
# Build
docker build -t ose/discovery .

# Run
docker run -p 8001:8001 ose/discovery

# Test
curl http://localhost:8001/api/v1/scan
```

### Local

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main.py

# Test
curl http://localhost:8001/api/v1/scan
```

## API Endpoints

### GET /api/v1/discover/hardware
Get hardware specifications

**Response:**
```json
{
  "cpu": {
    "model": "Intel Core i7",
    "cores_physical": 4,
    "cores_logical": 8,
    "frequency_mhz": 3600,
    "usage_percent": 25.5
  },
  "memory": {
    "total_gb": 16.0,
    "available_gb": 8.5,
    "used_gb": 7.5,
    "percent_used": 46.9
  },
  "disk": { ... },
  "network": { ... }
}
```

### GET /api/v1/discover/software
Get installed software

**Response:**
```json
{
  "os": {
    "name": "Linux",
    "version": "5.15.0",
    "distribution": "Ubuntu 22.04"
  },
  "packages": [ ... ],
  "applications": [ ... ],
  "services": [ ... ]
}
```

### POST /api/v1/scan
Run comprehensive scan

**Request:**
```json
{
  "scan_type": "full",
  "components": ["hardware", "software", "network", "security"]
}
```

**Response:**
```json
{
  "scan_id": "scan_20231213_143022",
  "timestamp": "2023-12-13T14:30:22",
  "hardware": { ... },
  "software": { ... },
  "network": { ... },
  "security": { ... }
}
```

## Scan Types

- `full` - All components (default)
- `quick` - Hardware + OS only
- `custom` - Specific components

## Interactive API Docs

http://localhost:8001/docs
