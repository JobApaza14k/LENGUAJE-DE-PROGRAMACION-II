# principio S
class CalculadoraOperacion:
    def calcular(self, a, b):
        raise NotImplementedError("debe implementar el metodo calcular")


# principio O y L
class Suma(CalculadoraOperacion):
    def calcular(self, a, b):
        return a + b


class Resta(CalculadoraOperacion):
    def calcular(self, a, b):
        return a - b


class Multiplicacion(CalculadoraOperacion):
    def calcular(self, a, b):
        return a * b


class Division(CalculadoraOperacion):
    def calcular(self, a, b):
        if b == 0:
            return "error: division entre cero"
        return a / b


# principio D
class Aplicacion:
    def __init__(self, calculadora):
        self.calculadora = calculadora

    def ejecutar(self, a, b):
        resultado = self.calculadora.calcular(a, b)
        print(f"El resultado es: {resultado}")


# menú simple con input
print("Calculadora extensible")
print("Operaciones disponibles: suma, resta, multiplicacion, division")

op = input("Ingrese la operación: ").strip().lower()
a = float(input("Ingrese el primer número: "))
b = float(input("Ingrese el segundo número: "))

if op == "suma":
    calc = Suma()
elif op == "resta":
    calc = Resta()
elif op == "multiplicacion":
    calc = Multiplicacion()
elif op == "division":
    calc = Division()
else:
    print("Operación no válida")
    exit()

app = Aplicacion(calc)
app.ejecutar(a, b)
