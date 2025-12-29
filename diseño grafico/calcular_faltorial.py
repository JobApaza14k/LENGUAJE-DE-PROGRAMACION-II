from typing import TypeVar, Generic

T = TypeVar("T", int, float)

class CalcularFactorial(Generic[T]):
    def __init__(self, numero: T):   
        self.numero = numero

    def calcular_factorial(self) -> int:
        n = int(self.numero)
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos")

        resultado = 1
        for i in range(1, n + 1):
            resultado *= i

        return resultado


def main():
    try:
        n = int(input("Ingrese un número para calcular su factorial: "))

        cal = CalcularFactorial(n)

        print(f"El factorial de {n} es: {cal.calcular_factorial()}")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":  
    main()

