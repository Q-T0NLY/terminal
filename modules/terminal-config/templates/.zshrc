#!/bin/zsh
# ============================================================================
# CLEANSLATESYSTEM - Advanced Zsh Configuration
# macOS Big Sur (Intel) - Production Grade Shell Environment
# Version: 3.0
# ============================================================================

# ============================================
# PERFORMANCE OPTIMIZATION - Load Time Tracking
# ============================================
CLEANSLATE_LOAD_START=$(date +%s.%N)

# ============================================
# CORE ENVIRONMENT SETUP
# ============================================

# Set locale
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

# Editor preferences
export EDITOR="vim"
export VISUAL="vim"
export PAGER="less"

# History configuration
export HISTFILE="${HOME}/.zsh_history"
export HISTSIZE=50000
export SAVEHIST=50000

# Advanced history options
setopt EXTENDED_HISTORY          # Write timestamp to history
setopt HIST_EXPIRE_DUPS_FIRST   # Expire duplicate entries first
setopt HIST_IGNORE_DUPS         # Don't record duplicate entries
setopt HIST_IGNORE_SPACE        # Don't record commands starting with space
setopt HIST_VERIFY              # Show command before running from history
setopt SHARE_HISTORY            # Share history between sessions
setopt INC_APPEND_HISTORY       # Write to history immediately

# ============================================
# PATH MANAGEMENT - Quantum Path Reconstruction
# ============================================

# Function to safely add to PATH if directory exists
add_to_path() {
    if [[ -d "$1" ]] && [[ ":$PATH:" != *":$1:"* ]]; then
        export PATH="$1:$PATH"
    fi
}

# Clear PATH and rebuild from scratch for clean state
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Homebrew paths (Intel Mac)
add_to_path "/usr/local/bin"
add_to_path "/usr/local/sbin"

# Apple Silicon Homebrew (if exists)
add_to_path "/opt/homebrew/bin"
add_to_path "/opt/homebrew/sbin"

# User local binaries
add_to_path "${HOME}/.local/bin"
add_to_path "${HOME}/bin"

# Development tools
add_to_path "/usr/local/opt/python/libexec/bin"
add_to_path "${HOME}/.cargo/bin"              # Rust
add_to_path "${HOME}/.npm-global/bin"         # npm global
add_to_path "/usr/local/go/bin"               # Go
add_to_path "${HOME}/go/bin"                  # Go workspace

# Clean Slate tools
add_to_path "${HOME}/.cleanslate/bin"

# ============================================
# SHELL OPTIONS & BEHAVIOR
# ============================================

# Directory navigation
setopt AUTO_CD              # cd by just typing directory name
setopt AUTO_PUSHD           # Make cd push old directory onto stack
setopt PUSHD_IGNORE_DUPS    # Don't push duplicates
setopt PUSHD_SILENT         # Don't print directory stack

# Globbing
setopt EXTENDED_GLOB        # Use extended globbing
setopt GLOB_DOTS            # Include dotfiles in globbing
setopt NO_CASE_GLOB         # Case insensitive globbing
setopt NUMERIC_GLOB_SORT    # Sort numeric filenames numerically

# Completion
setopt AUTO_MENU            # Show completion menu on successive tab press
setopt COMPLETE_IN_WORD     # Complete from both ends of a word
setopt ALWAYS_TO_END        # Move cursor to end after completion

# Correction
setopt CORRECT              # Spell check commands
setopt CORRECT_ALL          # Spell check all arguments

# Job control
setopt NO_BG_NICE           # Don't nice background jobs
setopt NO_HUP               # Don't kill jobs on exit
setopt NO_CHECK_JOBS        # Don't warn about running jobs on exit

# ============================================
# ZSH COMPLETION SYSTEM
# ============================================

# Load completion system
autoload -Uz compinit

# Only check cache once per day for faster startup
if [[ -n ${HOME}/.zcompdump(#qN.mh+24) ]]; then
    compinit
else
    compinit -C
fi

# Completion styling
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' special-dirs true
zstyle ':completion:*' squeeze-slashes true
zstyle ':completion:*:*:kill:*' menu yes select
zstyle ':completion:*:kill:*' force-list always
zstyle ':completion:*:*:*:*:processes' command "ps -u $USER -o pid,user,comm -w -w"

# ============================================
# KEY BINDINGS
# ============================================

# Use emacs key bindings
bindkey -e

# Custom key bindings
bindkey '^[[A' history-substring-search-up      # Up arrow
bindkey '^[[B' history-substring-search-down    # Down arrow
bindkey '^[[H' beginning-of-line                # Home
bindkey '^[[F' end-of-line                      # End
bindkey '^[[3~' delete-char                     # Delete
bindkey '^[[1;5C' forward-word                  # Ctrl+Right
bindkey '^[[1;5D' backward-word                 # Ctrl+Left

# ============================================
# COLORS & THEMING
# ============================================

# Enable colors
autoload -U colors && colors

# LS colors
export CLICOLOR=1
export LSCOLORS="ExGxBxDxCxEgEdxbxgxcxd"
export LS_COLORS='di=1;34:ln=1;36:so=1;31:pi=1;33:ex=1;32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=34;43'

# Grep colors
export GREP_COLOR='1;32'
export GREP_OPTIONS='--color=auto'

# Less colors
export LESS_TERMCAP_mb=$'\E[1;31m'     # begin bold
export LESS_TERMCAP_md=$'\E[1;36m'     # begin blink
export LESS_TERMCAP_me=$'\E[0m'        # reset bold/blink
export LESS_TERMCAP_so=$'\E[01;44;33m' # begin reverse video
export LESS_TERMCAP_se=$'\E[0m'        # reset reverse video
export LESS_TERMCAP_us=$'\E[1;32m'     # begin underline
export LESS_TERMCAP_ue=$'\E[0m'        # reset underline

# ============================================
# ENHANCED PROMPT - Multi-line with Git Integration
# ============================================

# Load vcs_info for git integration
autoload -Uz vcs_info
precmd_vcs_info() { vcs_info }
precmd_functions+=( precmd_vcs_info )
setopt PROMPT_SUBST

# Configure vcs_info
zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git:*' formats ' %F{yellow}(%b)%f'
zstyle ':vcs_info:git:*' actionformats ' %F{red}(%b|%a)%f'

# Custom prompt with system stats
PROMPT='
%F{cyan}╭─%f %F{green}%n@%m%f %F{blue}%~%f${vcs_info_msg_0_}
%F{cyan}╰─%f %(?.%F{green}.%F{red})❯%f '

# Right prompt with time and return code
RPROMPT='%F{yellow}%*%f %(?.%F{green}✓.%F{red}✗ %?)%f'

# ============================================
# ALIASES - Essential & Advanced
# ============================================

# Enhanced ls
alias ls='ls -G'
alias ll='ls -lhG'
alias la='ls -lahG'
alias l='ls -lG'
alias lt='ls -lhtrG'      # Sort by time
alias lsize='ls -lhSG'    # Sort by size

# Directory navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ~='cd ~'
alias -- -='cd -'

# Safety nets
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias mkdir='mkdir -pv'

# Enhanced commands
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias df='df -h'
alias du='du -h'
alias free='top -l 1 -s 0 | grep PhysMem'

# Network
alias myip='curl -s https://api.ipify.org && echo'
alias localip='ipconfig getifaddr en0'
alias ports='netstat -tulanp'
alias listening='lsof -iTCP -sTCP:LISTEN -n -P'

# System monitoring
alias cpu='top -o cpu'
alias mem='top -o mem'
alias psg='ps aux | grep -v grep | grep -i -e VSZ -e'

# Quick edits
alias zshrc='${EDITOR} ~/.zshrc'
alias zshcustom='${EDITOR} ~/.zshrc_custom'
alias vimrc='${EDITOR} ~/.vimrc'

# Git aliases
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gco='git checkout'
alias gb='git branch'
alias glog='git log --oneline --graph --decorate'

# macOS specific
alias showfiles='defaults write com.apple.finder AppleShowAllFiles YES; killall Finder'
alias hidefiles='defaults write com.apple.finder AppleShowAllFiles NO; killall Finder'
alias flushdns='sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder'
alias cleanup='sudo periodic daily weekly monthly'

# ============================================
# DEVELOPMENT TOOLS INTEGRATION
# ============================================

# Homebrew
if command -v brew &> /dev/null; then
    export HOMEBREW_NO_ANALYTICS=1
    export HOMEBREW_NO_AUTO_UPDATE=1
    alias brewup='brew update && brew upgrade && brew cleanup'
    alias brewinfo='brew info'
fi

# Python
if command -v python3 &> /dev/null; then
    alias python='python3'
    alias pip='pip3'
fi

# Node.js / npm
if command -v node &> /dev/null; then
    export NODE_OPTIONS="--max-old-space-size=4096"
fi

# Docker
if command -v docker &> /dev/null; then
    alias dps='docker ps'
    alias dpa='docker ps -a'
    alias di='docker images'
    alias drm='docker rm'
    alias drmi='docker rmi'
    alias dstop='docker stop $(docker ps -q)'
    alias dclean='docker system prune -af'
fi

# ============================================
# FUZZY FINDER (FZF) INTEGRATION
# ============================================

if command -v fzf &> /dev/null; then
    # Set up fzf key bindings
    [ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
    
    # Use fd instead of find if available
    if command -v fd &> /dev/null; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
    fi
    
    # Enhanced fzf options
    export FZF_DEFAULT_OPTS='
        --height 40%
        --layout=reverse
        --border
        --inline-info
        --color=fg:#d0d0d0,bg:#121212,hl:#5f87af
        --color=fg+:#d0d0d0,bg+:#262626,hl+:#5fd7ff
        --color=info:#afaf87,prompt:#d7005f,pointer:#af5fff
        --color=marker:#87ff00,spinner:#af5fff,header:#87afaf
    '
fi

# ============================================
# ZOXIDE (Smart Directory Jumping)
# ============================================

if command -v zoxide &> /dev/null; then
    eval "$(zoxide init zsh)"
    alias z='__zoxide_z'
    alias zi='__zoxide_zi'
fi

# ============================================
# BAT (Better Cat) INTEGRATION
# ============================================

if command -v bat &> /dev/null; then
    alias cat='bat --paging=never'
    alias catt='/bin/cat'
    export BAT_THEME="Dracula"
fi

# ============================================
# EZA (Modern LS) INTEGRATION
# ============================================

if command -v eza &> /dev/null; then
    alias ls='eza --icons'
    alias ll='eza -l --icons --git'
    alias la='eza -la --icons --git'
    alias tree='eza --tree --icons'
fi

# ============================================
# CUSTOM FUNCTIONS
# ============================================

# Quick directory creation and navigation
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract archives of any type
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"    ;;
            *.tar.gz)    tar xzf "$1"    ;;
            *.bz2)       bunzip2 "$1"    ;;
            *.rar)       unrar x "$1"    ;;
            *.gz)        gunzip "$1"     ;;
            *.tar)       tar xf "$1"     ;;
            *.tbz2)      tar xjf "$1"    ;;
            *.tgz)       tar xzf "$1"    ;;
            *.zip)       unzip "$1"      ;;
            *.Z)         uncompress "$1" ;;
            *.7z)        7z x "$1"       ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Find files by name
ff() {
    find . -type f -iname "*$1*"
}

# Find directories by name
fd() {
    find . -type d -iname "*$1*"
}

# Process finder
psgrep() {
    ps aux | grep -v grep | grep -i -e VSZ -e "$1"
}

# Quick server
serve() {
    local port="${1:-8000}"
    python3 -m http.server "$port"
}

# Git branch cleanup
gitclean() {
    git branch --merged | grep -v "\*" | grep -v master | grep -v main | xargs -n 1 git branch -d
}

# ============================================
# CLEANSLATESYSTEM INTEGRATION
# ============================================

# Load Clean Slate custom configuration
if [[ -f "${HOME}/.zshrc_custom" ]]; then
    source "${HOME}/.zshrc_custom"
fi

# Clean Slate quick commands
alias nova='cleanslate_system_menu'
alias cleanslate-scan='cleanslate_system_scan'
alias cleanslate-reset='cleanslate_cleanup_interface'
alias cleanslate-health='cleanslate_system_health'
alias cleanslate-backup='cleanslate_create_backup'

# ============================================
# PERFORMANCE - Load Time Display
# ============================================

CLEANSLATE_LOAD_END=$(date +%s.%N)
CLEANSLATE_LOAD_TIME=$(echo "$CLEANSLATE_LOAD_END - $CLEANSLATE_LOAD_START" | bc)

# Display load time on first prompt (only once)
if [[ ! -v CLEANSLATE_LOADED ]]; then
    echo "🚀 Clean Slate loaded in ${CLEANSLATE_LOAD_TIME}s"
    export CLEANSLATE_LOADED=1
fi

# ============================================
# ADDITIONAL TOOLS & INTEGRATIONS
# ============================================

# direnv (automatic environment switching)
if command -v direnv &> /dev/null; then
    eval "$(direnv hook zsh)"
fi

# thefuck (command correction)
if command -v thefuck &> /dev/null; then
    eval "$(thefuck --alias)"
fi

# iTerm2 shell integration
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# ============================================
# WELCOME MESSAGE
# ============================================

if [[ -o interactive ]]; then
    # Only show on interactive shells
    if [[ ! -v CLEANSLATE_WELCOME_SHOWN ]]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║            🌟 CLEANSLATESYSTEM - Factory Reset Ready 🌟              ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        echo "  Type 'cleanslate' for system menu | 'cleanslate-scan' for factory reset prep"
        echo ""
        export CLEANSLATE_WELCOME_SHOWN=1
    fi
fi

# ============================================
# END OF .zshrc
# ============================================
