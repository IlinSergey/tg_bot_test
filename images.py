import asyncio
from aiohttp import ClientSession
from config import UNSPLASH_API_KEY
from pprint import pprint


async def get_image(image_name: str):
    async with ClientSession() as session:
        url = 'https://api.unsplash.com/photos/random'        
        params = {'query': image_name, 'client_id': UNSPLASH_API_KEY}

        async with session.get(url=url, params=params) as response:
            image_json = await response.json()
            try:
                result = image_json['urls']['regular']
                return result
            except KeyError:
                return 'Нет данных'


async def main(image_name):
    task = asyncio.create_task(get_image(image_name))
    result = await asyncio.gather(task)
    print(result)


if __name__ == '__main__':
    asyncio.run((main('funny animal')))
