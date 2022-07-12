import os

import asyncio
import telebot
from telebot import types

from DB_control import db_control
from text_controle import find_func

bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id,
                     "hello, this bot will help you keep track of the prices for the game you want to buy with the "
                     "largest possible promotion print /help for more instruction")


@bot.message_handler(commands=['help'])
def help_command(m):
    bot.send_message(m.chat.id,
                     """Hi, this bot will help you keep track of games you don't have, but you want to buy and 
                     play.\nTo get started, write /menu""")


@bot.message_handler(commands=['menu'])
def my_button(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    find_btn = types.KeyboardButton("find game")
    markup.add(find_btn)
    bot.send_message(m.chat.id, "Hi", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def find_game(m):
    print("chat id: ", m.chat.id)
    find_func(m, bot)


bot.polling(interval=0)
