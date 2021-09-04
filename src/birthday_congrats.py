from threading import Thread
from time import sleep
import schedule
import local_config as config
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from imgurpython import ImgurClient

id = 206662948
bot = telebot.TeleBot(config.telegram_token)
client = ImgurClient(config.client_id, config.client_secret, config.access_token, config.refresh_token)


# generator of keyboard
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Ну че там дальше?", callback_data="further"))
    return markup

def fake_present_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("А подарок дома...", callback_data="fake_present"))
    return markup

def real_present_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Ура!", callback_data="real_present"))
    return markup

def end_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("И мы счастливы!", callback_data="the_end"))
    return markup


# Loop through all tasks that should be called
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def start_birthday():
    bot.send_message(id, "Вот это да! Бац, и тебе 20. Пожилая шокобрётхен получается. Начни поздравление командой /oldbutgold")
    return schedule.CancelJob


def first_message():
    comment = "Здесь можно уже начинать с того, почему ты мне нравишься. Ты реально самый настоящий человек, которого я встречал. Ты искренняя и не будешь из себя строить того, кем не являешься. Ну и как такая сладуля может не нравиться???"
    bot.send_photo(id, photo="https://imgur.com/RhREvde", caption=comment, reply_markup=gen_markup())

def second_message():
    comment = "У тебя пиздатое чувство юмора. Вообще считаю, что все предыдущие смехлысты были подкручены, ведь мне реально с тобой смешно и очень хорошо."
    bot.send_photo(id, photo="https://imgur.com/VfgieWp", caption=comment, reply_markup=gen_markup())

def third_message():
    comment = "С тобой я чувствую себя любимым, а все потому, что тебе не похуй! Ты очень чуткая и внимательная и твоя любовь мне очень важна"
    bot.send_photo(id, photo="https://imgur.com/5yBKSNG", caption=comment, reply_markup=gen_markup())

def fourth_message():
    comment = "А еще у нас есть кошка вонючка! Она тебя тоже любит. И вообще это она все тут написала так-то."
    bot.send_photo(id, photo="https://imgur.com/MoyhIYi", caption=comment, reply_markup=gen_markup())

def fifth_message():
    comment = "Разбавим еще парочкой гениальных фотографий. Не зря же я ловил все эти гениальные кадры..."
    bot.send_photo(id, photo="https://imgur.com/0kJ3a1W", caption=comment, reply_markup=gen_markup())

def sixth_message():
    comment = "Пирожок. Вкусный, кста"
    bot.send_photo(id, photo="https://imgur.com/gYEA4yS", caption=comment, reply_markup=gen_markup())

def seventh_message():
    comment = "Ну это вообще моя любимая фотка"
    bot.send_photo(id, photo="https://imgur.com/WZAYa1P", caption=comment, reply_markup=gen_markup())

def eighth_message():
    comment = "Ты очень талантливая и я только продолжаю в этом убеждаться. Большинство челиков (типо меня) не особо замарачиваются, но все, что делаешь ты, несет какой-то свой особенный вайб. А дьявол-то кроется в деталях!"
    bot.send_photo(id, photo="https://imgur.com/9T1ORTx", caption=comment, reply_markup=gen_markup())

def ninth_message():
    comment = "Ну и ебать, ты себя в зеркало видела вообще? Конечно видела. Ты просто охуеть какая красивая. И охуеть как сильно мне нравишься"
    bot.send_photo(id, photo="https://imgur.com/toO3UUL", caption=comment, reply_markup=gen_markup())

def tenth_message():
    comment = "Бубубу"
    bot.send_photo(id, photo="https://imgur.com/kCtdryJ", caption=comment, reply_markup=gen_markup())

def eleventh_message():
    comment = "Ну а еще ты икона стиля. Рядом с тобой уже как-то стыдно ходить как додик, приходится соответствовать"
    bot.send_photo(id, photo="https://imgur.com/YYb6jhv", caption=comment, reply_markup=gen_markup())

def twelveth_message():
    comment = "И с тобой я могу быть полностью настоящим. Ты мой лучший друг и я счастлив, что это так"
    bot.send_photo(id, photo="https://imgur.com/ZI8Wrey", caption=comment, reply_markup=gen_markup())

def thirteenth_message():
    comment = "А это ты в окружении турецких вонючкинсов. Но наш вонючкинс конечно и в сравнение не идет."
    bot.send_photo(id, photo="https://imgur.com/M3gxin9", caption=comment, reply_markup=gen_markup())

def fourteenth_message():
    comment = "Ты мне нравишься полностью такая, какая ты есть. Я не хочу тебя менять, но счастлив меняться вместе с тобой и быть благодарным за то, что такой кафи свалился мне с неба. А как известно, кафи я люблю. Я люблю тебя!"
    bot.send_photo(id, photo="https://imgur.com/km5khPi", caption=comment, reply_markup=fake_present_markup())

# def present_fake():
#     comment = "Ну надо брать с собой плавки получается"
#     bot.send_photo(id, photo="https://imgur.com/YYb6jhv", caption=comment, reply_markup=real_present_markup())
#
# def present_real():
#     comment = "Ну ладно, думаю, без плавок обойдемся"
#     bot.send_photo(id, photo="https://imgur.com/YYb6jhv", caption=comment, reply_markup=end_markup())
