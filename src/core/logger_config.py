import logging
import logging.config
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent.parent / "logs"
LOG_PATH.mkdir(exist_ok=True, parents=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s]: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_PATH / "app.log"),
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger()