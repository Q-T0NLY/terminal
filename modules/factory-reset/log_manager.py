"""
📋 Log Manager
Intelligent log file rotation and cleanup
"""

import gzip
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class LogFileInfo:
    """Information about a log file"""
    path: Path
    size: int
    age_days: int
    last_modified: datetime
    category: str  # system, application, user
    

class LogManager:
    """
    Manages log file rotation and cleanup
    
    Handles:
    - System logs (/var/log)
    - Journal logs (systemd-journald)
    - Application logs
    - User logs (~/.local/share/logs)
    """
    
    LOG_LOCATIONS = {
        "system": [
            "/var/log",
            "/var/log/syslog*",
            "/var/log/messages*",
            "/var/log/kern.log*"
        ],
        "journal": [
            "/var/log/journal"
        ],
        "application": [
            "/var/log/apache2",
            "/var/log/nginx",
            "/var/log/mysql",
            "/var/log/postgresql"
        ],
        "user": [
            "~/.local/share/logs",
            "~/.ose/logs",
            "~/.npm/_logs",
            "~/.cache/pip/log"
        ]
    }
    
    def __init__(
        self,
        max_age_days: int = 90,
        compress_older_than_days: int = 30,
        dry_run: bool = False
    ):
        """
        Initialize Log Manager
        
        Args:
            max_age_days: Remove logs older than this many days
            compress_older_than_days: Compress logs older than this many days
            dry_run: If True, only simulate operations
        """
        self.max_age_days = max_age_days
        self.compress_older_than_days = compress_older_than_days
        self.dry_run = dry_run
        
    def scan_logs(self) -> List[LogFileInfo]:
        """
        Scan all log locations
        
        Returns:
            List of LogFileInfo objects
        """
        logs = []
        
        for category, locations in self.LOG_LOCATIONS.items():
            for location in locations:
                path = Path(location).expanduser()
                
                # Handle glob patterns
                if "*" in str(path):
                    parent = Path(str(path).split("*")[0]).parent
                    pattern = path.name
                    
                    if parent.exists():
                        for log_file in parent.glob(pattern):
                            if log_file.is_file():
                                logs.append(self._get_log_info(log_file, category))
                else:
                    if path.is_file():
                        logs.append(self._get_log_info(path, category))
                    elif path.is_dir():
                        # Recursively find log files
                        for log_file in path.rglob("*.log"):
                            logs.append(self._get_log_info(log_file, category))
                            
        return logs
        
    def clean_old_logs(self) -> Dict[str, any]:
        """
        Remove logs older than max_age_days
        
        Returns:
            Dict with cleanup results
        """
        logs = self.scan_logs()
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        
        total_size = 0
        total_files = 0
        errors = []
        
        for log in logs:
            if log.last_modified < cutoff_date:
                try:
                    size = log.size
                    
                    if not self.dry_run:
                        log.path.unlink()
                        
                    total_size += size
                    total_files += 1
                    
                except (PermissionError, OSError) as e:
                    errors.append({
                        "file": str(log.path),
                        "error": str(e)
                    })
                    
        return {
            "total_size_freed": total_size,
            "total_files_removed": total_files,
            "errors": errors
        }
        
    def compress_logs(self) -> Dict[str, any]:
        """
        Compress logs older than compress_older_than_days
        
        Returns:
            Dict with compression results
        """
        logs = self.scan_logs()
        cutoff_date = datetime.now() - timedelta(days=self.compress_older_than_days)
        
        total_original_size = 0
        total_compressed_size = 0
        files_compressed = 0
        errors = []
        
        for log in logs:
            # Skip already compressed files
            if log.path.suffix == ".gz":
                continue
                
            if log.last_modified < cutoff_date:
                try:
                    original_size = log.size
                    
                    if not self.dry_run:
                        compressed_size = self._compress_log(log.path)
                    else:
                        # Estimate 10:1 compression ratio
                        compressed_size = original_size // 10
                        
                    total_original_size += original_size
                    total_compressed_size += compressed_size
                    files_compressed += 1
                    
                except (PermissionError, OSError) as e:
                    errors.append({
                        "file": str(log.path),
                        "error": str(e)
                    })
                    
        return {
            "total_original_size": total_original_size,
            "total_compressed_size": total_compressed_size,
            "space_saved": total_original_size - total_compressed_size,
            "files_compressed": files_compressed,
            "errors": errors
        }
        
    def rotate_log(self, log_path: Path, keep_count: int = 5) -> bool:
        """
        Rotate a log file (rename and compress old versions)
        
        Args:
            log_path: Path to log file
            keep_count: Number of rotated logs to keep
            
        Returns:
            True if successful
        """
        if not log_path.exists():
            return False
            
        try:
            # Rotate existing numbered logs
            for i in range(keep_count - 1, 0, -1):
                old_log = Path(f"{log_path}.{i}.gz")
                new_log = Path(f"{log_path}.{i + 1}.gz")
                
                if old_log.exists():
                    if not self.dry_run:
                        old_log.rename(new_log)
                        
            # Compress current log to .1.gz
            if not self.dry_run:
                self._compress_log(log_path, Path(f"{log_path}.1.gz"))
                
                # Create new empty log
                log_path.touch()
                
            # Remove oldest log if beyond keep_count
            oldest = Path(f"{log_path}.{keep_count + 1}.gz")
            if oldest.exists() and not self.dry_run:
                oldest.unlink()
                
            return True
            
        except (PermissionError, OSError):
            return False
            
    def clean_journal(self, vacuum_size: str = "100M") -> bool:
        """
        Clean systemd journal logs
        
        Args:
            vacuum_size: Keep only this much journal data
            
        Returns:
            True if successful
        """
        import subprocess
        
        try:
            if not self.dry_run:
                subprocess.run(
                    ["sudo", "journalctl", "--vacuum-size=" + vacuum_size],
                    check=True,
                    capture_output=True
                )
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    # ==================== Private Helper Methods ====================
    
    def _get_log_info(self, path: Path, category: str) -> LogFileInfo:
        """Get information about a log file"""
        stat = path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)
        age_days = (datetime.now() - last_modified).days
        
        return LogFileInfo(
            path=path,
            size=stat.st_size,
            age_days=age_days,
            last_modified=last_modified,
            category=category
        )
        
    def _compress_log(
        self,
        source: Path,
        dest: Optional[Path] = None
    ) -> int:
        """
        Compress a log file with gzip
        
        Args:
            source: Source log file
            dest: Destination (defaults to source.gz)
            
        Returns:
            Size of compressed file
        """
        if dest is None:
            dest = Path(str(source) + ".gz")
            
        with open(source, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        # Remove original file
        source.unlink()
        
        return dest.stat().st_size
