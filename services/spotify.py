import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import logging

from config import Settings

logger = logging.getLogger(__name__)


class Spotify:
    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=Settings.SPOTIFY_CLIENT_ID,
            client_secret=Settings.SPOTIFY_CLIENT_SECRET
        )

        scope = "user-read-playback-state,user-modify-playback-state,user-library-read"

        oauth = SpotifyOAuth(
            client_id=Settings.SPOTIFY_CLIENT_ID,
            client_secret=Settings.SPOTIFY_CLIENT_SECRET,
            scope=scope,
            redirect_uri="https://spotify.zeroinside.id/callback",
            open_browser=False,
        )

        self.api = spotipy.Spotify(client_credentials_manager=auth)
        self.api_client = spotipy.Spotify(client_credentials_manager=oauth)

        self.devices = []  # luist of devuces <id,is_active,is_private_session,is_restricted,name,type,volume>

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

        response = self.api_client.current_user_playlists()  # My Playlist

        response = self.api_client.volume(volume_percent=60, device_id=my_device['id'])

    def search_device(self, name: str):
        # get devices by name
        result = [device for device in self.devices if device['name'] == name]
        return result[0]


if __name__ == '__main__':
    spotify = Spotify()
    spotify.explore()
