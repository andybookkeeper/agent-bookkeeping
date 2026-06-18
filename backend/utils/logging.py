import logging
import logging.handlers
import os
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(exist_ok=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with both file and console handlers."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_DIR / f"{name}.log",
            maxBytes=10485760,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
