"""Consistent logging setup for CLI tools."""
from __future__ import annotations

import logging
import sys


def get_logger(name: str = "sysadmin", level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger that writes to stderr."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(handler)
    return logger
