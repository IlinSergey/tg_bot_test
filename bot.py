import logging
from config import TG_API_KEY

from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


bot = Bot(token=TG_API_KEY)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    logging.info("Бот стартовал")
    executor.start_polling(dp, skip_updates=True)
