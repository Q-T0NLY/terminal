# 🚀 OmniSystem Enhancer (OSE)

**The All-in-One System Optimization & Factory Reset Suite**

Transform system maintenance from a chore into an engaging, intuitive experience with powerful cleanup, optimization, factory reset, and package management capabilities.

---

## ✨ Features

### 🧹 System Cleanup & Junk Removal
- **Package Manager Caches** - APT, DNF, Pacman, Homebrew, pip, npm, cargo, etc.
- **Temporary Files** - /tmp, /var/tmp, Downloads cleanup
- **Log Management** - Intelligent rotation and compression
- **Duplicate Detection** - Find and remove duplicate files
- **Privacy Cleanup** - Browser history, cookies, recent documents

### ⚡ System Optimization & Tuning  
- **Startup Management** - Control startup applications and services
- **Kernel Tuning** - Optimize vm.swappiness, I/O schedulers
- **Memory Optimization** - Smart swap and zram management
- **Service Management** - Identify and stop resource hogs
- **Performance Profiling** - Boot time analysis and optimization

### 🔄 Factory Reset & System Restoration
- **Package Removal** - Remove user-installed packages, keep system packages
- **Config Purging** - Reset system settings and configurations
- **User Data Management** - Selective or complete user data wipe
- **Stateless Reset** - Clean /etc and /var for fresh start
- **Repository Cleanup** - Remove PPAs, AURs, custom repos

### 📦 Package Manager Management
- **Multi-PM Support** - APT, DNF, Pacman, Homebrew, Flatpak, Snap
- **Cache Optimization** - Clean and optimize package caches
- **Orphan Removal** - Remove orphaned dependencies
- **PM Migration** - Switch between package managers
- **⚠️ EXTREME: PM Removal** - Remove package managers (with safeguards)

### 💾 Quantum Backup System
- **Full System Snapshots** - Complete bootable system images
- **Incremental Backups** - Fast rsync-based backups
- **One-Click Rollback** - Restore entire system instantly
- **Compression** - SquashFS and zstd compression
- **Cloud Sync** - Optional cloud backup integration

### 🎨 Visual Interface (Coming Soon)
- **3D System Map** - Real-time filesystem visualization
- **Particle Effects** - Animated cleanup and optimization
- **Holographic Terminal** - Immersive command output
- **Adaptive Themes** - Dark, light, and neon modes

---

## 🚦 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/omnisystem-enhancer.git
cd omnisystem-enhancer

# Install dependencies
pip install -r requirements.txt

# Make CLI executable
chmod +x cli/ose.py

# Optional: Create symlink for system-wide access
sudo ln -s $(pwd)/cli/ose.py /usr/local/bin/ose
```

### Basic Usage

```bash
# Launch interactive dashboard
ose

# Run diagnostic scan
ose scan

# System cleanup
ose cleanup

# System optimization (coming soon)
ose optimize

# Factory reset (coming soon)
ose reset

# Quantum backup (coming soon)
ose backup

# Package manager management (coming soon)
ose pkg

# Show version
ose --version

# Show help
ose --help
```

---

## 📊 Example Workflows

### Workflow 1: Quick Cleanup

```bash
# Launch cleanup module
ose cleanup

# Select "Run all cleanup operations"
# This will:
# - Clean package manager caches
# - Remove temporary files
# - Clean old logs
# - Optionally find duplicates
# - Clear browser caches
```

**Expected Results:**
```
🧹 Cleaning caches...
  ✅ Freed 2.3 GB
🗑️  Cleaning temp files...
  ✅ Removed 1,247 files
📋 Cleaning logs...
  ✅ Removed 156 log files

🎉 Total space freed: 3.2 GB
```

### Workflow 2: System Health Check

```bash
# Run diagnostic scan
ose scan
```

**Output:**
```
╔═══════════════════ 📊 Diagnostic Results ═══════════════════╗
║                                                              ║
║  System Health: 87%                                          ║
║                                                              ║
║  📊 Disk Usage:                                              ║
║    • Total: 500.00 GB                                        ║
║    • Used: 350.00 GB                                         ║
║    • Junk: 3.20 GB                                           ║
║                                                              ║
║  ⚡ Performance:                                             ║
║    • Boot Time: 18.5s                                        ║
║    • Startup Apps: 12                                        ║
║    • Memory Usage: 65%                                       ║
║                                                              ║
║  📦 Packages:                                                ║
║    • Total: 1247                                             ║
║    • User Installed: 156                                     ║
║    • Orphaned: 23                                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Workflow 3: Full System Optimization (Coming Soon)

```bash
# 1. Create backup
ose backup

# 2. Run diagnostic
ose scan

# 3. Cleanup
ose cleanup

# 4. Optimize
ose optimize

# 5. Verify improvements
ose scan
```

---

## 🏗️ Architecture

```
omnisystem-enhancer/
├── ose/                          # Core application
│   ├── core/                     # Core engine
│   │   ├── orchestrator.py       # Main orchestration
│   │   ├── state_manager.py      # System state tracking
│   │   ├── config_loader.py      # YAML config parser
│   │   └── logger.py             # Advanced logging
│   ├── cleanup/                  # Cleanup module
│   │   ├── cache_cleaner.py
│   │   ├── temp_cleaner.py
│   │   ├── log_manager.py
│   │   ├── duplicate_finder.py
│   │   ├── privacy_cleaner.py
│   │   └── trash_manager.py
│   ├── optimize/                 # Optimization module (coming soon)
│   ├── factory_reset/            # Factory reset module (coming soon)
│   ├── pkg_manager/              # Package manager module (coming soon)
│   └── quantum_backup/           # Backup module (coming soon)
├── cli/                          # Command-line interface
│   └── ose.py                    # Main CLI entry point
├── config/                       # Configuration files
│   └── ose.yaml                  # Main configuration
├── docs/                         # Documentation
│   ├── OSE_ARCHITECTURE.md       # Full architecture
│   └── CLEANSLATE_GUIDE.md       # Original guide
└── requirements.txt              # Python dependencies
```

---

## ⚙️ Configuration

OSE uses YAML configuration files. Default config is created at `~/.ose/config/ose.yaml`:

```yaml
cleanup:
  enable_cache_cleanup: true
  enable_temp_cleanup: true
  enable_log_cleanup: true
  cache_max_age_days: 30
  log_max_age_days: 90
  
optimize:
  enable_startup_management: true
  enable_kernel_tuning: false  # Requires explicit enable
  target_boot_time: 15
  max_startup_apps: 5
  
factory_reset:
  enable_package_removal: true
  enable_user_data_wipe: false  # Requires explicit enable
  
backup:
  backup_location: "~/.ose/backups"
  compression_level: 6
  max_backups: 5
  
safety:
  ultra_paranoid_mode: false
  require_confirmation: true
  enable_dry_run: true
```

---

## 🛡️ Safety Features

### Multi-Level Protection

| Operation | Risk Level | Confirmations | Backup Required | Dry-Run |
|-----------|------------|---------------|-----------------|---------|
| Cleanup | 🟢 Low | 1x | Optional | ✅ Yes |
| Optimization | 🟡 Medium | 1x | Recommended | ✅ Yes |
| Factory Reset | 🔴 High | 3x | **Mandatory** | ✅ Yes |
| PM Removal | 🔴🔴 Extreme | 5x | **Mandatory** | ✅ Yes |

### Ultra-Paranoid Mode

When enabled, creates:
- Complete system snapshot before any changes
- Bootable recovery image
- Emergency recovery USB (optional)
- Detailed operation logs
- Rollback points at every step

---

## 📈 Roadmap

### Phase 1: Foundation ✅
- [x] Core architecture
- [x] Configuration system
- [x] State management
- [x] Advanced logging
- [x] CLI interface

### Phase 2: Cleanup Module ✅
- [x] Cache cleaning
- [x] Temp file removal
- [x] Log management
- [x] Duplicate detection
- [x] Privacy cleanup
- [x] Trash management

### Phase 3: Advanced Modules 🚧
- [ ] System optimization
- [ ] Factory reset
- [ ] Package manager management
- [ ] Quantum backup

### Phase 4: Visual Interface 📅
- [ ] 3D filesystem visualization
- [ ] Particle effects
- [ ] Holographic terminal
- [ ] Web dashboard

---

## 🤝 Contributing

Contributions welcome! Areas of focus:
- **Module Development** - Optimization, Factory Reset, Package Manager, Backup
- **Visual Interface** - 3D rendering, animations, themes
- **Testing** - Cross-platform testing, edge cases
- **Documentation** - Tutorials, examples, translations

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Built on top of excellent open-source tools:
- **BleachBit** - Privacy cleanup
- **Stacer** - System optimization
- **Resetter** - Factory reset inspiration
- **Rich** - Beautiful terminal output

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/omnisystem-enhancer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/omnisystem-enhancer/discussions)

---

**OmniSystem Enhancer** - Transform system maintenance into an art form! 🚀✨

*Bringing your system to peak performance with intelligence and style*
