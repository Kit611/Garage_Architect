import sqlite3
from itertools import count
from tkinter.font import names


conn = sqlite3.connect('game.db')
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


player_tb='CREATE TABLE IF NOT EXISTS player(id_player integer primary key autoincrement,name text,money real check(money>=0))'
c.execute(player_tb)
conn.commit()
car_tb='create table if not exists cars(id_car integer primary key autoincrement,player_id integer references player(id_player),name text,power integer check(power>0),weight integer check(weight>0), condition integer check(condition>=0),price real check(price>=0))'
c.execute(car_tb)
conn.commit()
part_tb='create table if not exists parts(id_part integer primary key autoincrement, name text,price real check(price>=0),boost integer check(boost>=0))'
c.execute(part_tb)
conn.commit()
playerpart_tb='create table if not exists player_parts(id integer primary key autoincrement,player_id integer references player(id_player),part_id integer  references parts(id_part))'
c.execute(playerpart_tb)
conn.commit()
carpart_tb='create table if not exists car_parts(id integer primary key autoincrement,car_id integer references cars(id_car), part_id integer references parts(id_part))'
c.execute(carpart_tb)
conn.commit()
pragma = 'PRAGMA foreign_keys=ON;'
c.execute(pragma)
conn.commit()
player_insert='insert into player (name,money) values(?,?)'
c.execute(player_insert,('Alex',50000))
conn.commit()
c.close()
conn.close()


def save_player():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    find_name='select name from player'
    c.execute(find_name)
    name=c.fetchall()
    find_money='select money from player where name=?'
    c.execute(find_money,name)
    money=c.fetchall()
    return name[0],money[0]
    c.close()
    conn.close()
