from datetime import datetime
import time
import schedule

import os
import telebot

#from main import *
from DB_control import db_control
import url_controle_code
from text_controle import find_func
from url_controle_code import get_data

db = db = db_control("gamechatdata.db")

def get_time():
    test_time = datetime.now().strftime("%H:%M:%S")
    db = db_control("gamechatdata.db")
    db.close()
    return test_time

bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))
need_time = "17:28:30"

def test_start():
    time = get_time()
    if time == need_time:
        all_user = db.get_all_user()
        for x in range(0, len(all_user)):
            need_user_id = all_user[x][0]
            print(need_user_id)
            need_user_game = all_user[x][1]

            need_game_cost = url_controle_code.get_data(need_user_game)
            bot.send_message(need_user_id,
                            """Hello, you subscribed game is {0} and this cost {1}""".format(all_user[x][2], need_game_cost[0]))

while True:
    test_start()

#db.add_user(1092387)
#print(get_data(db.get_user_game(1143256)))

