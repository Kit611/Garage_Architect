from Models.Player.player import   Player
from DataBase.database import  *
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

    def safe_int_input(self,prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print('Пожалуйста, введите число\n')

    def save_game(self):
        update_player(self.id_player, self.player)
        for car in self.player.list_cars:
            update_car(car)
        list_part = []
        for p in self.player.bought_parts:
            if not p.installed:
                list_part.append(p.id_part)
        for c in self.player.list_cars:
            for rp in range(len(list_part)):
                anwser = find_car_part(c.id_car, list_part[rp])
                if anwser:
                    delete_part(c.id_car, list_part[rp])

    def load_game(self,player_name):
        self.id_player = find_idplayer(player_name)
        name, money = load_player(self.id_player)
        self.player = Player(name, money)

        parts_by_id = {}
        for id_part in load_playerpart(self.id_player):
            part_id, name_part, price_part, boost = load_part(id_part)
            part = Part(name_part, price_part, boost, part_id)
            parts_by_id[id_part] = part
            self.player.add_part(part)

        for id_car in find_playercar(self.id_player):
            car_id, name_car, price, power, weight, condition = load_car(id_car)
            car = Car(name_car, price, power, weight, condition, id_car)
            for id_part in load_carpart(id_car):
                part = parts_by_id.get(id_part)
                if part is None:
                    part_id, name_part, price_part, boost = load_part(id_part)
                    part = Part(name_part, price_part, boost, part_id)
                car.install_part(part)

            self.player.add_car(car)

    def start_menu(self):
        print('1. Новая игра\n'
              '2. Загрузить игру\n'
              '3. Выход\n')
        mode = self.safe_int_input('Выберите: ')
        return mode

    def new_game(self):
        self.player = Player('Alex', 150000)
        id_player = save_player(self.player.name_player,self.player.money)
        if id_player:
            self.id_player = id_player
            return True
        else:
            print('Ошибка создания игрока\n')
            return False

    def setup_shop(self):
        skyline = Car("Skyline", 30000, 300, 1100, 70)
        mazda = Car("mazda", 25000, 120, 1350, 80)
        turbo = Part("Turbina", 30000, 50)
        exhaust = Part('Exhaust', 15000, 10)
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
                self.player.show_parts()
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
        while garage_menu != 6:
            self.player.show_cars()
            print('1. Починить автомомбиль\n'
                  '2. Установить деталь\n'
                  '3. Снять деталь\n'
                  '4. Посмотреть характеристики\n'
                  '5. Повредить автомобиль\n'
                  '6. Назад\n')
            garage_menu = self.safe_int_input("Выберите действие: ")
            print()
            if garage_menu == 1:
                if self.player.list_cars:
                    car_name = input('Введите название автомобиля: ').lower()
                    print()
                    try:
                        self.player.repair_car(car_name)
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 2:
                if self.player.list_cars:
                    if self.player.bought_parts:
                        car_name = input('Введите название автомобиля: ').lower()
                        print()
                        self.player.show_parts()
                        part_name = input('Введите название детали: ').lower()
                        print()
                        try:
                            car_id = self.player.car_find(car_name)
                            part_id = self.player.part_find(part_name)
                            self.player.install(car_name, part_name)
                            id_carpart = save_partcar(car_id, part_id)
                        except (ValueError, AttributeError) as e:
                            print(f'Не удалось установить деталь: {e}\n')
                    else:
                        print('У вас нет купленных деталей\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 3:
                if self.player.list_cars:
                    car_name = input('Введите название автомобиля: ').lower()
                    print()
                    print('Установленные детали: \n')
                    found = False
                    for car in self.player.list_cars:
                        if car.name.lower() == car_name:
                            found = True
                            if car.parts:
                                car.show_parts()
                                part_name = input('Введите название детали: ').lower()
                                print()
                                try:
                                    self.player.remove(car_name, part_name)
                                except (ValueError, AttributeError) as e:
                                    print(f'Не удалось снять деталь: {e}\n')
                            else:
                                print('На вашем автомобиле нет установленных деталей\n')
                    if not found:
                        print(f'Автомобиль "{car_name}" не найден\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 4:
                if self.player.list_cars:
                    car_name = input('Введите название автомобиля: ').lower()
                    print()
                    try:
                        self.player.info_car(car_name)
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu == 5:
                if self.player.list_cars:
                    car_name = input('Введите название автомобиля: ').lower()
                    print()
                    points = self.safe_int_input('Введите количество очков повреждения: ')
                    print()
                    try:
                        self.player.damage_car(car_name, points)
                    except (ValueError, AttributeError) as e:
                        print(f'Автомобиль не найден: {e}\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu != 6:
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
                    anwser = self.player.buy_car(car)
                    if anwser:
                        id_car = save_car(car, self.id_player)
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
                    anwser = self.player.buy_part(part)
                    if anwser:
                        id_part = save_parts(part)
                        id_playerpart = save_partplayer(self.id_player, id_part)
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось купить деталь: {e}\n')
            elif shop_menu != 2:
                print('Такого варианта нет')

    def run(self):
        while True:
            mode = self.start_menu()
            if mode==1:
                if self.new_game():
                    self.game_loop()
            elif mode==2:
                name = input('Введите имя игрока: ')
                try:
                    self.load_game(name.lower())
                    self.game_loop()
                except (ValueError, AttributeError) as e:
                    print(f'Не удалось загрузить игру: {e}\n')
                    continue
            elif mode==3:
                print('Выход')
                break
            else:
                print('Такого варианта нет\n')