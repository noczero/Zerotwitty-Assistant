import os
import random
from datetime import datetime
from operator import itemgetter

import requests
import tweepy
import logging
import stylecloud as sc

from config import Settings
from services.spotify import Spotify
from services.weather import Weather
from src.utils.word_cloud_helpers import generate_word_cloud

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

    def send_message_v2(self, msg: str, media_filename: str = None, img_url: str = None, in_reply_to_tweet_id=None):
        logger.info(f"Send Tweet using API v2 : {msg}")
        try:
            if media_filename:
                # any media
                media = self.api.media_upload(media_filename)
                response = self.api_v2.create_tweet(text=msg, media_ids=[media.media_id_string],
                                                    in_reply_to_tweet_id=in_reply_to_tweet_id)
                os.remove(media_filename)  # delete the files
            elif img_url:
                # upload from external url
                request = requests.get(img_url, stream=True)
                filename = f'{Settings.ROOT_DIR}/assets/temp.jpg'
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)

                    # upload
                    media = self.api.media_upload(filename)
                    response = self.api_v2.create_tweet(text=msg, media_ids=[media.media_id_string],
                                                        in_reply_to_tweet_id=in_reply_to_tweet_id)

                    os.remove(filename)  # delete the files
                else:
                    logger.error('Unable to download images')
                    raise Exception("Unable to download images")
            elif msg:
                # without meda
                response = self.api_v2.create_tweet(text=msg)
            else:
                raise Exception("invalid parameters, no message include")

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

        list_users = ["tssremindbot", "selfcare_bot"]

        choose_user = list_users[random.randint(0, 1)]

        user = self.api_v2.get_user(username=choose_user)
        # get tweet, just 10, only public account not private
        response = self.api_v2.get_users_tweets(user.data.id)
        logger.debug(response)

        if choose_user == "tssremindbot":
            # using randomize
            result = ''
            found = False
            while not found:
                try:
                    random_index = random.randint(0, 9)
                    raw_text = response.data[random_index]['text']
                    split_text = raw_text.split('\n')
                    text = split_text[2]

                    # check length
                    if max_length > len(text) > min_length:
                        result = text
                        found = True
                except Exception as e:
                    logger.error(f"Error parsing, {e}")
        else:
            random_index = random.randint(0, 9)
            result = response.data[random_index]['text']

        return result

    def morning_greetings(self):
        # get trends
        success = False
        limit = 3
        max_length = 200
        min_length = 100
        response = None
        while not success:
            trends_str = self.get_top_trend(limit=limit)
            weather_str = Weather(latitude=Settings.CITY_LATITUDE, longitude=Settings.CITY_LONGITUDE).get_weather()
            care_msg_str = self.get_care_message(max_length=max_length, min_length=min_length)

            # text_format = f"Currently in your location is {weather_str}. \n" \
            #               f"{care_msg_str} " \
            #               f"Most local people tweet about {trends_str}.\n"

            text_format = f"{care_msg_str}\n" \
                          f"Weather in your location was {weather_str}" \
                          f", also most people tweet {trends_str}.\n"

            logger.debug(f"{text_format}, length {len(text_format)}")

            if len(text_format) <= 280:
                # generate sc
                output_name_sc = generate_word_cloud(text_format=text_format)

                # send tweet using media
                response = self.send_message_v2(msg=text_format,
                                                media_filename=output_name_sc)
                success = True
                logger.info("Tweet has been sent")
            else:
                # change params
                limit -= 1
                max_length -= 25
                min_length -= 25

        return response

    def try_upload_media(self):
        media = self.api.media_upload(f'{Settings.ROOT_DIR}/assets/media_test.png')
        response = self.api_v2.create_tweet(text='test', media_ids=[media.media_id_string])
        logger.debug(response)

    def play_music_on_spotify(self, in_reply_to_tweet_id: str):
        spotify = Spotify()
        tweet_msg, img_url = spotify.start_playing(device_name=Settings.DEVICE_NAME)
        self.send_message_v2(msg=tweet_msg, img_url=img_url, in_reply_to_tweet_id=in_reply_to_tweet_id)


if __name__ == '__main__':
    bot = ZeroTwittyAssistant()
    # bot.send_message_v2(f"Hello world from bot! APIv2 {str(datetime.now())}")
    # bot.get_my_user_data()
    bot.get_top_trend()
