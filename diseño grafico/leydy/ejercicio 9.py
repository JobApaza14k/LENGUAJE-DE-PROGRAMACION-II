class DivisionPorCeroError(Exception):
    """Excepción personalizada para división por cero"""
    def __init__(self, mensaje="No se puede dividir por cero"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class NumeroNegativoError(Exception):
    """Excepción adicional para números negativos en raíz cuadrada"""
    def __init__(self, mensaje="No se puede calcular la raíz cuadrada de un número negativo"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class CalculadoraSegura:
    @staticmethod
    def dividir(a, b):
        """Divide a entre b, lanzando excepción si b es cero"""
        if b == 0:
            raise DivisionPorCeroError(f"Intento de dividir {a} entre cero")
        return a / b
    
    @staticmethod
    def sumar(a, b):
        return a + b
    
    @staticmethod
    def restar(a, b):
        return a - b
    
    @staticmethod
    def multiplicar(a, b):
        return a * b
    
    @staticmethod
    def raiz_cuadrada(a):
        """Calcula la raíz cuadrada, lanzando excepción si el número es negativo"""
        if a < 0:
            raise NumeroNegativoError(f"No se puede calcular la raíz de {a}")
        return a ** 0.5
    
    @staticmethod
    def potencia(base, exponente):
        return base ** exponente



if __name__ == "__main__":
    calc = CalculadoraSegura()
    
    print("=== CALCULADORA SEGURA ===\n")
    
    
    print("--- Operaciones válidas ---")
    try:
        resultado = calc.dividir(10, 2)
        print(f" 10 / 2 = {resultado}")
        
        resultado = calc.sumar(5, 3)
        print(f" 5 + 3 = {resultado}")
        
        resultado = calc.raiz_cuadrada(16)
        print(f" √16 = {resultado}")
    except Exception as e:
        print(f" Error: {e}")
    
    
    print("\n--- Intentar división por cero ---")
    try:
        resultado = calc.dividir(10, 0)
        print(f"Resultado: {resultado}")
    except DivisionPorCeroError as e:
        print(f" Error capturado: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
    
    
    print("\n--- Más pruebas de división por cero ---")
    numeros = [(15, 3), (20, 0), (8, 2), (100, 0)]
    
    for a, b in numeros:
        try:
            resultado = calc.dividir(a, b)
            print(f" {a} / {b} = {resultado:.2f}")
        except DivisionPorCeroError as e:
            print(f" {a} / {b} → Error: {e}")
    
   
    print("\n--- Intentar raíz cuadrada de números negativos ---")
    numeros_raiz = [25, -9, 16, -4, 0]
    
    for num in numeros_raiz:
        try:
            resultado = calc.raiz_cuadrada(num)
            print(f" √{num} = {resultado:.2f}")
        except NumeroNegativoError as e:
            print(f" √{num} → Error: {e}")
    
   
    print("\n--- Ejemplo con finally ---")
    try:
        print("Intentando operación...")
        resultado = calc.dividir(100, 0)
    except DivisionPorCeroError as e:
        print(f" Error: {e}")
    finally:
        print(" Bloque finally ejecutado (siempre se ejecuta)")
