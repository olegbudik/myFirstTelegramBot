#  МОЙ ПЕРВЫЙ БОТ с помощью библиотеки aiogram

#  ШАГ 1. Импортируем все необходимые библиотеки
#  импортируем токены из конфиг файла
from config import TOKEN, open_weather_token

#  для погоды, биатлона импортируем
import requests
from bs4 import BeautifulSoup

#  импортируем необходимые библиотеки
from aiogram import Bot, Dispatcher, executor, types
import datetime
from db_weather import db_weather  # файл, содержащий базу для погоды


#  ШАГ 2.
#  Объект бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

#  Диспетчер для бота
dp = Dispatcher(bot)


#  ШАГ 3
""" ================================= START ========================================"""
#  Приветствие бота
@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           """\tПривет!\nМеня зовут FIRSTBOT!
                            """)

# создаем кнопки для начала работы
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Поехали", "Помощь"]
    keyboard.add(*buttons)
    await message.answer("Ну что начали или нужна помощь, чтобы узнать что я умею?", reply_markup=keyboard)

#  Просим у бота помощи при нажатии кнопки Помощь
@dp.message_handler((lambda message: message.text == "Помощь"))
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Я могу показать погоду\n'
                                                 'Показать новости биатлона\n'
                                                 'Показать новости футбола\n'
                                                 'Бросать кости')

# создаем кнопки при нажатии ПОЕХАЛИ
@dp.message_handler((lambda message: message.text == "Поехали"))
async def big_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Биатлон", "Погода", "Футбол", "Кости", "Помощь"]
    keyboard.add(*buttons)
    await message.answer("Я готов", reply_markup=keyboard)


"""" =============================  КОСТИ  ================================== """

#  Бросаем кости
@dp.message_handler((lambda message: message.text == "Кости"))
async def cmd_dice(message: types.Message):
    await message.bot.send_dice(message.from_user.id, emoji="🎲")


''' ================================ НОВОСТИ БИАТЛОНА ==================================== '''
# @dp.message_handler(commands= "biathlon")
@dp.message_handler((lambda message: message.text == "Биатлон"))
async def process_biathlon(message: types.Message):

    URL = 'https://www.biathlon.com.ua/ua/'
    HEADERS = {'Accept': '*/*', 'User-Agent':
	            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
                }
## функция получения html
    def get_html(url, params = ''):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

## функция получения контента
    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_= "news-item")
        news = []
        url_news = []
        for item in items:
            news.append(
                (item.find('td', class_="news_title").find('a').get_text(strip=True))
                        )

            url_news.append(
                URL + (item.find('td', class_="news_title").find('a').get('href'))
            )

        news_out = f'{news[0]}\n{url_news[0]}\n{news[1]}\n{url_news[1]}\n' \
                   f'{news[2]}\n{url_news[2]}\n{news[3]}\n{url_news[3]}\n{news[4]}\n{url_news[4]}'
        return news_out



    html = get_html(URL)
    news = get_content(html.text)



    await bot.send_message(message.from_user.id, news)

''' =============================  ФУТБОЛ  ======================================='''
# НОВОСТИ ФУТБОЛА
@dp.message_handler(lambda message: message.text == "Футбол")
async def process_football(message: types.Message):

    URL = 'https://football24.ua/ru/'
    HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
               }

    # функция получения html
    def get_html(url, params=''):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    # функция получения контента
    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items_url = soup.find_all('li', class_="news-list-item important")
        items_news = soup.find_all('div', class_='title')
        news = []
        url_news = []

        for item in items_url[:8]:
            url_news.append(
                item.find('a').get('href')
            )

        for item in items_news[:8]:
            news.append(item.text.strip()
                        )

        news_out_football= f'{news[0]}\n{url_news[0]}\n{news[1]}\n{url_news[1]}\n' \
                           f'{news[2]}\n{url_news[2]}\n{news[3]}\n{url_news[3]}\n' \
                           f'{news[4]}\n{url_news[4]}\n{news[5]}\n{url_news[5]}\n' \
                           f'{news[6]}\n{url_news[6]}\n{news[7]}\n{url_news[7]}'
        print(news_out_football)
        return news_out_football



    html = get_html(URL)
    football_news = get_content(html.text)
    await bot.send_message(message.from_user.id, football_news)

'''=============================== ПОГОДА ========================================'''
# ЗАПРОС ПОГОДЫ
@dp.message_handler(lambda message: message.text == "Погода")
async def process_get_city(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вводим локацию: ')
@dp.message_handler(content_types="text")
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
                                             f'Описание  {db_weather[description_weather]}')
    await bot.send_message(msg.from_user.id, f' Хорошего дня! ')

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



