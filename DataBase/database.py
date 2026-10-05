import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'DataBase', 'game.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
pragma = 'PRAGMA foreign_keys=ON;'
c.execute(pragma)
conn.commit()


player_tb='CREATE TABLE IF NOT EXISTS player(id_player integer primary key autoincrement ,name text,money real check(money>=0))'
c.execute(player_tb)
conn.commit()
car_tb='create table if not exists cars(id_car integer primary key autoincrement,player_id integer references player(id_player) on delete cascade,name text,power integer check(power>0),weight integer check(weight>0), condition integer check(condition>=0),price real check(price>=0))'
c.execute(car_tb)
conn.commit()
part_tb='create table if not exists parts(id_part integer primary key autoincrement, name text,price real check(price>=0),boost integer check(boost>=0))'
c.execute(part_tb)
conn.commit()
playerpart_tb='create table if not exists player_parts(id integer primary key autoincrement,player_id integer references player(id_player) on delete cascade,part_id integer  references parts(id_part))'
c.execute(playerpart_tb)
conn.commit()
carpart_tb='create table if not exists car_parts(id integer primary key autoincrement,car_id integer references cars(id_car) on delete cascade, part_id integer references parts(id_part))'
c.execute(carpart_tb)
conn.commit()


def save_player(name,money):
    try:
        string='INSERT INTO player(name,money) VALUES(?,?)'
        c.execute(string,(name,money))
        player_id=c.lastrowid
        conn.commit()
        return player_id
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения игрока: {e}')
        return None

def save_car(car,id_player):
    try:
        string ='insert into cars(player_id,name,power,weight,condition,price) values(?,?,?,?,?,?)'
        c.execute(string,(id_player,car.name,car.power,car.weight,car.condition,car.price))
        id_car=c.lastrowid
        car.id_car=id_car
        conn.commit()
        return id_car
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения автомобиля: {e}')
        return None

def save_parts(part):
    try:
        string ='insert into parts(name,price,boost) values(?,?,?)'
        c.execute(string,(part.name,part.price,part.boost))
        id_part=c.lastrowid
        part.id_part=id_part
        conn.commit()
        return id_part
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения деталей: {e}')
        return None

def save_partplayer(player_id,part_id):
    try:
        s='select * from player_parts where player_id=? and part_id=?'
        c.execute(s,(player_id,part_id))
        row=c.fetchone()
        if row is None:
            string ='insert into player_parts(player_id,part_id) values(?,?)'
            c.execute(string,(player_id,part_id))
            id_partplayer=c.lastrowid
            conn.commit()
            return id_partplayer
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения деталей игрока: {e}')
        return None

def save_partcar(car_id,part_id):
    try:
        answer=find_car_part(car_id,part_id)
        if not answer:
            string ='insert into car_parts(car_id,part_id) values(?,?)'
            c.execute(string,(car_id,part_id))
            id_partcar=c.lastrowid
            conn.commit()
            return id_partcar
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения деталей автомобиля: {e}')
        return None

def load_player(id_player):
    string='select * from player where id_player=?'
    c.execute(string,(id_player,))
    player=c.fetchone()
    if player is not None:
        name=player[1]
        money=player[2]
        return name,money
    else:
        raise ValueError(f'Игрок с id: {id_player} не найден')

def load_car(id_car):
    string='select * from cars where id_car=?'
    c.execute(string,(id_car,))
    car=c.fetchone()
    if car is not None:
        car_id=car[0]
        name=car[2]
        power=car[3]
        weight=car[4]
        condition=car[5]
        price=car[6]
        return car_id,name,price,power,weight,condition
    else:
        raise ValueError(f'Автомобиль с id: {id_car} не найдена')

def load_part(id_part):
    string='select * from parts where id_part=?'
    c.execute(string,(id_part,))
    part=c.fetchone()
    if part is not None:
        id_part=part[0]
        name=part[1]
        price=part[2]
        boost=part[3]
        return id_part,name,price,boost
    else:
        raise ValueError(f'Деталь с id: {id_part} не найдена')

def load_playerpart(id_player):
    string='select part_id from player_parts where player_id=?'
    c.execute(string,(id_player,))
    rows=c.fetchall()
    return [row[0] for row in rows]

def load_carpart(id_car):
    string='select part_id from car_parts where car_id=?'
    c.execute(string,(id_car,))
    rows=c.fetchall()
    return [row[0] for row in rows]

def find_idplayer(name):
    string='select id_player from player where lower(name)=lower(?)'
    c.execute(string,(name.lower(),))
    row=c.fetchone()
    if row is None:
        raise ValueError(f'Игрок {name} не найден')
    return row[0]

def find_playercar(id_player):
    string='select id_car from cars where player_id=?'
    c.execute(string,(id_player,))
    rows=c.fetchall()
    return [row[0] for row in rows]

def update_player(id_player,alex):
    try:
        string='update player set name=?,money=? where id_player=?'
        c.execute(string,(alex.name_player,alex.money,id_player))
        conn.commit()
        if c.rowcount == 0:
            print(f'Игрок с именем: {alex.name_player} не найден, обновление не выполнено')
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка обновления денег: {e}')
        return None

def update_car(car):
    try:
        string='update cars set name=? ,weight=? ,condition=? ,price=? where id_car=?'
        c.execute(string,(car.name,car.weight,car.condition,car.price,car.id_car))
        conn.commit()
        if c.rowcount == 0:
            print(f'Автомобиль с id={car.id_car} не найден, обновление не выполнено')
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка обновления автомобиля {e}')
        return None

def delete_part(id_car,id_part):
    try:
        string='delete from car_parts where car_id=? and part_id=?'
        c.execute(string,(id_car,id_part))
        conn.commit()
        if c.rowcount == 0:
            print(f'Деталь с id={id_part}  или автомобиль с id={id_car} не найдены, обновление не выполнено')
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка удаления детали с автомобиля {e}')
        return None

def find_car_part(id_car,id_part):
    try:
        string='select * from car_parts where car_id=? and part_id=?'
        c.execute(string,(id_car,id_part))
        if c.fetchone() is None:
            return False
        else:
            return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Нет установленных деталей {e}')
        return None