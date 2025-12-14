"""
📝 OSE Logger
Advanced logging with emoji support and multiple outputs
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """OSE log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EmojiFormatter(logging.Formatter):
    """Custom formatter with emoji support"""
    
    EMOJI_MAP = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🔴"
    }
    
    COLOR_MAP = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[37m",       # White
        "SUCCESS": "\033[32m",    # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m"    # Magenta
    }
    
    RESET = "\033[0m"
    
    def format(self, record):
        """Format log record with emoji and color"""
        emoji = self.EMOJI_MAP.get(record.levelname, "")
        color = self.COLOR_MAP.get(record.levelname, "")
        
        # Add custom emoji if provided in extra
        if hasattr(record, "emoji"):
            emoji = record.emoji
            
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        
        # Build message
        if sys.stdout.isatty():
            # Terminal output with colors
            message = f"{color}{emoji} [{timestamp}] {record.getMessage()}{self.RESET}"
        else:
            # File output without colors
            message = f"{emoji} [{timestamp}] {record.getMessage()}"
            
        return message


class OSELogger:
    """
    Advanced logger for OSE
    
    Features:
    - Emoji-enhanced output
    - Color-coded levels
    - Multiple outputs (console + file)
    - Structured logging
    """
    
    # Add SUCCESS level (between INFO and WARNING)
    SUCCESS_LEVEL = 25
    logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
    
    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize OSE Logger
        
        Args:
            log_dir: Directory for log files (uses default if None)
        """
        if log_dir is None:
            log_dir = Path.home() / ".ose" / "logs"
            
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("OSE")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler (INFO and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(EmojiFormatter())
        self.logger.addHandler(console_handler)
        
        # File handler (DEBUG and above)
        log_file = log_dir / f"ose_{datetime.now().strftime('%Y%m')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(EmojiFormatter())
        self.logger.addHandler(file_handler)
        
        # Operation-specific log file
        operation_log = log_dir / f"operation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.operation_handler = logging.FileHandler(operation_log)
        self.operation_handler.setLevel(logging.DEBUG)
        self.operation_handler.setFormatter(EmojiFormatter())
        
    def debug(self, message: str, emoji: str = ""):
        """Log debug message"""
        self.logger.debug(message, extra={"emoji": emoji} if emoji else {})
        
    def info(self, message: str, emoji: str = ""):
        """Log info message"""
        self.logger.info(message, extra={"emoji": emoji} if emoji else {})
        
    def success(self, message: str, emoji: str = ""):
        """Log success message"""
        self.logger.log(
            self.SUCCESS_LEVEL,
            message,
            extra={"emoji": emoji} if emoji else {}
        )
        
    def warning(self, message: str, emoji: str = ""):
        """Log warning message"""
        self.logger.warning(message, extra={"emoji": emoji} if emoji else {})
        
    def error(self, message: str, emoji: str = ""):
        """Log error message"""
        self.logger.error(message, extra={"emoji": emoji} if emoji else {})
        
    def critical(self, message: str, emoji: str = ""):
        """Log critical message"""
        self.logger.critical(message, extra={"emoji": emoji} if emoji else {})
        
    def start_operation(self, operation_name: str):
        """Start logging a specific operation"""
        self.logger.addHandler(self.operation_handler)
        self.info(f"🚀 Starting operation: {operation_name}")
        
    def end_operation(self, success: bool = True):
        """End operation logging"""
        if success:
            self.success("✅ Operation completed successfully")
        else:
            self.error("❌ Operation failed")
            
        self.logger.removeHandler(self.operation_handler)
        self.operation_handler.close()
        
    def progress(self, current: int, total: int, message: str = ""):
        """Log progress update"""
        percentage = int((current / total) * 100)
        bar_length = 20
        filled = int((bar_length * current) / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        progress_msg = f"⚡ [{bar}] {percentage}% {message}"
        self.info(progress_msg)
