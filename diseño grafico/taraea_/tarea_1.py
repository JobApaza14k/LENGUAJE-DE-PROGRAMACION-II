class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        self.saldo += monto

    def retirar(self, monto):
        if monto <= self.saldo:
            self.saldo -= monto

    def mostrar_saldo(self):
        return self.saldo

c1 = CuentaBancaria("Ana", 500)
c2 = CuentaBancaria("Luis", 300)

c1.depositar(200)
c2.retirar(100)

print(c1.mostrar_saldo())
print(c2.mostrar_saldo())
