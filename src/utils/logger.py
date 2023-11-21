import logging
from src.utils.config import LOG_LEVEL

LOGGER_NAME = "Kite-clone-python"


def initialize_logging():
    # settig default log_level to info
    log_level = logging.INFO
    if LOG_LEVEL == "info":
        log_level = logging.INFO
    elif LOG_LEVEL == "error":
        log_level = logging.ERROR
    elif LOG_LEVEL == "debug":
        log_level = logging.DEBUG
    elif LOG_LEVEL == "warning":
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)


LOG = logging.getLogger(LOGGER_NAME)
