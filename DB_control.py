import sqlite3

class db_control:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_all_user(self):
        self.cursor.execute("SELECT * FROM 'subscribe_data'")
        res = self.cursor.fetchall()
        return res

    def get_user_game(self, user_id):
        self.cursor.execute("SELECT * FROM 'subscribe_data' WHERE chat_id=?", (user_id,))
        res = self.cursor.fetchone()
        return res

    def add_user(self, chat_id, game_id, game_name):
        self.cursor.execute("INSERT INTO subscribe_data(chat_id, game, game_name) VALUES(?, ?, ?)", (chat_id, game_id, game_name, ))
        self.conn.commit()

    def update_game(self, chat_id, game_id):
        self.cursor.execute("UPDATE subscribe_data SET game=? WHERE chat_id=?", (game_id, chat_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

#db = db_control("gamechatdata.db")
#print(len(db.get_all_user()))