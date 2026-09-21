from Models.Car.car import Car
from Models.Parts.part import Part
from Models.ShopPart.PartShop import ShopPart

class Player:
    def __init__(self,name_player,money):
        self.name_player = name_player
        self.money = money
        self.list_cars=[]
        self.bought_parts=[]

    def add_car(self,car):
        self.list_cars.append(car)

    def print_info(self):
        print(f"Имя: {self.name_player}\nБаланс: {self.money} Сoins\n")

    def buy_part(self,part):
        part_found = False
        for p in self.bought_parts:
            if p is part:
                part_found = True
                break
        if part_found:
            print('Деталь уже куплена\n')
        elif part:
            if self.money >= part.price:
                self.money-=part.price
                self.bought_parts.append(part)
                print('Деталь уже куплена\n')
            else:
                print("У вас недостаточно средств\n")
        else:
            print('Такой детали нет\n')

    def buy_car(self,car):
        car_found=False
        for c in self.list_cars:
            if c is car:
                car_found=True
                break
        if car_found:
            print('Автомобиль уже куплеn\n')
        elif car:
            if self.money >= car.price:
                self.money-=car.price
                self.add_car(car)
                print('Автомобиль успешно куплен\n')
            else:
                print('Недостаточно средств\n')


    def install(self,name_car,name):
        car_found=False
        part_found=False
        found_car=None
        found_part=None
        for car in self.list_cars:
            if car.name == name_car:
                car_found=True
                found_car=car
                break
        for part in self.bought_parts:
            if part.name == name:
                part_found=True
                found_part=part
                break

        if car_found and part_found:
            found_car.install_part(found_part)
            print('Деталь успешно установлена\n'
                  f'Прирост мощности составил: +{found_part.boost}\n'
                  f'Общая мощность автомобиля: {found_car.power}')
        elif not car_found:
            print('У вас нет такого автомобиля\n')
        elif not part_found:
            print('У вас нет такой детали\n')

    def remove(self,name_car,name):
        car_found = False
        part_found = False
        found_car = None
        found_part = None
        for car in self.list_cars:
            if car.name == name_car:
                car_found = True
                found_car = car
                break
        for part in self.bought_parts:
            if part.name == name:
                part_found = True
                found_part = part
                break

        if car_found and part_found and found_part.installed and found_part.installed_on is found_car:
            found_car.remove_part(found_part)
            print('Деталь успешно демонтирована\n')
        elif not car_found:
            print('У вас нет такого автомобиля\n')
        elif not part_found:
            print('У вас нет такой детали\n')
        elif not found_part.installed:
            print('Деталь не установлена\n')
        elif found_part.installed_on is not found_car:
            print('Деталь установлена на другой автомобиль\n')

    def show_cars(self):
        print("Мои автомобили:\n")
        if self.list_cars:
            for car in self.list_cars:
                print(f"Авто №{self.list_cars.index(car) + 1}")
                print(f'Название: {car.name}')
                print()
        else:
            print('Ваш список автомобилей пуст\n')

    def info_car(self,name):
        for car in self.list_cars:
            if car.name == name:
                car.print_characteristics()

    def show_parts(self):
        print("Мои детали:\n")
        if self.bought_parts:
            for part in self.bought_parts:
                print(f"Деталь №{self.bought_parts.index(part) + 1}")
                print(f'Название: {part.name}\n'
                      f'Мощность: {part.boost}')
                print()
        else:
            print('Ваш список деталей пуст\n')

    def sale_part(self,name):
        part_found=False
        found_part = None
        for part in self.bought_parts:
            if part.name == name:
                part_found=True
                found_part = part
                break
        if part_found:
            if found_part.installed:
                print('Деталь уже усновлена\n')
            elif not found_part.installed:
                self.bought_parts.remove(found_part)
                self.money+=found_part.price
        elif not part_found:
            print('У вас нет такой детали\n')

    def repair_car(self,name_car):
        car_found=False
        found_car = None
        for car in self.list_cars:
            if car.name == name_car:
                car_found = True
                found_car = car
                break
        if car_found:
            if found_car.condition<100:
                cond=100-found_car.condition
                price=cond*10
                if self.money >= price:
                    self.money-=price
                    found_car.repair()
                    print(f'Отремантировано: {cond} очков\n'
                          f'Текущее состояние автомобиля: {found_car.condition}/100\n')
                else:
                    print('У вас недостаточно средств\n')
            else:
                print('Ваш автомобиль не нуждается в ремонте\n')
        elif not car_found:
            print('У вас нет такого автомобиля\n')

    def damage_car(self,name_car,points):
        car_found=False
        found_car = None
        for car in self.list_cars:
            if car.name == name_car:
                car_found = True
                found_car = car
                break
        if car_found:
            if found_car.condition>0:
                found_car.damage(points)
            else:
                print('Состояние автомобиля уже 0\n')
        else:
            print('У вас нет такого автомобиля\n')