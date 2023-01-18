from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


def get_logging():
    if os.getenv("ENV_NAME") == 'development':
        return 'logging_dev.conf'
    else:
        return 'logging_prod.conf'


class Settings:
    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    CITY_LATITUDE = float(os.getenv("CITY_LATITUDE"))
    CITY_LONGITUDE = float(os.getenv("CITY_LONGITUDE"))
    ROOT_DIR = os.path.dirname(os.path.abspath("__FILE__"))
    ENV_NAME = os.getenv("ENV_NAME")
    MORNING_GREETINGS_HOUR = os.getenv("MORNING_GREETINGS_HOUR")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIPY_CLIENT_USERNAME = os.getenv("SPOTIPY_CLIENT_USERNAME")
    DEVICE_NAME = os.getenv("DEVICE_NAME")
    LOG_FILE_CONFIG = get_logging()