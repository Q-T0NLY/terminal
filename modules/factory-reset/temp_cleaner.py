"""
🗑️ Temporary File Cleaner
Removes temporary files and directories
"""

import os
import time
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TempFileInfo:
    """Information about a temporary file"""
    path: Path
    size: int
    age_hours: float
    category: str  # system, user, app
    

class TempCleaner:
    """
    Cleans temporary files from various locations
    
    Locations:
    - /tmp
    - /var/tmp
    - ~/.tmp
    - ~/Downloads (old files)
    - ~/.Trash
    - Application temp directories
    """
    
    TEMP_LOCATIONS = {
        "system": ["/tmp", "/var/tmp"],
        "user": ["~/.tmp", "~/tmp"],
        "downloads": ["~/Downloads"],
        "trash": [
            "~/.Trash",
            "~/.local/share/Trash",
            "$XDG_DATA_HOME/Trash"
        ],
        "app_temp": [
            "~/Library/Application Support/*/Temp",
            "~/.config/*/temp",
            "~/.local/share/*/temp"
        ]
    }
    
    def __init__(
        self,
        max_age_hours: int = 24,
        dry_run: bool = False
    ):
        """
        Initialize Temp Cleaner
        
        Args:
            max_age_hours: Remove files older than this many hours
            dry_run: If True, only simulate cleanup
        """
        self.max_age_hours = max_age_hours
        self.dry_run = dry_run
        self.max_age_seconds = max_age_hours * 3600
        
    def scan_temp_files(self) -> List[TempFileInfo]:
        """
        Scan for temporary files
        
        Returns:
            List of TempFileInfo objects
        """
        temp_files = []
        current_time = time.time()
        
        for category, locations in self.TEMP_LOCATIONS.items():
            for location in locations:
                path = Path(location).expanduser()
                
                if not path.exists():
                    continue
                    
                try:
                    for item in path.rglob("*"):
                        if not item.is_file():
                            continue
                            
                        stat = item.stat()
                        age = current_time - stat.st_mtime
                        age_hours = age / 3600
                        
                        # Only include files older than threshold
                        if age > self.max_age_seconds:
                            temp_files.append(TempFileInfo(
                                path=item,
                                size=stat.st_size,
                                age_hours=age_hours,
                                category=category
                            ))
                except (PermissionError, OSError):
                    continue
                    
        return temp_files
        
    def clean_temp_files(self) -> Dict[str, any]:
        """
        Clean temporary files
        
        Returns:
            Dict with cleanup results
        """
        temp_files = self.scan_temp_files()
        
        total_size = 0
        total_files = 0
        errors = []
        
        for temp_file in temp_files:
            try:
                if not self.dry_run:
                    temp_file.path.unlink()
                    
                total_size += temp_file.size
                total_files += 1
                
            except (PermissionError, OSError) as e:
                errors.append({
                    "file": str(temp_file.path),
                    "error": str(e)
                })
                
        return {
            "total_size_freed": total_size,
            "total_files_removed": total_files,
            "errors": errors
        }
        
    def clean_system_temp(self) -> int:
        """
        Clean /tmp and /var/tmp
        
        Returns:
            Bytes freed
        """
        total_freed = 0
        
        for location in ["/tmp", "/var/tmp"]:
            path = Path(location)
            
            if not path.exists():
                continue
                
            try:
                before = self._get_dir_size(path)
                
                if not self.dry_run:
                    for item in path.iterdir():
                        # Skip if recently accessed
                        if time.time() - item.stat().st_mtime < self.max_age_seconds:
                            continue
                            
                        try:
                            if item.is_file():
                                item.unlink()
                            elif item.is_dir():
                                import shutil
                                shutil.rmtree(item)
                        except (PermissionError, OSError):
                            continue
                            
                after = self._get_dir_size(path)
                total_freed += before - after
                
            except (PermissionError, OSError):
                continue
                
        return total_freed
        
    def clean_downloads(self, older_than_days: int = 30) -> int:
        """
        Clean old files from Downloads directory
        
        Args:
            older_than_days: Remove files older than this many days
            
        Returns:
            Bytes freed
        """
        downloads = Path.home() / "Downloads"
        
        if not downloads.exists():
            return 0
            
        max_age = older_than_days * 86400  # seconds
        current_time = time.time()
        total_freed = 0
        
        try:
            for item in downloads.iterdir():
                if not item.is_file():
                    continue
                    
                age = current_time - item.stat().st_mtime
                
                if age > max_age:
                    size = item.stat().st_size
                    
                    if not self.dry_run:
                        try:
                            item.unlink()
                            total_freed += size
                        except (PermissionError, OSError):
                            continue
                    else:
                        total_freed += size
                        
        except (PermissionError, OSError):
            pass
            
        return total_freed
        
    def empty_trash(self) -> int:
        """
        Empty system trash
        
        Returns:
            Bytes freed
        """
        import shutil
        
        trash_locations = [
            Path.home() / ".Trash",
            Path.home() / ".local" / "share" / "Trash"
        ]
        
        total_freed = 0
        
        for trash_path in trash_locations:
            if not trash_path.exists():
                continue
                
            try:
                before = self._get_dir_size(trash_path)
                
                if not self.dry_run:
                    # Remove contents but keep directory structure
                    for item in trash_path.iterdir():
                        try:
                            if item.is_file():
                                item.unlink()
                            elif item.is_dir():
                                shutil.rmtree(item)
                        except (PermissionError, OSError):
                            continue
                            
                after = self._get_dir_size(trash_path)
                total_freed += before - after
                
            except (PermissionError, OSError):
                continue
                
        return total_freed
        
    # ==================== Private Helper Methods ====================
    
    def _get_dir_size(self, path: Path) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        
        try:
            for item in path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
        except (PermissionError, OSError):
            pass
            
        return total_size
