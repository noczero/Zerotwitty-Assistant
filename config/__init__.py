from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


class Settings:
    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
