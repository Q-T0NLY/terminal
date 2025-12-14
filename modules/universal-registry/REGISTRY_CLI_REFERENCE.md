# 🚀 UREG - Quick Reference Card

## Universal Hyper Registry Management CLI v∞.10

---

## 📦 PLUGIN OPERATIONS

```bash
universal-registry-cli plugin add                    # ➕ Add new plugin
universal-registry-cli plugin install <id>           # 📥 Install plugin
universal-registry-cli plugin enable <id>            # ✅ Enable plugin
universal-registry-cli plugin disable <id>           # ⏸️ Disable plugin
universal-registry-cli plugin uninstall <id>         # 🗑️ Uninstall plugin
universal-registry-cli plugin remove <id>            # ❌ Remove plugin
universal-registry-cli plugin import plugins.json    # 📤 Import plugins
universal-registry-cli plugin export [file]          # 📦 Export plugins
universal-registry-cli plugin list                   # 📋 List all plugins
universal-registry-cli plugin config <id>            # ⚙️ Configure plugin
```

---

## ⚙️ SERVICE OPERATIONS

```bash
universal-registry-cli service add                   # ➕ Add new service
universal-registry-cli service install <id>          # 📥 Install service
universal-registry-cli service enable <id>           # ✅ Start service
universal-registry-cli service disable <id>          # ⏸️ Stop service
universal-registry-cli service uninstall <id>        # 🗑️ Uninstall service
universal-registry-cli service remove <id>           # ❌ Remove service
universal-registry-cli service import services.json  # 📤 Import services
universal-registry-cli service export [file]         # 📦 Export services
universal-registry-cli service list                  # 📋 List all services
universal-registry-cli service config <id>           # ⚙️ Configure service
```

---

## 🚀 ENGINE OPERATIONS

```bash
universal-registry-cli engine add                    # ➕ Add engine
universal-registry-cli engine install <id>           # 📥 Install engine
universal-registry-cli engine enable <id>            # ✅ Enable engine
universal-registry-cli engine disable <id>           # ⏸️ Disable engine
universal-registry-cli engine remove <id>            # ❌ Remove engine
universal-registry-cli engine list                   # 📋 List all engines
```

**Types**: processing, analytics, ai, compute, storage

---

## 📦 COMPONENT OPERATIONS

```bash
universal-registry-cli component add                 # ➕ Add component
universal-registry-cli component enable <id>         # ✅ Enable component
universal-registry-cli component disable <id>        # ⏸️ Disable component
universal-registry-cli component remove <id>         # ❌ Remove component
universal-registry-cli component list                # 📋 List all components
```

**Types**: cache, database, queue, storage, proxy

---

## 🏢 SUB-REGISTRY OPERATIONS

```bash
universal-registry-cli registry add                  # ➕ Add sub-registry
universal-registry-cli registry enable <id>          # ✅ Enable sub-registry
universal-registry-cli registry disable <id>         # ⏸️ Disable sub-registry
universal-registry-cli registry remove <id>          # ❌ Remove sub-registry
universal-registry-cli registry list                 # 📋 List all sub-registries
```

---

## 🎯 FEATURE OPERATIONS

```bash
universal-registry-cli feature add                   # ➕ Add feature
universal-registry-cli feature enable <id>           # ✅ Enable feature
universal-registry-cli feature disable <id>          # ⏸️ Disable feature
universal-registry-cli feature remove <id>           # ❌ Remove feature
universal-registry-cli feature list                  # 📋 List all features
```

---

## 🎛️ GRID OPERATIONS

```bash
universal-registry-cli grid add                      # ➕ Add grid node
universal-registry-cli grid enable <id>              # ✅ Enable node
universal-registry-cli grid disable <id>             # ⏸️ Disable node
universal-registry-cli grid remove <id>              # ❌ Remove node
universal-registry-cli grid list                     # 📋 List all nodes
```

**Types**: compute, storage, hybrid

---

## 🔧 CONFIGURATION OPERATIONS

```bash
universal-registry-cli config show                   # 👁️ Show configuration
universal-registry-cli config set <key> <value>      # ✏️ Set config value
universal-registry-cli config reset                  # 🔄 Reset to defaults
universal-registry-cli config export [file]          # 📦 Export config
universal-registry-cli config import <file>          # 📤 Import config
```

---

## 🌐 MESH OPERATIONS

```bash
universal-registry-cli mesh add-route                # ➕ Add route
universal-registry-cli mesh remove-route <id>        # ❌ Remove route
universal-registry-cli mesh list-routes              # 📋 List routes
universal-registry-cli mesh enable-tracing           # ✅ Enable tracing
universal-registry-cli mesh disable-tracing          # ⏸️ Disable tracing
```

**Protocols**: http, grpc, tcp  
**Load Balancing**: round-robin, least-conn, random

---

## 🆘 GENERAL COMMANDS

```bash
universal-registry-cli help                          # 📖 Show full help
universal-registry-cli version                       # ℹ️ Show version
universal-registry-cli health                        # 🏥 Health check
```

---

## 💡 QUICK EXAMPLES

### Deploy Plugin
```bash
universal-registry-cli plugin add
universal-registry-cli plugin install my-plugin-123
universal-registry-cli plugin enable my-plugin-123
```

### Export/Import Everything
```bash
# Export
universal-registry-cli plugin export plugins.json
universal-registry-cli service export services.json
universal-registry-cli config export config.json

# Import on another system
universal-registry-cli plugin import plugins.json
universal-registry-cli service import services.json
universal-registry-cli config import config.json
```

### Set Up Grid
```bash
universal-registry-cli grid add  # Add nodes
universal-registry-cli grid enable node-1
universal-registry-cli grid enable node-2
universal-registry-cli grid list
```

### Configure Service Mesh
```bash
universal-registry-cli mesh add-route
universal-registry-cli mesh enable-tracing
universal-registry-cli mesh list-routes
```

---

## 🔍 INTERACTIVE MODE

All `add` commands are interactive:
```bash
$ universal-registry-cli plugin add
  Plugin Name: ai-optimizer
  Version: 2.0.0
  Type: ai-ml
  Description: AI-powered optimizer
  Author: Your Name
  Repository URL: https://...
✓ Plugin added successfully
```

---

## ⚠️ SAFETY FEATURES

All `remove` commands require confirmation:
```bash
$ universal-registry-cli service remove critical-api
  Confirm removal of 'critical-api'? (yes/no): yes
✓ Service removed
```

---

## 📊 OUTPUT FORMATS

All `list` commands show formatted tables:
```
╔═══════════════════════════════════════════════════╗
║  🔌 Installed Plugins                             ║
╚═══════════════════════════════════════════════════╝

ID            Name                Version    Status
----------------------------------------------------
✓ plugin-001  AI Optimizer        2.0.0      active
○ plugin-002  Web3 Gateway        1.5.0      inactive
✓ plugin-003  Cloud Manager       3.0.0      active
```

---

## 🌟 ALIASES

Create shortcuts:
```bash
alias ua='universal-registry-cli plugin add'
alias ul='universal-registry-cli plugin list'
alias ue='universal-registry-cli plugin enable'
alias ud='universal-registry-cli plugin disable'
```

---

## 📚 MORE INFO

- Full Documentation: `universal-registry-cli help`
- Component Details: [COMPLETE_CRUD_OPERATIONS.md](COMPLETE_CRUD_OPERATIONS.md)
- Architecture: [CONSOLIDATED_ARCHITECTURE.md](CONSOLIDATED_ARCHITECTURE.md)
- Quick Start: [START_HERE.md](START_HERE.md)

---

**UREG v∞.10** - Your complete Universal Hyper Registry management tool! 🚀
