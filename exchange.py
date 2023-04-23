from typing import Union

from aiohttp import ClientSession

from config import EXCHANGE_API_KEY


async def change_money(currency: str, target_currency: str, amount: str) -> Union[int, str]:
    '''
    Функция принимает на вход три параметра в виде строки, currency - текущая валюта,
    target_currency - целевая валюта для обмена, amount - количество.
    Делает запрос к сервису Exchange Rates AP и возвращает результат обмена валют.
    '''
    async with ClientSession() as session:
        url = 'https://api.apilayer.com/exchangerates_data/convert'
        headers = {'apikey': EXCHANGE_API_KEY}
        params = {'to': target_currency.upper(), 'from': currency.upper(), 'amount': int(amount)}

        async with session.get(url=url, headers=headers, params=params) as response:
            current_json = await response.json()
            try:
                result = current_json['result']
                return result
            except KeyError:
                return 'Нет данных'
