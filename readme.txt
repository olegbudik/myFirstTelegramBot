name bot: lesson_bot_oleh

username: oleh_lessons_bot

ЕСЛИ ПОЯВЛЯЕТСЯ ОШИБКА: ModuleNotFoundError: No module named 'aiogram'

надо создать правильно переменные окружения.
создание виртуальной папки с vevn
$ python3.8 -m pip install --upgrade pip
$ pip install virtualenv
$ mkdir
$ cd fonlinebot
$ virtualenv venv
#( - активировать среду, чтобы выйти bash или deactivate)
$ source venv/bin/activate  

после этого надо проинсталировать для вашей версии python3.9 (ваша версия)
$ python3.9 -m pip install -U aiogram

и запускайте ваш код после команды:
$ source venv/bin/activate


