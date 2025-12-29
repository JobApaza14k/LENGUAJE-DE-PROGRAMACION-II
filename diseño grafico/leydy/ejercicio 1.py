class CuentaBancaria:
    def __init__(self, nombre, saldo_inicial=0):
        self.nombre = nombre
        self.saldo = saldo_inicial
    
    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            print(f"Depósito exitoso. Nuevo saldo: ${self.saldo:.2f}")
        else:
            print("La cantidad debe ser positiva")
    
    def retirar(self, cantidad):
        if cantidad > 0:
            if cantidad <= self.saldo:
                self.saldo -= cantidad
                print(f"Retiro exitoso. Nuevo saldo: ${self.saldo:.2f}")
            else:
                print("Fondos insuficientes. No se puede retirar.")
        else:
            print("La cantidad debe ser positiva")
    
    def mostrar_saldo(self):
        print(f"Titular: {self.nombre} - Saldo: ${self.saldo:.2f}")



if __name__ == "__main__":
    
    cuenta1 = CuentaBancaria("Juan Pérez", 1000)
    cuenta2 = CuentaBancaria("María García", 500)
    
    print("Estado inicial")
    cuenta1.mostrar_saldo()
    cuenta2.mostrar_saldo()
    
    print("\n Operaciones en Cuenta 1 ")
    cuenta1.depositar(500)
    cuenta1.retirar(200)
    cuenta1.retirar(2000)  
    
    print("\n Operaciones en Cuenta 2 ")
    cuenta2.depositar(300)
    cuenta2.retirar(700)
    
    print("\n Estado final ")
    cuenta1.mostrar_saldo()
    cuenta2.mostrar_saldo()
