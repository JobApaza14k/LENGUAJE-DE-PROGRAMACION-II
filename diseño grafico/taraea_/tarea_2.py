class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor >= 0:
            self._precio = valor

    def aplicar_descuento(self, porcentaje):
        if 0 <= porcentaje <= 100:
            self._precio -= self._precio * (porcentaje / 100)

p1 = Producto("Laptop", 1500)
p1.aplicar_descuento(10)
print(p1.precio)

p1.precio = -50
print(p1.precio)
