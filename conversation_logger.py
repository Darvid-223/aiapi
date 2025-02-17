import os
from dotenv import load_dotenv
import logging
from logging.handlers import SysLogHandler

load_dotenv()


def configure_papertrail_logging():
    """
    Configures logging to send logs to Papertrail.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log nivå (INFO, WARNING, ERROR, etc.)

    # Konfigurera Papertrail SysLogHandler
    papertrail_handler = SysLogHandler(address=("logs2.papertrailapp.com", int(os.environ.get("PAPERTRAIL_PORT"))))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    papertrail_handler.setFormatter(formatter)
    
    logger.addHandler(papertrail_handler)
    
    return logger
