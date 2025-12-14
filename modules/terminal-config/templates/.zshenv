#!/bin/zsh
# ============================================================================
# .zshenv - Environment Variables (Loaded FIRST, Always)
# macOS Big Sur Intel - Enterprise Configuration
# ============================================================================
# This file is sourced on ALL invocations of the shell.
# It should contain environment variables and PATH setup.
# ============================================================================

# ============================================
# SYSTEM DETECTION & ARCHITECTURE
# ============================================

# Detect OS and architecture
export OSTYPE_DETECTED="$(uname -s)"
export ARCH_DETECTED="$(uname -m)"
export OS_VERSION="$(sw_vers -productVersion 2>/dev/null || echo 'unknown')"

# macOS Big Sur specific
export MACOS_VERSION="${OS_VERSION}"
export IS_BIG_SUR="$([[ "$OS_VERSION" =~ ^11\. ]] && echo "true" || echo "false")"
export IS_INTEL="$([[ "$ARCH_DETECTED" == "x86_64" ]] && echo "true" || echo "false")"
export IS_ARM="$([[ "$ARCH_DETECTED" == "arm64" ]] && echo "true" || echo "false")"

# Set platform identifier
if [[ "$IS_INTEL" == "true" ]]; then
    export PLATFORM="macos-intel"
else
    export PLATFORM="macos-arm"
fi

# ============================================
# XDG BASE DIRECTORY SPECIFICATION
# ============================================

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp/runtime-$USER}"

# Create XDG directories
mkdir -p "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_CACHE_HOME" "$XDG_RUNTIME_DIR"

# ============================================
# CORE ENVIRONMENT VARIABLES
# ============================================

# User and system
export USER="${USER:-$(whoami)}"
export HOSTNAME="${HOSTNAME:-$(hostname -s)}"
export HOSTTYPE="${ARCH_DETECTED}"

# Default editor and pager
export EDITOR="vim"
export VISUAL="vim"
export PAGER="less"

# Language and locale
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"

# Terminal
export TERM="${TERM:-xterm-256color}"
export CLICOLOR=1
export COLORTERM="truecolor"

# ============================================
# SMART PATH CONSTRUCTION
# ============================================

# Initialize empty path array
typeset -U path  # Unique paths only
path=()

# Function to safely add to PATH
_add_to_path() {
    local dir="$1"
    # Resolve symlinks and add real path
    if [[ -d "$dir" ]]; then
        local real_dir="$(cd "$dir" 2>/dev/null && pwd -P)"
        if [[ -n "$real_dir" ]] && [[ ! "${path[@]}" =~ "$real_dir" ]]; then
            path+=("$real_dir")
        fi
    fi
}

# Function to prepend to PATH
_prepend_to_path() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        local real_dir="$(cd "$dir" 2>/dev/null && pwd -P)"
        if [[ -n "$real_dir" ]]; then
            path=("$real_dir" "${path[@]}")
        fi
    fi
}

# ===== SYSTEM PATHS =====
_add_to_path "/usr/local/bin"
_add_to_path "/usr/local/sbin"
_add_to_path "/usr/bin"
_add_to_path "/usr/sbin"
_add_to_path "/bin"
_add_to_path "/sbin"

# ===== INTEL-SPECIFIC HOMEBREW PATHS =====
if [[ "$IS_INTEL" == "true" ]]; then
    _prepend_to_path "/usr/local/opt/coreutils/libexec/gnubin"
    _prepend_to_path "/usr/local/opt/findutils/libexec/gnubin"
    _prepend_to_path "/usr/local/opt/gnu-sed/libexec/gnubin"
    _prepend_to_path "/usr/local/opt/grep/libexec/gnubin"
    _prepend_to_path "/usr/local/opt/make/libexec/gnubin"
    _prepend_to_path "/usr/local/bin"
    _prepend_to_path "/usr/local/sbin"
fi

# ===== ARM-SPECIFIC HOMEBREW PATHS (for future compatibility) =====
if [[ "$IS_ARM" == "true" ]]; then
    _prepend_to_path "/opt/homebrew/bin"
    _prepend_to_path "/opt/homebrew/sbin"
fi

# ===== USER PATHS =====
_prepend_to_path "$HOME/.local/bin"
_prepend_to_path "$HOME/bin"

# ===== DEVELOPMENT TOOL PATHS =====

# Python
if [[ -d "$HOME/Library/Python" ]]; then
    for pyver in "$HOME"/Library/Python/*/bin; do
        [[ -d "$pyver" ]] && _add_to_path "$pyver"
    done
fi
_add_to_path "/usr/local/opt/python/libexec/bin"

# Ruby (macOS system)
_add_to_path "/usr/local/opt/ruby/bin"
_add_to_path "/usr/local/lib/ruby/gems/3.0.0/bin"

# Node.js
_add_to_path "/usr/local/opt/node/bin"
_add_to_path "$HOME/.npm-global/bin"

# Go
if [[ -d "/usr/local/go/bin" ]]; then
    _add_to_path "/usr/local/go/bin"
    export GOPATH="${GOPATH:-$HOME/go}"
    _add_to_path "$GOPATH/bin"
fi

# Rust
if [[ -d "$HOME/.cargo/bin" ]]; then
    _add_to_path "$HOME/.cargo/bin"
    export CARGO_HOME="$HOME/.cargo"
    export RUSTUP_HOME="$HOME/.rustup"
fi

# Java
if /usr/libexec/java_home &>/dev/null; then
    export JAVA_HOME="$(/usr/libexec/java_home 2>/dev/null)"
    [[ -n "$JAVA_HOME" ]] && _add_to_path "$JAVA_HOME/bin"
fi

# Postgres
_add_to_path "/usr/local/opt/postgresql/bin"

# MySQL
_add_to_path "/usr/local/opt/mysql/bin"

# ===== ADDITIONAL TOOL PATHS =====
_add_to_path "/usr/local/opt/curl/bin"
_add_to_path "/usr/local/opt/openssl/bin"
_add_to_path "/usr/local/opt/sqlite/bin"

# Export the constructed PATH
export PATH="${(j/:/)path}"

# ============================================
# MANPATH CONFIGURATION
# ============================================

typeset -U manpath
manpath=()

_add_to_manpath() {
    [[ -d "$1" ]] && manpath+=("$1")
}

_add_to_manpath "/usr/local/share/man"
_add_to_manpath "/usr/share/man"
_add_to_manpath "/usr/local/opt/coreutils/libexec/gnuman"
_add_to_manpath "/usr/local/opt/findutils/libexec/gnuman"

export MANPATH="${(j/:/)manpath}"

# ============================================
# LIBRARY PATHS
# ============================================

typeset -U dyld_library_path
dyld_library_path=()

_add_to_dyld() {
    [[ -d "$1" ]] && dyld_library_path+=("$1")
}

_add_to_dyld "/usr/local/lib"
_add_to_dyld "/usr/lib"

export DYLD_LIBRARY_PATH="${(j/:/)dyld_library_path}"

# PKG_CONFIG_PATH
typeset -U pkg_config_path
pkg_config_path=()
[[ -d "/usr/local/lib/pkgconfig" ]] && pkg_config_path+=("/usr/local/lib/pkgconfig")
[[ -d "/usr/local/share/pkgconfig" ]] && pkg_config_path+=("/usr/local/share/pkgconfig")
export PKG_CONFIG_PATH="${(j/:/)pkg_config_path}"

# ============================================
# APPLICATION-SPECIFIC ENVIRONMENT
# ============================================

# Homebrew
export HOMEBREW_PREFIX="/usr/local"
export HOMEBREW_CELLAR="/usr/local/Cellar"
export HOMEBREW_REPOSITORY="/usr/local/Homebrew"
export HOMEBREW_NO_ANALYTICS=1
export HOMEBREW_NO_AUTO_UPDATE=1
export HOMEBREW_NO_INSTALL_CLEANUP=1

# Python
export PYTHONIOENCODING="utf-8"
export PYTHONDONTWRITEBYTECODE=1
export PIP_REQUIRE_VIRTUALENV=false
export PIPENV_VENV_IN_PROJECT=1

# Node.js
export NODE_ENV="${NODE_ENV:-development}"
export NPM_CONFIG_PREFIX="$HOME/.npm-global"

# Less
export LESS="-R -M -i -j10"
export LESSCHARSET="utf-8"

# Grep
export GREP_OPTIONS="--color=auto"
export GREP_COLOR="1;32"

# ls colors (BSD style for macOS)
export LSCOLORS="ExGxBxDxCxEgEdxbxgxcxd"

# GNU ls colors (if using GNU coreutils)
export LS_COLORS="di=1;34:ln=1;36:so=1;31:pi=1;33:ex=1;32:bd=1;34;46:cd=1;34;43:su=0;41:sg=0;46:tw=0;42:ow=0;43:"

# History
export HISTFILE="${XDG_STATE_HOME}/zsh/history"
export HISTSIZE=100000
export SAVEHIST=100000

# ============================================
# SECURITY & PERFORMANCE
# ============================================

# Disable .lesshst file
export LESSHISTFILE="-"

# Secure creation of files and directories
umask 022

# Core dump control
ulimit -c 0

# ============================================
# VERSION MANAGERS AUTO-DETECTION
# ============================================

# NVM (Node Version Manager)
export NVM_DIR="$HOME/.nvm"

# RVM (Ruby Version Manager)
export RVM_DIR="$HOME/.rvm"

# PYENV (Python Version Manager)
export PYENV_ROOT="$HOME/.pyenv"
if [[ -d "$PYENV_ROOT" ]]; then
    _prepend_to_path "$PYENV_ROOT/bin"
fi

# RBENV (Ruby Version Manager)
export RBENV_ROOT="$HOME/.rbenv"
if [[ -d "$RBENV_ROOT" ]]; then
    _prepend_to_path "$RBENV_ROOT/bin"
fi

# JENV (Java Version Manager)
export JENV_ROOT="$HOME/.jenv"
if [[ -d "$JENV_ROOT" ]]; then
    _prepend_to_path "$JENV_ROOT/bin"
fi

# ============================================
# CUSTOM APPLICATION PATHS
# ============================================

# Docker
if [[ -d "/Applications/Docker.app" ]]; then
    export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"
fi

# VS Code
if [[ -d "/Applications/Visual Studio Code.app" ]]; then
    _add_to_path "/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
fi

# Sublime Text
if [[ -d "/Applications/Sublime Text.app" ]]; then
    _add_to_path "/Applications/Sublime Text.app/Contents/SharedSupport/bin"
fi

# ============================================
# ENTERPRISE-SPECIFIC VARIABLES
# ============================================

# Build optimization for Intel
export ARCHFLAGS="-arch x86_64"
export CFLAGS="-O2 -march=native"
export CXXFLAGS="-O2 -march=native"

# Compilation cores (use all available)
export MAKEFLAGS="-j$(sysctl -n hw.ncpu)"

# ============================================
# STATE RECONSTRUCTION MARKER
# ============================================

# Create a state file for session reconstruction
export ZSH_STATE_FILE="${XDG_STATE_HOME}/zsh/session_state"
mkdir -p "$(dirname "$ZSH_STATE_FILE")"

# Save environment state
{
    echo "# Last environment initialization: $(date)"
    echo "export PATH='$PATH'"
    echo "export PLATFORM='$PLATFORM'"
    echo "export MACOS_VERSION='$MACOS_VERSION'"
} > "$ZSH_STATE_FILE"

# ============================================
# END OF .zshenv
# ============================================
