import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import local_config as config


bot = telebot.TeleBot(config.telegram_token)
id = 206662948
counter = 1

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Ну че там дальше?", callback_data="further"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "further":
        bot.answer_callback_query(call.id, "Ну погнали")
        global counter
        if counter == 1:
            first_message()
            counter += 1
        elif counter == 2:



@bot.message_handler(func=lambda message: True)
def start_birthday(message):
    bot.send_message(id, "Вот это да! Бац, и тебе 20. Пожилая шокобрётхен получается. Начни поздравление командой /oldbutgold", reply_markup=gen_markup())


def first_message():
    bot.send_message(id, "Hui")


bot.polling(none_stop=True)