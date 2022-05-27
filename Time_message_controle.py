from datetime import datetime
import time
import schedule

from DB_control import db_control
from url_controle_code import get_data

test_time = datetime.now().strftime("%H:%M:%S")
db = db_control("gamechatdata.db")

#db.add_user(1092387)
#print(get_data(db.get_user_game(1143256)))

db.close()

