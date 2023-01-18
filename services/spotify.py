import json
import random
import time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import logging

from config import Settings
from services.utils.spotify_helpers import beautiful_tracks_item_format_list, \
    scrape_lyrics, generate_informational_features, parsing_to_twitter_msg

logger = logging.getLogger(__name__)


class Spotify:
    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=Settings.SPOTIFY_CLIENT_ID,
            client_secret=Settings.SPOTIFY_CLIENT_SECRET
        )

        scope = "user-read-playback-state," \
                "user-modify-playback-state," \
                "user-library-read," \
                "app-remote-control"

        oauth = SpotifyOAuth(
            client_id=Settings.SPOTIFY_CLIENT_ID,
            client_secret=Settings.SPOTIFY_CLIENT_SECRET,
            scope=scope,
            redirect_uri="https://spotify.zeroinside.id/callback",
            open_browser=False,
        )

        self.api = spotipy.Spotify(client_credentials_manager=auth)
        self.api_client = spotipy.Spotify(client_credentials_manager=oauth)

        self.devices = self.api_client.devices()[
            'devices']  # luist of devuces <id,is_active,is_private_session,is_restricted,name,type,volume>
        self.my_playlist = self.api_client.current_user_playlists()  # My Playlist
        self.track_features = None  # <danceability, energy, valance, acousticness> # https://www.therecordindustry.io/spotify-audio-features/

    def explore(self):
        artist_name = "avenged sevenfold"
        query = f"artist:{artist_name}"

        # type - the types of items to return. One or more of 'artist', 'album',
        #                          'track', 'playlist', 'show', and 'episode'.  If multiple types are desired,
        #                          pass in a comma separated string; e.g., 'track,album,episode'
        response = self.api.search(q=query, type='artist')
        logger.debug(response)

        track_name = "so far away"
        query = f"track:{track_name}"
        response = self.api.search(q=query, type='track')
        logger.debug(response)

        response = self.api_client.me()  # denied
        logger.debug(response)

        response = self.api_client.devices()
        self.devices = response['devices']  # set first devices as play
        logger.debug(self.devices)

        my_device = self.search_device(name='Nexus 5')
        # logger.debug(my_device)
        # response = self.api_client.pause_playback(device_id=my_device['id'])
        # logger.debug(response)

        # get saved tracks
        results = self.api_client.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])

        response = self.api_client.currently_playing()

        # response = self.api_client.current_user_top_tracks() # None

        self.my_playlist = self.api_client.current_user_playlists()  # My Playlist

        # response = self.api_client.volume(volume_percent=60, device_id=my_device['id'])

        # self.api_client.next_track(device_id=my_device['id'])  # next track control

        my_playlist = self.search_own_playlist(name='ZeroPlay')
        track_result = self.api_client.playlist_items(playlist_id=my_playlist['id'])

        logger.info(beautiful_tracks_item_format_list(track_result=track_result))

        # play
        # self.api_client
        self.api_client.shuffle(state=True, device_id=my_device['id'])  # shuffle
        response = self.api_client.start_playback(device_id=my_device['id'],
                                                  context_uri=my_playlist['uri'])  # play my playlist
        logger.info(response)

        time.sleep(1)
        response = self.api_client.currently_playing()
        logger.info(json.dumps(response, indent=4))

        now_playing_str, img_url = parsing_to_twitter_msg(response)
        logger.info(f"{now_playing_str}, url_img: {img_url}")

        # analysis music
        # logger.info(self.api_client.audio_analysis(track_id=response['item']['id'])) # for detailed analyusis
        self.track_features = self.api_client.audio_features(tracks=response['item']['id'])[0]  # brief
        logger.info(self.get_track_summary())
        # logger.info(self.api_client.audio_features(track_id=response['item']['id']))

        # search lyrics
        # logger.info(scrape_lyrics(artistname=response['item']['artists'][0]['name'], songname=response['item']['name']))

    def search_device(self, name: str):
        # get devices by name
        if self.devices:
            res = [device for device in self.devices if device['name'] == name]
            if len(res) > 0:
                return res[0]
        return None

    def search_own_playlist(self, name: str):
        # get my play list by name
        if self.my_playlist:
            res = [item for item in self.my_playlist['items'] if item['name'] == name]
            if len(res) > 0:
                return res[0]
        return None

    def get_track_summary(self) -> str:
        # get track summary
        if self.track_features:
            return generate_informational_features(result=self.track_features)  # get
        return ''

    def start_playing(self, device_name: str = 'Nexus 5', my_playlist_name: str = 'ZeroPlay') -> tuple:
        # find playable device
        my_device = self.search_device(name=device_name)
        twitter_msg, img_url = None, None

        if my_device:
            my_playlist = self.search_own_playlist(name=my_playlist_name)

            logger.debug(f"Playlist uri : {my_playlist}")

            tracks_list = self.api_client.playlist_items(my_playlist['id'])

            logger.debug(f"Tracks list: {tracks_list}")

            # self.api_client.shuffle(state=True, device_id=my_device['id'])  # shuffle
            # logger.info(random.randint(0, tracks_list['total']))

            choosen_track = tracks_list['items'][random.randint(0, tracks_list['total'])]

            logger.debug(f"Choosen track {choosen_track}")

            self.api_client.start_playback(device_id=my_device['id'],
                                           # context_uri=my_playlist['uri']
                                           uris=[choosen_track['track']['uri']]
                                           )  # play my playlist

            time.sleep(1.5)  # wait 1.5 sec

            current_track = self.api_client.currently_playing()  # get playing tracks

            # add playlist key
            current_track['playlist'] = my_playlist

            logger.debug(f"Current track {current_track}")

            # get summary
            self.track_features = self.api_client.audio_features(tracks=current_track['item']['id'])[0]  # brief

            # parsing result to one string and img url for uplading in tweet
            twitter_msg, img_url = parsing_to_twitter_msg(current_track=current_track, summary=self.get_track_summary())

        return twitter_msg, img_url


if __name__ == '__main__':
    spotify = Spotify()
    spotify.start_playing(device_name=Settings.DEVICE_NAME)
