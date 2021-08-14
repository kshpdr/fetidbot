import os
import telebot
import random
#import requests
#import datetime

bot = telebot.TeleBot('1935288146:AAEhOpae8frmTLSKwRxW80phpSWz3ikklpg')
url = "https://api.telegram.org/bot1935288146:AAEhOpae8frmTLSKwRxW80phpSWz3ikklpg/"

path = "/Users/koselev/Desktop/vanya"
#files = os.listdir(path)

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


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Ваня! На самом деле, вонючка. Потому что воняю. Если тебе грустно, я подниму тебе настроение своей мордашкой!\n "
                                      "\nПока что я немного глупая и особо ничего не умею, но ты можешь написать мне что угодно, я тебя порадую. Правда моя мордашка придет не сразу, а секунд через пять, но как говорится: кто не терпит, тот не русский.")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# @bot.message_handler(func=lambda m: True)
# def send_photo(message):
#     d = random.choice(files)
#     bot.send_message(message.chat.id, "Мяу!")
#     bot.send_photo(message.chat.id, photo=open(f"/Users/koselev/Desktop/vanya/{d}", "rb"))


bot.polling()