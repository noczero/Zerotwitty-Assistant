WMO_CODE_ID_STR = {
    0: 'sangat cerah',
    1: 'cerah',
    2: 'berawan',
    3: 'mendung',
    45: 'berkabut',
    48: 'berkabut',
    51: 'gerimis kecil',
    52: 'gerimis sedang',
    55: 'gerimis besar',
    56: 'gerimis membeku kecil',
    57: 'gerimis membeku sedang',
    61: 'hujan ringan',
    63: 'hujan sedang',
    65: 'hujan lebat',
    66: 'hujan membeku ringan',
    67: 'hujan membeku lebat',
    71: 'bersalju ringan',
    73: 'bersalju sedang',
    75: 'bersalju lebat',
    77: 'butiran salju',
    80: 'gerimis ringan',
    81: 'gerimis sedang',
    82: 'gerimis lebat',
    85: 'gerimis bersalju ringan',
    86: 'gerimis bersalju berat',
    95: 'badai petir ringan',
    96: 'badai petir dengan hujan ringan',
    99: 'badai petir dengan hujan es lebat'
}

WMO_CODE_EN_STR = {
    0: 'clear sky',
    1: 'mainly clear',
    2: 'partly cloudy',
    3: 'overcast',
    45: 'fog',
    48: 'deposting rime fog',
    51: 'light drizzle',
    52: 'moderate drizzle',
    55: 'dense drizzle',
    56: 'light freezing drizzle',
    57: 'dense freezing drizzle',
    61: 'slight rain',
    63: 'moderate rain',
    65: 'heavy rain',
    66: 'light freezing rain',
    67: 'heavy freezing rain',
    71: 'slight snow fall',
    73: 'moderate snow fall',
    75: 'heavy snow fall',
    77: 'snow grains',
    80: 'slight rain showers',
    81: 'moderate rain showers',
    82: 'violent rain showers',
    85: 'slight snow showers',
    86: 'heavy snow showers',
    95: 'slight thunderstorm',
    96: 'moderate thunderstorm',
    99: 'Thunderstorm with slight and heavy hail'
}


def parse_weather_response(current_weather: list, daily_weather_list: list) -> str:
    # make sentences,

    return f"{current_weather}C and {WMO_CODE_EN_STR[current_weather['weather_code']]}, " \
           f"expecting {WMO_CODE_EN_STR[daily_weather_list[0]]} today"
