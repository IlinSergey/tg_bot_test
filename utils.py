from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup


class Weather(StatesGroup):
    city = State()


class Exchange(StatesGroup):
    currency = State()
    target_currency = State()
    amount = State()


class Quiz(StatesGroup):
    question = State()
    option = State()
    end = State()


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


keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/weather'),
                                                         KeyboardButton('/exchange'),
                                                         KeyboardButton('/photo'),
                                                         KeyboardButton('/quiz'),
                                                         KeyboardButton('/help')
                                                         )

keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))

keyboard_quiz = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'),
                                                              KeyboardButton('/end'))
