class DivisionPorCeroError(Exception):
    pass

class CalculadoraSegura:
    def dividir(self, a, b):
        if b == 0:
            raise DivisionPorCeroError("No se puede dividir entre cero")
        return a / b

c = CalculadoraSegura()

try:
    print(c.dividir(10, 2))
    print(c.dividir(5, 0))
except DivisionPorCeroError as e:
    print(e)
