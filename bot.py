import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


from config import TG_API_KEY
from exchange import change_money
from exchange_symbols import support_exchange_symbols
from images import get_image

from utils import (help_commands, popular_currencies, keyboard,
                   keyboard_cancel, keyboard_quiz, Exchange, Quiz, Weather)
from weather import get_weather

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


srorage = MemoryStorage()
bot = Bot(token=TG_API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def greet_user(message: types.Message):
    ''' Функция отлавливает команду /start, приветствует пользователя
    и выводит информацию о своих возможностях'''
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет!\nВот что я умею:\n{help_commands}',
                           parse_mode='HTML', reply_markup=keyboard)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    ''' Функция отлавливает команду /help и возвращает список доступных комманд'''
    await bot.send_message(chat_id=message.from_user.id,
                           text=help_commands, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['cancel'], state='*')
async def command_cancel(message: types.Message, state: FSMContext):
    ''' Функция отлавливает команду /cancel для прерывания команд,
        выполняющихся в несколько запросов'''
    if state is None:
        return
    await state.finish()
    await message.reply('Комманда прервана!', reply_markup=keyboard)


# Блок функций для обработки комманды получения погоды
@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    '''Отлавливаем комманду /weather, ничинаем диалог и запрашиваем
    город для запроса погоды'''
    await message.reply('В каком городе интересует погода?',
                        reply_markup=keyboard_cancel)
    await Weather.city.set()


@dp.message_handler(state=Weather.city)
async def weather_on_city(message: types.Message, state: FSMContext):
    '''Отлавливаем введенный город и запрашиваем информацию о погоде'''
    city = message.text
    weather = await get_weather(city)
    await message.reply(weather, reply_markup=keyboard)
    await state.finish()


# Блок кода для обработки комманд для запроса курса валют
@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    '''Отлавливаем комманду /exchange, ничинаем диалог и запрашиваем
    текущую валюту'''
    await message.reply(f'Какую валюту меняем?\nСамые популярные:\n{popular_currencies}',
                        parse_mode='HTML',
                        reply_markup=keyboard_cancel)
    await Exchange.currency.set()


@dp.message_handler(lambda message: (message.text).upper() not in support_exchange_symbols,
                    state=Exchange.currency)
async def check_currency(message: types.Message):
    '''Проверяем валюту по списку поддерживаемых валют'''
    await message.reply('Данная валюта не поддерживается')


@dp.message_handler(state=Exchange.currency)
async def set_currency(message: types.Message, state: FSMContext):
    '''Запрашиваем целевую валюту'''
    async with state.proxy() as data:
        data['currency'] = message.text
    await message.reply('На какую валюту меняем?', reply_markup=keyboard_cancel)
    await Exchange.next()


@dp.message_handler(lambda message: (message.text).upper() not in support_exchange_symbols,
                    state=Exchange.target_currency)
async def check_target_currency(message: types.Message):
    '''Проверяем валюту по списку поддерживаемых валют'''
    await message.reply('Данная валюта не поддерживается')


@dp.message_handler(state=Exchange.target_currency)
async def set_turget_currency(message: types.Message, state: FSMContext):
    '''Запрашиваем количество текущей валюты'''
    async with state.proxy() as data:
        data['target_currency'] = message.text
    await message.reply('Сколько меняем?', reply_markup=keyboard_cancel)
    await Exchange.next()


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 1,
                    state=Exchange.amount)
async def check_amount(message: types.Message):
    '''Проверяем введенное количество'''
    await message.reply('Введите число и убедитесь что оно больше 0!')


@dp.message_handler(state=Exchange.amount)
async def set_amount(message: types.Message, state: FSMContext):
    '''Запрашиваем результат обмена выбранных валют по текущему курсу,
    возвращаем результат и завершаем диалог'''
    async with state.proxy() as data:
        data['amount'] = message.text
    result = await change_money(currency=data['currency'],
                                target_currency=data['target_currency'],
                                amount=data['amount'])
    result = round(result, 2)
    await message.reply(f'{result} {data["target_currency"]}', reply_markup=keyboard)
    await state.finish()


# Функция для отправки случайной, забавной картинки с животными
@dp.message_handler(commands=['photo'])
async def send_image(message: types.Message):
    '''Отлавливаем комманду /photo, запрашиваем в стороннем сервисе фото с забавным животным
    и в случае успеха, отправляем пользователю'''
    photo = await get_image('funny animal')
    await bot.send_photo(chat_id=message.chat.id,
                         photo=photo, caption='Смотри какая зверюшка!🐾',
                         reply_markup=keyboard)
    await message.delete()


# Блок кода для создания и отправки опросов (polls)
@dp.message_handler(commands=['quiz'])
async def quiz(message: types.Message):
    '''Отлавливаем комманду /quiz, ничинаем диалог для создания опроса'''
    await message.reply('Введите вопрос: ', reply_markup=keyboard_cancel)
    await Quiz.question.set()


@dp.message_handler(state=Quiz.question)
async def quiz_question(message: types.Message, state=FSMContext):
    '''Запрашиваем вопрос для опроса'''
    async with state.proxy() as data:
        data['question'] = message.text
        data['options'] = []
    await message.reply('Введите вариант ответа', reply_markup=keyboard_cancel)
    await Quiz.next()


@dp.message_handler(commands=['end'], state=Quiz.option)
async def quiz_end(message: types.Message, state=FSMContext):
    '''Комманда отлавливает комманду /end во время создания опроса,
    это означает что пользователь закончил формирование опроса.
    Отправляет сформированный опрос в чат'''
    async with state.proxy() as data:
        question = data['question']
        options = data['options']
    await bot.send_poll(chat_id=message.chat.id,
                        question=question,
                        options=options,
                        is_anonymous=False,
                        reply_markup=keyboard)
    await state.finish()


@dp.message_handler(state=Quiz.option)
async def quiz_option(message: types.Message, state=FSMContext):
    '''Запрашиваем вариант ответа для опроса, функция циклически добавляет варианты,
    пока пользователь не отправит комманду /end, которая будет перехвачена ранее'''
    async with state.proxy() as data:
        data['options'].append(message.text)
    await message.reply('Введите следующий вариант ответа или закончите ввод',
                        reply_markup=keyboard_quiz)


if __name__ == '__main__':
    logging.info("Бот стартовал")
    executor.start_polling(dp, skip_updates=True)
