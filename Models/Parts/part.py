#название: турбина, цена: 30 000, прибавка к мощности: 50, флаг установлености

class Part:
    def __init__(self,name,price,boost):
        self.name = name
        self.price = price
        self.boost = boost
        self.installed = False
        self.installed_on=None


    def print_characteristics(self):
        if self.installed:
            print(f"Название: {self.name}\nЦена: {self.price}\nПрибавка к мощности: {self.boost}\nУстановлен: Да\nУстановлен на:{self.installed_on.name}\n")
        elif not self.installed:
            print(
                f"Название: {self.name}\nЦена: {self.price}\nПрибавка к мощности: {self.boost}\nУстановлен: Нет\n")