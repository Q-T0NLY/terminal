"""
🔍 Duplicate File Finder
Find and remove duplicate files to free space
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DuplicateGroup:
    """Group of duplicate files"""
    hash: str
    size: int
    files: List[Path]
    
    @property
    def wasted_space(self) -> int:
        """Space wasted by duplicates (size * (count - 1))"""
        return self.size * (len(self.files) - 1)
        

class DuplicateFinder:
    """
    Find duplicate files by content hash
    
    Uses multi-stage hashing:
    1. Group by file size
    2. Quick hash of first 1KB
    3. Full MD5 hash for final verification
    """
    
    def __init__(
        self,
        min_size: int = 1024,  # 1KB minimum
        dry_run: bool = False
    ):
        """
        Initialize Duplicate Finder
        
        Args:
            min_size: Minimum file size to consider (bytes)
            dry_run: If True, only simulate removal
        """
        self.min_size = min_size
        self.dry_run = dry_run
        
    def find_duplicates(
        self,
        search_paths: List[Path],
        exclude_patterns: Optional[List[str]] = None
    ) -> List[DuplicateGroup]:
        """
        Find duplicate files in specified paths
        
        Args:
            search_paths: List of directories to search
            exclude_patterns: Glob patterns to exclude
            
        Returns:
            List of DuplicateGroup objects
        """
        if exclude_patterns is None:
            exclude_patterns = []
            
        # Stage 1: Group by file size
        size_groups = self._group_by_size(search_paths, exclude_patterns)
        
        # Stage 2: Quick hash (first 1KB)
        quick_hash_groups = self._group_by_quick_hash(size_groups)
        
        # Stage 3: Full hash for final verification
        duplicate_groups = self._group_by_full_hash(quick_hash_groups)
        
        return duplicate_groups
        
    def remove_duplicates(
        self,
        duplicate_groups: List[DuplicateGroup],
        keep_strategy: str = "first"  # first, oldest, newest, shortest_path
    ) -> Dict[str, any]:
        """
        Remove duplicate files, keeping one copy
        
        Args:
            duplicate_groups: List of DuplicateGroup objects
            keep_strategy: Strategy for choosing which file to keep
            
        Returns:
            Dict with removal results
        """
        total_size_freed = 0
        total_files_removed = 0
        errors = []
        
        for group in duplicate_groups:
            # Choose which file to keep
            keep_file = self._choose_keeper(group.files, keep_strategy)
            
            # Remove duplicates
            for file_path in group.files:
                if file_path == keep_file:
                    continue
                    
                try:
                    size = file_path.stat().st_size
                    
                    if not self.dry_run:
                        file_path.unlink()
                        
                    total_size_freed += size
                    total_files_removed += 1
                    
                except (PermissionError, OSError) as e:
                    errors.append({
                        "file": str(file_path),
                        "error": str(e)
                    })
                    
        return {
            "total_size_freed": total_size_freed,
            "total_files_removed": total_files_removed,
            "groups_processed": len(duplicate_groups),
            "errors": errors
        }
        
    # ==================== Private Helper Methods ====================
    
    def _group_by_size(
        self,
        search_paths: List[Path],
        exclude_patterns: List[str]
    ) -> Dict[int, List[Path]]:
        """Group files by size"""
        size_map = defaultdict(list)
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            for file_path in search_path.rglob("*"):
                # Skip if not a file
                if not file_path.is_file():
                    continue
                    
                # Skip if matches exclude pattern
                if any(file_path.match(pattern) for pattern in exclude_patterns):
                    continue
                    
                try:
                    size = file_path.stat().st_size
                    
                    # Skip files smaller than minimum
                    if size < self.min_size:
                        continue
                        
                    size_map[size].append(file_path)
                    
                except (PermissionError, OSError):
                    continue
                    
        # Keep only sizes with multiple files
        return {
            size: files
            for size, files in size_map.items()
            if len(files) > 1
        }
        
    def _group_by_quick_hash(
        self,
        size_groups: Dict[int, List[Path]]
    ) -> Dict[str, List[Path]]:
        """Group by quick hash (first 1KB)"""
        hash_map = defaultdict(list)
        
        for size, files in size_groups.items():
            for file_path in files:
                try:
                    quick_hash = self._quick_hash(file_path)
                    hash_map[quick_hash].append(file_path)
                except (PermissionError, OSError):
                    continue
                    
        # Keep only hashes with multiple files
        return {
            hash_val: files
            for hash_val, files in hash_map.items()
            if len(files) > 1
        }
        
    def _group_by_full_hash(
        self,
        quick_hash_groups: Dict[str, List[Path]]
    ) -> List[DuplicateGroup]:
        """Group by full MD5 hash"""
        duplicate_groups = []
        
        for quick_hash, files in quick_hash_groups.items():
            hash_map = defaultdict(list)
            
            for file_path in files:
                try:
                    full_hash = self._full_hash(file_path)
                    hash_map[full_hash].append(file_path)
                except (PermissionError, OSError):
                    continue
                    
            # Create DuplicateGroup for each hash with multiple files
            for full_hash, duplicate_files in hash_map.items():
                if len(duplicate_files) > 1:
                    size = duplicate_files[0].stat().st_size
                    
                    duplicate_groups.append(DuplicateGroup(
                        hash=full_hash,
                        size=size,
                        files=duplicate_files
                    ))
                    
        return duplicate_groups
        
    def _quick_hash(self, file_path: Path, chunk_size: int = 1024) -> str:
        """Calculate hash of first 1KB"""
        hasher = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            hasher.update(chunk)
            
        return hasher.hexdigest()
        
    def _full_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of entire file"""
        hasher = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
                
        return hasher.hexdigest()
        
    def _choose_keeper(
        self,
        files: List[Path],
        strategy: str
    ) -> Path:
        """Choose which file to keep based on strategy"""
        if strategy == "first":
            return files[0]
            
        elif strategy == "oldest":
            return min(files, key=lambda f: f.stat().st_mtime)
            
        elif strategy == "newest":
            return max(files, key=lambda f: f.stat().st_mtime)
            
        elif strategy == "shortest_path":
            return min(files, key=lambda f: len(str(f)))
            
        else:
            return files[0]


from typing import Optional
