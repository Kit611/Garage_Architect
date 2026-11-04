class CarShop:
    def __init__(self):
        self.cars=[]

    def add_car(self, car):
        self.cars.append(car)

    def show(self):
        for car in self.cars:
            print(f"Авто №{self.cars.index(car)+1}")
            print(f"Название: {car.name.capitalize()}\n"
                  f"Мощность: {car.power}\n"
                  f"Разгон:{car.initial_acceleration}\n"
                  f"Цена: {car.price}\n")

    def find_car(self, name):
        for car in self.cars:
            if car.name.lower() == name.lower():
                return car
        raise ValueError('Такого автомобиля нет в продаже')