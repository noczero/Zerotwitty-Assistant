import logging.config

from src.bot import ZeroTwittyAssistant

logging.config.fileConfig('logs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    # bot.send_message_v2(f"Hello world from bot! APIv2 {str(datetime.now())}")
    # bot.get_my_user_data()
    bot.explore()