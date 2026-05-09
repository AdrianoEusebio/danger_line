import logging
import sys
from .config import Config

def setup_logger(name: str) -> logging.Logger:
    """Sets up a standardized logger for Danger Line."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup multiple times
    if not logger.handlers:
        logger.setLevel(Config.LOG_LEVEL)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
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
