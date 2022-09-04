import logging
import logging.config
import schedule
import time

from config import Settings, get_logging
from src.bot import ZeroTwittyAssistant

logging.config.fileConfig(f'{Settings.ROOT_DIR}/logs/{Settings.LOG_FILE_CONFIG}', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def send_morning_greetings():
    bot = ZeroTwittyAssistant()
    bot.morning_greetings()
    logger.info(schedule.get_jobs())


if __name__ == '__main__':
    schedule.every().day.at(Settings.MORNING_GREETINGS_HOUR).do(send_morning_greetings)

    logger.info(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)
