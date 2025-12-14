#!/bin/zsh
# ============================================================================
# .zlogin - Login Shell Final Configuration
# macOS Big Sur Intel - Enterprise Configuration
# ============================================================================
# Sourced after .zshrc for login shells
# Use for final setup steps that need everything else loaded
# ============================================

# ============================================
# SESSION INITIALIZATION
# ============================================

# Session ID for tracking
export SESSION_ID="$(date +%Y%m%d_%H%M%S)_$$"
export SESSION_START_TIME="$(date +%s)"

# Session log file
export SESSION_LOG="${XDG_STATE_HOME}/zsh/sessions/${SESSION_ID}.log"
mkdir -p "$(dirname "$SESSION_LOG")"

# Log session start
{
    echo "Session started: $(date)"
    echo "User: $USER"
    echo "Hostname: $(hostname)"
    echo "TTY: $(tty)"
    echo "Shell: $SHELL ($ZSH_VERSION)"
    echo "Platform: $PLATFORM"
} > "$SESSION_LOG"

# ============================================
# DISPLAY SYSTEM SUMMARY
# ============================================

# Only for interactive shells
if [[ -o interactive ]] && [[ -z "$TMUX" ]]; then
    # System uptime
    local uptime_info=$(uptime | sed 's/.*up \([^,]*\),.*/\1/')
    
    # Load average
    local load_avg=$(uptime | awk -F'load averages:' '{print $2}' | xargs)
    
    # Disk usage
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}')
    
    # Memory usage (macOS)
    local mem_info=$(vm_stat | head -5 | tail -4)
    
    echo "  System Uptime: $uptime_info"
    echo "  Load Average: $load_avg"
    echo "  Disk Usage: $disk_usage"
    echo ""
fi

# ============================================
# AUTO-CLEANUP
# ============================================

# Clean old session logs (keep last 30)
(
    cd "${XDG_STATE_HOME}/zsh/sessions" 2>/dev/null || exit
    ls -t | tail -n +31 | xargs -I {} rm {} 2>/dev/null
) &

# Clean old zsh completion cache (older than 7 days)
find "${XDG_CACHE_HOME}/zsh" -name "*.zwc" -mtime +7 -delete 2>/dev/null &

# ============================================
# TMUX AUTO-ATTACH (Optional)
# ============================================

# Uncomment to auto-attach to tmux on login
# if command -v tmux &>/dev/null && [[ -z "$TMUX" ]] && [[ -z "$INSIDE_EMACS" ]]; then
#     # Try to attach to existing session or create new one
#     tmux attach-session -t default || tmux new-session -s default
# fi

# ============================================
# END OF .zlogin
# ============================================
