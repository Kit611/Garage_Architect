class Player:
    def __init__(self,name_player,money,wins=0,losses=0,draws=0,rating=0,experience=0,level=1):
        self.name_player = name_player
        self.money = money
        self.list_cars=[]
        self.bought_parts=[]
        self.wins=wins
        self.losses=losses
        self.draws=draws
        self.rating=rating
        self.experience=experience
        self.level=level

    def add_car(self,car):
        self.list_cars.append(car)

    def add_part(self,part):
        self.bought_parts.append(part)

    def print_info(self):
        print(f"Имя: {self.name_player.capitalize()}\n"
              f"Баланс: {self.money} Coins\n"
              f"Уровень: {self.level}\n"
              f"Опыт: {self.experience}\n"
              f"Рейтинг: {self.rating}\n"
              f"Победы: {self.wins}\n"
              f"Поражения: {self.losses}\n"
              f"Ничьи: {self.draws}")

    def buy_part(self,part):
        part_found = False
        for p in self.bought_parts:
            if p is part:
                part_found = True
                break
        if part_found:
            print('Деталь уже куплена\n')
            return False
        elif part:
            self.money-=part.price
            self.add_part(part)
            print('Деталь успешно куплена\n')
            return True
        else:
            print('Такой детали нет\n')
            return False

    def buy_car(self,car):
        car_found=False
        for c in self.list_cars:
            if c is car:
                car_found=True
                break
        if car_found:
            print('Автомобиль уже куплен\n')
            return False
        elif car:
            self.money-=car.price
            self.add_car(car)
            print('Автомобиль успешно куплен\n')
            return True
        else:
            print('Такой детали нет\n')
            return False

    def install(self, car, part):
        if car.install_part(part) == 1:
            print('Деталь успешно установлена\n'
                  f'Прирост мощности составил: +{part.boost}\n'
                  f'Общая мощность автомобиля: {car.power}\n'
                  f'Сокращение времени разгона на: -{part.acceleration}\n')
            return car, part
        return None

    def remove(self, car, part):
        car.remove_part(part)
        print('Деталь успешно демонтирована\n')
        return car, part

    def show_cars(self):
        print("Мои автомобили:\n")
        if self.list_cars:
            for number,car in enumerate(self.list_cars,start=1):
                print(f"Авто №{number}:\n")
                print(f'Название: {car.name.capitalize()}')
                print()
        else:
            print('Ваш список автомобилей пуст\n')

    def find_car(self,number_car):
        if number_car <1 or number_car>len(self.list_cars):
            raise ValueError('Авто с таким номером нет\n')
        return self.list_cars[number_car-1]

    def find_part(self, number_part):
        if number_part < 1 or number_part > len(self.bought_parts):
            raise ValueError('Детали с таким номером нет\n')
        return self.bought_parts[number_part - 1]

    def show_parts(self):
        loose_part=False
        print("Мои детали:\n")
        if self.bought_parts:
            for number, part in enumerate(self.bought_parts,start=1):
                if not part.installed:
                    print(f"Деталь №{number}")
                    print(f'Название: {part.name.capitalize()}\n'
                              f'Мощность: {part.boost}')
                    print()
                    loose_part=True
            if not loose_part:
                print('У вас нет свободных деталей\n')
        else:
            print('Ваш список деталей пуст\n')

    def sale_part(self,part,cost):
        if part.installed:
            print('Деталь уже установлена\n')
        elif not part.installed:
            self.bought_parts.remove(part)
            self.money+= cost

    def sale_car(self, car, cost, list_id_part=None):
        if list_id_part is not None:
            self.bought_parts = [
                part for part in self.bought_parts
                if part.id_part not in list_id_part
            ]
        self.list_cars.remove(car)
        self.money += cost

    def repair_car(self,car):
        if car.condition<100:
            cond=100-car.condition
            price=cond*10
            if self.money >= price:
                self.money-=price
                car.repair()
                print(f'Отремонтировано: {cond} очков\n'
                f'Текущее состояние автомобиля: {car.condition}/100\n')
            else:
                print('У вас недостаточно средств\n')
        else:
            print('Ваш автомобиль не нуждается в ремонте\n')

    def damage_car(self,car,points):
        if car.condition>0:
            car.damage(points)
        else:
            print('Состояние автомобиля уже 0\n')

    def check_level_up(self):
        while self.experience>=self.level*300:
            self.level+=1
            self.money+=10000
            print(f'Поздравляю вы достигли уровня: {self.level}!!!\n'
                  f'Вы получили: +{10000} Coins\n')