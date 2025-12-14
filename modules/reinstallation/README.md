# 🔄 Reinstallation Service

**Ultra-Advanced Package Reinstallation & Auto-Config Regeneration**

## Overview

The Reinstallation Service provides automated package reinstallation and configuration file generation using industry-standard templates. It supports multiple package managers and includes pre-built templates for common services.

## Features

- ✅ **Multi-Platform Support** - APT (Debian/Ubuntu), DNF/YUM (RHEL/Fedora), RPM
- ✅ **Package Detection** - Automatically detect installed packages
- ✅ **Config Templates** - Pre-built templates for Nginx, PostgreSQL, Sysctl
- ✅ **Template Engine** - Jinja2-style variable substitution
- ✅ **Backup Support** - Create backups before reinstallation
- ✅ **Version Pinning** - Maintain package versions during reinstall

## Quick Start

### Docker

```bash
# Build
docker build -t ose/reinstallation .

# Run
docker run -p 8003:8003 ose/reinstallation

# Test
curl http://localhost:8003/health
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main.py

# Access API docs
open http://localhost:8003/docs
```

## API Endpoints

### GET /api/v1/packages
List installed packages

**Query Parameters:**
- `manager` (optional): Package manager (auto, apt, dnf, rpm)
- `limit` (optional): Maximum number of packages to return (default: 100)

**Example:**
```bash
curl http://localhost:8003/api/v1/packages?manager=apt&limit=50
```

**Response:**
```json
{
  "total": 1247,
  "manager": "apt",
  "packages": [
    {
      "name": "nginx",
      "version": "1.18.0-0ubuntu1",
      "manager": "apt",
      "installed": true
    }
  ]
}
```

### POST /api/v1/reinstall
Reinstall packages (DRY RUN by default for safety)

**Request:**
```json
{
  "packages": ["nginx", "postgresql", "redis-server"],
  "package_manager": "apt",
  "pin_versions": true,
  "create_backup": true
}
```

**Response:**
```json
{
  "task_id": "reinstall_20231213_143022",
  "packages_reinstalled": 3,
  "packages_failed": 0,
  "errors": [],
  "backup_path": "/var/backups/ose/packages/reinstall_20231213_143022"
}
```

### GET /api/v1/config/templates
List available configuration templates

**Query Parameters:**
- `category` (optional): Filter by category (webserver, database, system)

**Example:**
```bash
curl http://localhost:8003/api/v1/config/templates?category=webserver
```

**Response:**
```json
{
  "total": 3,
  "templates": [
    {
      "id": "nginx",
      "name": "Nginx Configuration",
      "description": "Production-ready Nginx config",
      "category": "webserver",
      "variables": {
        "worker_connections": 1024,
        "keepalive_timeout": 65
      }
    }
  ]
}
```

### GET /api/v1/config/templates/{template_id}
Get template details

**Example:**
```bash
curl http://localhost:8003/api/v1/config/templates/nginx
```

**Response:**
```json
{
  "id": "nginx",
  "name": "Nginx Configuration",
  "description": "Production-ready Nginx config",
  "category": "webserver",
  "template": "user www-data;\nworker_processes auto;\n...",
  "default_variables": {
    "worker_connections": 1024,
    "keepalive_timeout": 65
  }
}
```

### POST /api/v1/config/generate
Generate configuration from template

**Request:**
```json
{
  "template_id": "nginx",
  "variables": {
    "worker_connections": 2048,
    "keepalive_timeout": 75
  },
  "output_path": "/etc/nginx/nginx.conf"
}
```

**Response:**
```json
{
  "template_id": "nginx",
  "output_path": "/etc/nginx/nginx.conf",
  "content": "user www-data;\nworker_processes auto;\n...",
  "variables_used": {
    "worker_connections": 2048,
    "keepalive_timeout": 75
  }
}
```

## Available Templates

### 1. Nginx Configuration

**Category:** webserver  
**Variables:**
- `worker_connections` (default: 1024)
- `keepalive_timeout` (default: 65)

**Features:**
- Auto worker processes
- Gzip compression
- SSL/TLS optimization
- Security headers

### 2. PostgreSQL Configuration

**Category:** database  
**Variables:**
- `max_connections` (default: 100)
- `shared_buffers` (default: "256MB")
- `effective_cache_size` (default: "1GB")
- `work_mem` (default: "4MB")

**Features:**
- Performance tuning
- Connection pooling
- Memory optimization
- Parallel workers

### 3. Sysctl Optimizations

**Category:** system  
**Variables:**
- `swappiness` (default: 10)
- `file_max` (default: 2097152)
- `tcp_rmem_max` (default: 16777216)
- `tcp_wmem_max` (default: 16777216)

**Features:**
- Network tuning
- File system optimization
- Memory management
- TCP/IP stack tuning

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@postgres:5432/ose
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
```

## Docker Compose Integration

```yaml
reinstallation:
  build:
    context: ./modules/reinstallation
  ports:
    - "8003:8003"
  environment:
    - DATABASE_URL=postgresql://ose:password@postgres:5432/ose
    - REDIS_URL=redis://redis:6379
  volumes:
    - /etc:/host/etc:ro
  networks:
    - ose-network
```

## Health Check

```bash
curl http://localhost:8003/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-13T14:30:22.123456",
  "service": "reinstallation"
}
```

## Examples

### Reinstall Web Stack

```bash
curl -X POST http://localhost:8003/api/v1/reinstall \
  -H "Content-Type: application/json" \
  -d '{
    "packages": ["nginx", "certbot", "python3-certbot-nginx"],
    "package_manager": "apt",
    "pin_versions": true,
    "create_backup": true
  }'
```

### Generate Production Nginx Config

```bash
curl -X POST http://localhost:8003/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "nginx",
    "variables": {
      "worker_connections": 4096,
      "keepalive_timeout": 30
    },
    "output_path": "/etc/nginx/nginx.conf"
  }'
```

### Generate Optimized PostgreSQL Config

```bash
curl -X POST http://localhost:8003/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "postgresql",
    "variables": {
      "max_connections": 200,
      "shared_buffers": "512MB",
      "effective_cache_size": "2GB"
    },
    "output_path": "/etc/postgresql/postgresql.conf"
  }'
```

## Security Considerations

- **DRY RUN Mode** - Package reinstallation is simulated by default for safety
- **Backup Creation** - Always creates backups before modifications
- **Read-Only Mounts** - System directories mounted as read-only in Docker
- **Template Validation** - All templates are validated before rendering

## Troubleshooting

### Package Manager Not Detected

**Problem:** Service can't detect package manager

**Solution:**
```bash
# Manually specify package manager
curl http://localhost:8003/api/v1/packages?manager=apt
```

### Template Not Found

**Problem:** Template ID doesn't exist

**Solution:**
```bash
# List available templates
curl http://localhost:8003/api/v1/config/templates
```

### Permission Denied

**Problem:** Can't write to output path

**Solution:**
- Use a writable output path
- Run container with appropriate volumes
- Check file permissions

## Development

### Adding a New Template

Edit `main.py` and add to `CONFIG_TEMPLATES`:

```python
CONFIG_TEMPLATES["myservice"] = {
    "name": "My Service Configuration",
    "description": "Description here",
    "category": "custom",
    "template": """
# Your config template here
setting = {{ variable_name }}
""",
    "default_variables": {
        "variable_name": "default_value"
    }
}
```

### Running Tests

```bash
# Install test dependencies
pip install pytest requests

# Run tests
pytest tests/
```

## License

MIT License

## Support

- API Documentation: http://localhost:8003/docs
- Health Check: http://localhost:8003/health
- GitHub Issues: Report bugs and request features
