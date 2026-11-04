from traceback import print_tb

from Models.Player.player import   Player
from DataBase.database import (
    save_player,
    find_playercar,
    delete_part,
    load_part,
    load_carpart,
    load_car,
    load_playerpart,
    load_player,
    find_idplayer,
    save_partcar,
    save_parts,
    save_car,
    update_player,
    sell_part,
    sale_car
)
from Models.Parts.part import Part
from Models.Car.car import Car
from Models.ShopCar.CarShop import CarShop
from Models.ShopPart.PartShop import ShopPart


class Game:
    def __init__(self):
        self.player = None
        self.id_player = None
        self.car_shop=CarShop()
        self.part_shop=ShopPart()
        self.setup_shop()

    @staticmethod
    def safe_int_input(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print('Пожалуйста, введите число\n')

    def save_game(self):
        if not self.player.list_cars:
            update_player(self.id_player, self.player)
        else:
            for car in self.player.list_cars:
                update_player(self.id_player,self.player,car)

    def load_game(self,player_name):
        self.id_player = find_idplayer(player_name)
        name, money = load_player(self.id_player)
        self.player = Player(name, money)

        parts_by_id = {}
        for id_part in load_playerpart(self.id_player):
            part_id, name_part, price_part, boost,acceleration = load_part(id_part)
            part = Part(name_part, price_part, boost, acceleration,part_id)
            parts_by_id[id_part] = part
            self.player.add_part(part)

        for id_car in find_playercar(self.id_player):
            car_id, name_car, price, power, weight, condition,initial_acceleration = load_car(id_car)
            car = Car(name_car, price, power, weight, condition,initial_acceleration,id_car)
            for id_part in load_carpart(id_car):
                part = parts_by_id.get(id_part)
                if part is None:
                    part_id, name_part, price_part, boost,acceleration = load_part(id_part)
                    part = Part(name_part, price_part, boost,acceleration,part_id)
                car.install_part(part)

            self.player.add_car(car)

    def start_menu(self):
        print('1. Новая игра\n'
              '2. Загрузить игру\n'
              '3. Выход\n')
        mode = self.safe_int_input('Выберите: ')
        return mode

    def new_game(self):
        name=input('Введите имя вашего персонажа: ').strip().lower()
        print()
        if name:
            self.player = Player(name, 150000)
            id_player = save_player(self.player.name_player,self.player.money)
            if id_player:
                self.id_player = id_player
                return True
            return False
        else:
            print('Недопустимое имя\n')
            return False

    def setup_shop(self):
        skyline = Car("Skyline", 30000, 300, 1100, 70,5.5)
        mazda = Car("mazda", 25000, 120, 1350, 80,9.9)
        turbo = Part("Turbina", 30000, 50,0.5)
        exhaust = Part('Exhaust', 15000, 10,0.2)
        self.part_shop.add_part(turbo)
        self.part_shop.add_part(exhaust)
        self.car_shop.add_car(skyline)
        self.car_shop.add_car(mazda)

    def game_loop(self):
        item_menu=0
        while item_menu != 6:
            print("=== МЕНЮ ===\n")
            print("1. Информация о игроке\n"
                  "2. Гараж\n"
                  "3. Мои детали\n"
                  "4. Автосалон\n"
                  "5. Магазин деталей\n"
                  "6. Выход\n")
            number = self.safe_int_input("Выберите действие: ")
            print()
            if number <= 0 or number > 6:
                print('Такого варианта нет\n')
                continue
            elif number == 1:
                self.player.print_info()
                print()
                continue
            elif number == 2:
                self.garage_menu()
            elif number == 3:
                self.detail_menu()
                print()
                continue
            elif number == 4:
                self.car_shop_menu()
            elif number == 5:
                self.part_shop_menu()
            elif number == 6:
                self.save_game()
                return

    def garage_menu(self):
        garage_menu = 0
        while garage_menu != 8:
            self.player.show_cars()
            print('1. Починить автомомбиль\n'
                  '2. Установить деталь\n'
                  '3. Снять деталь\n'
                  '4. Посмотреть характеристики\n'
                  '5. Заезд\n'
                  '6. Повредить автомобиль\n'
                  '7. Продать автомобиль\n'
                  '8. Назад\n')
            garage_menu = self.safe_int_input("Выберите действие: ")
            print()
            if garage_menu == 1:
                if self.player.list_cars:
                    number_car =self.safe_int_input('Введите номер автомобиля: ')
                    print()
                    try:
                        car=self.player.find_car(number_car)
                        self.player.repair_car(car)
                        self.save_game()
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 2:
                if self.player.list_cars:
                    if self.player.bought_parts:
                        number_car = self.safe_int_input('Введите номер автомобиля: ')
                        print()
                        self.player.show_parts()
                        part_number = self.safe_int_input('Введите номер детали: ')
                        print()
                        try:
                            car=self.player.find_car(number_car)
                            part=self.player.find_part(part_number)
                            result = self.player.install(car, part)
                            if result:
                                installed_car, installed_part = result
                                save_partcar(installed_car.id_car, installed_part.id_part)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось установить деталь: {e}\n')
                    else:
                        print('У вас нет купленных деталей\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 3:
                try:
                    if self.player.list_cars:
                        number_car = self.safe_int_input('Введите номер автомобиля: ')
                        print()
                        print('Установленные детали: \n')
                        if number_car:
                            car=self.player.find_car(number_car)
                            if car.parts:
                                car.show_parts()
                                number_part = self.safe_int_input('Введите номер детали: ')
                                print()
                                part=self.player.find_part(number_part)
                                result = self.player.remove(car, part)
                                if result:
                                    removed_car, removed_part = result
                                    delete_part(removed_car.id_car, removed_part.id_part)
                            else:
                                print('На вашем автомобиле нет установленных деталей\n')
                        else:
                            print(f'Автомобиль с номером "{number_car}" не найден\n')
                    else:
                        print('У вас нет автомобилей\n')
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось снять деталь: {e}\n')
            elif garage_menu == 4:
                if self.player.list_cars:
                    number_car = self.safe_int_input('Введите номер автомобиля: ')
                    print()
                    try:
                        car=self.player.find_car(number_car)
                        car.print_characteristics()
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 5:
                if self.player.list_cars:
                    number_car = self.safe_int_input('Введите номер автомобиля: ')
                    print()
                    try:
                        car=self.player.find_car(number_car)
                        car.arreal()
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
            elif garage_menu == 6:
                if self.player.list_cars:
                    number_car = self.safe_int_input('Введите номер автомобиля: ')
                    print()
                    points = self.safe_int_input('Введите количество очков повреждения: ')
                    print()
                    try:
                        car=self.player.find_car(number_car)
                        self.player.damage_car(car, points)
                        self.save_game()
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 7:
                confirm=input('Подтвердите выбор(y/n): ').strip().lower()
                if confirm=='y':
                    if self.player.list_cars:
                        number_car=self.safe_int_input('Введите номер автомобиля: ')
                        print()
                        try:
                            car=self.player.find_car(number_car)
                            cost=car.price//2
                            list_id_part=[]
                            for part in car.parts:
                                cost+=part.price//2
                                list_id_part.append(part.id_part)
                            answer=sale_car(self.player,self.id_player,car.id_car,cost,list_id_part)
                            if answer:
                                self.player.sale_car(car,cost,list_id_part)
                                self.save_game()
                            else:
                                print('Ошибка продажи\n')
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось продать автомобиль: {e}\n')
                elif confirm=='n':
                    continue
                else:
                    print('Такого варианта нет\n')
            elif garage_menu != 8:
                print('Такого варианта нет')

    def car_shop_menu(self):
        shop_menu = 0
        while shop_menu != 2:
            self.car_shop.show()
            print('1.Купить автомобиль\n'
                  '2. Назад\n')
            shop_menu = self.safe_int_input("Выберите действие: ")
            if shop_menu == 1:

                car_name = input('Введите название автомобиля: ').lower()
                print()
                try:
                    car = self.car_shop.find_car(car_name)
                    copy_car=Car(car.name,car.price,car.power,car.weight,car.condition,car.initial_acceleration)
                    if self.player.money>=copy_car.price:
                        answer=save_car(copy_car, self.id_player,self.player)
                        if answer:
                            answer1=self.player.buy_car(copy_car)
                            if answer1:
                                self.save_game()
                            else:
                                print('Не удалось купить автомобиль\n')
                        else:
                            print('Не удалось сохранить покупку автомобиля\n')
                    else:
                        print('У вас недостаточно средств\n')
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось купить автомобиль: {e}\n')
            elif shop_menu!=2:
                print('Такого варианта нет')

    def part_shop_menu(self):
        shop_menu = 0
        while shop_menu != 2:
            self.part_shop.show()
            print('1. Купить деталь\n'
                  '2. Назад\n')
            shop_menu = self.safe_int_input("Выберите действие: ")
            if shop_menu == 1:
                part_name = input('Введите название детили: ').lower()
                print()
                try:
                    part = self.part_shop.find_part(part_name)
                    copy_part=Part(part.name,part.price,part.boost,part.acceleration)
                    if self.player.money>=copy_part.price:
                        answer = save_parts(copy_part,self.id_player,self.player)
                        if answer:
                            answer1 = self.player.buy_part(copy_part)
                            if answer1:
                                self.save_game()
                            else:
                                print('Не удалось купить деталь\n')
                        else:
                            print('Не удалось сохранить покупку детали\n')
                    else:
                        print('У вас недостаточно средств\n')
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось купить деталь: {e}\n')
            elif shop_menu != 2:
                print('Такого варианта нет')

    def detail_menu(self):
        detail_menu = 0
        while detail_menu != 2:
            self.player.show_parts()
            print('1. Продать деталь\n'
                  '2. Назад\n')
            detail_menu = self.safe_int_input("Выберите действие: ")
            if detail_menu == 1:
                confirm=input('Подтвердите выбор(y/n): ').strip().lower()
                if confirm=='y':
                    if self.player.bought_parts:
                        number_part = self.safe_int_input('Введите номер детали: ')
                        try:
                            part=self.player.find_part(number_part)
                            cost=part.price//2
                            if part:
                                answer=sell_part(self.player,self.id_player,part.id_part,cost)
                                if answer:
                                    self.player.sale_part(part,cost)
                                    self.save_game()
                                else:
                                    print('Ошибка обновления БД\n')
                            else:
                                print('Такой детали нет\n')
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось продать деталь: {e}\n')
                    else:
                        print('Ваш список деталей пуст\n')
                elif confirm=='n':
                    continue
                else:
                    print('Такого варианта нет\n')
            elif detail_menu != 2:
                print('Такого варианта нет\n')

    def run(self):
        while True:
            mode = self.start_menu()
            if mode==1:
                if self.new_game():
                    self.game_loop()
            elif mode==2:
                name = input('Введите имя игрока: ')
                try:
                    self.load_game(name.strip().lower())
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось загрузить игру: {e}\n')
                    continue
                self.game_loop()
            elif mode==3:
                print('Выход')
                break
            else:
                print('Такого варианта нет\n')