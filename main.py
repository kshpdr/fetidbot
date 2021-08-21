import os
import telebot
import random
import psycopg2

# environment for starting server and webhook
from flask import Flask, request
import logging

# for taking comments out from the photos
from PIL import Image

#import requests
#import datetime

bot = telebot.TeleBot('***REMOVED***')
url = "https://api.telegram.org/bot***REMOVED***/"

# for local use
# conn = psycopg2.connect(database="fetidbot", user="denis", password="KatzeVanya", host="127.0.0.1", port="5432")
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

path = "photos"
files = os.listdir(path)

# class BotHandler:
#
#     def __init__(self, token):
#         self.token = token
#         self.api_url = "https://api.telegram.org/bot{}/".format(token)
#
#     def get_updates(self, offset=None, timeout=30):
#         method = 'getUpdates'
#         params = {'timeout': timeout, 'offset': offset}
#         resp = requests.get(self.api_url + method, params)
#         result_json = resp.json()['result']
#         return result_json
#
#     def send_message(self, chat_id, text):
#         params = {'chat_id': chat_id, 'text': text}
#         method = 'sendMessage'
#         resp = requests.post(self.api_url + method, params)
#         return resp
#
#     def get_last_update(self):
#         get_result = self.get_updates()
#
#         if len(get_result) > 0:
#             last_update = get_result[-1]
#         else:
#             last_update = get_result[len(get_result)]
#
#         return last_update

# inserting chat_id in data base
def insert_user(chat_id, message):
    cur.execute("INSERT INTO users (chat_id) \
                VALUES (%d) \
                ON CONFLICT (chat_id) DO NOTHING" % message.chat.id)
    conn.commit()



# inserting chat_id and photo_name in data base
def insert_photo(chat_id, message, photo):
    cur.execute("SELECT * FROM sent_photos")
    # checking whether photo has been already sent
    row = cur.fetchone()
    while row is not None:
        if row[1] == photo and row[0] == chat_id:
            return False
        row = cur.fetchone()

    # if not, addr to database and update photos amount
    cur.execute("INSERT INTO sent_photos (chat_id, photo_name)\
                    VALUES (%d, '%s') \
                ON CONFLICT ON CONSTRAINT unique_photos DO NOTHING" % (chat_id, photo))
    cur.execute("UPDATE users SET total_photos = total_photos + 1 WHERE chat_id = '%d'" % chat_id)
    conn.commit()
    return True

@bot.message_handler(commands=['start', 'help', 'hui'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Ваня! На самом деле, вонючка. Потому что воняю. Если тебе грустно, я подниму тебе настроение своей мордашкой!\n "
                                      "\nПока что я немного глупая и особо ничего не умею, но ты можешь написать мне что угодно, я тебя порадую. Правда моя мордашка придет не сразу, а секунд через пять, но как говорится: кто не терпит, тот не русский.")
    insert_user(message.chat.id, message)

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


@bot.message_handler(func=lambda m: True)
def send_photo(message):
    cur.execute("SELECT * FROM users WHERE chat_id = %d" % message.chat.id)
    row = cur.fetchone()
    if row[1] == len(files):
        bot.send_message(message.chat.id, "К сожалению, коллекция вонючкинса закончилась. Мы отправили запрос на пополнение и пришлем новую мордушка как только, так сразу!")
        bot.send_message(206662948, "У кого-то закончился вонючкинс! Срочно контента!")
        return
    d = random.choice(files)
    # recursively go through all photos to find a new one
    if insert_photo(message.chat.id, message, d):
        comment = Image.open(f"photos/{d}").info["comment"].decode("utf-8")
        bot.send_photo(message.chat.id, photo=open(f"photos/{d}", "rb"), caption=comment)
    else:
        send_photo(message)

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
        bot.set_webhook(url="https://vast-ravine-49209.herokuapp.com") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)

#bot.polling()