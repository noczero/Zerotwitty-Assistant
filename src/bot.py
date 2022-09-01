import random
from datetime import datetime
import pathlib

import tweepy
import logging
from os import path

from config import Settings

logger = logging.getLogger(__name__)


class ZeroTwittyAssistant():
    def __init__(self):
        auth = tweepy.OAuthHandler(
            consumer_key=Settings.API_KEY,
            consumer_secret=Settings.API_KEY_SECRET
        )
        auth.set_access_token(
            key=Settings.ACCESS_TOKEN,
            secret=Settings.ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(auth=auth,
                              wait_on_rate_limit=True)

        self.api_v2 = tweepy.Client(consumer_key=Settings.API_KEY,
                                    consumer_secret=Settings.API_KEY_SECRET,
                                    access_token=Settings.ACCESS_TOKEN,
                                    access_token_secret=Settings.ACCESS_TOKEN_SECRET,
                                    bearer_token=Settings.BEARER_TOKEN)

        self.user_data = self.get_my_user_data().data  # <id,name,username>

    def send_message(self, msg: str):
        logger.info(f"Send Tweet using API v1 : {msg}")
        try:
            response = self.api.update_status(msg)
            logger.debug(f"Response : {response}")
        except Exception as e:
            logger.error(f"Failed to send, {e}")

    def send_message_v2(self, msg: str):
        logger.info(f"Send Tweet using API v2 : {msg}")
        try:
            response = self.api_v2.create_tweet(text=msg)
            logger.debug(f"Response : {response}")
        except Exception as e:
            logger.error(f"Failed to send, {e}")

    def get_my_user_data(self):
        response = self.api_v2.get_me()
        logger.debug(
            f"RAW : {response}, id : {response.data.id}, name : {response.data.name}, username : {response.data.username}")
        return response

    def get_home_timeline(self):
        response = self.api_v2.get_home_timeline()
        logger.debug(response)

    def explore(self):
        user = self.api_v2.get_user(username="testdrivenio")
        logger.debug(user)

        # get tweet, just 10, only public account not private
        response = self.api_v2.get_users_tweets(user.data.id)
        logger.debug(response)

        # get single tweet from id
        response = self.api_v2.get_tweet(id=1564613426491670529)
        logger.debug(response)

        # get followers
        response = self.api_v2.get_users_followers(id=user.data.id)
        logger.debug(response)

        # get user mentions
        response = self.api_v2.get_users_mentions(id=user.data.id)
        logger.debug(response)

        # get my pinned list
        response = self.api_v2.get_pinned_lists()
        logger.debug(response)

        # get my pinned list
        response = self.api.get_direct_messages()
        logger.debug(response)


if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    # bot.send_message_v2(f"Hello world from bot! APIv2 {str(datetime.now())}")
    # bot.get_my_user_data()
    bot.explore()
