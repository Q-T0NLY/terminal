#!/bin/zsh
# ============================================================================
# .zlogout - Logout Shell Configuration
# macOS Big Sur Intel - Enterprise Configuration
# ============================================================================
# Sourced when a login shell exits
# ============================================================================

# ============================================
# SESSION CLEANUP
# ============================================

# Log session end
if [[ -n "$SESSION_LOG" ]] && [[ -f "$SESSION_LOG" ]]; then
    {
        echo ""
        echo "Session ended: $(date)"
        
        # Calculate session duration
        if [[ -n "$SESSION_START_TIME" ]]; then
            local end_time=$(date +%s)
            local duration=$((end_time - SESSION_START_TIME))
            local hours=$((duration / 3600))
            local minutes=$(((duration % 3600) / 60))
            local seconds=$((duration % 60))
            
            echo "Session duration: ${hours}h ${minutes}m ${seconds}s"
        fi
        
        # Command count
        if [[ -f "$HISTFILE" ]]; then
            local cmd_count=$(tail -1000 "$HISTFILE" | wc -l | tr -d ' ')
            echo "Commands executed (last 1000): $cmd_count"
        fi
    } >> "$SESSION_LOG"
fi

# ============================================
# TEMPORARY FILE CLEANUP
# ============================================

# Clean up any temporary files created during session
rm -f /tmp/.zsh-${USER}-* 2>/dev/null

# Clean socket files
rm -f /tmp/ssh-*/${USER}-agent.* 2>/dev/null

# ============================================
# BACKUP IMPORTANT DATA
# ============================================

# Backup command history
if [[ -f "$HISTFILE" ]]; then
    cp "$HISTFILE" "${HISTFILE}.backup.$(date +%Y%m%d)" 2>/dev/null
fi

# ============================================
# CLEAR SCREEN (Optional)
# ============================================

# Uncomment to clear screen on logout
# clear

# ============================================
# FAREWELL MESSAGE
# ============================================

if [[ -o interactive ]]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              Goodbye! Session terminated.                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
fi

# ============================================
# END OF .zlogout
# ============================================
