from aiohttp import ClientSession

import config


async def get_weather(city: str) -> str:
    '''
    Функция принимает на вход строку с названием города и делает запрос к сервису OpenWeathermap
     и возвращает строку с информацией о текущей погоде в заданном городе.
    '''
    async with ClientSession() as session:
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': config.WEATHER_API_KEY,
                  'lang': 'ru', 'units': 'metric'}
        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            try:
                weather = weather_json["weather"][0]["description"]
                temp = round(int(weather_json["main"]["temp"]))
                return f'Погода в городе {city}: {weather}, температура {temp} градусов.'
            except KeyError:
                return 'Нет данных, проверьте корректность названия города!'
