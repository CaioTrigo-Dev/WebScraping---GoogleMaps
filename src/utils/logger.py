import logging
import sys
from logging import DEBUG
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "google_maps_scraper", level: str = DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt = '%d/%m/%Y %H:%M:%S',
    )

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


