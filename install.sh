#!/usr/bin/env bash
# ============================================================================
# ZSH Enterprise Configuration Installer
# macOS Big Sur Intel - Complete Setup Script
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${HOME}/.zsh_config_backup_$(date +%Y%m%d_%H%M%S)"

# ============================================
# HELPER FUNCTIONS
# ============================================

print_header() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC} $1"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

confirm() {
    local prompt="$1"
    local default="${2:-y}"
    local answer
    
    if [[ "$default" == "y" ]]; then
        read -rp "$(echo -e "${YELLOW}?${NC} ${prompt} [Y/n]: ")" answer
        answer=${answer:-y}
    else
        read -rp "$(echo -e "${YELLOW}?${NC} ${prompt} [y/N]: ")" answer
        answer=${answer:-n}
    fi
    
    [[ "$answer" =~ ^[Yy] ]]
}

# ============================================
# SYSTEM DETECTION
# ============================================

detect_system() {
    print_header "Detecting System Configuration"
    
    OS_TYPE="$(uname -s)"
    ARCH_TYPE="$(uname -m)"
    OS_VERSION="$(sw_vers -productVersion 2>/dev/null || echo 'unknown')"
    
    print_info "OS: ${OS_TYPE}"
    print_info "Architecture: ${ARCH_TYPE}"
    print_info "Version: ${OS_VERSION}"
    
    # Verify macOS Big Sur
    if [[ ! "$OS_VERSION" =~ ^11\. ]]; then
        print_warning "This configuration is optimized for macOS Big Sur (11.x)"
        print_info "Detected version: ${OS_VERSION}"
        
        if ! confirm "Continue anyway?"; then
            print_error "Installation cancelled"
            exit 1
        fi
    fi
    
    # Verify Intel architecture
    if [[ "$ARCH_TYPE" != "x86_64" ]]; then
        print_warning "This configuration is optimized for Intel (x86_64)"
        print_info "Detected architecture: ${ARCH_TYPE}"
        
        if ! confirm "Continue anyway?"; then
            print_error "Installation cancelled"
            exit 1
        fi
    fi
    
    print_success "System detection complete"
}

# ============================================
# BACKUP EXISTING CONFIGURATION
# ============================================

backup_existing() {
    print_header "Backing Up Existing Configuration"
    
    mkdir -p "$BACKUP_DIR"
    print_info "Backup directory: ${BACKUP_DIR}"
    
    local files=(
        ".zshenv"
        ".zprofile"
        ".zshrc"
        ".zlogin"
        ".zlogout"
        ".zshrc_custom"
        ".zshrc_enterprise"
        ".zshrc_aliases"
    )
    
    local backed_up=0
    
    for file in "${files[@]}"; do
        if [[ -f "${HOME}/${file}" ]]; then
            cp "${HOME}/${file}" "${BACKUP_DIR}/"
            print_success "Backed up: ${file}"
            ((backed_up++))
        fi
    done
    
    if [[ $backed_up -eq 0 ]]; then
        print_info "No existing configuration files found"
    else
        print_success "Backed up ${backed_up} file(s)"
    fi
}

# ============================================
# INSTALL ZSH CONFIGURATION FILES
# ============================================

install_configs() {
    print_header "Installing Configuration Files"
    
    local files=(
        ".zshenv"
        ".zprofile"
        ".zshrc"
        ".zlogin"
        ".zlogout"
        ".zshrc_custom"
        ".zshrc_enterprise"
        ".zshrc_aliases"
    )
    
    for file in "${files[@]}"; do
        if [[ -f "${SCRIPT_DIR}/${file}" ]]; then
            cp "${SCRIPT_DIR}/${file}" "${HOME}/"
            chmod 644 "${HOME}/${file}"
            print_success "Installed: ${file}"
        else
            print_warning "Not found: ${file}"
        fi
    done
}

# ============================================
# CREATE DIRECTORY STRUCTURE
# ============================================

create_directories() {
    print_header "Creating Directory Structure"
    
    local directories=(
        "${HOME}/.config"
        "${HOME}/.local/share"
        "${HOME}/.local/state"
        "${HOME}/.cache"
        "${HOME}/.local/bin"
        "${HOME}/.config/zsh"
        "${HOME}/.local/state/zsh"
        "${HOME}/.local/state/zsh/sessions"
        "${HOME}/.cache/zsh"
        "${HOME}/.nova"
        "${HOME}/.nova/bin"
        "${HOME}/.nova/data"
        "${HOME}/.nova/logs"
        "${HOME}/.nova/reports"
        "${HOME}/.nova/trash"
        "${HOME}/.nova/config"
        "${HOME}/.nova/cache"
    )
    
    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            print_success "Created: ${dir}"
        else
            print_info "Exists: ${dir}"
        fi
    done
}

# ============================================
# CHECK DEPENDENCIES
# ============================================

check_dependencies() {
    print_header "Checking Dependencies"
    
    local required_tools=("zsh" "git")
    local optional_tools=("brew" "fzf" "bat" "eza" "ripgrep" "fd")
    
    # Required tools
    print_info "Required tools:"
    for tool in "${required_tools[@]}"; do
        if command -v "$tool" &>/dev/null; then
            print_success "${tool} is installed"
        else
            print_error "${tool} is NOT installed"
        fi
    done
    
    # Optional tools
    echo ""
    print_info "Optional tools (recommended):"
    for tool in "${optional_tools[@]}"; do
        if command -v "$tool" &>/dev/null; then
            print_success "${tool} is installed"
        else
            print_warning "${tool} is not installed (optional)"
        fi
    done
}

# ============================================
# INSTALL RECOMMENDED TOOLS
# ============================================

install_tools() {
    print_header "Install Recommended Tools"
    
    if ! command -v brew &>/dev/null; then
        print_warning "Homebrew is not installed"
        
        if confirm "Install Homebrew?"; then
            print_info "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            print_success "Homebrew installed"
        else
            print_info "Skipping Homebrew installation"
            return
        fi
    fi
    
    if confirm "Install recommended tools via Homebrew?"; then
        local tools=(
            "fzf"           # Fuzzy finder
            "bat"           # Better cat
            "eza"           # Modern ls
            "ripgrep"       # Better grep
            "fd"            # Better find
            "zoxide"        # Smart cd
            "git-delta"     # Better git diff
            "htop"          # Better top
            "tree"          # Directory tree
            "wget"          # Downloader
            "jq"            # JSON processor
            "coreutils"     # GNU core utilities
            "findutils"     # GNU find utilities
            "gnu-sed"       # GNU sed
            "grep"          # GNU grep
        )
        
        for tool in "${tools[@]}"; do
            print_info "Installing: ${tool}"
            brew install "$tool" || print_warning "Failed to install ${tool}"
        done
        
        print_success "Tool installation complete"
    fi
}

# ============================================
# SETUP COMPLETIONS
# ============================================

setup_completions() {
    print_header "Setting Up Completions"
    
    if command -v brew &>/dev/null; then
        # Install zsh-completions
        if ! brew list zsh-completions &>/dev/null; then
            print_info "Installing zsh-completions..."
            brew install zsh-completions
        fi
        
        # Install zsh-syntax-highlighting
        if ! brew list zsh-syntax-highlighting &>/dev/null; then
            print_info "Installing zsh-syntax-highlighting..."
            brew install zsh-syntax-highlighting
        fi
        
        # Install zsh-autosuggestions
        if ! brew list zsh-autosuggestions &>/dev/null; then
            print_info "Installing zsh-autosuggestions..."
            brew install zsh-autosuggestions
        fi
        
        print_success "Completions installed"
    else
        print_warning "Homebrew not available - skipping completions"
    fi
}

# ============================================
# CONFIGURE DEFAULT SHELL
# ============================================

configure_shell() {
    print_header "Configure Default Shell"
    
    local current_shell="$(dscl . -read ~/ UserShell | sed 's/UserShell: //')"
    print_info "Current shell: ${current_shell}"
    
    if [[ "$current_shell" != "$(which zsh)" ]]; then
        if confirm "Set zsh as default shell?"; then
            chsh -s "$(which zsh)"
            print_success "Default shell changed to zsh"
            print_warning "Please log out and log back in for changes to take effect"
        fi
    else
        print_success "zsh is already the default shell"
    fi
}

# ============================================
# FINALIZE INSTALLATION
# ============================================

finalize() {
    print_header "Installation Complete!"
    
    echo -e "${GREEN}"
    cat << 'EOF'
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║       🎉 ZSH Enterprise Configuration Installed! 🎉       ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    echo ""
    print_info "Next steps:"
    echo ""
    echo "  1. Restart your terminal or run: source ~/.zshrc"
    echo "  2. Explore available aliases: listalias"
    echo "  3. Check system info: sysinfo"
    echo "  4. Access NovaSystem: nova"
    echo ""
    
    if [[ -d "$BACKUP_DIR" ]]; then
        print_info "Backup saved to: ${BACKUP_DIR}"
    fi
    
    echo ""
    print_success "Enjoy your new terminal environment!"
    echo ""
}

# ============================================
# MAIN INSTALLATION FLOW
# ============================================

main() {
    clear
    
    echo -e "${MAGENTA}"
    cat << 'EOF'
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║        ZSH Enterprise Configuration Installer              ║
    ║        macOS Big Sur Intel - Complete Setup                ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    echo ""
    print_info "This script will install a comprehensive zsh configuration"
    print_info "with enterprise features, auto-detection, and advanced tools."
    echo ""
    
    if ! confirm "Proceed with installation?"; then
        print_error "Installation cancelled"
        exit 0
    fi
    
    # Run installation steps
    detect_system
    backup_existing
    create_directories
    install_configs
    check_dependencies
    install_tools
    setup_completions
    configure_shell
    finalize
}

# Run main function
main "$@"
