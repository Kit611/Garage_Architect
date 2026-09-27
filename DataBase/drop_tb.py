import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'DataBase', 'game.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

drop_player='drop table if exists player'
c.execute(drop_player)
conn.commit()
drop_car='drop table if exists cars'
c.execute(drop_car)
conn.commit()
drop_part='drop table if exists parts'
c.execute(drop_part)
conn.commit()
drop_playerpart='drop table if exists player_parts'
c.execute(drop_playerpart)
conn.commit()
drop_carpart='drop table if exists car_parts'
c.execute(drop_carpart)
conn.commit()

c.close()
conn.close()