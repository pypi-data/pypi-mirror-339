
import os
import logging
from pathlib import Path

from battkit.logging_config import logger

# Hides non-specified functions from auto-import
__all__ = [
    'MEMORY_LIMIT',
]


MEMORY_LIMIT = 4    # Maximum amount of data that can loaded into memory (in Gb)

logger.info("BattKit logger intiallized.")