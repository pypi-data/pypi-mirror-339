
import os, sys
import logging
import logging.config
from pathlib import Path




# ==============================================================================
#   DEFINE COMMON FILEPATHS
# ==============================================================================
DIR_MAIN = Path(os.path.abspath(os.path.dirname(__file__)))
DIR_LOG = DIR_MAIN.parent.joinpath("logs")


# ==============================================================================
#   SETUP LOGGER
# ==============================================================================
logger = logging.getLogger("battkit")


# Only configure the logger if it hasn't been configured already
def setup_logging(level=logging.DEBUG, logging_dir=None):
    """
    Configures logging for the entire package.

    Args:
        name (str): Create logger with the specified name.
        level (int): The minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    # Clear existing loggers and handlers to prevent duplicate log entries
    logging.getLogger().handlers = []
    logging.getLogger().filters = []
    
    # Create log directory if it doesn't exist
    if logging_dir is None:
        logging_dir = Path(os.path.abspath(os.path.dirname(__file__))).parent.joinpath("logs")
    if not os.path.isdir(logging_dir):  os.mkdir(logging_dir)

    # Define log config
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(process)d - [%(module)s.%(funcName)s] - %(message)s"
            },
            "readable": {
                "format": "%(asctime)s - %(levelname)s - %(message)s",
                "datefmt":"%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "readable",
                "level": level,
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "level": level,
                "filename": os.path.join(logging_dir, f"battkit.log"),
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": level,
        },
        "loggers": {
            "battkit": {
                "handlers": ["console", "file"],
                "level": level,
                "propagate": False,
            }
        },
    }

    # Apply logging config
    logging.config.dictConfig(log_config)

    # Initiallize logger
    logger = logging.getLogger("battkit")
    logger.info("Intiallized logger")

    return logger

if not logger.hasHandlers():
    logger = setup_logging(level=logging.DEBUG, logging_dir=DIR_LOG)

