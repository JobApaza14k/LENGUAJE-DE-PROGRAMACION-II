from abc import ABC, abstractmethod
from datetime import datetime

# Clase base Producto

class Producto:
    def __init__(self, codigo, nombre, precio, stock=0):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = stock  # encapsulado
    
    # Getters y setters (encapsulamiento)
    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, cantidad):
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo")
        self._stock = cantidad

    def __str__(self):
        return f"{self._codigo} - {self._nombre} | Precio: {self._precio} | Stock: {self._stock}"



# Clase abstracta para reportes

class Reporte(ABC):
    @abstractmethod
    def generar(self):
        pass



# Clases de reportes concretos (polimorfismo)

class ReporteInventario(Reporte):
    def __init__(self, productos):
        self.productos = productos

    def generar(self):
        print("\n--- INVENTARIO ---")
        for producto in self.productos:
            print(producto)


class ReporteRecortes(Reporte):
    def __init__(self, productos):
        self.productos = productos

    def generar(self):
        print("\n--- RECORTES DE INVENTARIO ---")
        for producto in self.productos:
            if producto.stock <= 5:
                print(f"{producto.nombre} | Stock bajo: {producto.stock}")


# -------------------------------
# Clase Inventario
# -------------------------------
class Inventario:
    def __init__(self):
        self.productos = []

    # Métodos para agregar productos
    def registrar_producto(self, producto):
        if any(p.codigo == producto.codigo for p in self.productos):
            raise ValueError("Producto ya registrado")
        self.productos.append(producto)

    # Métodos para entradas y salidas de stock
    def entrada_stock(self, codigo, cantidad):
        producto = self.buscar_producto(codigo)
        producto.stock += cantidad
        print(f"Se agregaron {cantidad} unidades a {producto.nombre}")

    def salida_stock(self, codigo, cantidad):
        producto = self.buscar_producto(codigo)
        if producto.stock < cantidad:
            raise ValueError("Stock insuficiente")
        producto.stock -= cantidad
        print(f"Se retiraron {cantidad} unidades de {producto.nombre}")

    # Método para buscar producto
    def buscar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        raise ValueError("Producto no encontrado")


# -------------------------------
# Ejemplo de uso
# -------------------------------
def main():
    inventario = Inventario()

    # Crear productos (construcción de objetos)
    p1 = Producto("001", "Laptop", 3500, 10)
    p2 = Producto("002", "Mouse", 50, 20)
    p3 = Producto("003", "Teclado", 80, 3)

    # Registrar productos
    inventario.registrar_producto(p1)
    inventario.registrar_producto(p2)
    inventario.registrar_producto(p3)

    # Gestionar stock
    inventario.entrada_stock("003", 5)
    inventario.salida_stock("002", 10)

    # Generar reportes (polimorfismo)
    reporte_inv = ReporteInventario(inventario.productos)
    reporte_inv.generar()

    reporte_rec = ReporteRecortes(inventario.productos)
    reporte_rec.generar()


if __name__ == "__main__":
    main()
