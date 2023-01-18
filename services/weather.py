import requests

from config import Settings
from services.utils.wmo_code_weather import WMO_CODE_ID_STR, WMO_CODE_EN_STR


class Weather():
    def __init__(self, city_name: str = '', latitude: float = 0.0, longitude: float = 0.0):
        self.city_name = city_name
        self.latitude = Settings.CITY_LATITUDE
        self.longitude = Settings.CITY_LONGITUDE
        self.temperature = 0.0
        self.wind_dir_angle = 315.0
        self.weather_code = 0

    def get_weather(self) -> str:
        """
            Get weather information
            Api Specs :
            https://api.open-meteo.com/v1/forecast?latitude=-6.92&longitude=107.61&timezone=auto&daily=weathercode,temperature_2m_max&current_weather=true
        """
        url = f'https://api.open-meteo.com/v1/forecast'  # one line output
        params = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timezone': 'auto',
            'current_weather': 'true',
            'daily': 'weathercode',
        }

        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            """
            {'latitude': -6.875, 'longitude': 107.5, 'generationtime_ms': 0.5249977111816406, 'utc_offset_seconds': 25200, 'timezone': 'Asia/Jakarta', 'timezone_abbreviation': 'WIB', 'elevation': 0.0, 'current_weather': {'temperature': 28.0, 'windspeed': 5.6, 'winddirection': 333.0, 'weathercode': 95, 'time': '2023-01-18T17:00'}, 'daily_units': {'time': 'iso8601', 'weathercode': 'wmo code'}, 'daily': {'time': ['2023-01-18', '2023-01-19', '2023-01-20', '2023-01-21', '2023-01-22', '2023-01-23', '2023-01-24'], 'weathercode': [96, 95, 80, 95, 95, 95, 95]}}
            """

            # parsing
            current_weather = response.json()['current_weather']
            daily_weather_code = response.json()['daily']['weathercode']  # 7 days list weather code

            text = f"{current_weather['temperature']}°C, {WMO_CODE_EN_STR[current_weather['weathercode']]}, and " \
                   f"expecting {WMO_CODE_EN_STR[daily_weather_code[0]]} until midnight"

            return text
        else:
            return "-"


if __name__ == '__main__':
    weather = Weather(latitude=Settings.CITY_LATITUDE, longitude=Settings.CITY_LONGITUDE)
    print(weather.get_weather())
