import random

class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"(x={self.x}, y={self.y}, z={self.z})"

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.x = random.randint(-1000, 1000)
        self.y = random.randint(-1000, 1000)
        self.z = random.randint(-1000, 1000)

    def getPoz(self):
        return Coordinates(self.x, self.y, self.z)

class World:
    @staticmethod
    def move(empty, poz):
        if isinstance(empty, Person) and isinstance(poz, Coordinates):
            empty.x = poz.x
            empty.y = poz.y
            empty.z = poz.z
            print(f'{empty.name} has been moved to {poz}')
        else:
            raise ValueError("Invalid arguments: person must be a Person instance and poz must be a Coordinates instance.")