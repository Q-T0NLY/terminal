#!/bin/zsh
# ============================================================================
# .zprofile - Login Shell Configuration
# macOS Big Sur Intel - Enterprise Configuration
# ============================================================================
# This file is sourced for LOGIN shells (before .zshrc)
# Use for environment setup that should run once per login
# ============================================================================

# ============================================
# STARTUP DIAGNOSTICS
# ============================================

# Enable profiling if requested
if [[ -n "$ZSH_PROFILE" ]]; then
    zmodload zsh/zprof
fi

# ============================================
# HOMEBREW INITIALIZATION
# ============================================

# Intel Homebrew
if [[ "$IS_INTEL" == "true" ]] && [[ -f "/usr/local/bin/brew" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi

# ARM Homebrew (future compatibility)
if [[ "$IS_ARM" == "true" ]] && [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# ============================================
# VERSION MANAGER INITIALIZATION
# ============================================

# NVM (Node Version Manager)
if [[ -d "$NVM_DIR" ]] && [[ -s "$NVM_DIR/nvm.sh" ]]; then
    # Load NVM
    source "$NVM_DIR/nvm.sh"
    
    # Load NVM bash completion
    [[ -s "$NVM_DIR/bash_completion" ]] && source "$NVM_DIR/bash_completion"
    
    # Auto-use .nvmrc if present
    autoload -U add-zsh-hook
    load-nvmrc() {
        local node_version="$(nvm version)"
        local nvmrc_path="$(nvm_find_nvmrc)"
        
        if [[ -n "$nvmrc_path" ]]; then
            local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")
            
            if [[ "$nvmrc_node_version" = "N/A" ]]; then
                nvm install
            elif [[ "$nvmrc_node_version" != "$node_version" ]]; then
                nvm use
            fi
        elif [[ "$node_version" != "$(nvm version default)" ]]; then
            echo "Reverting to default Node version"
            nvm use default
        fi
    }
    add-zsh-hook chpwd load-nvmrc
    load-nvmrc
fi

# PYENV (Python Version Manager)
if command -v pyenv &>/dev/null; then
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    
    # Pyenv virtualenv
    if command -v pyenv-virtualenv-init &>/dev/null; then
        eval "$(pyenv virtualenv-init -)"
    fi
fi

# RBENV (Ruby Version Manager)
if command -v rbenv &>/dev/null; then
    eval "$(rbenv init - zsh)"
fi

# JENV (Java Version Manager)
if [[ -d "$JENV_ROOT" ]]; then
    eval "$(jenv init -)"
fi

# RVM (Ruby Version Manager)
if [[ -d "$RVM_DIR" ]] && [[ -s "$RVM_DIR/scripts/rvm" ]]; then
    source "$RVM_DIR/scripts/rvm"
fi

# ============================================
# SSH AGENT
# ============================================

# Start SSH agent if not running
if [[ -z "$SSH_AUTH_SOCK" ]]; then
    eval "$(ssh-agent -s)" >/dev/null
    
    # Add keys from .ssh directory
    if [[ -d "$HOME/.ssh" ]]; then
        for key in "$HOME"/.ssh/id_{rsa,ed25519,ecdsa}; do
            [[ -f "$key" ]] && ssh-add --apple-use-keychain "$key" 2>/dev/null
        done
    fi
fi

# ============================================
# GPG AGENT
# ============================================

# Setup GPG agent
if command -v gpg-agent &>/dev/null; then
    export GPG_TTY=$(tty)
    
    # Start gpg-agent if not running
    if ! pgrep -x gpg-agent &>/dev/null; then
        gpg-agent --daemon --use-standard-socket &>/dev/null
    fi
fi

# ============================================
# TERMINAL MULTIPLEXER AUTO-ATTACH
# ============================================

# Auto-attach to tmux session (disabled by default)
# Uncomment to enable
# if command -v tmux &>/dev/null && [[ -z "$TMUX" ]] && [[ -z "$INSIDE_EMACS" ]]; then
#     tmux attach-session -t default || tmux new-session -s default
# fi

# ============================================
# DIRECTORY BOOKMARKS SYSTEM
# ============================================

# Load directory bookmarks
export BOOKMARKS_FILE="${XDG_CONFIG_HOME}/zsh/bookmarks"
mkdir -p "$(dirname "$BOOKMARKS_FILE")"
touch "$BOOKMARKS_FILE"

# Bookmark functions
bookmark() {
    local name="$1"
    local path="${2:-$PWD}"
    
    if [[ -z "$name" ]]; then
        echo "Usage: bookmark <name> [path]"
        return 1
    fi
    
    echo "${name}:${path}" >> "$BOOKMARKS_FILE"
    echo "Bookmarked: $name -> $path"
}

goto() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        echo "Available bookmarks:"
        cat "$BOOKMARKS_FILE" | sed 's/:/ -> /'
        return 0
    fi
    
    local path=$(grep "^${name}:" "$BOOKMARKS_FILE" | cut -d: -f2- | tail -1)
    
    if [[ -n "$path" ]] && [[ -d "$path" ]]; then
        cd "$path"
    else
        echo "Bookmark not found: $name"
        return 1
    fi
}

# Tab completion for goto
compdef '_files -/' goto

# ============================================
# PROJECT DETECTION & AUTO-SETUP
# ============================================

# Auto-detect and setup project environments
auto_project_setup() {
    local current_dir="$PWD"
    
    # Node.js project
    if [[ -f "package.json" ]]; then
        export PROJECT_TYPE="nodejs"
        [[ -d "node_modules" ]] || echo "💡 Tip: Run 'npm install' to install dependencies"
    fi
    
    # Python project
    if [[ -f "requirements.txt" ]] || [[ -f "setup.py" ]] || [[ -f "pyproject.toml" ]]; then
        export PROJECT_TYPE="python"
        
        # Auto-activate virtualenv
        if [[ -d "venv" ]]; then
            source venv/bin/activate 2>/dev/null
        elif [[ -d ".venv" ]]; then
            source .venv/bin/activate 2>/dev/null
        fi
    fi
    
    # Ruby project
    if [[ -f "Gemfile" ]]; then
        export PROJECT_TYPE="ruby"
        [[ -d "vendor/bundle" ]] || echo "💡 Tip: Run 'bundle install' to install dependencies"
    fi
    
    # Go project
    if [[ -f "go.mod" ]]; then
        export PROJECT_TYPE="go"
    fi
    
    # Rust project
    if [[ -f "Cargo.toml" ]]; then
        export PROJECT_TYPE="rust"
    fi
    
    # Docker project
    if [[ -f "Dockerfile" ]] || [[ -f "docker-compose.yml" ]]; then
        export HAS_DOCKER="true"
    fi
    
    # Git repository
    if git rev-parse --git-dir &>/dev/null; then
        export GIT_REPO="true"
    fi
}

# Run auto-setup in current directory
auto_project_setup

# Hook for directory changes
autoload -U add-zsh-hook
add-zsh-hook chpwd auto_project_setup

# ============================================
# SYMLINK RESOLUTION SYSTEM
# ============================================

# Function to resolve all symlinks in path
resolve_symlinks() {
    local path="$1"
    local resolved=""
    
    if [[ -L "$path" ]]; then
        resolved="$(readlink -f "$path" 2>/dev/null || greadlink -f "$path" 2>/dev/null)"
        if [[ -n "$resolved" ]]; then
            echo "$resolved"
        else
            echo "$path"
        fi
    else
        echo "$path"
    fi
}

# Create symlink registry
export SYMLINK_REGISTRY="${XDG_STATE_HOME}/zsh/symlinks"
mkdir -p "$(dirname "$SYMLINK_REGISTRY")"

# Scan and register symlinks in PATH
register_path_symlinks() {
    > "$SYMLINK_REGISTRY"
    
    for dir in "${path[@]}"; do
        if [[ -L "$dir" ]]; then
            local target="$(resolve_symlinks "$dir")"
            echo "${dir} -> ${target}" >> "$SYMLINK_REGISTRY"
        fi
        
        # Check executables in directory
        if [[ -d "$dir" ]]; then
            for exe in "$dir"/*; do
                if [[ -L "$exe" ]]; then
                    local target="$(resolve_symlinks "$exe")"
                    echo "${exe} -> ${target}" >> "$SYMLINK_REGISTRY"
                fi
            done
        fi
    done
}

# Run symlink registration in background
(register_path_symlinks &) &>/dev/null

# ============================================
# SYSTEM HEALTH CHECK
# ============================================

# Check for common issues
check_system_health() {
    local warnings=()
    
    # Check disk space
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $disk_usage -gt 90 ]]; then
        warnings+=("⚠️  Disk space critical: ${disk_usage}% used")
    fi
    
    # Check for outdated Homebrew
    if command -v brew &>/dev/null; then
        local brew_age=$(find /usr/local/.git/FETCH_HEAD -mtime +7 2>/dev/null)
        if [[ -n "$brew_age" ]]; then
            warnings+=("💡 Homebrew hasn't been updated in 7+ days")
        fi
    fi
    
    # Check for zombie processes
    local zombies=$(ps aux | awk '{if($8=="Z") print $0}' | wc -l | tr -d ' ')
    if [[ $zombies -gt 0 ]]; then
        warnings+=("⚠️  Found ${zombies} zombie processes")
    fi
    
    # Display warnings
    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo ""
        echo "═══════════════════════════════════════════════"
        echo "  System Health Warnings"
        echo "═══════════════════════════════════════════════"
        for warning in "${warnings[@]}"; do
            echo "$warning"
        done
        echo "═══════════════════════════════════════════════"
        echo ""
    fi
}

# Run health check (async)
(check_system_health &) &>/dev/null

# ============================================
# WELCOME MESSAGE
# ============================================

# Display welcome message (only for interactive shells)
if [[ -o interactive ]]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  🧹 Enterprise Terminal with Clean Slate Factory Reset    ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "  Platform: ${PLATFORM}"
    echo "  macOS Version: ${MACOS_VERSION}"
    echo "  Shell: Zsh ${ZSH_VERSION}"
    echo "  Date: $(date '+%A, %B %d, %Y at %I:%M %p')"
    echo ""
fi

# ============================================
# END OF .zprofile
# ============================================
