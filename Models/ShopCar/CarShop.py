from Models.Car.car import Car

class CarShop:
    def __init__(self):
        self.cars=[]

    def add_car(self, car):
        self.cars.append(car)

    def show(self):
        for car in self.cars:
            print(f"Авто №{self.cars.index(car)+1}")
            print(f"Название:{car.name}\nЦена: {car.price}\n")

    def find_car(self,name):
        for car in self.cars:
            if car.name == name:
                return car
        print("Такого автомобиля нет в продаже\n")
        return None
