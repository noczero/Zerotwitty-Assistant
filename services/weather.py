import requests


class Weather():
    def __init__(self, city_name: str):
        self.city_name = city_name

    def get_weather(self):
        url = f'https://wttr.in/{self.city_name}'  # one line output

        """
            c    Weather condition,
            C    Weather condition textual name,
            x    Weather condition, plain-text symbol,
            h    Humidity,
            t    Temperature (Actual),
            f    Temperature (Feels Like),
            w    Wind,
            l    Location,
            m    Moon phase 🌑🌒🌓🌔🌕🌖🌗🌘,
            M    Moon day,
            p    Precipitation (mm/3 hours),
            P    Pressure (hPa),
            u    UV index (1-12),
        
            D    Dawn*,
            S    Sunrise*,
            z    Zenith*,
            s    Sunset*,
            d    Dusk*,
            T    Current time*,
            Z    Local timezone.
        
        (*times are shown in the local timezone)
        """
        params = {
            'format': '%c%t UV:%u %w %m'
        }

        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return ''


if __name__ == '__main__':
    weather = Weather(city_name="Bandung")
    print(weather.get_weather())
