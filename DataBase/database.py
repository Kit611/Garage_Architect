import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'DataBase', 'game.db')

conn = sqlite3.connect(DB_PATH)
conn.create_function('lower', 1, lambda s: s.lower() if isinstance(s, str) else s, deterministic=True)
c = conn.cursor()
pragma = 'PRAGMA foreign_keys=ON;'
c.execute(pragma)
conn.commit()


player_tb=('CREATE TABLE IF NOT EXISTS player(id_player integer primary key autoincrement,'
           'name text collate nocase UNIQUE,'
           'money real check(money>=0))')
c.execute(player_tb)
conn.commit()
car_tb=('create table if not exists cars(id_car integer primary key autoincrement,'
        'player_id integer references player(id_player) on delete cascade,'
        'name text,'
        'power integer check(power>0),'
        'weight integer check(weight>0),'
        'condition integer check(condition>=0),'
        'price real check(price>=0),'
        'acceleration float check(acceleration >=0))')
c.execute(car_tb)
conn.commit()
part_tb=('create table if not exists parts(id_part integer primary key autoincrement,'
         'name text,'
         'price real check(price>=0),'
         'boost integer check(boost>=0),'
         'acceleration float check(acceleration>=0))')
c.execute(part_tb)
conn.commit()
playerpart_tb=('create table if not exists player_parts(id integer primary key autoincrement,'
               'player_id integer references player(id_player) on delete cascade,'
               'part_id integer  references parts(id_part))')
c.execute(playerpart_tb)
conn.commit()
carpart_tb=('create table if not exists car_parts(id integer primary key autoincrement'
            ',car_id integer references cars(id_car) on delete cascade,'
            'part_id integer references parts(id_part))')
c.execute(carpart_tb)
conn.commit()


def save_player(name,money):
    try:
        s = 'select * from player where lower(name)=lower(?)'
        c.execute(s, (name,))
        row=c.fetchone()
        if not row:
            string='INSERT INTO player(name,money) VALUES(?,?)'
            c.execute(string,(name,money))
            player_id=c.lastrowid
            conn.commit()
            return player_id
        else:
            print('Игрок с таким именем уже существует')
            return None
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения игрока: {e}')
        return None

def save_car(car,id_player,player):
    try:
        string ='insert into cars(player_id,name,power,weight,condition,price,acceleration) values(?,?,?,?,?,?,?)'
        c.execute(string,(id_player,car.name,car.power,car.weight,car.condition,car.price,car.initial_acceleration))
        id_car=c.lastrowid
        string1='update player set money=? where id_player=?'
        c.execute(string1,(player.money-car.price,id_player))
        if c.rowcount == 0:
            conn.rollback()
            print('Не удалось обновить баланс игрока\n')
            return False
        conn.commit()
        car.id_car=id_car
        return True
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка сохранения автомобиля: {e}')
        return False

def save_parts(part,player_id,player):
    try:
        string ='insert into parts(name,price,boost,acceleration) values(?,?,?,?)'
        c.execute(string,(part.name,part.price,part.boost,part.acceleration))
        id_part=c.lastrowid
        s = 'select * from player_parts where player_id=? and part_id=?'
        c.execute(s, (player_id, id_part))
        row = c.fetchone()
        if row is None:
            string = 'insert into player_parts(player_id,part_id) values(?,?)'
            c.execute(string, (player_id, id_part))
        string1='update player set money=? where id_player=?'
        c.execute(string1, (player.money-part.price,player_id))
        if c.rowcount == 0:
            conn.rollback()
            print('Не удалось обновить баланс игрока\n')
            return False
        conn.commit()
        part.id_part=id_part
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Ошибка сохранения деталей: {e}')
        return False

def save_partcar(car_id,part_id):
    try:
        answer=find_car_part(car_id,part_id)
        if not answer:
            string ='insert into car_parts(car_id,part_id) values(?,?)'
            c.execute(string,(car_id,part_id))
            conn.commit()
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
        initial_acceleration=car[7]
        return car_id,name,price,power,weight,condition,initial_acceleration
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
        initial_acceleration=part[4]
        return id_part,name,price,boost,initial_acceleration
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

def update_player(id_player,alex,car=None):
    try:
        if car is not None:
            string='update player set name=?,money=? where id_player=?'
            c.execute(string,(alex.name_player,alex.money,id_player))
            if c.rowcount == 0:
                conn.rollback()
                print(f'Игрок с именем: {alex.name_player} не найден, обновление не выполнено')
                return False
            string1 = 'update cars set name=? ,weight=? ,condition=? ,price=? where id_car=?'
            c.execute(string1, (car.name, car.weight, car.condition, car.price, car.id_car))
            if c.rowcount == 0:
                conn.rollback()
                print(f'Автомобиль с id={car.id_car} не найден, обновление не выполнено')
                return False
            conn.commit()
            return True
        else:
            string = 'update player set name=?,money=? where id_player=?'
            c.execute(string, (alex.name_player, alex.money, id_player))
            if c.rowcount == 0:
                conn.rollback()
                print(f'Игрок с именем: {alex.name_player} не найден, обновление не выполнено')
                return False
            conn.commit()
            return True
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f'Ошибка обновления игрока: {e}')
        return False

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

def sell_part(player,id_player,part_id,cost):
    try:
        string='delete from player_parts where player_id=? and part_id=?'
        c.execute(string,(id_player,part_id))
        if c.rowcount == 0:
            conn.rollback()
            print('Ошибка удаления связи\n')
            return False
        string1='delete from parts where part_id=?'
        c.execute(string1,(part_id,))
        if c.rowcount == 0:
            conn.rollback()
            print('Ошибка удаления из деталей\n')
            return False
        str='update player set money=? where id_player=?'
        c.execute(str,(player.money+cost,id_player))
        if c.rowcount == 0:
            conn.rollback()
            print('Ошибка обновления баланса\n')
            return False
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Ошибка сохранения изменений:{e}\n')
        return False

def sale_car(player,player_id,car_id,cost,list_id_part):
    try:
        if list_id_part:
            string = 'delete from car_parts where car_id=?'
            c.execute(string, (car_id,))
            for id in list_id_part:
                string1 = 'delete from player_parts where player_id=? and part_id=?'
                c.execute(string1, (player_id, id))
                if c.rowcount == 0:
                    conn.rollback()
                    print('Ошибка удаления связи\n')
                    return False
                string2='delete from parts where id_part=?'
                c.execute(string2,(id,))
                if c.rowcount == 0:
                    conn.rollback()
                    print('Ошибка удаления детали')
                    return False
        string3 = 'delete from cars where player_id=? and id_car=?'
        c.execute(string3, (player_id, car_id))
        if c.rowcount == 0:
            conn.rollback()
            print('Ошибка удаления связи\n')
            return False
        str='update player set money=? where id_player=?'
        c.execute(str,(player.money+cost,player_id))
        if c.rowcount == 0:
            conn.rollback()
            print('Ошибка обновления баланса\n')
            return False
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Ошибка сохранения изменений:{e}\n')
        return False