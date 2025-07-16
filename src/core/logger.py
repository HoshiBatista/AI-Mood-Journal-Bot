import logging
import sys

from pathlib import Path
from logging import Formatter, StreamHandler
from colorlog import ColoredFormatter

def setup_logger():
    log_dir = Path("../logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "bot.log"
    
    logger = logging.getLogger("mood_bot")
    logger.setLevel(logging.DEBUG)
    
    
    console_format = (
        "%(log_color)s[%(asctime)s] %(blue)s%(name)s:%(reset)s "
        "%(log_color)s%(levelname)s%(reset)s | "
        "%(cyan)s%(funcName)s:%(reset)s %(log_color)s%(message)s"
    )
    
    console_formatter = ColoredFormatter(
        console_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )
    
    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_formatter = Formatter(
        "[%(asctime)s] %(name)s:%(levelname)s | %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logger.debug("Debug message test")
    logger.info("Info message test")
    logger.warning("Warning message test")
    logger.error("Error message test")
    logger.critical("Critical message test")
    
    return logger

class LoggingMiddleware:
    def __init__(self, logger):
        self.logger = logger

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        user_info = f"{user.id} ({user.username})" if user else "Unknown"
        
        self.logger.info(
            f"Processing {type(event).__name__} from {user_info}",
            extra={'user': user_info}
        )
        
        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.error(
                f"Error handling event: {str(e)}", 
                exc_info=True,
                extra={'user': user_info}
            )
            raise