#Название: скайлайн. Мощность: 300 л.с. Масса: 1,100. Состояние: 70/100
#Ремотнироваться, показывать характеристики, получать повреждения
import time
from asyncio import timeout


class Car:
    def __init__(self,name,price,power,weight,condition,initial_acceleration,id_car=None):
        self.id_car=id_car
        self.name=name
        self.price=price
        self.power=power
        self.weight=weight
        self.condition=condition
        self.initial_acceleration=initial_acceleration
        self.acceleration=initial_acceleration
        self.parts=[]

    def print_characteristics(self):
        print(f"Название: {self.name.capitalize()}"
              f"\nЦена:{self.price}"
              f"\nМощность: {self.power}"
              f"\nВес: {self.weight}"
              f"\nСостояние: {self.condition}/100\n"
              f"Текущее ускорении 0-100 км/ч: {self.acceleration} cек.\n"
              f"Заводское значение: {self.initial_acceleration} cек.\n")
        for part in self.parts:
            print(f"Установленные детали:\n{part.name.capitalize()}\n")

    def show_parts(self):
        for part in self.parts:
            if part.installed:
                print(f"Название: {part.name.capitalize()}\n")

    def repair(self):
        repair_points=100-self.condition
        self.condition+=repair_points

    def damage(self, points_damage):
        if points_damage <= 0:
            print('Количество очков повреждения должно быть больше нуля\n')
            return False
        real_damage = min(points_damage, self.condition)
        self.condition -= real_damage
        print(f'Автомобиль поврежден на {real_damage} очков\n')
        return True

    def install_part(self,part):
        if not part.installed:
            self.parts.append(part)
            self.power+=part.boost
            self.acceleration-=part.acceleration
            part.installed=True
            part.installed_on=self
            return 1
        else:
            print('Деталь уже установлена\n')
            return 0

    def count_pricepart(self):
        count_price=0
        for part in self.parts:
            count_price+=int(part.price)
        return count_price

    def remove_part(self,part):
        if self is part.installed_on:
            self.parts.remove(part)
            self.power-=part.boost
            part.installed=False
            part.installed_on=None
            self.acceleration+=part.acceleration
        else:
            print('Деталь установлена на другой автомобиль\n')

    def arreal(self):
        fine=(100-self.condition)*0.01
        print('Разгон от 0 до 100 км/ч\n')
        print('Начало заезда через 3\n')
        time.sleep(1)
        print('2\n')
        time.sleep(1)
        print('1\n')
        time.sleep(1)
        print('Заезд окончен.\n'
              f'Заводское время: {self.initial_acceleration:.2f} сек.\n'
              f'Штраф за повреждения: {fine:.2f}\n'
              f'Выигрыш от тюнинга:  {self.initial_acceleration-self.acceleration:.2f} сек.\n'
              f'Итоговое время разгона: {self.acceleration+fine:.2f} сек.\n'
              )