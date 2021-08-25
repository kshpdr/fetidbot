import os
import telebot
import random
import psycopg2
import config

# environment for starting server and webhook
from flask import Flask, request
import logging

# for taking comments out from the photos
from PIL import Image
import requests
from imgurpython import ImgurClient
import posixpath
import urllib.parse

from database import insert_user, insert_photo

bot = telebot.TeleBot(config.telegram_token)
url = config.telegram_url

# for local use
# conn = psycopg2.connect(database="fetidbot", user="denis", password="KatzeVanya", host="127.0.0.1", port="5432")
# DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(config.database_url, sslmode='require')
cur = conn.cursor()

# path = "photos"
# files = os.listdir(path)

client = ImgurClient(config.client_id, config.client_secret, config.access_token, config.refresh_token)


@bot.message_handler(commands=['start', 'help', 'hui'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Ваня! На самом деле, вонючка. Потому что воняю. Если тебе грустно, я подниму тебе настроение своей мордашкой!\n "
                                      "\nПока что я немного глупая и особо ничего не умею, но ты можешь написать мне что угодно, я тебя порадую. Правда моя мордашка придет не сразу, а секунд через пять, но как говорится: кто не терпит, тот не русский.")
    insert_user(message.chat.id, message)

# @bot.message_handler(func=lambda m: True)
# def send_photo(message):
#     cur.execute("SELECT * FROM users WHERE chat_id = %d" % message.chat.id)
#     row = cur.fetchone()
#     print(row)
#     if row[1] == len(files):
#         bot.send_message(message.chat.id, "К сожалению, коллекция вонючкинса закончилась. Мы отправили запрос на пополнение и пришлем новую мордушка как только, так сразу!")
#         bot.send_message(206662948, "У кого-то закончился вонючкинс! Срочно контента!")
#         return
#     d = random.choice(files)
#     while d == ".DS_Store":
#         d = random.choice(files)
#     print(d)
#     # recursively go through all photos to find a new one
#     if insert_photo(message.chat.id, message, d):
#         comment = Image.open(f"photos/{d}").info["comment"].decode("utf-8")
#         bot.send_photo(message.chat.id, photo=open(f"photos/{d}", "rb"), caption=comment)
#     else:
#         send_photo(message)

@bot.message_handler(func=lambda m: True)
def send_photo(message):
    # check how many photos have been already sent
    cur.execute("SELECT * FROM users WHERE chat_id = %d" % message.chat.id)
    row = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM photos")
    total = cur.fetchone()[0]  # number of photos
    # if it matches with amount of files, then a corresponding message
    if row[1] >= total:
        bot.send_message(message.chat.id, "К сожалению, коллекция вонючкинса закончилась. Мы отправили запрос на пополнение и пришлем новую мордушка как только, так сразу!")
        bot.send_message(206662948, "У кого-то закончился вонючкинс! Срочно контента!")
        return
    # otherwise choose a random photo
    cur.execute("SELECT * FROM photos ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    photo_link = row[0]
    # recursively go through all photos to find a new one
    if insert_photo(message.chat.id, message, photo_link):
        comment = row[1]
        bot.send_photo(message.chat.id, photo=photo_link, caption=comment)
    else:
        send_photo(message)


@bot.message_handler(func=lambda message: message.chat.id == 206662948 or message.chat.id == 189636044, content_types=['photo'])
def upload_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.telegram_token, file_info.file_path))
    file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.telegram_token, file_info.file_path)

    configs = {
        'album': config.album_id,
        'name': 'fetidbot',
    }
    image = client.upload_from_url(file_url, config=configs, anon=False)

    cur.execute("SELECT COUNT(*) FROM photos")
    total = cur.fetchone()[0]  # number of photos

    cur.execute("SELECT chat_id FROM users WHERE total_photos >= %d" % total)
    users_to_update = cur.fetchone()
    for user in users_to_update:
        bot.send_message(user, "Архив снова пополнен. Напиши мне!")

    cur.execute("INSERT INTO photos VALUES ('%s', '%s');" % (image['link'], message.caption))
    conn.commit()
    bot.send_message(message.chat.id, "Архив вонючкинсов пополнен!")

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)

    @server.route("/", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=config.app_url) # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)

#bot.polling()

