#  МОЙ ПЕРВЫЙ БОТ с помощью библиотеки aiogram

#  ШАГ 1. Импортируем все необходимые библиотеки
#  импортируем токены из конфиг файла
from config import TOKEN, open_weather_token
#  для погоды импортируем
import requests
#  импортируем необходимые библиотеки
import logging
from aiogram import Bot, Dispatcher, executor, types
import datetime
from db_weather import db_weather

#  ШАГ 2.
#  Объект бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
#  Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

#  ШАГ 3.
#  Приветствие бота
@dp.message_handler(commands=['start'])
async def process_hello(message: types.Message):
    await bot.send_message(message.from_user.id,'Привет!\nМеня зовут FIRSTBOT!\n'
                                                'Введи /help, чтобы узнать что я умею')

#  Просим у бота помощи
@dp.message_handler(commands=['help'])
async def process_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Я могу пока найти погоду - /weather')

'''=============================== ПОГОДА ========================================'''

# ЗАПРОС ПОГОДЫ
@dp.message_handler(commands= "weather")
async def process_get_city(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вводим локацию: ')
@dp.message_handler(content_types=["text"])
async def process_get_weather(msg: types.Message):
    city = msg.text
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}'
                         f'&appid={open_weather_token}&units=metric')
    data_weather = r.json()
    errs = {"cod":"404","message":"city not found"}
    if data_weather == errs:
        await bot.send_message(msg.from_user.id,'Проверь локацию')
    else:
        city = data_weather['name']
        temp = data_weather['main']['temp']
        pressure = data_weather['main']['pressure']
        humidity = data_weather['main']['humidity']
        description_weather = data_weather['weather'][0]['main']
        today = datetime.datetime.now()
        today_string = today.strftime(" %d-%b-%Y ")

    await bot.send_message(msg.from_user.id, f'Погода на {today_string} для {city}:\n'
                                             f'Температура  {int(temp)} C\n'
                                             f'Давление  {pressure} мм рт.ст\n'
                                             f'Влажность  {humidity} %\n'
                                             f'Описание  {db_weather[description_weather]}\n'
                                             f'------- Хорошего дня! -------')

''' =========================================== ПОПУГАЙ ====================================== '''

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# #  Бросаем кости
# @dp.message_handler(commands="dice")
# async def cmd_dice(message: types.Message):
#     await message.bot.send_dice(message.from_user.id, emoji="🎲")
#
# #  Отправляем назад сообщения ПОПУГАЙ
# @dp.message_handler(commands="reply")
# async def cmd_answer(message: types.Message):
#     await message.answer('Начинаю повторять')
#
# @dp.message_handler()
# async def echo_message(msg: types.Message):
#         await bot.send_message(msg.from_user.id, msg.text)
