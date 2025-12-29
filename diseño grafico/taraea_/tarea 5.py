import math

class Figura:
    def area(self):
        pass

class Rectangulo(Figura):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def area(self):
        return self.a * self.b

class Triangulo(Figura):
    def __init__(self, b, h):
        self.b = b
        self.h = h

    def area(self):
        return (self.b * self.h) / 2

class Circulo(Figura):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

figuras = [
    Rectangulo(4, 5),
    Triangulo(4, 6),
    Circulo(3)
]

for f in figuras:
    print(f.area())
