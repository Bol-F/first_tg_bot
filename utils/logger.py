import logging
import sys
from utils.config import Config


def setup_logger():
    """Setup logging configuration"""
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log_level,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("bot.log", encoding="utf-8"),
        ],
    )

    # Reduce httpx logging noise
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
