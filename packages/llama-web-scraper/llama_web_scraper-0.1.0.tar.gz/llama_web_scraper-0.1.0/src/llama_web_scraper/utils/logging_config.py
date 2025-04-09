import os

from config import settings
from loguru import logger


def setup_logging():
    logger.remove()
    os.makedirs("logs", exist_ok=True)
    logger.add("logs/app.log", rotation="1 week", level=settings.log_level.upper())
    logger.add(lambda msg: print(msg, end=""), level=settings.log_level.upper())


setup_logging()
