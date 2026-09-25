import sqlite3


conn = sqlite3.connect('game.db')
c = conn.cursor()
pragma = 'PRAGMA foreign_keys=ON;'
c.execute(pragma)
conn.commit()

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



def save_player(name,money):
    string='INSERT INTO player(name,money) VALUES(?,?)'
    c.execute(string,(name,money))
    player_id=c.lastrowid
    conn.commit()
    return player_id

def save_car(car,id_player):
    string ='insert into cars(player_id,name,power,weight,condition,price) values(?,?,?,?,?,?)'
    c.execute(string,(id_player,car.name,car.power,car.weight,car.condition,car.price))
    id_car=c.lastrowid
    conn.commit()
    return id_car

def save_parts(part):
    string ='insert into parts(name,boost) values(?,?)'
    c.execute(string,(part.name,part.boost))
    id_part=c.lastrowid
    conn.commit()
    return id_part

def save_partplayer(player_id,part_id):
    string ='insert into player_parts(player_id,part_id) values(?,?)'
    c.execute(string,(player_id,part_id))
    id_part=c.lastrowid
    conn.commit()
    return id_part

def save_partcar(car_id,part_id):
    string ='insert into car_parts(car_id,part_id) values(?,?)'
    c.execute(string,(car_id,part_id))
    id_part=c.lastrowid
    conn.commit()
    return id_part

def load_player(name_player):
    string='select * from player where name=?'
    c.execute(string,name_player)
    # name=c.fetchone()[0]
    # money=c.fetchone()[1]
    conn.commit()
    # return name,money

# def print_select():
#     conn = sqlite3.connect('game.db')
#     c = conn.cursor()
#     st='select * from cars'
#     c.execute(st)
#     ss=c.fetchall()
#     conn.commit()
#     c.close()
#     conn.close()
#     return ss
# c.close()
# conn.close()