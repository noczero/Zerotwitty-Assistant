import os
import random
from datetime import datetime
import pathlib
from operator import itemgetter
import tweepy
import logging
from os import path
import stylecloud as sc

from config import Settings
from services.weather import Weather

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

        self.city = None

    def send_message(self, msg: str):
        logger.info(f"Send Tweet using API v1 : {msg}")
        try:
            response = self.api.update_status(msg)
            logger.debug(f"Response : {response}")
        except Exception as e:
            logger.error(f"Failed to send, {e}")

    def send_message_v2(self, msg: str, media_filename: str = None):
        logger.info(f"Send Tweet using API v2 : {msg}")
        try:
            if media_filename:
                # any media
                media = self.api.media_upload(media_filename)
                response = self.api_v2.create_tweet(text=msg, media_ids=[media.media_id_string])
            else:
                # without meda
                response = self.api_v2.create_tweet(text=msg)

            logger.debug(f"Response : {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send, {e}")
            return None

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

        # get place trends
        response = self.api.closest_trends(Settings.CITY_LATITUDE, Settings.CITY_LONGITUDE)
        self.city = response[0]
        logger.debug(f"RAW : {response}, woeid : {response[0]['woeid']}")

        response = self.api.get_place_trends(id=self.city['woeid'])
        logger.debug(response)

    def get_top_trend(self, limit: int = 3):
        self.city = self.api.closest_trends(Settings.CITY_LATITUDE, Settings.CITY_LONGITUDE)[0]
        response = self.api.get_place_trends(id=self.city['woeid'])

        # remove none from tweet vvolume
        clean_list = []
        for item in response[0]['trends']:
            if item['tweet_volume']:
                clean_list.append(item)

        # sorted by tweet_volume
        trend_by_volumes = sorted(clean_list, key=itemgetter('tweet_volume'), reverse=True)

        result_str = ''
        topic_total = 0
        for i, item in enumerate(trend_by_volumes):
            if i >= limit - 1 and topic_total > 0:
                result_str += f"and {item['name']}"
                break
            else:
                if limit > 2:
                    result_str += f"{item['name']}, "
                elif limit > 1:
                    result_str += f"{item['name']} "
                else:
                    result_str += item['name']
                    break
                topic_total += 1

        return result_str

    def get_care_message(self, max_length=200, min_length=100):
        # more human remind bot
        user = self.api_v2.get_user(username="tssremindbot")
        # get tweet, just 10, only public account not private
        response = self.api_v2.get_users_tweets(user.data.id)
        logger.debug(response)

        # using randomize
        result = ''
        found = False
        while not found:
            random_index = random.randint(0, 9)
            raw_text = response.data[random_index]['text']
            split_text = raw_text.split('\n')
            text = split_text[2]

            # check length
            if max_length > len(text) > min_length:
                result = text
                found = True

        return result

    def morning_greetings(self):
        # get trends
        success = False
        limit = 3
        max_length = 200
        min_length = 100
        while not success:
            trends_str = self.get_top_trend(limit=limit)
            weather_str = Weather(city_name=self.city['name']).get_weather()
            care_msg_str = self.get_care_message(max_length=max_length, min_length=min_length)

            text_format = f"Currently in your location is {weather_str}. \n" \
                          f"{care_msg_str} " \
                          f"Most local people tweet about {trends_str}.\n"

            logger.debug(f"{text_format}, length {len(text_format)}")

            if len(text_format) <= 280:

                # generated word clouds
                suffix = datetime.now().strftime("%y%m%d_%H%M%S")
                filename = f"cloud_word_{suffix}"
                sc.gen_stylecloud(
                    text=text_format,
                    palette='colorbrewer.sequential.Blues_9',
                    font_path=f'{Settings.ROOT_DIR}/assets/OpenSans-SemiBold.ttf',
                    icon_name="fab fa-twitter",
                    output_name=f'{Settings.ROOT_DIR}/assets/{filename}.png',
                    gradient='horizontal',
                )

                # send tweet using media
                self.send_message_v2(msg=text_format, media_filename=f'{Settings.ROOT_DIR}/assets/{filename}.png')
                success = True
                logger.info("Tweet has been sent")
            else:
                # change params
                limit -= 1
                max_length -= 25
                min_length -= 25

    def try_upload_media(self):
        media = self.api.media_upload(f'{Settings.ROOT_DIR}/assets/media_test.png')
        response = self.api_v2.create_tweet(text='test', media_ids=[media.media_id_string])
        logger.debug(response)


if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    # bot.send_message_v2(f"Hello world from bot! APIv2 {str(datetime.now())}")
    # bot.get_my_user_data()
    bot.get_top_trend()
