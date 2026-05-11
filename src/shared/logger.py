import logging
import sys
from .config import Config

def setup_logger(name: str) -> logging.Logger:
    """Sets up a standardized logger for Danger Line."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup multiple times
    if not logger.handlers:
        logger.setLevel(Config.LOG_LEVEL)
        
        # Force UTF-8 encoding on stderr to avoid 'charmap' errors on Windows
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
            
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(Config.LOG_LEVEL)
        
        # Formatting
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
    return logger

# Global logger for the core
logger = setup_logger("danger-line")
