import asyncio
from aiohttp import ClientSession
from config import EXCHANGE_API_KEY
from pprint import pprint


async def change_money(currency, target_currency, amount):
    async with ClientSession() as session:
        url = 'https://api.apilayer.com/exchangerates_data/convert'
        headers = {'apikey': EXCHANGE_API_KEY}
        params = {'to': target_currency, 'from': currency, 'amount': amount}

        async with session.get(url=url, headers=headers, params=params) as response:
            current_json = await response.json()
            pprint(current_json)


async def main(currency, target_currency, amount):
    task = asyncio.create_task(change_money(currency, target_currency, amount))
    result = await asyncio.gather(task)
    print(result)


if __name__ == '__main__':
    asyncio.run((main('eur', 'rub', 10)))
