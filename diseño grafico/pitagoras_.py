import math
from typing import TypeVar

T = TypeVar("T", int, float)

def calcular_hipotenusa(cateto_a: T, cateto_b: T) -> T:
    return math.sqrt(cateto_a*2 + cateto_b*2)

a = float(input("Ingrese el valor de A: "))
b = float(input("Ingrese el valor de B: "))

print("Hipotenusa =", calcular_hipotenusa(a, b))
