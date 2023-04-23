
## Установка

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install requirements.txt`
4. Создайте файл `config.py`
5. Впишите в `config.py` переменные:
```
TG_API_KEY = 'API ключ бота, полученный в BotFather'
WEATHER_API_KEY = 'API ключ, для сервиса OpenWeathermap'
EXCHANGE_API_KEY = 'API ключ, для сервиса Exchange Rates'
UNSPLASH_API_KEY = 'API ключ, для сервиса Unsplash'
```
6. Запустите бота командой `python bot.py`

### Функционал бота
1. `/start` Начать работу с ботом.
2. `/photo` Присылает забавную картинку с животным.
3. `/weather` Получить погоду в выбранном городе.
4. `/exchange` Узнать текущий курс валют.
5. `/quiz` Создать опрос.
6. `/help` Прислать список доступных комманд.