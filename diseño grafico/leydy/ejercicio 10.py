from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    @abstractmethod
    def hacer_sonido(self):
        pass
    
    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Edad: {self.edad} años")


class Perro(Animal):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)
        self.raza = raza
    
    def hacer_sonido(self):
        return "Guau guau"
    
    def mostrar_info(self):
        super().mostrar_info()
        print(f"Raza: {self.raza}")


class Gato(Animal):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color
    
    def hacer_sonido(self):
        return "Miau miau"
    
    def mostrar_info(self):
        super().mostrar_info()
        print(f"Color: {self.color}")


class Vaca(Animal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
    
    def hacer_sonido(self):
        return "Muuu"


class Pato(Animal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
    
    def hacer_sonido(self):
        return "Cuac cuac"


class Oveja(Animal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad)
    
    def hacer_sonido(self):
        return "Beee"


if __name__ == "__main__":
    print("=== GRANJA DE ANIMALES ===\n")
    
    animales = [
        Perro("Rex", 5, "Pastor Alemán"),
        Gato("Michi", 3, "Naranja"),
        Vaca("Lola", 4),
        Pato("Donald", 2),
        Perro("Max", 2, "Golden Retriever"),
        Gato("Luna", 1, "Blanco"),
        Oveja("Dolly", 3)
    ]
    
    print("--- Concierto de animales ---\n")
    for i, animal in enumerate(animales, 1):
        print(f"{i}. {animal.__class__.__name__}: {animal.nombre}")
        animal.mostrar_info()
        print(f"   Sonido: {animal.hacer_sonido()}")
        print("-" * 50)
    
    print("\n--- Animales agrupados por tipo ---\n")
    tipos = {}
    for animal in animales:
        tipo = animal.__class__.__name__
        if tipo not in tipos:
            tipos[tipo] = []
        tipos[tipo].append(animal)
    
    for tipo, lista in tipos.items():
        print(f"{tipo}s ({len(lista)}):")
        for animal in lista:
            print(f"  - {animal.nombre}: {animal.hacer_sonido()}")
        print()
    
    print("--- Intentar crear instancia de Animal ---")
    try:
        animal_generico = Animal("Genérico", 1)
    except TypeError as e:
        print("Error: No se puede instanciar una clase abstracta")
        print(f"   Detalle: {e}")
