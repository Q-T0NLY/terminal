"""
🗑️ Trash Manager  
Smart trash handling and recovery
"""

import shutil
import time
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrashItem:
    """Represents an item in trash"""
    original_path: str
    trash_path: Path
    size: int
    trashed_at: datetime
    

class TrashManager:
    """
    Manages OSE trash for safe file recovery
    
    Features:
    - Move files to trash instead of deleting
    - List trash contents
    - Recover files from trash
    - Empty trash (permanent deletion)
    - Automatic cleanup of old trash items
    """
    
    def __init__(self, trash_dir: Optional[Path] = None):
        """
        Initialize Trash Manager
        
        Args:
            trash_dir: Custom trash directory (uses default if None)
        """
        if trash_dir is None:
            trash_dir = Path.home() / ".ose" / "trash"
            
        self.trash_dir = trash_dir
        self.trash_dir.mkdir(parents=True, exist_ok=True)
        
        # Metadata directory
        self.metadata_dir = self.trash_dir / ".metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        
    def move_to_trash(self, file_path: Path) -> bool:
        """
        Move file to trash
        
        Args:
            file_path: Path to file or directory to trash
            
        Returns:
            True if successful
        """
        if not file_path.exists():
            return False
            
        try:
            # Create timestamped trash directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_subdir = self.trash_dir / timestamp
            trash_subdir.mkdir(exist_ok=True)
            
            # Destination in trash
            dest = trash_subdir / file_path.name
            
            # Move file/directory
            shutil.move(str(file_path), str(dest))
            
            # Save metadata
            self._save_metadata(
                original_path=str(file_path.absolute()),
                trash_path=dest,
                size=self._get_size(dest),
                timestamp=timestamp
            )
            
            return True
            
        except (PermissionError, OSError):
            return False
            
    def list_trash(self) -> List[TrashItem]:
        """
        List all items in trash
        
        Returns:
            List of TrashItem objects
        """
        items = []
        
        for metadata_file in self.metadata_dir.glob("*.meta"):
            try:
                item = self._load_metadata(metadata_file)
                if item:
                    items.append(item)
            except Exception:
                continue
                
        return items
        
    def recover_file(
        self,
        trash_path: Path,
        restore_to: Optional[Path] = None
    ) -> bool:
        """
        Recover file from trash
        
        Args:
            trash_path: Path to file in trash
            restore_to: Destination (uses original location if None)
            
        Returns:
            True if successful
        """
        if not trash_path.exists():
            return False
            
        try:
            # Load metadata to get original location
            metadata = self._find_metadata(trash_path)
            
            if metadata is None:
                return False
                
            # Determine restore location
            if restore_to is None:
                restore_to = Path(metadata["original_path"])
                
            # Ensure parent directory exists
            restore_to.parent.mkdir(parents=True, exist_ok=True)
            
            # Move back from trash
            shutil.move(str(trash_path), str(restore_to))
            
            # Remove metadata
            self._remove_metadata(trash_path)
            
            return True
            
        except (PermissionError, OSError):
            return False
            
    def empty_trash(self, older_than_days: Optional[int] = None) -> Dict[str, any]:
        """
        Empty trash (permanent deletion)
        
        Args:
            older_than_days: Only delete items older than this (deletes all if None)
            
        Returns:
            Dict with deletion results
        """
        items = self.list_trash()
        
        total_size_freed = 0
        total_items_deleted = 0
        errors = []
        
        cutoff_time = None
        if older_than_days is not None:
            cutoff_time = time.time() - (older_than_days * 86400)
            
        for item in items:
            # Check age if specified
            if cutoff_time is not None:
                item_time = item.trashed_at.timestamp()
                if item_time > cutoff_time:
                    continue
                    
            try:
                # Permanently delete
                if item.trash_path.is_file():
                    item.trash_path.unlink()
                elif item.trash_path.is_dir():
                    shutil.rmtree(item.trash_path)
                    
                # Remove metadata
                self._remove_metadata(item.trash_path)
                
                total_size_freed += item.size
                total_items_deleted += 1
                
            except (PermissionError, OSError) as e:
                errors.append({
                    "item": str(item.trash_path),
                    "error": str(e)
                })
                
        return {
            "total_size_freed": total_size_freed,
            "total_items_deleted": total_items_deleted,
            "errors": errors
        }
        
    def get_trash_size(self) -> int:
        """Get total size of trash in bytes"""
        total_size = 0
        
        for item in self.trash_dir.rglob("*"):
            if item.is_file() and not item.parent.name == ".metadata":
                total_size += item.stat().st_size
                
        return total_size
        
    # ==================== Private Helper Methods ====================
    
    def _get_size(self, path: Path) -> int:
        """Get size of file or directory"""
        if path.is_file():
            return path.stat().st_size
            
        total_size = 0
        for item in path.rglob("*"):
            if item.is_file():
                total_size += item.stat().st_size
                
        return total_size
        
    def _save_metadata(
        self,
        original_path: str,
        trash_path: Path,
        size: int,
        timestamp: str
    ):
        """Save metadata about trashed item"""
        import json
        
        metadata = {
            "original_path": original_path,
            "trash_path": str(trash_path),
            "size": size,
            "timestamp": timestamp
        }
        
        # Use trash_path basename as metadata filename
        metadata_file = self.metadata_dir / f"{trash_path.name}_{timestamp}.meta"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def _load_metadata(self, metadata_file: Path) -> Optional[TrashItem]:
        """Load metadata from file"""
        import json
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
            
        trash_path = Path(data["trash_path"])
        
        # Check if trash item still exists
        if not trash_path.exists():
            # Clean up stale metadata
            metadata_file.unlink()
            return None
            
        return TrashItem(
            original_path=data["original_path"],
            trash_path=trash_path,
            size=data["size"],
            trashed_at=datetime.strptime(data["timestamp"], "%Y%m%d_%H%M%S")
        )
        
    def _find_metadata(self, trash_path: Path) -> Optional[Dict]:
        """Find metadata for trash item"""
        import json
        
        for metadata_file in self.metadata_dir.glob("*.meta"):
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                
            if Path(data["trash_path"]) == trash_path:
                return data
                
        return None
        
    def _remove_metadata(self, trash_path: Path):
        """Remove metadata for trash item"""
        import json
        
        for metadata_file in self.metadata_dir.glob("*.meta"):
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                
            if Path(data["trash_path"]) == trash_path:
                metadata_file.unlink()
                break
