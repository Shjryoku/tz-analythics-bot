import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger("error_logger")
logger.setLevel(logging.ERROR)

file_handler = RotatingFileHandler(
    "errors.log", maxBytes=1024, backupCount=1, encoding="utf-8"
)
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)