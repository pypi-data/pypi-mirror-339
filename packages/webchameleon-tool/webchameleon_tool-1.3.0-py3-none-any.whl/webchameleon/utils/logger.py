import logging
import os
from datetime import datetime


def configure_logging(log_level: str = "INFO", log_file: str = "webchameleon.log"):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logger = logging.getLogger("webchameleon")
    logger.info(f"Logging configured at {datetime.now().isoformat()}")


def log_action(message):
    logging.getLogger("webchameleon").info(message)
