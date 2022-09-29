import requests
from bs4 import BeautifulSoup


def beautiful_tracks_item_format_list(track_result: list) -> str:
    list_result_str = ''
    for idx, item in enumerate(track_result['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
        list_result_str += f"{idx} {track['artists'][0]['name']} - {track['name']} \n"

    return list_result_str


def parsing_artist_str(artists: [dict]) -> str:
    parsing_artist = ''
    for index, artist in enumerate(artists):
        if len(artists) > 1:
            if index == 1:
                # second artist
                parsing_artist += f"(feat. {artist['name']}"

            if index == len(artists) - 1:
                # last list
                parsing_artist += ")"  # closing
                break

            parsing_artist += artist['name']
        else:
            parsing_artist += artist['name']

    return parsing_artist


def parsing_to_twitter_msg(current_track: dict, summary:str) -> tuple:
    artists = current_track['item']['artists']
    artists_str = parsing_artist_str(artists)

    if current_track['context']:
        playlist_url = current_track['context']['external_urls']['spotify']
    else:
        playlist_url = current_track['playlist']['external_urls']['spotify']

    format_text = f"🎧 Now playing {current_track['item']['name']} - {artists_str}. {summary} " \
                  f"Check out my playlist on {playlist_url}"

    img_url = current_track['item']['album']['images'][0]['url']

    return format_text, img_url


def scrape_lyrics(artistname, songname, join_name=None):
    # function to scrape lyrics from genius
    if not join_name:
        artistname2 = str(artistname.replace(' ', '-')) if ' ' in artistname else str(artistname)
        songname2 = str(songname.replace(' ', '-')) if ' ' in songname else str(songname)
        page = requests.get('https://genius.com/' + artistname2 + '-' + songname2 + '-' + 'lyrics')
    else:
        page = requests.get('https://genius.com/' + join_name + '-' + 'lyrics')

    html = BeautifulSoup(page.text, 'html.parser')
    print(html)
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics


def generate_informational_features(result: dict):
    """
    Get more informationa track features
    https://www.therecordindustry.io/spotify-audio-features/
    :param result:
    :return:
    """
    if result['valence'] > 0.5:
        valance_str = 'It sounds more positive vibes, so enjoy it'
    else:
        valance_str = "But, it sounds less positive vibes, so just enjoy it"

    dance_str = ''
    if result['danceability'] > 0.5:
        dance_str = 'It can be used for dancing.'

    if result['energy'] > 0.5:
        energy_str = 'high'
    else:
        energy_str = 'low'

    result_str = f"It has {result['tempo']} bpm tempo, {result['key']} pitch class, and {energy_str} energy. " \
                 f"{valance_str}. {dance_str}".strip()

    return result_str
