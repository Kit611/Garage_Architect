from Models.Parts.part import Part

class ShopPart:
    def __init__(self):
        self.parts=[]

    def add_part(self, part):
        self.parts.append(part)

    def show(self):
        for part in self.parts:
            print(f"Деталь №{self.parts.index(part)+1}")
            print(f"Название: {part.name}\nЦена: {part.price}\nПрибавка к мощности: {part.boost}\n")

    def find_part(self, name):
        for part in self.parts:
            if part.name == name:
                return part
        print('Такой детали нет\n')
        return None