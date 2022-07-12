from telebot import types

from url_controle_code import *
#from Time_message_controle import *
from DB_control import db_control

final_status = 0
find_status = 0
control_status = 0
games_list = []
find_word = ""
chose_game_id = None
chose_game_name = None


def subscribe(m, bot):
    global chose_game_name
    global chose_game_id
    db = db_control("gamechatdata.db")

    if db.get_user_game(m.chat.id) == None:
        db.add_user(m.chat.id, chose_game_id, chose_game_name)
        chose_game_id = None
        chose_game_name = None
    else:
        db.update_game(m.chat.id, chose_game_id, chose_game_name)
        chose_game_name = None
    bot.send_message(m.chat.id, "You subscribed")
    chose_game_id = None
    db.close()


def control_control(m, bot):
    global find_word
    global control_status
    global find_status
    global final_status
    global chose_game_id
    global chose_game_name

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    subscribe_btn = types.KeyboardButton("subscribe")

    user_chose = int(m.text) - 1
    print("user chose: ", user_chose)
    user_game = games_list[user_chose]
    chose_game_name = user_game
    game_id = get_id(find_word, user_chose)
    chose_game_id = game_id

    print("game id: ", game_id)
    game_price = get_data(game_id)

    if game_price == []:
        bot.send_message(m.chat.id, "You chose {0}, this game is free".format(user_game))
    else:
        action_control = game_price[0].endswith("%")

        if action_control == False:
            bot.send_message(m.chat.id, "You chose {0}, this game is worth it {1}".format(user_game, game_price[0]))
        else:
            bot.send_message(m.chat.id, "You chose {0}.".format(user_game))
            bot.send_message(m.chat.id,
                             "this game is worth it {0}, with discount {1}, original price {2}".format(game_price[2],
                                                                                                       game_price[0],
                                                                                                       game_price[1]))

    markup.add(subscribe_btn)
    bot.send_message(m.chat.id,
                     "if you want to subscribe to the price update, click on the button. Messages come every day at 9 and 18 o'clock",
                     reply_markup=markup)

    control_status = 0
    find_word = ""
    find_status = 0
    final_status = 0


def find_func(m, bot):
    global find_word
    global games_list
    global control_status
    global find_status
    global final_status
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # create button
    yes_btn = types.KeyboardButton("yes")
    no_btn = types.KeyboardButton("no")
    find_btn = types.KeyboardButton("find game")

    if m.text == "subscribe" and chose_game_id != None:
        subscribe(m, bot)

    elif find_status == 1:
        games_list = find_games(m.text)
        find_word = m.text
        text = """"""
        gamelistlen = len(games_list)

        if games_list[0] == None:
            bot.send_message(m.chat.id, "No results were received for this query try again")
        else:
            for x in range(0, gamelistlen):
                text = text + str(x + 1) + ". " + games_list[x] + "\n"
            bot.send_message(m.chat.id, text)
            markup.add(yes_btn, no_btn)
            final_status = 1
            find_status = 0
            bot.send_message(m.chat.id, "your game is among the offered", reply_markup=markup)

    elif (m.text == "find game") and find_status == 0:
        find_status += 1
        bot.send_message(m.chat.id, "Ok, print key word")

    elif final_status == 1 and m.text == "no":
        final_status = 0
        markup.add(find_btn)
        bot.send_message(m.chat.id, "ok, {function not added}", reply_markup=markup)

    elif final_status == 1 and m.text == "yes" or final_status == 1:
        if control_status == 1:
            control_control(m, bot)

        elif control_status == 0:
            control_status = 1
            markup.add()
            bot.send_message(m.chat.id, "print game number in list", reply_markup=markup)

    else:
        bot.send_message(m.chat.id, "sorry, you have not set any tasks for me")
