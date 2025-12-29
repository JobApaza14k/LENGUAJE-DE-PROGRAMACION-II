import math

class Figura:
    def area(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")


class Rectangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def area(self):
        return self.base * self.altura
    
    def __str__(self):
        return f"Rectángulo (base={self.base}, altura={self.altura})"


class Triangulo(Figura):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def area(self):
        return (self.base * self.altura) / 2
    
    def __str__(self):
        return f"Triángulo (base={self.base}, altura={self.altura})"


class Circulo(Figura):
    def __init__(self, radio):
        self.radio = radio
    
    def area(self):
        return math.pi * (self.radio ** 2)
    
    def __str__(self):
        return f"Círculo (radio={self.radio})"



if __name__ == "__main__":
    
    figuras = [
        Rectangulo(5, 10),
        Circulo(7),
        Triangulo(6, 8),
        Rectangulo(4, 4),
        Circulo(3.5),
        Triangulo(10, 5)
    ]
    
    print("=== CÁLCULO DE ÁREAS ===\n")
    
    area_total = 0
    
   
    for i, figura in enumerate(figuras, 1):
        area = figura.area()
        area_total += area
        print(f"{i}. {figura}")
        print(f"   Área: {area:.2f} unidades²")
        print("-" * 50)
    
    print(f"\n Área total de todas las figuras: {area_total:.2f} unidades²")
    print(f" Área promedio: {area_total/len(figuras):.2f} unidades²")
