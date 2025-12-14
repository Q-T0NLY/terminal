# 🔧 Terminal Config Service

**ZSH Configuration Generation & Management with Themes and Cloud Sync**

## Directory Structure

```
terminal-config/
├── main.py              - FastAPI application (350 lines)
├── Dockerfile           - Container definition
├── requirements.txt     - Python dependencies
├── README.md            - This file
├── .dockerignore        - Build optimization
├── run.sh               - Quick start script
└── templates/           - ZSH configuration templates (120KB)
    ├── README.md        - Template documentation
    ├── .zshrc           - Main ZSH config (15KB)
    ├── .zshenv          - Environment variables (10KB)
    ├── .zprofile        - Login shell config (11KB)
    ├── .zlogin          - Post-login setup (3KB)
    ├── .zlogout         - Exit cleanup (3KB)
    ├── .zshrc_aliases   - Command aliases (17KB)
    ├── .zshrc_custom    - Custom functions (42KB)
    └── .zshrc_enterprise - Enterprise features (19KB)
```

## Overview

The Terminal Config Service provides dynamic ZSH configuration generation with support for popular themes, plugins, and cloud synchronization. It offers pre-built profiles for different user types and allows extensive customization.

**The service reads configuration templates from the `templates/` directory** to generate customized ZSH configs based on user requests.

## Features

- ✅ **4 Configuration Profiles** - Minimal, Standard, Enterprise, Power User
- ✅ **Popular Themes** - Powerlevel10k, Starship, Agnoster
- ✅ **Plugin Ecosystem** - Autosuggestions, Syntax Highlighting, FZF, Z
- ✅ **Version Managers** - Auto-detection for nvm, pyenv, rbenv, goenv
- ✅ **Custom Aliases** - User-defined aliases and functions
- ✅ **Cloud Sync** - S3/MinIO integration (planned)
- ✅ **Git Versioning** - Configuration version control (planned)

## Quick Start

### Docker

```bash
# Build
docker build -t ose/terminal-config .

# Run
docker run -p 8005:8005 ose/terminal-config

# Test
curl http://localhost:8005/health
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main.py

# Access API docs
open http://localhost:8005/docs
```

## API Endpoints

### GET /api/v1/profiles
Get available configuration profiles

**Response:**
```json
{
  "profiles": [
    {
      "id": "minimal",
      "name": "Minimal",
      "description": "Lightweight ZSH with essentials",
      "features": ["basic_aliases", "history", "completion"]
    },
    {
      "id": "standard",
      "name": "Standard",
      "description": "Standard ZSH setup",
      "features": ["aliases", "history", "completion", "syntax_highlighting"]
    },
    {
      "id": "enterprise",
      "name": "Enterprise",
      "description": "Advanced enterprise configuration",
      "features": [
        "auto_detection", "path_management", "version_managers",
        "syntax_highlighting", "auto_suggestions", "themes"
      ]
    },
    {
      "id": "power_user",
      "name": "Power User",
      "description": "Maximum features and customization",
      "features": [
        "auto_detection", "advanced_completion", "fuzzy_finder",
        "git_integration", "kubernetes", "docker", "aws", "gcp"
      ]
    }
  ]
}
```

### GET /api/v1/themes
Get available themes

**Response:**
```json
{
  "themes": [
    {
      "id": "powerlevel10k",
      "name": "Powerlevel10k",
      "author": "romkatv",
      "repo": "romkatv/powerlevel10k",
      "popularity": 100
    },
    {
      "id": "starship",
      "name": "Starship",
      "author": "starship",
      "repo": "starship/starship",
      "popularity": 95
    },
    {
      "id": "agnoster",
      "name": "Agnoster",
      "author": "agnoster",
      "repo": "agnoster/agnoster-zsh-theme",
      "popularity": 85
    }
  ]
}
```

### GET /api/v1/plugins
Get available plugins

**Query Parameters:**
- `category` (optional): Filter by category (productivity, visual, navigation)

**Response:**
```json
{
  "total": 4,
  "plugins": [
    {
      "id": "zsh-autosuggestions",
      "name": "Autosuggestions",
      "description": "Fish-like autosuggestions",
      "category": "productivity",
      "repo": "zsh-users/zsh-autosuggestions"
    },
    {
      "id": "zsh-syntax-highlighting",
      "name": "Syntax Highlighting",
      "description": "Fish-like syntax highlighting",
      "category": "visual",
      "repo": "zsh-users/zsh-syntax-highlighting"
    }
  ]
}
```

### POST /api/v1/config/generate
Generate ZSH configuration

**Request:**
```json
{
  "profile": "enterprise",
  "theme": "powerlevel10k",
  "plugins": ["zsh-autosuggestions", "zsh-syntax-highlighting", "fzf"],
  "custom_aliases": {
    "ll": "ls -lah",
    "gs": "git status"
  },
  "enable_auto_detection": true
}
```

**Response:**
```json
{
  "config_id": "config_20231213_143022",
  "generated_files": [
    ".zshrc",
    ".zshenv",
    ".zprofile",
    ".p10k.zsh"
  ],
  "download_url": "https://ose.example.com/configs/config_20231213_143022.zip",
  "git_repo": "https://github.com/ose/configs/config_20231213_143022"
}
```

### GET /api/v1/config/{config_id}
Get generated configuration

**Response:**
```json
{
  "config_id": "config_20231213_143022",
  "status": "available",
  "files": [".zshrc", ".zshenv", ".zprofile", ".p10k.zsh"],
  "download_url": "https://ose.example.com/configs/config_20231213_143022.zip"
}
```

## Configuration Profiles

### Minimal
**Best for:** New users, minimal setups  
**Features:**
- Basic aliases
- History management
- Tab completion

**Startup time:** ~50ms

### Standard
**Best for:** General use  
**Features:**
- All Minimal features
- Syntax highlighting
- Git integration
- Common aliases

**Startup time:** ~100ms

### Enterprise
**Best for:** Professional developers  
**Features:**
- All Standard features
- Auto-detection (OS, tools, projects)
- PATH management
- Version managers (nvm, pyenv, rbenv)
- Advanced aliases
- Performance optimization

**Startup time:** ~150ms

### Power User
**Best for:** Advanced users, DevOps  
**Features:**
- All Enterprise features
- Advanced completions
- Fuzzy finder (fzf)
- Kubernetes integration
- Docker integration
- Cloud CLIs (AWS, GCP, Azure)
- Custom prompt engineering

**Startup time:** ~200ms

## Supported Themes

### Powerlevel10k
- ✅ Fast and customizable
- ✅ Instant prompt
- ✅ Configuration wizard
- ✅ Git status
- ✅ Battery indicator
- ✅ Cloud provider indicators

### Starship
- ✅ Cross-shell compatible
- ✅ Minimal and fast
- ✅ Modern design
- ✅ Language version indicators
- ✅ Git status
- ✅ Cloud context

### Agnoster
- ✅ Classic design
- ✅ Powerline fonts
- ✅ Git status
- ✅ Simple and clean

## Supported Plugins

### Productivity
- **zsh-autosuggestions** - Fish-like suggestions based on history
- **fzf** - Fuzzy finder for files, history, and more
- **z** - Directory jumper based on frequency

### Visual
- **zsh-syntax-highlighting** - Fish-like syntax highlighting
- **colorls** - Colorful ls with icons

### Development
- **git** - Git aliases and functions
- **docker** - Docker completions and aliases
- **kubectl** - Kubernetes completions

## Environment Variables

```bash
GIT_REPO_URL=https://github.com/ose/configs
S3_BUCKET=ose-configs
DATABASE_URL=postgresql://user:pass@postgres:5432/ose
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
```

## Docker Compose Integration

```yaml
terminal-config:
  build:
    context: ./modules/terminal-config
  ports:
    - "8005:8005"
  environment:
    - DATABASE_URL=postgresql://ose:password@postgres:5432/ose
    - REDIS_URL=redis://redis:6379
    - GIT_REPO_URL=https://github.com/ose/configs
  volumes:
    - config_data:/app/configs
  networks:
    - ose-network
```

## Health Check

```bash
curl http://localhost:8005/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-13T14:30:22.123456",
  "service": "terminal-config"
}
```

## Examples

### Generate Minimal Config

```bash
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "minimal",
    "theme": "starship",
    "plugins": []
  }' | jq
```

### Generate Enterprise Config with Powerlevel10k

```bash
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "enterprise",
    "theme": "powerlevel10k",
    "plugins": ["zsh-autosuggestions", "zsh-syntax-highlighting"],
    "enable_auto_detection": true
  }' | jq
```

### Generate Power User Config

```bash
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "power_user",
    "theme": "powerlevel10k",
    "plugins": ["zsh-autosuggestions", "zsh-syntax-highlighting", "fzf", "z"],
    "custom_aliases": {
      "k": "kubectl",
      "tf": "terraform",
      "d": "docker"
    },
    "enable_auto_detection": true
  }' | jq
```

## Installation (Generated Config)

Once you generate a configuration:

1. **Download the config:**
   ```bash
   wget https://ose.example.com/configs/config_20231213_143022.zip
   unzip config_20231213_143022.zip
   ```

2. **Backup existing config:**
   ```bash
   mv ~/.zshrc ~/.zshrc.backup
   ```

3. **Install generated config:**
   ```bash
   cp .zshrc ~/.zshrc
   cp .zshenv ~/.zshenv
   cp .zprofile ~/.zprofile
   ```

4. **Restart terminal or source:**
   ```bash
   source ~/.zshrc
   ```

## Best Practices

1. **Start minimal** - Begin with minimal profile, add features as needed
2. **Test themes** - Try different themes to find your favorite
3. **Enable auto-detection** - Automatically detect tools and environments
4. **Version control** - Keep your config in Git
5. **Backup** - Always backup before installing new config
6. **Incremental plugins** - Add plugins one at a time to avoid conflicts

## Troubleshooting

### Slow Startup

**Problem:** ZSH takes too long to start

**Solution:**
- Use minimal or standard profile
- Disable unused plugins
- Enable lazy loading
- Profile startup: `zsh -xv`

### Theme Not Working

**Problem:** Theme doesn't display correctly

**Solution:**
- Install Nerd Fonts
- Check terminal true color support
- Verify theme installation

### Plugins Not Loading

**Problem:** Plugins don't work

**Solution:**
- Check plugin installation path
- Verify plugin compatibility
- Check for conflicts

## License

MIT License

## Support

- API Documentation: http://localhost:8005/docs
- Health Check: http://localhost:8005/health
- GitHub Issues: Report bugs and request features
