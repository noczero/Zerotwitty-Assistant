import logging
import logging.config
import os

import schedule
import time

from config import Settings, get_logging
from src.bot import ZeroTwittyAssistant

logging.config.fileConfig(f'{Settings.ROOT_DIR}/logs/{get_logging()}', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    bot.morning_greetings()
