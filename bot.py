import time
import telebot
import random

from telebot import types
from cities import cities

cache = ['оттава']
used_commands = ['start']

bot = telebot.TeleBot('5821515156:AAGCcHcAxmr84wAl0G90Ac_3LGVBPl5SleM')
bot.set_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    startGame = types.KeyboardButton('/playCities')
    markup.add(startGame)
    msg = f'Привет, <b>{message.from_user.full_name}!</b> \nЧтобы начать играть введи: \n/playCities'
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)
    used_commands.append('start')


@bot.message_handler(commands=['endGame'])
def end_game(message):
    msg = f'Классно поиграли, <b>{message.from_user.full_name}!</b>'
    bot.send_message(message.chat.id, msg, parse_mode='html')
    used_commands.append('endGame')


@bot.message_handler(commands=['hint'])
def end_game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    endGame = types.KeyboardButton('/endGame')
    hint = types.KeyboardButton('/hint')
    markup.add(hint)
    markup.add(endGame)
    next = ''
    msg = cache[-1]
    while len(next) == 0 or next in cache:
        n = list(cities[msg[-1]].keys())
        m = random.choice(n)
        index = random.randint(0, len(cities[msg[-1]][m]) - 1)
        next = cities[msg[-1]][m][index]
    next = next[0].upper() + '*'*(len(next) - 2) + next[-1]
    bot.send_message(message.chat.id, f'Попробуй этот город: {next[0].upper() + next[1:]}', reply_markup=markup)


@bot.message_handler(commands=['playCities'])
def lets_start(message):
    used_commands.append('playCities')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    endGame = types.KeyboardButton('/endGame')
    hint = types.KeyboardButton('/hint')
    markup.add(hint)
    markup.add(endGame)
    bot.send_message(message.chat.id, 'Давай сыграем в города! Я начну: Оттава', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_message(message):
    if used_commands[-1] != 'playCities':
        bot.send_message(message.chat.id, 'Чтобы начать играть введи: \n/playCities')
    else:
        msg = message.text.lower()
        if msg[-1] == 'ь' or msg[-1] == 'ъ':
            msg = msg[:-1]
        if msg[0] not in 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя' or msg[1] not in 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя':
            bot.send_message(message.chat.id, 'Такого города нет -_-')
        elif msg not in cities[msg[0]][msg[:2]]:
            bot.send_message(message.chat.id, 'Я не знаю такого города( \nПопробуй другой')
        elif msg[0] != cache[-1][-1]:
            bot.send_message(message.chat.id,
                             f'Надо чтоб новый город начинался с последней буквы предыдущего\n(с буквы "{cache[-1][-1].upper()}")\nПопробуй снова')
        elif msg in cache:
            bot.send_message(message.chat.id, 'Такой город был!\nПопробуй снова')
        else:
            next = ''
            while len(next) == 0 or next in cache:
                n = list(cities[msg[-1]].keys())
                m = random.choice(n)
                index = random.randint(0, len(cities[msg[-1]][m]) - 1)
                next = cities[msg[-1]][m][index]

            bot.send_message(message.chat.id, next[0].upper() + next[1:])
            if next[-1] == 'ь' or next[-1] == 'ъ':
                next = next[:-1]
            cache.append(msg)
            cache.append(next.lower())


@bot.message_handler(
    content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact',
                   'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
                   'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
                   'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message'])
def zaglushka(message):
    trash = bot.send_sticker(message.chat.id,
                             sticker='CAACAgIAAxkBAAEJqblkrcu1L2upz79_UkiojBiehbpqZAACQBIAAmVBKEr_AZcT9JqjLS8E')
    time.sleep(3)
    bot.delete_message(message.chat.id, message.message_id)
    time.sleep(3)
    bot.delete_message(message.chat.id, trash.message_id)


bot.polling(none_stop=True)
