from DataBase.database import *
from Models.Player.player import Player
from Models.ShopCar.CarShop import CarShop
from Models.Car.car import Car
from Models.Parts.part import Part
from Models.ShopPart.PartShop import ShopPart

item_menu=0
Alex=Player('Alex',150000)
id_player=save_player(Alex.name_player,Alex.money)
name,money=load_player(id_player)
print(name,money)
skyline=Car("Skyline",30000, 300,1100,70)
mazda=Car("mazda",25000,120,1350,80)
turbo=Part("Turbina",30000,50)
exhaust=Part('Exhaust', 15000,10)
shop_p=ShopPart()
shop_p.add_part(turbo)
shop_p.add_part(exhaust)
shop_c=CarShop()
shop_c.add_car(skyline)
shop_c.add_car(mazda)
while item_menu!=6:
    print("=== МЕНЮ ===\n")
    print("1. Информация о игроке\n"
          "2. Гараж\n"
          "3. Мои детали\n"
          "4. Автосалон\n"
          "5. Магазин деталей\n"
          "6. Выход\n")
    number=int(input("Выберите действие: "))
    print()
    if number<=0 or number>6:
        print('Такого варианта нет\n')
        continue
    elif number==1:
        Alex.print_info()
        print()
        continue
    elif number==2:
        garage_menu=0
        while garage_menu!=6:
            Alex.show_cars()
            print('1. Починить автомомбиль\n'
                  '2. Установить деталь\n'
                  '3. Снять деталь\n'
                  '4. Посмотреть характеристики\n'
                  '5. Повредить автомобиль\n'
                  '6. Назад\n')
            garage_menu = int(input("Выберите действие: "))
            print()
            if garage_menu==1:
                if Alex.list_cars:
                    car_name=input('Введите название автомобиля: ')
                    print()
                    Alex.repair_car(car_name)
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu==2:
                if Alex.list_cars:
                    if Alex.bought_parts:
                        car_name = input('Введите название автомобиля: ')
                        print()
                        Alex.show_parts()
                        part_name = input('Введите название детали: ')
                        print()
                        Alex.install(car_name, part_name)
                        id_carpart=save_partcar(id_car,id_part)
                        carpart_id=load_carpart(id_car)
                        print(carpart_id)
                    else:
                        print('У вас нет купленных деталей\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu==3:
                if Alex.list_cars:
                    car_name=input('Введите название автомобиля: ')
                    print()
                    print('Установленные детали: \n')
                    for car in Alex.list_cars:
                        if car.name == car_name:
                            if car.parts:
                                car.show_parts()
                                part_name=input('Введите название детали: ')
                                print()
                                Alex.remove(car_name,part_name)
                            else:
                                print('На вашем автомобиле нет установленных деталей\n')
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu==4:
                if Alex.list_cars:
                    car_name=input('Введите название автомобиля: ')
                    print()
                    Alex.info_car(car_name)
                else:
                    print('У вас нет автомобилей\n')
            elif garage_menu==5:
                if Alex.list_cars:
                    car_name=input('Введите название автомобиля: ')
                    print()
                    points=int(input('Введите количество очков повреждения: '))
                    print()
                    Alex.damage_car(car_name,points)
                else:
                    print('У вас нет автомобилей\n')
            else:
                print('Такого вариатна нет')
        continue
    elif number==3:
        Alex.show_parts()
        part_id=load_playerpart(id_player)
        print(part_id)
        print()
        continue
    elif number==4:
        shop_menu=0
        while shop_menu!=2:
            shop_c.show()
            print('1.Купить автомобиль\n'
                  '2. Назад\n')
            shop_menu = int(input("Выберите действие: "))
            if shop_menu==1:
                car_name=input('Введите название автомобиля: ')
                print()
                car=shop_c.find_car(car_name)
                Alex.buy_car(car)
                id_car=save_car(car,id_player)
                name_car,power,weight,condition,price=load_car(id_car)
                print(name_car,power,weight,condition,price)
            else:
                print('Tакого варианта нет')
    elif number == 5:
        shop_menu=0
        while shop_menu!=2:
            shop_p.show()
            print('1. Купить деталь\n'
                  '2. Назад\n')
            shop_menu = int(input("Выберите действие: "))
            if shop_menu==1:
                part_name=input('Введите название детили: ')
                print()
                part=shop_p.find_part(part_name)
                Alex.buy_part(part)
                id_part=save_parts(part)
                id_playerpart=save_partplayer(id_player,id_part)
                name_part,price_part,boost=load_part(id_part)
                print(name_part,price_part,boost)
            else:
                print('Tакого варианта нет')
    elif number==6:
        item_menu=number
        continue