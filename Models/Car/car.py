#Название: скайлайн. Мощность: 300 л.с. Масса: 1,100. Состояние: 70/100
#Ремотнироваться, показывать характеристики, получать повреждения
from unittest import skipIf
from Models.Parts.part import Part

class Car:
    def __init__(self,name,price,power,weight,condition):
        self.name=name
        self.price=price
        self.power=power
        self.weight=weight
        self.condition=condition
        self.parts=[]

    def print_characteristics(self):
        print(f"Название: {self.name}\nЦена:{self.price} \nМощность: {self.power} \nВес: {self.weight} \nСостояние: {self.condition}/100")
        for part in self.parts:
            print(f"Установленные детали:\n{part.name}\n")

    def show_parts(self):
        for part in self.parts:
            print(f"Название: {part.name}\n")

    def repair(self):
        repair_points=100-self.condition
        self.condition+=repair_points

    def damage(self,points_damege):
        self.condition-=points_damege
        if self.condition<=0:
            self.condition=0
        print(f'Автомобиль поврежден на {points_damege} очков\n')

    def install_part(self,part):
        if not part.installed:
            self.parts.append(part)
            self.power+=part.boost
            part.installed=True
            part.installed_on=self
        else:
            print('Деталь уже установлена\n')

    def print_parts(self):
        for part in self.parts:
            print(part.name)

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
        else:
            print('Деталь установлена на другой автомобиль\n')
