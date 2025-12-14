"""
🔐 Privacy Cleaner
Privacy-focused cleanup (BleachBit integration)
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class PrivacyCleaner:
    """
    Privacy-focused system cleaning
    
    Integrates with BleachBit for deep privacy cleanup:
    - Browser history/cookies
    - Recent documents
    - Clipboard history
    - Thumbnail cache
    - Bash history
    - And more...
    """
    
    PRIVACY_TARGETS = {
        "browser_history": [
            "firefox.url_history",
            "google_chrome.history",
            "chromium.history"
        ],
        "browser_cookies": [
            "firefox.cookies",
            "google_chrome.cookies",
            "chromium.cookies"
        ],
        "recent_documents": [
            "system.recent_documents",
            "nautilus.history"
        ],
        "clipboard": [
            "system.clipboard"
        ],
        "thumbnails": [
            "system.thumbnails"
        ],
        "bash_history": [
            "bash.history"
        ],
        "trash": [
            "system.trash"
        ]
    }
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize Privacy Cleaner
        
        Args:
            dry_run: If True, only simulate cleanup
        """
        self.dry_run = dry_run
        self.has_bleachbit = self._check_bleachbit()
        
    def clean_privacy_data(
        self,
        targets: Optional[List[str]] = None
    ) -> Dict[str, any]:
        """
        Clean privacy-sensitive data
        
        Args:
            targets: List of target categories (uses all if None)
            
        Returns:
            Dict with cleanup results
        """
        if targets is None:
            targets = list(self.PRIVACY_TARGETS.keys())
            
        results = {
            "cleaned_categories": [],
            "errors": []
        }
        
        if self.has_bleachbit:
            # Use BleachBit
            for target in targets:
                if target in self.PRIVACY_TARGETS:
                    for bleachbit_target in self.PRIVACY_TARGETS[target]:
                        success = self._run_bleachbit(bleachbit_target)
                        
                        if success:
                            results["cleaned_categories"].append(target)
                        else:
                            results["errors"].append({
                                "target": target,
                                "error": "BleachBit cleanup failed"
                            })
        else:
            # Fallback to manual cleanup
            for target in targets:
                success = self._manual_privacy_clean(target)
                
                if success:
                    results["cleaned_categories"].append(target)
                    
        return results
        
    def clean_browser_data(self, browser: str = "all") -> bool:
        """
        Clean browser history and cookies
        
        Args:
            browser: Browser name (firefox, chrome, chromium, all)
            
        Returns:
            True if successful
        """
        browsers = {
            "firefox": [
                "~/.mozilla/firefox/*/places.sqlite",
                "~/.mozilla/firefox/*/cookies.sqlite"
            ],
            "chrome": [
                "~/.config/google-chrome/*/History",
                "~/.config/google-chrome/*/Cookies"
            ],
            "chromium": [
                "~/.config/chromium/*/History",
                "~/.config/chromium/*/Cookies"
            ]
        }
        
        if browser == "all":
            targets = []
            for browser_targets in browsers.values():
                targets.extend(browser_targets)
        else:
            targets = browsers.get(browser, [])
            
        for target_pattern in targets:
            for file_path in Path.home().glob(target_pattern):
                try:
                    if not self.dry_run and file_path.exists():
                        file_path.unlink()
                except (PermissionError, OSError):
                    continue
                    
        return True
        
    def clean_bash_history(self) -> bool:
        """Clean bash history"""
        history_file = Path.home() / ".bash_history"
        
        if history_file.exists():
            try:
                if not self.dry_run:
                    history_file.write_text("")
                return True
            except (PermissionError, OSError):
                return False
                
        return True
        
    # ==================== Private Helper Methods ====================
    
    def _check_bleachbit(self) -> bool:
        """Check if BleachBit is installed"""
        try:
            subprocess.run(
                ["bleachbit", "--version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _run_bleachbit(self, target: str) -> bool:
        """Run BleachBit for specific target"""
        try:
            cmd = ["bleachbit", "--clean", target]
            
            if self.dry_run:
                cmd = ["bleachbit", "--preview", target]
                
            subprocess.run(cmd, check=True, capture_output=True)
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _manual_privacy_clean(self, target: str) -> bool:
        """Manual privacy cleanup without BleachBit"""
        if target == "browser_history":
            return self.clean_browser_data()
        elif target == "bash_history":
            return self.clean_bash_history()
        else:
            return False
