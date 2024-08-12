import logging
from logging.config import dictConfig

from mlhomeserver.settings import LOG_PATH


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
        "simple": {"format": "%(levelname)s: %(message)s"},
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": LOG_PATH,
            "maxBytes": 100_000,
            "backupCount": 3,
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {"root": {"level": "INFO", "handlers": ["file", "console"]}},
}

# Instanciamos el logger
dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("mlhomeserver")
