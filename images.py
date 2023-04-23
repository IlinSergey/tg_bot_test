from aiohttp import ClientSession

from config import UNSPLASH_API_KEY


async def get_image(image_name: str) -> str:
    '''
    Функция принимает на вход строку с названием картинки, выполняет запрос к сервису Unsplash,
    и возвращает ссылку на рандомную картинку согласно запроса.
    '''
    async with ClientSession() as session:
        url = 'https://api.unsplash.com/photos/random'
        params = {'query': image_name, 'client_id': UNSPLASH_API_KEY}
        async with session.get(url=url, params=params) as response:
            image_json = await response.json()
            try:
                result = image_json['urls']['regular']
                return result
            except KeyError:
                return 'Нет данных, ошибка в получении картинки.'
