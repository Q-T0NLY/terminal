# Enterprise ZSH Terminal Configuration
## macOS Big Sur Intel - Complete Professional Setup

[![Platform](https://img.shields.io/badge/platform-macOS%20Big%20Sur-blue.svg)](https://www.apple.com/macos/)
[![Architecture](https://img.shields.io/badge/architecture-Intel%20x86__64-green.svg)](https://www.intel.com/)
[![Shell](https://img.shields.io/badge/shell-Zsh%205.8+-orange.svg)](https://www.zsh.org/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration Files](#-configuration-files)
- [Key Features](#-key-features)
- [Usage](#-usage)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Advanced Features](#-advanced-features)

---

## 🚀 Features

### Core Features
- ✅ **Auto-Detection System**: Automatic detection of OS, architecture, and available tools
- ✅ **Smart PATH Management**: Intelligent PATH construction with symlink resolution
- ✅ **Alias Auto-Propagation**: Comprehensive alias system with registry and categorization
- ✅ **Version Manager Integration**: Auto-loading for NVM, PYENV, RBENV, JENV, RVM
- ✅ **Project Auto-Setup**: Automatic environment configuration based on project type
- ✅ **Advanced Completions**: Intelligent tab completion with caching
- ✅ **Git Integration**: Rich prompt with branch info and status indicators
- ✅ **Performance Optimized**: Fast startup with lazy loading and caching

### Enterprise Features
- 🏢 **Session Management**: Comprehensive logging and state tracking
- 🏢 **Security**: SSH/GPG agent integration, secure file permissions
- 🏢 **Multi-Environment**: Support for development, staging, production configs
- 🏢 **Team Collaboration**: Shared configuration standards
- 🏢 **Audit Trail**: Command history with timestamps
- 🏢 **Resource Management**: Automatic cleanup and optimization

### Development Tools
- 🛠 **Python**: Virtual environment auto-activation, pip management
- 🛠 **Node.js**: NVM integration, npm/yarn shortcuts
- 🛠 **Ruby**: RVM/RBENV support, bundle management
- 🛠 **Go**: GOPATH auto-configuration
- 🛠 **Rust**: Cargo integration
- 🛠 **Docker**: Comprehensive docker/docker-compose aliases
- 🛠 **Git**: 40+ git aliases and functions

---

## ⚡ Quick Start

### One-Line Installation

```bash
git clone <repository-url> ~/zsh-config && cd ~/zsh-config && chmod +x install.sh && ./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone <repository-url> ~/zsh-config
cd ~/zsh-config

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

### Immediate Activation

```bash
# Restart your terminal OR
source ~/.zshrc
```

---

## 📦 Installation

### Prerequisites

**Required:**
- macOS Big Sur (11.x) - Intel
- Zsh 5.8 or later
- Git

**Recommended:**
- Homebrew package manager
- Internet connection (for optional tools)

### Installation Steps

1. **Run the Installer**
   ```bash
   ./install.sh
   ```

2. **Follow Prompts**
   - System detection
   - Backup creation
   - Configuration installation
   - Optional tool installation

3. **Restart Terminal**
   - Log out and log back in, OR
   - Run `source ~/.zshrc`

---

## 📁 Configuration Files

### Core Files

| File | Purpose | Load Order |
|------|---------|------------|
| `.zshenv` | Environment variables, PATH setup | 1st (always) |
| `.zprofile` | Login shell initialization | 2nd (login) |
| `.zshrc` | Interactive shell configuration | 3rd (interactive) |
| `.zlogin` | Final login setup | 4th (login) |
| `.zlogout` | Cleanup on logout | Last (logout) |

### Additional Files

| File | Purpose |
|------|---------|
| `.zshrc_custom` | Clean Slate advanced features |
| `.zshrc_enterprise` | Enterprise-grade configuration |
| `.zshrc_aliases` | Comprehensive alias collection |

### Directory Structure

```
~/.config/zsh/         # Configuration files
~/.local/share/        # Data files
~/.local/state/zsh/    # State and history
~/.cache/zsh/          # Cache files
~/.cleanslate/               # Clean Slate files
```

---

## 🔑 Key Features

### 1. Smart PATH Management

Automatically detects and adds to PATH:
- Homebrew binaries (Intel `/usr/local` or ARM `/opt/homebrew`)
- User binaries (`~/.local/bin`, `~/bin`)
- Language version managers (pyenv, rbenv, nvm, etc.)
- Development tools (Go, Rust, Python, Node, etc.)
- GNU utilities (coreutils, findutils, etc.)

### 2. Auto-Detection System

Detects and configures:
- Operating system and version
- CPU architecture (Intel vs ARM)
- Available package managers
- Installed development tools
- Project type (Node, Python, Ruby, etc.)
- Git repositories

### 3. Alias System

**Categories:**
- File operations (ls, cp, mv, etc.)
- Directory navigation (cd shortcuts)
- Search and find (grep, fgrep, egrep)
- Process management (ps, kill, top)
- Network utilities (ip, ports, ping)
- Git commands (40+ aliases)
- Docker operations
- Development tools

**Usage:**
```bash
listalias         # List all aliases
findalias <term>  # Search aliases
```

### 4. Advanced Prompt

Features:
- User and hostname
- Current directory (shortened if long)
- Git branch and status
- Python virtualenv indicator
- Node.js version (when in project)
- Exit code indicator
- Timestamp

### 5. Completion System

- **Smart matching**: Case-insensitive, fuzzy matching
- **Menu selection**: Visual completion menu
- **Caching**: Fast completions with 24-hour cache
- **Context-aware**: Different completions for different commands
- **SSH/SCP**: Host completion from known_hosts

---

## 💡 Usage

### Common Commands

```bash
# System Information
sysinfo           # Display system information

# Directory Navigation
..                # Go up one directory
...               # Go up two directories
~                 # Go to home directory
-                 # Go to previous directory

# File Operations
ll                # Long listing with human-readable sizes
la                # List all files including hidden
tree2             # Tree view with depth 2

# Search
ff <name>         # Find files by name
fd <name>         # Find directories by name
ftext <pattern>   # Search file contents

# Git
gst               # git status
gco <branch>      # git checkout
glog              # git log (pretty graph)
gclone <url>      # Clone and cd into repo

# Development
mkcd <dir>        # Create and cd into directory
extract <file>    # Extract any archive type
serve [port]      # Start HTTP server (default: 8000)

# Docker
dps               # docker ps
dexec <container> # docker exec -it
dprune            # Clean up docker system

# System
reload            # Reload zsh configuration
update            # Update Homebrew packages
cleanup           # Remove cache files
```

### Clean Slate Initialization Commands

```bash
cleanslate              # Factory Reset Control Center
cleanslate-scan         # Scan system for factory reset
cleanslate-reset        # Interactive factory reset interface
cleanslate-health       # Pre-reset health check
cleanslate-backup       # Backup before factory reset
```

**What is Clean Slate Initialization?**

Clean Slate is an intelligent factory reset preparation tool that:
- **Scans** your entire system and classifies files
- **Identifies** what's critical (OS), what's safe to remove (user files, apps)
- **Moves** files to trash (not delete) for safe recovery
- **Customizes** the reset process based on your needs
- **Backs up** important data before any changes
- **Restores** your system to a clean state with dynamic customizations

---

## 🎨 Customization

### Personal Customization

Create `~/.zshrc_local` for machine-specific settings:

```bash
# ~/.zshrc_local

# Custom aliases
alias myproject='cd ~/Projects/important-project'

# Custom environment variables
export MY_API_KEY='secret'

# Custom functions
myfunc() {
    echo "Hello from custom function"
}
```

### Modifying Existing Configuration

**Don't edit core files directly!** Instead:

1. **Add to `.zshrc_local`** for local changes
2. **Modify `.zshrc_custom`** for Clean Slate features
3. **Fork and maintain** your own version

### Theme Customization

Edit prompt in `.zshrc` or `.zshrc_enterprise`:

```bash
# Simple prompt
PROMPT='%F{green}%n@%m%f %F{blue}%~%f %# '

# Minimal prompt
PROMPT='%F{cyan}❯%f '

# Power prompt (current)
PROMPT='
%F{cyan}╭─%f %F{magenta}%n%f@%F{yellow}%m%f %F{blue}$(prompt_dir)%f${vcs_info_msg_0_}
%F{cyan}╰─%f %(?.%F{green}.%F{red})❯%f '
```

---

## 🔧 Troubleshooting

### Slow Startup

1. **Profile startup time:**
   ```bash
   ZSH_PROFILE=1 zsh -ic exit
   ```

2. **Disable plugins temporarily:**
   - Comment out sections in `.zshrc`
   - Test startup time

3. **Clear completion cache:**
   ```bash
   rm -rf ~/.cache/zsh/*
   ```

### PATH Issues

1. **Check PATH order:**
   ```bash
   echo $PATH | tr ':' '\n'
   ```

2. **Rebuild PATH:**
   ```bash
   source ~/.zshenv
   ```

3. **Verify symlinks:**
   ```bash
   resolve /usr/local/bin/python3
   ```

### Completion Not Working

1. **Rebuild completions:**
   ```bash
   rm -f ~/.zcompdump*
   compinit
   ```

2. **Check permissions:**
   ```bash
   chmod 755 ~/.config/zsh
   ```

### Git Prompt Issues

1. **Verify git is installed:**
   ```bash
   which git
   ```

2. **Test vcs_info:**
   ```bash
   vcs_info && echo $vcs_info_msg_0_
   ```

---

## 🚀 Advanced Features

### Version Manager Integration

**Automatic activation:**
- NVM: Auto-use `.nvmrc` files
- PYENV: Auto-switch Python versions
- RBENV: Auto-switch Ruby versions
- JENV: Auto-switch Java versions

**Manual override:**
```bash
nvm use <version>
pyenv local <version>
rbenv local <version>
jenv local <version>
```

### Project Auto-Setup

Detects and configures:
- **Node.js**: Checks for `package.json`
- **Python**: Activates virtualenv from `venv/` or `.venv/`
- **Ruby**: Detects `Gemfile`
- **Go**: Detects `go.mod`
- **Rust**: Detects `Cargo.toml`
- **Docker**: Detects `Dockerfile` or `docker-compose.yml`

### Symlink Resolution

```bash
resolve <file>    # Show symlink chain
```

**Features:**
- Recursive resolution
- Circular symlink detection
- Full path display
- Registry of all PATH symlinks

### Session Management

**Automatic logging:**
- Session start/end times
- Command count
- Duration tracking
- TTY information

**View session logs:**
```bash
ls ~/.local/state/zsh/sessions/
```

### Bookmark System

```bash
bookmark <name> [path]   # Create bookmark
goto <name>              # Jump to bookmark
goto                     # List all bookmarks
```

---

## 📊 Performance

### Optimizations

- ✅ Lazy loading of version managers
- ✅ Completion caching (24-hour refresh)
- ✅ Background process cleanup
- ✅ Minimal prompt rendering
- ✅ Compiled completion functions

### Benchmarks

Typical startup times on Intel Mac:
- **Cold start**: ~0.3-0.5 seconds
- **Warm start**: ~0.1-0.2 seconds

---

## 🤝 Contributing

### Reporting Issues

Include:
- macOS version
- Zsh version (`zsh --version`)
- Architecture (`uname -m`)
- Error messages
- Steps to reproduce

### Feature Requests

Submit detailed descriptions of:
- Use case
- Expected behavior
- Examples

---

## 📄 License

This configuration is provided as-is for personal and enterprise use.

---

## 🙏 Acknowledgments

Built with inspiration from:
- Oh My Zsh
- Prezto
- Zim
- Antibody
- And the amazing Zsh community

---

## 📞 Support

For questions or support:
1. Check this README
2. Review configuration files
3. Check issue tracker
4. Review zsh documentation

---

**Enjoy your enterprise-grade terminal environment! 🎉**
