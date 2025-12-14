"""
🔧 OSE Terminal Config Service
ZSH Configuration Generation & Management

Features:
- Dynamic ZSH config generation
- Theme management
- Plugin ecosystem
- Cloud sync (S3/MinIO)
- Version control (Git)
- Profile templates
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json

app = FastAPI(
    title="OSE Terminal Config Service",
    description="ZSH Configuration Generation & Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Models ====================

class ConfigProfile(BaseModel):
    id: str
    name: str
    description: str
    features: List[str]


class ThemeInfo(BaseModel):
    id: str
    name: str
    author: str
    preview_url: Optional[str]
    popularity: int


class PluginInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    repo_url: str


class ConfigRequest(BaseModel):
    profile: str = "enterprise"
    theme: str = "powerlevel10k"
    plugins: List[str] = []
    custom_aliases: Dict[str, str] = {}
    enable_auto_detection: bool = True


class ConfigResult(BaseModel):
    config_id: str
    generated_files: List[str]
    download_url: Optional[str]
    git_repo: Optional[str]


# ==================== Predefined Configs ====================

PROFILES = {
    "minimal": {
        "name": "Minimal",
        "description": "Lightweight ZSH with essentials",
        "features": ["basic_aliases", "history", "completion"]
    },
    "standard": {
        "name": "Standard",
        "description": "Standard ZSH setup",
        "features": ["aliases", "history", "completion", "syntax_highlighting"]
    },
    "enterprise": {
        "name": "Enterprise",
        "description": "Advanced enterprise configuration",
        "features": [
            "auto_detection", "path_management", "version_managers",
            "syntax_highlighting", "auto_suggestions", "themes"
        ]
    },
    "power_user": {
        "name": "Power User",
        "description": "Maximum features and customization",
        "features": [
            "auto_detection", "advanced_completion", "fuzzy_finder",
            "git_integration", "kubernetes", "docker", "aws", "gcp"
        ]
    }
}

THEMES = [
    {
        "id": "powerlevel10k",
        "name": "Powerlevel10k",
        "author": "romkatv",
        "repo": "romkatv/powerlevel10k",
        "popularity": 100
    },
    {
        "id": "starship",
        "name": "Starship",
        "author": "starship",
        "repo": "starship/starship",
        "popularity": 95
    },
    {
        "id": "agnoster",
        "name": "Agnoster",
        "author": "agnoster",
        "repo": "agnoster/agnoster-zsh-theme",
        "popularity": 85
    }
]

PLUGINS = [
    {
        "id": "zsh-autosuggestions",
        "name": "Autosuggestions",
        "description": "Fish-like autosuggestions",
        "category": "productivity",
        "repo": "zsh-users/zsh-autosuggestions"
    },
    {
        "id": "zsh-syntax-highlighting",
        "name": "Syntax Highlighting",
        "description": "Fish-like syntax highlighting",
        "category": "visual",
        "repo": "zsh-users/zsh-syntax-highlighting"
    },
    {
        "id": "fzf",
        "name": "FZF",
        "description": "Fuzzy finder integration",
        "category": "productivity",
        "repo": "junegunn/fzf"
    },
    {
        "id": "z",
        "name": "Z",
        "description": "Directory jumper",
        "category": "navigation",
        "repo": "agkozak/zsh-z"
    }
]


# ==================== Config Templates ====================

def generate_zshrc(request: ConfigRequest) -> str:
    """Generate .zshrc content"""
    
    profile = PROFILES.get(request.profile, PROFILES["standard"])
    
    content = f"""# OSE Terminal Configuration
# Profile: {profile['name']}
# Generated: {datetime.now().isoformat()}

# Path configuration
export PATH="$HOME/bin:/usr/local/bin:$PATH"

# History configuration
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt SHARE_HISTORY

# Completion
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{{a-zA-Z}}={{A-Za-z}}'

"""
    
    # Add theme
    if request.theme == "powerlevel10k":
        content += """
# Powerlevel10k theme
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
source ~/.oh-my-zsh/custom/themes/powerlevel10k/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

"""
    
    # Add plugins
    if request.plugins:
        content += "\n# Plugins\n"
        for plugin in request.plugins:
            if plugin == "zsh-autosuggestions":
                content += "source ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh\n"
            elif plugin == "zsh-syntax-highlighting":
                content += "source ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh\n"
    
    # Add custom aliases
    if request.custom_aliases:
        content += "\n# Custom Aliases\n"
        for alias, command in request.custom_aliases.items():
            content += f"alias {alias}='{command}'\n"
    
    # Add auto-detection (if enabled)
    if request.enable_auto_detection:
        content += """
# Auto-detection and version managers
# Node.js (nvm)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh"

# Python (pyenv)
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

# Ruby (rbenv)
if command -v rbenv 1>/dev/null 2>&1; then
  eval "$(rbenv init -)"
fi

# Go
export GOPATH="$HOME/go"
export PATH="$PATH:$GOPATH/bin"

# Rust
export PATH="$HOME/.cargo/bin:$PATH"

"""
    
    return content


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OSE Terminal Config Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "profiles": "/api/v1/profiles",
            "themes": "/api/v1/themes",
            "plugins": "/api/v1/plugins",
            "generate": "/api/v1/config/generate",
            "docs": "/docs"
        }
    }


@app.get("/api/v1/profiles")
async def get_profiles():
    """Get available configuration profiles"""
    return {
        "profiles": [
            ConfigProfile(id=k, **v) for k, v in PROFILES.items()
        ]
    }


@app.get("/api/v1/themes")
async def get_themes():
    """Get available themes"""
    return {
        "themes": [ThemeInfo(**t) for t in THEMES]
    }


@app.get("/api/v1/plugins")
async def get_plugins(category: Optional[str] = None):
    """Get available plugins"""
    plugins = PLUGINS
    if category:
        plugins = [p for p in plugins if p["category"] == category]
    
    return {
        "total": len(plugins),
        "plugins": [PluginInfo(**p) for p in plugins]
    }


@app.post("/api/v1/config/generate", response_model=ConfigResult)
async def generate_config(request: ConfigRequest):
    """Generate ZSH configuration"""
    
    config_id = f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Generate config content
    zshrc_content = generate_zshrc(request)
    
    # In production, would write to files/S3/Git
    # For now, just return metadata
    
    generated_files = [
        ".zshrc",
        ".zshenv",
        ".zprofile"
    ]
    
    if request.theme == "powerlevel10k":
        generated_files.append(".p10k.zsh")
    
    return ConfigResult(
        config_id=config_id,
        generated_files=generated_files,
        download_url=f"https://ose.example.com/configs/{config_id}.zip",
        git_repo=f"https://github.com/ose/configs/{config_id}"
    )


@app.get("/api/v1/config/{config_id}")
async def get_config(config_id: str):
    """Get generated configuration"""
    # In production, retrieve from storage
    return {
        "config_id": config_id,
        "status": "available",
        "files": [".zshrc", ".zshenv"],
        "download_url": f"https://ose.example.com/configs/{config_id}.zip"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "terminal-config"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
