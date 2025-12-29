class ConversorTemperatura:
    def __init__(self, temperatura_fahrenheit):
        self.temperatura_fahrenheit = temperatura_fahrenheit
    
    @classmethod
    def desde_celsius(cls, celsius):
        """Método de clase: crea un objeto a partir de grados Celsius"""
        fahrenheit = cls.celsius_a_fahrenheit(celsius)
        print(f" Convirtiendo {celsius}°C a Fahrenheit...")
        return cls(fahrenheit)
    
    @classmethod
    def desde_kelvin(cls, kelvin):
        """Método de clase adicional: crea un objeto desde Kelvin"""
        celsius = kelvin - 273.15
        fahrenheit = cls.celsius_a_fahrenheit(celsius)
        print(f" Convirtiendo {kelvin}K a Fahrenheit...")
        return cls(fahrenheit)
    
    @staticmethod
    def celsius_a_fahrenheit(celsius):
        """Método estático: convierte Celsius a Fahrenheit sin necesitar instancia"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_a_celsius(fahrenheit):
        """Método estático adicional"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def kelvin_a_celsius(kelvin):
        """Método estático adicional"""
        return kelvin - 273.15
    
    def obtener_celsius(self):
        """Obtiene la temperatura almacenada en Celsius"""
        return self.fahrenheit_a_celsius(self.temperatura_fahrenheit)
    
    def obtener_kelvin(self):
        """Obtiene la temperatura almacenada en Kelvin"""
        celsius = self.obtener_celsius()
        return celsius + 273.15
    
    def mostrar_temperatura(self):
        celsius = self.obtener_celsius()
        kelvin = self.obtener_kelvin()
        print(f"\n️  Temperatura actual:")
        print(f"   Fahrenheit: {self.temperatura_fahrenheit:.2f}°F")
        print(f"   Celsius: {celsius:.2f}°C")
        print(f"   Kelvin: {kelvin:.2f}K")



if __name__ == "__main__":
    print("=== CONVERSOR DE TEMPERATURA ===\n")
    
   
    print("--- Uso de métodos estáticos ---")
    print(f"25°C = {ConversorTemperatura.celsius_a_fahrenheit(25):.2f}°F")
    print(f"77°F = {ConversorTemperatura.fahrenheit_a_celsius(77):.2f}°C")
    print(f"300K = {ConversorTemperatura.kelvin_a_celsius(300):.2f}°C")
    
   
    print("\n--- Crear objeto con Fahrenheit ---")
    temp1 = ConversorTemperatura(32)
    temp1.mostrar_temperatura()
    
    
    print("\n--- Crear objeto desde Celsius (método de clase) ---")
    temp2 = ConversorTemperatura.desde_celsius(100)
    temp2.mostrar_temperatura()
    
  
    print("\n--- Crear objeto desde Kelvin (método de clase) ---")
    temp3 = ConversorTemperatura.desde_kelvin(273.15)
    temp3.mostrar_temperatura()
    
    
    print("\n--- Más conversiones ---")
    temp4 = ConversorTemperatura.desde_celsius(37)  
    print("Temperatura corporal normal:")
    temp4.mostrar_temperatura()
    
    temp5 = ConversorTemperatura.desde_celsius(-40) 
    print("\nPunto donde Celsius y Fahrenheit son iguales:")
    temp5.mostrar_temperatura()
