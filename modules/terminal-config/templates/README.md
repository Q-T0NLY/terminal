# 🖥️ Terminal Configuration Templates

This directory contains ZSH (Z Shell) configuration file templates used by the **Terminal Configuration Service** (Port 8005).

These templates are read by the FastAPI microservice to generate customized terminal configurations based on user-selected profiles, themes, and plugins.

---

## 📋 Configuration Files (120KB Total)

### Core ZSH Files (4 files - 39KB)

**[.zshrc](zshrc)** (15KB)
- Main ZSH configuration loaded on shell startup
- Plugin manager, theme engine, auto-completion
- Performance optimization, cross-platform support
- **Role**: Master configuration file

**[.zshenv](.zshenv)** (10KB)
- Environment variables (loaded first, always)
- PATH setup, language configs (Node, Python, Go, Rust, Java, Docker)
- Tool configurations
- **Role**: Environment initialization

**[.zprofile](.zprofile)** (11KB)
- Login shell configuration
- System detection, Homebrew setup, SSH agent, GPG config
- Startup messages
- **Role**: Login session setup

**[.zlogin](.zlogin)** (3KB)
- Additional login shell initialization
- Welcome message, system info display
- **Role**: Post-login setup

**[.zlogout](.zlogout)** (3KB)
- Cleanup on shell exit
- Session cleanup, history backup, temp cleanup
- **Role**: Graceful termination

---

### Extended Configuration (3 files - 78KB)

**[.zshrc_aliases](.zshrc_aliases)** (17KB)
- 450+ command aliases and shortcuts
- **Categories**:
  - Git shortcuts (ga, gco, gp, etc)
  - Docker shortcuts (dps, dimg, etc)
  - System utilities (ports, myip, etc)
  - Network tools
  - File operations
  - Development shortcuts
- **Role**: Productivity enhancement

**[.zshrc_custom](.zshrc_custom)** (42KB)
- 50+ custom functions for power users
- **Features**:
  - File operations (extract, mkcd, backup)
  - Git helpers (gitlog, gitclean)
  - System utilities (sysinfo, cleanup)
  - Network tools (scan, speedtest)
  - Developer tools
- **Role**: Advanced functionality

**[.zshrc_enterprise](.zshrc_enterprise)** (19KB)
- Enterprise security and compliance features
- **Features**:
  - Security checks and audit logging
  - Compliance mode (SOC2, ISO27001)
  - Encrypted backups
  - API key management
  - Session recording
- **Role**: Corporate environment support

---

## 🎨 Terminal Profiles

These files are combined into different profiles:

### ⚡ Minimal Profile
**Files**: `.zshenv` + `.zshrc` (core only)
- Fast startup (<50ms)
- Essential features only
- No heavy plugins
- **Use case**: Servers, minimal systems

### 🎨 Balanced Profile
**Files**: Minimal + `.zshrc_aliases`
- Good performance (~100ms)
- Useful aliases
- Popular plugins
- **Use case**: Daily development work

### 🚀 Power User Profile
**Files**: Balanced + `.zshrc_custom`
- Full features
- All custom functions
- Advanced integrations
- **Use case**: Power users, advanced workflows

### 💼 Enterprise Profile
**Files**: Power User + `.zshrc_enterprise`
- Complete feature set
- Security & compliance
- Audit logging
- **Use case**: Corporate environments, compliance requirements

---

## 📦 Installation

### Manual Installation

```bash
# Copy files to home directory
cp terminal-configs/.z* ~/

# Reload shell
source ~/.zshrc
```

### Using install.sh

```bash
# Automated installation with backup
./install.sh

# Select profile interactively
# Creates backups of existing configs
```

### Using TUI

```bash
# Launch interactive interface
python3 cli/ose_tui.py

# Navigate to: 4 (Terminal Profile Regeneration)
# Select desired profile
```

### Using Terminal Config Service

```bash
# Via microservice API
curl -X POST http://localhost:8005/api/v1/config/generate \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "balanced",
    "theme": "powerlevel10k",
    "plugins": ["git", "docker", "syntax-highlighting"]
  }'
```

---

## 🎯 Configuration Matrix

| File | Minimal | Balanced | Power User | Enterprise |
|------|---------|----------|------------|------------|
| .zshenv | ✅ | ✅ | ✅ | ✅ |
| .zshrc | ✅ | ✅ | ✅ | ✅ |
| .zprofile | ✅ | ✅ | ✅ | ✅ |
| .zlogin | ✅ | ✅ | ✅ | ✅ |
| .zlogout | ✅ | ✅ | ✅ | ✅ |
| .zshrc_aliases | ❌ | ✅ | ✅ | ✅ |
| .zshrc_custom | ❌ | ❌ | ✅ | ✅ |
| .zshrc_enterprise | ❌ | ❌ | ❌ | ✅ |

---

## 🔧 Customization

### Adding Custom Aliases

Edit `.zshrc_aliases`:
```bash
alias myalias='command'
```

### Adding Custom Functions

Edit `.zshrc_custom`:
```bash
function myfunction() {
    # Your code here
}
```

### Environment Variables

Edit `.zshenv`:
```bash
export MY_VAR="value"
```

---

## 🎨 Theme Support

Themes are configured in `.zshrc`:

- **Powerlevel10k** (recommended) - Modern, fast, customizable
- **Starship** - Cross-shell, minimal, fast
- **Agnoster** - Classic, git-aware
- **Pure** - Minimal, elegant
- **Custom** - DIY themes

---

## 🔌 Plugin Support

Common plugins enabled:

**Syntax Highlighting**
```bash
# Installed via: git clone https://github.com/zsh-users/zsh-syntax-highlighting
```

**Auto-suggestions**
```bash
# Installed via: git clone https://github.com/zsh-users/zsh-autosuggestions
```

**Git Integration**
- Built into .zshrc_aliases

**Docker Completion**
- Built into .zshrc_custom

---

## 📊 File Sizes & Line Counts

| File | Size | Lines | Features |
|------|------|-------|----------|
| .zshrc | 15KB | 400+ | Core config |
| .zshenv | 10KB | 280+ | Environment |
| .zprofile | 11KB | 300+ | Login setup |
| .zlogin | 3KB | 70+ | Post-login |
| .zlogout | 3KB | 75+ | Cleanup |
| .zshrc_aliases | 17KB | 450+ | Aliases |
| .zshrc_custom | 42KB | 1,100+ | Functions |
| .zshrc_enterprise | 19KB | 500+ | Enterprise |
| **Total** | **120KB** | **3,175+** | All features |

---

## 🔄 Backup & Restore

### Create Backup

```bash
# Using install.sh
./install.sh backup

# Manual backup
cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d)
```

### Restore from Backup

```bash
# Restore specific file
cp ~/.zshrc.backup.20251213 ~/.zshrc

# Restore all
./install.sh restore
```

---

## 🚀 Quick Start Examples

### Example 1: Install Balanced Profile
```bash
./install.sh
# Select: 2 (Balanced Profile)
# Confirm installation
source ~/.zshrc
```

### Example 2: Generate Custom Config via API
```bash
curl -X POST http://localhost:8005/api/v1/config/generate \
  -d '{"profile": "power-user", "theme": "starship"}'
```

### Example 3: Export Current Config
```bash
# Via TUI
python3 cli/ose_tui.py
# Menu: 4 → 10 (Export Config)
```

---

## 📚 Related Documentation

- **TUI Interface**: [../docs/TUI_INTERFACE.md](../docs/TUI_INTERFACE.md)
- **Terminal Config Service**: [../modules/terminal-config/README.md](../modules/terminal-config/README.md)
- **Installation Guide**: [../docs/README_INSTALL.md](../docs/README_INSTALL.md)
- **Package Summary**: [../docs/PACKAGE_SUMMARY.md](../docs/PACKAGE_SUMMARY.md)

---

## 🎯 Integration Points

These config files integrate with:

1. **[install.sh](../install.sh)** - Automated installer
2. **[cli/ose_tui.py](../cli/ose_tui.py)** - Interactive TUI (Menu #4)
3. **[modules/terminal-config/](../modules/terminal-config/)** - Microservice API
4. **Terminal Profile Regeneration** - System menu in TUI

---

## 📝 Notes

- Files start with `.` (dot) - they're hidden by default
- Must be in `$HOME` directory to work (symbolic links supported)
- Source order: `.zshenv` → `.zprofile` → `.zshrc` → `.zlogin`
- Exit order: `.zlogout`
- Compatible with: macOS, Linux (Ubuntu, Fedora, CentOS, Arch)

---

<div align="center">

**Part of the Terminal Profile Regeneration System**

*Professional • Customizable • Enterprise-Ready*

</div>
