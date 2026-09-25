import sqlite3


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
pragma = 'PRAGMA foreign_keys=ON;'
c.execute(pragma)
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
    string ='insert into parts(name,price,boost) values(?,?,?)'
    c.execute(string,(part.name,part.price,part.boost))
    id_part=c.lastrowid
    conn.commit()
    s='select * from parts where id_part=?'
    c.execute(s,(id_part,))
    print(c.fetchone())
    return id_part

def save_partplayer(player_id,part_id):
    string ='insert into player_parts(player_id,part_id) values(?,?)'
    c.execute(string,(player_id,part_id))
    id_partplayer=c.lastrowid
    conn.commit()
    return id_partplayer

def save_partcar(car_id,part_id):
    string ='insert into car_parts(car_id,part_id) values(?,?)'
    c.execute(string,(car_id,part_id))
    id_partcar=c.lastrowid
    conn.commit()
    s='select * from car_parts where car_id=?'
    c.execute(s,(car_id,))
    print(c.fetchone())
    return id_partcar

def load_player(id_player):
    string='select * from player where id_player=?'
    c.execute(string,(id_player,))
    player=c.fetchone()
    name=player[1]
    money=player[2]
    return name,money

def load_car(id_car):
    string='select * from cars where id_car=?'
    c.execute(string,(id_car,))
    car=c.fetchone()
    name=car[2]
    power=car[3]
    weight=car[4]
    condition=car[5]
    price=car[6]
    return name,power,weight,condition,price

def load_part(id_part):
    string='select * from parts where id_part=?'
    c.execute(string,(id_part,))
    part=c.fetchone()
    name=part[1]
    price=part[2]
    boost=part[3]
    return name,price,boost

def load_playerpart(id_player):
    string='select * from player_parts where player_id=?'
    c.execute(string,(id_player,))
    part=c.fetchall()
    part_id=[]
    for p in range (len(part)):
        part_id.append(part[p][2])
    return part_id

def load_carpart(id_car):
    string='select * from car_parts where car_id=?'
    c.execute(string,(id_car,))
    part=c.fetchall()
    part_id=[]
    for p in range (len(part)):
        part_id.append(part[p][2])
    return part_id