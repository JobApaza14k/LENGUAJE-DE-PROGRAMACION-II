import math

def calcular_hipotenusa(cateto_a, cateto_b):
    return math.sqrt(cateto_a*2 + cateto_b*2)

def main():
    try:
        a = float(input("Ingresa el valor de A: "))
        b = float(input("Ingresa el valor de B: "))

        if a <= 0 or b <= 0:
            raise ValueError("Los catetos deben ser números positivos")

        hipotenusa = calcular_hipotenusa(a, b)
        print(f"La hipotenusa es: {hipotenusa:.2f}")

    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

if _name_ == "_main_":
    main()
