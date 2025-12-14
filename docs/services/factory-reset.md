# 🧹 Factory Reset Service

**Ultra-Advanced Factory Reset with Dynamic User Customizations**

## Features

- 4 reset profiles (light, medium, deep, nuclear)
- Granular component selection
- Real-time analysis and preview
- Safe backup creation
- Dry-run mode
- Rollback support
- Interactive React UI

## Quick Start

```bash
# Build
docker build -t ose/factory-reset .

# Run
docker run -p 8002:8002 ose/factory-reset
```

## API Endpoints

### GET /api/v1/reset/profiles
Get available reset profiles

### GET /api/v1/reset/analyze
Analyze what can be reset

**Response:**
```json
{
  "total_items": 15234,
  "total_size_mb": 8432.5,
  "estimated_time_minutes": 25,
  "components": [
    {
      "id": "cache_files",
      "name": "Cache Files",
      "size_mb": 2340.2,
      "risk_level": "low"
    }
  ],
  "warnings": ["⚠️  Large amount of data detected"],
  "recommendations": ["💡 Create backup before proceeding"]
}
```

### POST /api/v1/reset/execute
Execute factory reset

**Request:**
```json
{
  "profile": "medium",
  "selected_components": ["cache_files", "temp_files"],
  "create_backup": true,
  "dry_run": false,
  "confirmation_code": "NUCLEAR_RESET_CONFIRMED"
}
```

## Reset Profiles

### Light (5 min)
- Cache files
- Temporary files
- Risk: **LOW**

### Medium (15 min)
- Light + Browser data
- Risk: **MEDIUM**

### Deep (30 min)
- Medium + User configs
- Medium + Applications
- Risk: **HIGH**

### Nuclear (60 min)
- Everything including packages
- **Requires confirmation code**
- Risk: **CRITICAL**

## Safety Features

- Dry-run mode to preview
- Automatic backups
- Confirmation required for nuclear
- Risk level warnings
- Rollback support

## Interactive Docs

http://localhost:8002/docs
