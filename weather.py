import asyncio
from aiohttp import ClientSession
import config


async def get_weather(city):
    async with ClientSession() as session:
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': config.WEATHER_API_KEY,
                  'lang': 'ru', 'units': 'metric'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            try:
                weather = {weather_json["weather"][0]["description"]}
                temp = {weather_json["main"]["temp"]}
                return f'Погода в городе {city}: {weather}, температура {temp}'
            except KeyError:
                return 'Нет данных'


async def main(city):
    task = asyncio.create_task(get_weather(city))
    result = await asyncio.gather(task)
    print(result)


if __name__ == '__main__':
    asyncio.run((main('Вытегра')))
