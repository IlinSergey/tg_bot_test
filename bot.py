import logging
from config import TG_API_KEY
from weather import get_weather
from images import get_image
from exchange import change_money

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)

help_commands = '''
<b>/start</b> - <em>начать работу с ботом</em>
<b>/help</b> - <em>поддерживаемые команды</em>
<b>/weather</b> - <em>получить погоду в выбранном городе</em>
<b>/photo</b> - <em>получить забавную картинку животного</em>
<b>/exchange</b> - <em>конвертировать выбранные валюты</em>
<b>/quiz</b> - <em>создать опрос</em>
'''


popular_currencies = '''
<b>USD</b> - <em>Американский доллар</em>
<b>EUR</b> - <em>Евро</em>
<b>RUB</b> - <em>Российский рубль</em>
<b>GBP</b> - <em>Британский фунт стерлингов</em>
<b>CHF</b> - <em>Швейцарский франк</em>
<b>JPY</b> - <em>Японская иена</em>
<b>CNY</b> - <em>Китайский юань</em>
'''


srorage = MemoryStorage()
bot = Bot(token=TG_API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


class Weather(StatesGroup):
    city = State()


class Exchange(StatesGroup):
    currency = State()
    target_currency = State()
    amount = State()


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('/weather'),
             KeyboardButton('/exchange'),
             KeyboardButton('/photo'),
             KeyboardButton('/quiz'),
             KeyboardButton('/help')
             )


@dp.message_handler(commands=['start'])
async def greet_user(message: types.Message):
    await message.answer(f'Привет!\nВот что я умею:\n{help_commands}',
                         parse_mode='HTML', reply_markup=keyboard)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(help_commands, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    await message.reply('В каком городе интересует погода?')
    await Weather.city.set()


@dp.message_handler(state=Weather.city)
async def weather_on_city(message: types.Message, state: FSMContext):
    city = message.text
    weather = await get_weather(city)
    await message.reply(weather)
    await state.finish()


@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    await message.reply(f'Какую валюту меняем?\nСамые популярные:\n{popular_currencies}',
                        parse_mode='HTML')
    await Exchange.currency.set()


@dp.message_handler(state=Exchange.currency)
async def set_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
    await message.reply('На какую валюту меняем?')
    await Exchange.next()


@dp.message_handler(state=Exchange.target_currency)
async def set_turget_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['target_currency'] = message.text
    await message.reply('Сколько меняем?')
    await Exchange.next()


@dp.message_handler(state=Exchange.amount)
async def set_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    result = await change_money(currency=data['currency'],
                                target_currency=data['target_currency'],
                                amount=data['amount'])
    result = round(result, 2)
    await message.reply(f'{result} {data["target_currency"]}')
    await state.finish()


@dp.message_handler(commands=['photo'])
async def send_image(message: types.Message):
    photo = await get_image('funny animal')
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo, caption='Смотри какая зверюшка!🐾')
    await message.delete()


@dp.message_handler(commands=['quiz'])
async def make_quiz(message: types.Message):
    pass


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    logging.info("Бот стартовал")
    executor.start_polling(dp, skip_updates=True)
