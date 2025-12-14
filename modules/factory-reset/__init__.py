"""
🧹 OSE Factory Reset Module
Ultra-Advanced Factory Reset with Integrated Cleanup

Includes:
- Factory Reset Service (4 profiles: light, medium, deep, nuclear)
- Cache Cleaner (apt, npm, pip, cargo, etc.)
- Temp Cleaner (tmp, downloads, system temp)
- Log Manager (system logs, application logs)
- Duplicate Finder (find and remove duplicates)
- Privacy Cleaner (browser data, history, cookies)
- Trash Manager (empty trash across platforms)
"""

from cache_cleaner import CacheCleaner
from temp_cleaner import TempCleaner
from log_manager import LogManager
from duplicate_finder import DuplicateFinder
from privacy_cleaner import PrivacyCleaner
from trash_manager import TrashManager

__all__ = [
    "CacheCleaner",
    "TempCleaner",
    "LogManager",
    "DuplicateFinder",
    "PrivacyCleaner",
    "TrashManager",
]
