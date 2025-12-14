# 🧹 Factory Reset Service

**Ultra-Advanced Factory Reset with Integrated Cleanup Modules**

## Features

### Factory Reset
- 4 reset profiles (light, medium, deep, nuclear)
- Granular component selection
- Real-time analysis and preview
- Safe backup creation
- Dry-run mode
- Rollback support

### Integrated Cleanup Modules
- **Cache Cleaner** - apt, npm, pip, cargo, homebrew, and more
- **Temp Cleaner** - /tmp, /var/tmp, downloads, system temp
- **Log Manager** - system logs, application logs, rotation
- **Duplicate Finder** - find and remove duplicate files
- **Privacy Cleaner** - browser data, history, cookies, sessions
- **Trash Manager** - empty trash across all platforms

## Quick Start

```bash
# Build
dockFactory Reset Endpoints

#### GET /api/v1/reset/profiles
Get available reset profiles

#### GET /api/v1/reset/analyze
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

#### POST /api/v1/reset/execute
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

### Cleanup Module Endpoints

#### GET /api/v1/cleanup/cache
Clean all caches (apt, npm, pip, cargo, etc.)

#### GET /api/v1/cleanup/temp
Clean temporary files (/tmp, downloads, etc.)

#### GET /api/v1/cleanup/logs
Clean old log files (30+ days)

#### GET /api/v1/cleanup/duplicates
Find duplicate files in home directory

#### GET /api/v1/cleanup/trash
Empty trash/recycle bin

#### GET /api/v1/cleanup/privacy
Clean privacy-sensitive data (browser history, cookies, etc.)

#### POST /api/v1/cleanup/all
Run all cleanup operations

**Response:**
```json
{
  "status": "success",
  "total_freed_space_mb": 5432.1,
  "details": {
    "cache": {"total_freed_mb": 2100.5},
    "temp": {"total_freed_mb": 1500.3},
    "logs": {"total_freed_mb": 800.2},
    "trash": {"total_freed_mb": 900.1},
    "privacy": {"total_freed_mb": 131.0}
  }
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
