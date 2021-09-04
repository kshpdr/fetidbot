import os
import telebot
import random
import psycopg2
import env_config as config
# import local_config as config

# environment for starting server and webhook
from flask import Flask, request
import logging

# for taking comments out from the photos
# was necessary for the version without data base
from PIL import Image
import requests
from imgurpython import ImgurClient
import posixpath
import urllib.parse

# for uploading and downloading files from/to google drive
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# local imports from other files
from database import insert_user, insert_photo

# for scheduled message
from threading import Thread
import schedule
import birthday_congrats as bc

bot = telebot.TeleBot(config.telegram_token)
url = config.telegram_url

# for local use
# conn = psycopg2.connect(database="fetidbot", user="denis", password="KatzeVanya", host="127.0.0.1", port="5432")
conn = psycopg2.connect(config.database_url, sslmode='require')
cur = conn.cursor()

# path = "photos"
# files = os.listdir(path)

client = ImgurClient(config.client_id, config.client_secret, config.access_token, config.refresh_token)

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()
# drive = GoogleDrive(gauth)
counter = 0

# handling a keyboard answer
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global counter
    if call.data == "further":
        bot.answer_callback_query(call.id, "Ну погнали")
        if counter == 1:
            bc.first_message()
            counter += 1
        elif counter == 2:
            bc.second_message()
            counter += 1
        elif counter == 3:
            bc.third_message()
            counter += 1
        elif counter == 4:
            bc.fourth_message()
            counter += 1
        elif counter == 5:
            bc.fifth_message()
            counter += 1
        elif counter == 6:
            bc.sixth_message()
            counter += 1
        elif counter == 7:
            bc.seventh_message()
            counter += 1
        elif counter == 8:
            bc.eighth_message()
            counter += 1
        elif counter == 9:
            bc.ninth_message()
            counter += 1
        elif counter == 10:
            bc.tenth_message()
            counter += 1
        elif counter == 11:
            bc.eleventh_message()
            counter += 1
        elif counter == 12:
            bc.twelveth_message()
            counter += 1
        elif counter == 13:
            bc.thirteenth_message()
            counter += 1
        elif counter == 14:
            bc.fourteenth_message()
            counter += 1
    elif call.data == "fake_present":
        bot.answer_callback_query(call.id, "Че, реально подарок?")
    #     if counter == 15:
    #         bc.present_fake()
    #         counter += 1
    # elif call.data == "real_present":
    #     bot.answer_callback_query(call.id, "А щас че тогда?")
    #     if counter == 16:
    #         bc.present_real()
    #         counter += 1



@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Ваня! На самом деле, вонючка. Потому что воняю. Если тебе грустно, я подниму тебе настроение своей мордашкой!\n "
                                      "\nПока что я немного глупая и особо ничего не умею, но ты можешь написать мне что угодно, я тебя порадую. Правда моя мордашка придет не сразу, а секунд через пять, но как говорится: кто не терпит, тот не русский.")
    insert_user(message.chat.id, message)


@bot.message_handler(commands=['oldbutgold'])
def birthday(message):
    comment = "Чтобы скушно не было, будем разбавлять мои гениальные сообщения не менее гениальными фотографиями! На этой например я успешно парадирую вонючку..."
    bot.send_photo(206662948, photo="https://imgur.com/rNFXNOB", caption=comment, reply_markup=bc.gen_markup())
    global counter
    counter = 1


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
    # file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.telegram_token, file_info.file_path))
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


@bot.message_handler(func=lambda message: message.chat.id == 206662948, content_types=['voice'])
def upload_voice(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(config.telegram_token, file_info.file_path)
    voice = drive.CreateFile({'parents': [{'id': '1q76yX9lg0UzYORBOqKXlUuUh7dHCmsgn'}], 'title': file_info.file_path, 'download_url': file_url})
    voice.FetchMetadata()
    voice.FetchContent()
    voice.Upload()


# Setup for scheduled messages
schedule.every().day.at("23:56").do(bc.start_birthday)
Thread(target=bc.schedule_checker).start()


# check if heroku variable is in the environment
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
        bot.set_webhook(url=config.app_url)
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # without heroku variable local use
    # delete webhook and use long polling
    bot.remove_webhook()
    bot.polling(none_stop=True)
