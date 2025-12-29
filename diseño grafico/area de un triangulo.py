import math
from typing import TypeVar

T = TypeVar("T", int, float)

def calcular_hipotenusa(cateto_a: T, cateto_b: T) -> T:
    return math.sqrt(cateto_a*2 + cateto_b*2)
a = float(input("Ingrese el valor de A: "))
b = float(input("Ingrese el valor de B: "))
h=print("Hipotenusa =", calcular_hipotenusa(a, b))

def calcular_perimetro(cateto_a: T, cateto_b: T, hipotenusa: T) -> T:
    return cateto_a +  cateto_b + hipotenusa
p= calcular_perimetro(a, b, h)
print("perimetro", calcular_perimetro)

def calcular_area(cateto_a: T, cateto_b: T) -> T:
    return (cateto_a * cateto_b)/2
area=calcular_area(a,b)
print("area= ", calcular_area)

