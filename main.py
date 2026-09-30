from DataBase.database import *
from Models.Player.player import Player
from Models.ShopCar.CarShop import CarShop
from Models.Car.car import Car
from Models.Parts.part import Part
from Models.ShopPart.PartShop import ShopPart


def load_game(player_name):
    id_player = find_idplayer(player_name)
    name, money = load_player(id_player)
    alex = Player(name, money)

    parts_by_id = {}
    for id_part in load_playerpart(id_player):
        _, name_part, price_part, boost = load_part(id_part)
        part = Part(name_part, price_part, boost)
        parts_by_id[id_part] = part
        alex.add_part(part)

    for id_car in find_playercar(id_player):
        car_id,name_car, price, power, weight, condition = load_car(id_car)
        car = Car(name_car, price, power, weight, condition,id_car)
        for id_part in load_carpart(id_car):
            part = parts_by_id.get(id_part)
            if part is None:
                _, name_part, price_part, boost = load_part(id_part)
                part = Part(name_part, price_part, boost)
            car.install_part(part)
            if part in alex.bought_parts:
                alex.bought_parts.remove(part)

        alex.add_car(car)

    return alex, id_player


def safe_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Пожалуйста, введите число\n')

def save_game(id_player, alex):
    change_player(id_player, alex)
    for car in alex.list_cars:
        update_car(car)

mode = 0
while mode != 3:
    print('1. Новая игра\n'
          '2. Загрузить игру\n'
          '3. Выход\n')
    mode = safe_int_input('Выберите: ')

    if mode == 1:
        item_menu = 0
        alex = Player('Alex', 150000)
        id_player = save_player('Alex', 150000)
        skyline = Car("Skyline", 30000, 300, 1100, 70)
        mazda = Car("mazda", 25000, 120, 1350, 80)
        turbo = Part("Turbina", 30000, 50)
        exhaust = Part('Exhaust', 15000, 10)
        shop_p = ShopPart()
        shop_p.add_part(turbo)
        shop_p.add_part(exhaust)
        shop_c = CarShop()
        shop_c.add_car(skyline)
        shop_c.add_car(mazda)

        while item_menu != 6:
            print("=== МЕНЮ ===\n")
            print("1. Информация о игроке\n"
                  "2. Гараж\n"
                  "3. Мои детали\n"
                  "4. Автосалон\n"
                  "5. Магазин деталей\n"
                  "6. Выход\n")
            number = safe_int_input("Выберите действие: ")
            print()
            if number <= 0 or number > 6:
                print('Такого варианта нет\n')
                continue
            elif number == 1:
                alex.print_info()
                print()
                continue
            elif number == 2:
                garage_menu = 0
                while garage_menu != 6:
                    alex.show_cars()
                    print('1. Починить автомомбиль\n'
                          '2. Установить деталь\n'
                          '3. Снять деталь\n'
                          '4. Посмотреть характеристики\n'
                          '5. Повредить автомобиль\n'
                          '6. Назад\n')
                    garage_menu = safe_int_input("Выберите действие: ")
                    print()
                    if garage_menu == 1:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            try:
                                alex.repair_car(car_name)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 2:
                        if alex.list_cars:
                            if alex.bought_parts:
                                car_name = input('Введите название автомобиля: ').lower()
                                print()
                                alex.show_parts()
                                part_name = input('Введите название детали: ').lower()
                                print()
                                try:
                                    alex.install(car_name, part_name)
                                    id_carpart = save_partcar(car_name, part_name)
                                except (ValueError, AttributeError) as e:
                                    print(f'Не удалось установить деталь: {e}\n')
                            else:
                                print('У вас нет купленных деталей\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 3:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            print('Установленные детали: \n')
                            found = False
                            for car in alex.list_cars:
                                if car.name.lower() == car_name:
                                    found = True
                                    if car.parts:
                                        car.show_parts()
                                        part_name = input('Введите название детали: ').lower()
                                        print()
                                        try:
                                            alex.remove(car_name, part_name)
                                        except (ValueError, AttributeError) as e:
                                            print(f'Не удалось снять деталь: {e}\n')
                                    else:
                                        print('На вашем автомобиле нет установленных деталей\n')
                            if not found:
                                print(f'Автомобиль "{car_name}" не найден\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 4:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            try:
                                alex.info_car(car_name)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 5:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            points = safe_int_input('Введите количество очков повреждения: ')
                            print()
                            try:
                                alex.damage_car(car_name, points)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu != 6:
                        print('Такого варианта нет')
                continue
            elif number == 3:
                alex.show_parts()
                print()
                continue
            elif number == 4:
                shop_menu = 0
                while shop_menu != 2:
                    shop_c.show()
                    print('1.Купить автомобиль\n'
                          '2. Назад\n')
                    shop_menu = safe_int_input("Выберите действие: ")
                    if shop_menu == 1:
                        car_name = input('Введите название автомобиля: ').lower()
                        print()
                        try:
                            car = shop_c.find_car(car_name)
                            anwser=alex.buy_car(car)
                            if anwser:
                                id_car = save_car(car, id_player)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось купить автомобиль: {e}\n')
                    else:
                        print('Такого варианта нет')
            elif number == 5:
                shop_menu = 0
                while shop_menu != 2:
                    shop_p.show()
                    print('1. Купить деталь\n'
                          '2. Назад\n')
                    shop_menu = safe_int_input("Выберите действие: ")
                    if shop_menu == 1:
                        part_name = input('Введите название детили: ').lower()
                        print()
                        try:
                            part = shop_p.find_part(part_name)
                            anwser=alex.buy_part(part)
                            if anwser:
                                id_part = save_parts(part)
                                id_playerpart = save_partplayer(id_player, id_part)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось купить деталь: {e}\n')
                    else:
                        print('Такого варианта нет')
            elif number == 6:
                item_menu = number
                save_game(id_player, alex)
                continue

    elif mode == 2:
        try:
            alex, id_player = load_game('Alex')
        except ValueError as e:
            print(f'Не удалось загрузить игру: {e}\n')
            continue

        item_menu = 0
        skyline = Car("Skyline", 30000, 300, 1100, 70)
        mazda = Car("mazda", 25000, 120, 1350, 80)
        turbo = Part("Turbina", 30000, 50)
        exhaust = Part('Exhaust', 15000, 10)
        shop_p = ShopPart()
        shop_p.add_part(turbo)
        shop_p.add_part(exhaust)
        shop_c = CarShop()
        shop_c.add_car(skyline)
        shop_c.add_car(mazda)

        while item_menu != 6:
            print("=== МЕНЮ ===\n")
            print("1. Информация о игроке\n"
                  "2. Гараж\n"
                  "3. Мои детали\n"
                  "4. Автосалон\n"
                  "5. Магазин деталей\n"
                  "6. Выход\n")
            number = safe_int_input("Выберите действие: ")
            print()
            if number <= 0 or number > 6:
                print('Такого варианта нет\n')
                continue
            elif number == 1:
                alex.print_info()
                print()
                continue
            elif number == 2:
                garage_menu = 0
                while garage_menu != 6:
                    alex.show_cars()
                    print('1. Починить автомомбиль\n'
                          '2. Установить деталь\n'
                          '3. Снять деталь\n'
                          '4. Посмотреть характеристики\n'
                          '5. Повредить автомобиль\n'
                          '6. Назад\n')
                    garage_menu = safe_int_input("Выберите действие: ")
                    print()
                    if garage_menu == 1:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            try:
                                alex.repair_car(car_name)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 2:
                        if alex.list_cars:
                            if alex.bought_parts:
                                car_name = input('Введите название автомобиля: ').lower()
                                print()
                                alex.show_parts()
                                part_name = input('Введите название детали: ').lower()
                                print()
                                try:
                                    alex.install(car_name, part_name)
                                    id_carpart = save_partcar(car_name, part_name)
                                except (ValueError, AttributeError) as e:
                                    print(f'Не удалось установить деталь: {e}\n')
                            else:
                                print('У вас нет купленных деталей\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 3:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            print('Установленные детали: \n')
                            found = False
                            for car in alex.list_cars:
                                if car.name.lower() == car_name:
                                    found = True
                                    if car.parts:
                                        car.show_parts()
                                        part_name = input('Введите название детали: ').lower()
                                        print()
                                        try:
                                            alex.remove(car_name, part_name)
                                        except (ValueError, AttributeError) as e:
                                            print(f'Не удалось снять деталь: {e}\n')
                                    else:
                                        print('На вашем автомобиле нет установленных деталей\n')
                            if not found:
                                print(f'Автомобиль "{car_name}" не найден\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 4:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            try:
                                alex.info_car(car_name)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu == 5:
                        if alex.list_cars:
                            car_name = input('Введите название автомобиля: ').lower()
                            print()
                            points = safe_int_input('Введите количество очков повреждения: ')
                            print()
                            try:
                                alex.damage_car(car_name, points)
                            except (ValueError, AttributeError) as e:
                                print(f'Автомобиль не найден: {e}\n')
                        else:
                            print('У вас нет автомобилей\n')
                    elif garage_menu!=6:
                        print('Такого варианта нет')
                continue
            elif number == 3:
                alex.show_parts()
                print()
                continue
            elif number == 4:
                shop_menu = 0
                while shop_menu != 2:
                    shop_c.show()
                    print('1.Купить автомобиль\n'
                          '2. Назад\n')
                    shop_menu = safe_int_input("Выберите действие: ")
                    if shop_menu == 1:
                        car_name = input('Введите название автомобиля: ').lower()
                        print()
                        try:
                            car = shop_c.find_car(car_name)
                            alex.buy_car(car)
                            id_car = save_car(car, id_player)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось купить автомобиль: {e}\n')
                    else:
                        print('Такого варианта нет')
            elif number == 5:
                shop_menu = 0
                while shop_menu != 2:
                    shop_p.show()
                    print('1. Купить деталь\n'
                          '2. Назад\n')
                    shop_menu = safe_int_input("Выберите действие: ")
                    if shop_menu == 1:
                        part_name = input('Введите название детили: ').lower()
                        print()
                        try:
                            part = shop_p.find_part(part_name)
                            alex.buy_part(part)
                            id_part = save_parts(part)
                            id_playerpart = save_partplayer(id_player, id_part)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось купить деталь: {e}\n')
                    else:
                        print('Такого варианта нет')
            elif number == 6:
                item_menu = number
                save_game(id_player, alex)
                continue

    elif mode != 3:
        print('Такого варианта нет\n')