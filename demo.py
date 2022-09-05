import logging
import logging.config
import os

import schedule
import time

from config import Settings, get_logging
from services.spotify import Spotify
from src.bot import ZeroTwittyAssistant

logging.config.fileConfig(f'{Settings.ROOT_DIR}/logs/{Settings.LOG_FILE_CONFIG}', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    response = bot.morning_greetings()
    bot.play_music_on_spotify(response.data['id'])

    # test spotify
    # spotify = Spotify()
    # spotify.start_playing()


