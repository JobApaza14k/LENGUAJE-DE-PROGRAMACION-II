class Producto:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio if precio >= 0 else 0
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, valor):
        if valor >= 0:
            self._precio = valor
        else:
            print("Error: El precio no puede ser negativo")
    
    @property
    def nombre(self):
        return self._nombre
    
    def aplicar_descuento(self, porcentaje):
        if 0 <= porcentaje <= 100:
            descuento = self._precio * (porcentaje / 100)
            self._precio -= descuento
            print(f"Descuento del {porcentaje}% aplicado. Nuevo precio: ${self._precio:.2f}")
        else:
            print("Error: El porcentaje debe estar entre 0 y 100")
    
    def mostrar_info(self):
        print(f"Producto: {self._nombre} - Precio: ${self._precio:.2f}")



if __name__ == "__main__":
    
    producto1 = Producto("Laptop", 1200)
    producto2 = Producto("Mouse", 25)
    
    print(" Productos creados ")
    producto1.mostrar_info()
    producto2.mostrar_info()
    
    print("\n Aplicar descuentos válidos")
    producto1.aplicar_descuento(10) 
    producto2.aplicar_descuento(20) 
    
    print("\n Intentar descuentos inválidos ")
    producto1.aplicar_descuento(150)  
    producto1.aplicar_descuento(-5)   
    
    print("\nIntentar asignar precio negativo ")
    producto1.precio = -100  
    producto1.mostrar_info()
    
    print("\n Asignar precio válido ")
    producto1.precio = 1000
    producto1.mostrar_info()
