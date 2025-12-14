# ⚡ Optimization Service

**Ultra-Advanced System & Terminal Performance Optimization**

## Overview

The Optimization Service provides intelligent system tuning recommendations and automated optimizations across CPU, memory, disk, network, kernel, and terminal components. It uses industry best practices and can automatically apply safe optimizations.

## Features

- ✅ **6 Optimization Categories** - CPU, Memory, Disk, Network, Kernel, Terminal
- ✅ **4 Optimization Profiles** - Conservative, Balanced, Aggressive, Extreme
- ✅ **Smart Recommendations** - AI-powered suggestions with impact scores
- ✅ **Benchmarking** - Built-in performance testing
- ✅ **Risk Assessment** - Clear risk levels for each optimization
- ✅ **Rollback Support** - Save state before applying changes

## Quick Start

### Docker

```bash
# Build
docker build -t ose/optimization .

# Run (requires privileged mode for system access)
docker run --privileged \
  -v /sys:/host/sys \
  -v /proc:/host/proc:ro \
  -p 8004:8004 \
  ose/optimization

# Test
curl http://localhost:8004/health
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main.py

# Access API docs
open http://localhost:8004/docs
```

## API Endpoints

### GET /api/v1/optimize/profiles
Get available optimization profiles

**Response:**
```json
{
  "profiles": [
    {
      "id": "conservative",
      "name": "Conservative",
      "description": "Safe optimizations, minimal risk",
      "impact": "low",
      "risk": "low"
    },
    {
      "id": "balanced",
      "name": "Balanced",
      "description": "Balanced performance and safety",
      "impact": "medium",
      "risk": "low"
    },
    {
      "id": "aggressive",
      "name": "Aggressive",
      "description": "Maximum performance, some risk",
      "impact": "high",
      "risk": "medium"
    },
    {
      "id": "extreme",
      "name": "Extreme",
      "description": "Experimental optimizations",
      "impact": "maximum",
      "risk": "high"
    }
  ]
}
```

### GET /api/v1/optimize/recommendations
Get optimization recommendations

**Query Parameters:**
- `categories` (optional): Comma-separated list (cpu,memory,disk,network,kernel,terminal)

**Example:**
```bash
curl "http://localhost:8004/api/v1/optimize/recommendations?categories=cpu,memory"
```

**Response:**
```json
{
  "total_recommendations": 12,
  "categories": ["cpu", "memory", "disk", "network", "kernel", "terminal"],
  "recommendations": [
    {
      "id": "cpu_governor",
      "category": "cpu",
      "title": "Set CPU Governor to Performance",
      "description": "Use 'performance' governor for maximum CPU speed",
      "current_value": "powersave",
      "recommended_value": "performance",
      "impact_score": 8,
      "risk_level": "low",
      "command": "echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
    },
    {
      "id": "swappiness",
      "category": "memory",
      "title": "Reduce Swappiness",
      "description": "Lower swappiness for better performance",
      "current_value": 60,
      "recommended_value": 10,
      "impact_score": 7,
      "risk_level": "low",
      "command": "sudo sysctl vm.swappiness=10"
    }
  ]
}
```

### POST /api/v1/optimize/apply
Apply optimizations (DRY RUN by default)

**Request:**
```json
{
  "profile": "balanced",
  "categories": ["cpu", "memory", "network"],
  "auto_apply": false,
  "create_rollback": true
}
```

**Response:**
```json
{
  "task_id": "opt_20231213_143022",
  "applied_optimizations": ["cpu", "memory", "network"],
  "performance_improvement_percent": 15.3,
  "rollback_path": "/var/backups/ose/optimizations/opt_20231213_143022",
  "benchmark_before": {
    "cpu_score": 75.5,
    "memory_score": 68.2,
    "overall_score": 71.8
  },
  "benchmark_after": {
    "cpu_score": 86.8,
    "memory_score": 75.0,
    "overall_score": 82.8
  }
}
```

### POST /api/v1/benchmark/run
Run performance benchmark

**Request:**
```json
{
  "categories": ["cpu", "memory", "disk"],
  "duration_seconds": 10
}
```

**Response:**
```json
{
  "cpu_score": 75.5,
  "memory_score": 68.2,
  "disk_iops": 1000.0,
  "disk_throughput_mbs": 500.0,
  "overall_score": 71.8
}
```

## Optimization Categories

### 1. CPU Optimization

**Recommendations:**
- Set CPU governor (powersave → performance)
- Configure CPU affinity for processes
- Disable CPU throttling
- Enable turbo boost

**Impact:** High (8/10)  
**Risk:** Low

### 2. Memory Optimization

**Recommendations:**
- Reduce swappiness (60 → 10)
- Enable transparent huge pages
- Configure memory caching
- Optimize dirty ratios

**Impact:** Medium-High (7/10)  
**Risk:** Low

### 3. Disk I/O Optimization

**Recommendations:**
- Set I/O scheduler (none for NVMe, mq-deadline for SATA)
- Configure read-ahead
- Enable writeback caching
- Optimize mount options

**Impact:** High (7/10)  
**Risk:** Low

### 4. Network Optimization

**Recommendations:**
- Enable TCP BBR congestion control
- Increase network buffers
- Optimize TCP window sizes
- Enable TCP timestamps

**Impact:** Very High (8/10)  
**Risk:** Low

### 5. Kernel Tuning

**Recommendations:**
- Increase file descriptor limits
- Optimize inotify watches
- Configure kernel parameters
- Tune virtual memory

**Impact:** Medium (6/10)  
**Risk:** Low

### 6. Terminal Optimization

**Recommendations:**
- Switch to ZSH
- Enable GPU acceleration (Alacritty, Kitty)
- Use modern terminal emulator
- Configure shell caching

**Impact:** High (7-8/10)  
**Risk:** Low

## Optimization Profiles

### Conservative (Recommended for Production)
- Only applies safe, well-tested optimizations
- No experimental features
- Minimal risk of instability
- Expected improvement: 10-15%

### Balanced (Default)
- Mix of safe and moderately aggressive optimizations
- Tested on common systems
- Low risk of issues
- Expected improvement: 15-25%

### Aggressive (Power Users)
- Maximum safe performance
- Some less-tested features
- Medium risk
- Expected improvement: 25-40%

### Extreme (Experimental)
- Bleeding-edge optimizations
- Experimental features
- Higher risk of instability
- Expected improvement: 40%+
- **Use at your own risk**

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@postgres:5432/ose
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
ENABLE_AUTO_APPLY=false  # Safety: disable auto-apply by default
```

## Docker Compose Integration

```yaml
optimization:
  build:
    context: ./modules/optimization
  ports:
    - "8004:8004"
  environment:
    - DATABASE_URL=postgresql://ose:password@postgres:5432/ose
    - REDIS_URL=redis://redis:6379
  volumes:
    - /sys:/host/sys
    - /proc:/host/proc:ro
  privileged: true  # Required for system modifications
  networks:
    - ose-network
```

## Health Check

```bash
curl http://localhost:8004/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-13T14:30:22.123456",
  "service": "optimization"
}
```

## Examples

### Get All Recommendations

```bash
curl http://localhost:8004/api/v1/optimize/recommendations | jq
```

### Get CPU-Only Recommendations

```bash
curl "http://localhost:8004/api/v1/optimize/recommendations?categories=cpu" | jq
```

### Apply Balanced Optimizations (Dry Run)

```bash
curl -X POST http://localhost:8004/api/v1/optimize/apply \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "balanced",
    "categories": ["cpu", "memory", "network"],
    "auto_apply": false,
    "create_rollback": true
  }' | jq
```

### Run Quick Benchmark

```bash
curl -X POST http://localhost:8004/api/v1/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["cpu", "memory"],
    "duration_seconds": 5
  }' | jq
```

## Safety Features

- **DRY RUN Mode** - All optimizations simulated by default
- **Rollback Points** - State saved before changes
- **Risk Assessment** - Clear risk levels for each optimization
- **Impact Scoring** - Know what will make the biggest difference
- **Validation** - All changes validated before applying

## Best Practices

1. **Always test first** - Use `auto_apply: false` for dry runs
2. **Benchmark before and after** - Measure actual improvements
3. **Start conservative** - Begin with low-risk optimizations
4. **Monitor** - Watch system metrics after applying changes
5. **Create rollbacks** - Always enable `create_rollback: true`
6. **Test incrementally** - Apply one category at a time

## Typical Performance Gains

| System Type | Profile | Expected Improvement |
|-------------|---------|---------------------|
| Desktop | Balanced | 15-25% |
| Server | Aggressive | 25-40% |
| Gaming | Aggressive | 30-45% |
| Development | Balanced | 20-30% |

## Troubleshooting

### Permission Denied

**Problem:** Can't modify system settings

**Solution:**
```bash
# Run container with privileged mode
docker run --privileged ...
```

### No Recommendations

**Problem:** No optimizations suggested

**Solution:** System may already be optimized or using unsupported platform

### Benchmark Fails

**Problem:** Benchmark returns errors

**Solution:** Check that required system files are accessible via volume mounts

## License

MIT License

## Support

- API Documentation: http://localhost:8004/docs
- Health Check: http://localhost:8004/health
- GitHub Issues: Report bugs and request features
