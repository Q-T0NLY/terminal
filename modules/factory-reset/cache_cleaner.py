"""
💾 Cache Cleaner
Package manager and system cache cleanup
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CacheInfo:
    """Information about a cache location"""
    name: str
    path: Path
    size: int  # bytes
    file_count: int
    description: str
    

class CacheCleaner:
    """
    Cleans package manager and system caches
    
    Supports:
    - APT (Debian/Ubuntu)
    - DNF/YUM (Fedora/RHEL)
    - Pacman (Arch)
    - Homebrew (macOS/Linux)
    - pip (Python)
    - npm (Node.js)
    - cargo (Rust)
    - go (Go)
    - User cache directories (~/.cache)
    """
    
    CACHE_LOCATIONS = {
        # Package managers
        "apt": ["/var/cache/apt/archives"],
        "dnf": ["/var/cache/dnf"],
        "yum": ["/var/cache/yum"],
        "pacman": ["/var/cache/pacman/pkg"],
        "homebrew": [
            "~/Library/Caches/Homebrew",
            "/usr/local/Homebrew/Library/Taps",
            "~/.cache/homebrew"
        ],
        
        # Language package managers
        "pip": ["~/.cache/pip"],
        "npm": ["~/.npm"],
        "yarn": ["~/.yarn/cache"],
        "cargo": ["~/.cargo/registry/cache"],
        "go": ["~/go/pkg/mod/cache"],
        "gem": ["~/.gem/cache"],
        
        # System caches
        "fontconfig": ["~/.cache/fontconfig"],
        "thumbnails": ["~/.cache/thumbnails", "~/.thumbnails"],
        "mesa": ["~/.cache/mesa_shader_cache"],
        
        # Application caches
        "browser_cache": [
            "~/.cache/mozilla",
            "~/.cache/google-chrome",
            "~/.cache/chromium",
            "~/Library/Caches/Google/Chrome",
            "~/Library/Caches/Firefox"
        ]
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Cache Cleaner
        
        Args:
            dry_run: If True, only simulate cleanup without removing files
        """
        self.dry_run = dry_run
        self.cleaned_caches: List[CacheInfo] = []
        
    def scan_caches(self) -> List[CacheInfo]:
        """
        Scan all cache locations and return information
        
        Returns:
            List of CacheInfo objects for all found caches
        """
        caches = []
        
        for cache_type, locations in self.CACHE_LOCATIONS.items():
            for location in locations:
                path = Path(location).expanduser()
                
                if path.exists():
                    size, file_count = self._get_dir_info(path)
                    
                    if size > 0:  # Only include non-empty caches
                        caches.append(CacheInfo(
                            name=cache_type,
                            path=path,
                            size=size,
                            file_count=file_count,
                            description=self._get_cache_description(cache_type)
                        ))
                        
        return caches
        
    def clean_all(self) -> Dict[str, any]:
        """
        Clean all discovered caches
        
        Returns:
            Dict with cleanup results:
            - total_size_freed: Total bytes freed
            - total_files_removed: Total files removed
            - caches_cleaned: List of cleaned cache names
        """
        caches = self.scan_caches()
        
        total_size = 0
        total_files = 0
        cleaned_names = []
        
        for cache in caches:
            size_freed, files_removed = self._clean_cache(cache)
            total_size += size_freed
            total_files += files_removed
            cleaned_names.append(cache.name)
            
        return {
            "total_size_freed": total_size,
            "total_files_removed": total_files,
            "caches_cleaned": cleaned_names
        }
        
    def clean_package_managers(self) -> Dict[str, int]:
        """
        Clean package manager caches using native commands
        
        Returns:
            Dict mapping package manager to bytes freed
        """
        results = {}
        
        # APT cleanup
        if self._has_command("apt-get"):
            before = self._get_cache_size("/var/cache/apt/archives")
            if not self.dry_run:
                subprocess.run(["sudo", "apt-get", "clean"], check=False)
                subprocess.run(["sudo", "apt-get", "autoclean"], check=False)
            after = self._get_cache_size("/var/cache/apt/archives")
            results["apt"] = before - after
            
        # DNF cleanup
        if self._has_command("dnf"):
            before = self._get_cache_size("/var/cache/dnf")
            if not self.dry_run:
                subprocess.run(["sudo", "dnf", "clean", "all"], check=False)
            after = self._get_cache_size("/var/cache/dnf")
            results["dnf"] = before - after
            
        # Pacman cleanup
        if self._has_command("pacman"):
            before = self._get_cache_size("/var/cache/pacman/pkg")
            if not self.dry_run:
                subprocess.run(["sudo", "pacman", "-Sc", "--noconfirm"], check=False)
            after = self._get_cache_size("/var/cache/pacman/pkg")
            results["pacman"] = before - after
            
        # Homebrew cleanup
        if self._has_command("brew"):
            before = self._get_homebrew_cache_size()
            if not self.dry_run:
                subprocess.run(["brew", "cleanup", "-s"], check=False)
            after = self._get_homebrew_cache_size()
            results["homebrew"] = before - after
            
        return results
        
    def clean_user_caches(self) -> int:
        """
        Clean user-level caches in ~/.cache
        
        Returns:
            Total bytes freed
        """
        cache_dir = Path.home() / ".cache"
        
        if not cache_dir.exists():
            return 0
            
        # Exclude certain directories we want to keep
        exclude = {"fontconfig", "mesa_shader_cache", "pip"}
        
        before_size = self._get_dir_size(cache_dir)
        
        if not self.dry_run:
            for item in cache_dir.iterdir():
                if item.name not in exclude:
                    try:
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except (PermissionError, OSError):
                        continue
                        
        after_size = self._get_dir_size(cache_dir)
        return before_size - after_size
        
    # ==================== Private Helper Methods ====================
    
    def _get_dir_info(self, path: Path) -> Tuple[int, int]:
        """Get total size and file count for directory"""
        total_size = 0
        file_count = 0
        
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
        except (PermissionError, OSError):
            pass
            
        return total_size, file_count
        
    def _get_dir_size(self, path: Path) -> int:
        """Get total size of directory in bytes"""
        size, _ = self._get_dir_info(path)
        return size
        
    def _get_cache_size(self, path_str: str) -> int:
        """Get cache size from path string"""
        path = Path(path_str).expanduser()
        if path.exists():
            return self._get_dir_size(path)
        return 0
        
    def _get_homebrew_cache_size(self) -> int:
        """Get total Homebrew cache size"""
        total = 0
        for location in self.CACHE_LOCATIONS["homebrew"]:
            total += self._get_cache_size(location)
        return total
        
    def _clean_cache(self, cache: CacheInfo) -> Tuple[int, int]:
        """
        Clean a specific cache
        
        Returns:
            Tuple of (bytes_freed, files_removed)
        """
        before_size, before_files = self._get_dir_info(cache.path)
        
        if not self.dry_run:
            try:
                if cache.path.is_dir():
                    # Remove contents but keep directory
                    for item in cache.path.iterdir():
                        try:
                            if item.is_file():
                                item.unlink()
                            elif item.is_dir():
                                shutil.rmtree(item)
                        except (PermissionError, OSError):
                            continue
            except (PermissionError, OSError):
                return 0, 0
                
        after_size, after_files = self._get_dir_info(cache.path)
        
        self.cleaned_caches.append(cache)
        
        return before_size - after_size, before_files - after_files
        
    def _has_command(self, command: str) -> bool:
        """Check if command is available"""
        return shutil.which(command) is not None
        
    def _get_cache_description(self, cache_type: str) -> str:
        """Get human-readable description of cache type"""
        descriptions = {
            "apt": "APT package cache (Debian/Ubuntu)",
            "dnf": "DNF package cache (Fedora/RHEL)",
            "pacman": "Pacman package cache (Arch Linux)",
            "homebrew": "Homebrew formula cache",
            "pip": "Python pip package cache",
            "npm": "Node.js npm package cache",
            "yarn": "Yarn package cache",
            "cargo": "Rust cargo package cache",
            "go": "Go module cache",
            "gem": "Ruby gem cache",
            "fontconfig": "Font configuration cache",
            "thumbnails": "Image thumbnail cache",
            "mesa": "Mesa shader cache",
            "browser_cache": "Web browser cache"
        }
        
        return descriptions.get(cache_type, f"{cache_type} cache")
        
    @staticmethod
    def format_size(bytes_size: int) -> str:
        """Format bytes into human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
