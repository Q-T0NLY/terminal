# ZSH Enterprise Configuration - Quick Reference
## macOS Big Sur Intel

---

## 🚀 Installation (30 seconds)

```bash
chmod +x install.sh && ./install.sh
# Follow prompts → Restart terminal → Done!
```

---

## 📂 Files Installed

| File | Purpose |
|------|---------|
| `.zshenv` | PATH & environment (always loaded) |
| `.zprofile` | Login setup (version managers, agents) |
| `.zshrc` | Main config (aliases, prompt, completions) |
| `.zlogin` | Session start (logging, cleanup) |
| `.zlogout` | Session end (cleanup, backup) |
| `.zshrc_custom` | Clean Slate features |
| `.zshrc_enterprise` | Alternative enterprise config |
| `.zshrc_aliases` | 100+ aliases with registry |

---

## ⚡ Essential Commands

### System
```bash
sysinfo          # System information
reload           # Reload zsh config
update           # Update Homebrew packages
cleanup          # Remove cache files
path             # Show PATH breakdown
```

### Navigation
```bash
..               # cd ..
...              # cd ../..
~                # cd ~
-                # cd to previous directory
mkcd <dir>       # Create and cd into directory
```

### Files
```bash
ll               # Long list with details
la               # List all including hidden
tree2            # Tree view depth 2
ff <name>        # Find files by name
fd <name>        # Find directories by name
extract <file>   # Extract any archive
```

### Git
```bash
gst              # git status
gco <branch>     # git checkout
glog             # git log --oneline --graph
gd               # git diff
ga <files>       # git add
gc -m "msg"      # git commit
gp               # git push
gpl              # git pull
```

### Development
```bash
serve [port]     # HTTP server (default 8000)
venv             # Create Python virtualenv
activate         # Activate virtualenv
py               # python3
pip              # pip3
```

### Docker
```bash
dps              # docker ps
dpa              # docker ps -a
dexec <id>       # docker exec -it
dprune           # docker system prune
```

### Clean Slate Initialization (Factory Reset)
```bash
cleanslate              # Factory reset control center
cleanslate-scan         # Scan system for reset
cleanslate-reset        # Interactive factory reset
cleanslate-health       # Pre-reset health check
cleanslate-backup       # Backup before reset
```

---

## 🎨 Aliases

### View & Search
```bash
listalias                # List all aliases
findalias <term>         # Search aliases
```

### Categories
- **File Operations**: ls, ll, la, cp, mv, rm, mkdir
- **Navigation**: .., ..., ...., ~, -
- **Search**: grep, fgrep, egrep, ff, fd
- **Process**: ps, psg, top, cpu, mem, ka
- **Network**: myip, localip, ports, ping
- **Git**: 40+ aliases (g, gst, gco, glog, etc.)
- **Docker**: d, dc, dps, dexec, dprune
- **Python**: py, pip, venv, activate
- **Node**: ni, nr, ns, nt, nb
- **System**: reload, update, cleanup

---

## 🔧 Customization

### Create Personal Config
```bash
# Create ~/.zshrc_local for your customizations
cat > ~/.zshrc_local << 'EOF'
# My custom aliases
alias myproject='cd ~/Projects/my-app'

# My environment variables
export MY_VAR='value'

# My functions
myfunc() {
    echo "My custom function"
}
EOF

# Reload
source ~/.zshrc
```

---

## 🐛 Troubleshooting

### Slow Startup
```bash
ZSH_PROFILE=1 zsh -ic exit    # Profile startup
rm -rf ~/.cache/zsh/*          # Clear cache
```

### PATH Problems
```bash
echo $PATH | tr ':' '\n'       # View PATH
source ~/.zshenv               # Reload PATH
```

### Completions Not Working
```bash
rm -f ~/.zcompdump*            # Remove completion cache
compinit                       # Rebuild completions
```

### Git Prompt Missing
```bash
which git                      # Verify git installed
vcs_info && echo $vcs_info_msg_0_  # Test git info
```

---

## 📊 Prompt Format

```
╭─ username@hostname ~/current/directory [git-branch]* (venv) ⬢ v16.0.0
╰─ ❯
```

**Indicators:**
- `*` = Uncommitted changes
- `+` = Staged changes
- `?` = Untracked files
- `↑n` = n commits ahead
- Green `❯` = Last command success
- Red `❯` = Last command failed
- Right side: `[time] ✓` or `✗ error-code`

---

## 🎯 Directory Structure Created

```
~/.config/zsh/              # Configuration files
~/.local/share/             # Data files
~/.local/state/zsh/         # State and history
  └── sessions/             # Session logs
~/.cache/zsh/               # Cache files
~/.local/bin/               # User binaries
~/.cleanslate/                    # Clean Slate
  ├── bin/
  ├── data/
  ├── logs/
  ├── reports/
  ├── trash/
  ├── config/
  └── cache/
```

---

## 🔑 Environment Variables

### Key Variables Set
```bash
PLATFORM          # macos-intel or macos-arm
IS_INTEL          # true/false
IS_BIG_SUR        # true/false
XDG_CONFIG_HOME   # ~/.config
XDG_DATA_HOME     # ~/.local/share
XDG_STATE_HOME    # ~/.local/state
XDG_CACHE_HOME    # ~/.cache
```

### Development Tools
```bash
GOPATH            # ~/go
CARGO_HOME        # ~/.cargo
JAVA_HOME         # Auto-detected
NVM_DIR           # ~/.nvm
PYENV_ROOT        # ~/.pyenv
RBENV_ROOT        # ~/.rbenv
```

---

## 📱 Functions

### Built-in Functions
```bash
mkcd <dir>               # Create and cd
extract <archive>        # Smart extraction
ff <pattern>             # Find files
fd <pattern>             # Find directories
ftext <pattern>          # Search in files
backup <file>            # Backup with timestamp
serve [port]             # HTTP server
ka <process> [signal]    # Kill by name
dirsize [path]           # Directory sizes
gclone <url>             # Clone and cd
resolve <path>           # Show symlink chain
sysinfo                  # System information
```

### Clean Slate Functions
```bash
collect_file_metadata <file>    # Get file metadata
classify_file <file>            # Classify file
nova_system_scan [path]         # Scan directory
nova_cleanup_interface          # Cleanup UI
nova_system_health              # Health check
nova_create_backup              # Backup system
```

---

## 🚦 Version Managers

### Auto-loaded
- **NVM**: Node.js versions (`.nvmrc` auto-use)
- **PYENV**: Python versions
- **RBENV**: Ruby versions  
- **JENV**: Java versions
- **RVM**: Ruby versions (if installed)

### Usage
```bash
nvm use <version>        # Switch Node version
pyenv local <version>    # Set Python version
rbenv local <version>    # Set Ruby version
jenv local <version>     # Set Java version
```

---

## ⚙️ Options Enabled

### History
- Extended history with timestamps
- Duplicate removal
- Shared across sessions
- Ignore commands starting with space

### Navigation
- Auto cd (type directory name)
- Auto pushd (directory stack)
- Case-insensitive globbing

### Completion
- Menu selection
- Fuzzy matching
- Case-insensitive
- Cached for speed

---

## 📦 Recommended Tools

### Install via Homebrew
```bash
brew install fzf bat eza ripgrep fd zoxide git-delta
brew install htop tree wget jq
brew install coreutils findutils gnu-sed grep
```

### Zsh Plugins
```bash
brew install zsh-completions
brew install zsh-syntax-highlighting
brew install zsh-autosuggestions
```

---

## 💡 Tips & Tricks

1. **Use Tab Completion**: Press `Tab` twice for menu
2. **Use Ctrl+R**: Search command history
3. **Use Aliases**: Type `listalias` to discover
4. **Use Functions**: Check docs for custom functions
5. **Customize Locally**: Use `~/.zshrc_local`
6. **Profile Startup**: Set `ZSH_PROFILE=1`
7. **Check PATH**: Use `path` command
8. **Resolve Symlinks**: Use `resolve <file>`

---

## 🎓 Learning Resources

### Zsh Documentation
- Zsh Manual: `man zsh`
- Completion: `man zshcompsys`
- Expansion: `man zshexpn`

### Quick Help
```bash
which <command>          # Find command location
whence <command>         # Show command type
type <command>           # Show command definition
alias <name>             # Show alias definition
```

---

## 🔄 Updates & Maintenance

### Keep Updated
```bash
update               # Update Homebrew packages
brew upgrade zsh     # Update zsh itself
```

### Backup Configuration
```bash
cleanslate-backup                                    # Clean Slate backup
tar -czf ~/zsh-backup.tar.gz ~/.zsh*          # Manual backup
```

### Clean Up
```bash
cleanup              # Remove cache files
rm -rf ~/.cache/zsh/*                        # Clear all cache
```

---

## 📋 Checklist After Installation

- [ ] Run `install.sh`
- [ ] Restart terminal
- [ ] Run `sysinfo` to verify
- [ ] Run `listalias` to explore
- [ ] Test `gst` in git repo
- [ ] Create `~/.zshrc_local` for customizations
- [ ] Install recommended tools
- [ ] Configure git: `git config --global user.name "Your Name"`
- [ ] Set up SSH keys if needed
- [ ] Enjoy your new terminal! 🎉

---

**Quick Reference Version 1.0**  
For detailed documentation, see `README_INSTALL.md`
