import math

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, otro):
        """Suma de vectores"""
        return Vector2D(self.x + otro.x, self.y + otro.y)
    
    def __sub__(self, otro):
        """Resta de vectores"""
        return Vector2D(self.x - otro.x, self.y - otro.y)
    
    def __mul__(self, escalar):
        """Multiplicación por escalar"""
        return Vector2D(self.x * escalar, self.y * escalar)
    
    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()
    
    def magnitud(self):
        """Calcula la magnitud del vector"""
        return math.sqrt(self.x**2 + self.y**2)
    
    def __eq__(self, otro):
        """Compara si dos vectores son iguales"""
        return self.x == otro.x and self.y == otro.y



if __name__ == "__main__":
    
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    v3 = Vector2D(5, -1)
    
    print("OPERACIONES CON VECTORES \n")
    
    print(f"Vector 1: {v1}")
    print(f"Vector 2: {v2}")
    print(f"Vector 3: {v3}")
    
    print("\n SUMA DE VECTORES ")
    suma = v1 + v2
    print(f"{v1} + {v2} = {suma}")
    
    print("\n RESTA DE VECTORES ")
    resta = v1 - v2
    print(f"{v1} - {v2} = {resta}")
    
    print("\n MULTIPLICACIÓN POR ESCALAR ")
    mult1 = v1 * 2
    mult2 = v2 * 3
    mult3 = v3 * -1
    print(f"{v1} * 2 = {mult1}")
    print(f"{v2} * 3 = {mult2}")
    print(f"{v3} * -1 = {mult3}")
    
    print("\n OPERACIONES COMBINADAS ")
    resultado = (v1 + v2) * 2 - v3
    print(f"({v1} + {v2}) * 2 - {v3} = {resultado}")
    
    print("\n MAGNITUDES ")
    print(f"Magnitud de {v1}: {v1.magnitud():.2f}")
    print(f"Magnitud de {v2}: {v2.magnitud():.2f}")
    print(f"Magnitud de {suma}: {suma.magnitud():.2f}")
    
    print("\nCOMPARACIONES ")
    v4 = Vector2D(3, 4)
    print(f"{v1} == {v4}: {v1 == v4}")
    print(f"{v1} == {v2}: {v1 == v2}")
