class Motor:
    def __init__(self, tipo, cilindros, caballos_fuerza):
        self.tipo = tipo
        self.cilindros = cilindros
        self.caballos_fuerza = caballos_fuerza
        self.encendido = False
        self.rpm = 0
    
    def encender(self):
        if not self.encendido:
            self.encendido = True
            self.rpm = 800  
            print(f" Motor {self.tipo} encendido")
            print(f"   Cilindros: {self.cilindros}")
            print(f"   Potencia: {self.caballos_fuerza} HP")
            print(f"   RPM: {self.rpm}")
        else:
            print(" El motor ya está encendido")
    
    def apagar(self):
        if self.encendido:
            self.encendido = False
            self.rpm = 0
            print(" Motor apagado")
        else:
            print("️ El motor ya está apagado")
    
    def acelerar(self, incremento_rpm):
        if self.encendido:
            self.rpm += incremento_rpm
            print(f" Acelerando motor... RPM: {self.rpm}")
        else:
            print(" No se puede acelerar. El motor está apagado")


class Auto:
    def __init__(self, marca, modelo, motor):
        self.marca = marca
        self.modelo = modelo
        self.motor = motor 
        self.velocidad = 0
    
    def arrancar(self):
        print(f"\n Intentando arrancar {self.marca} {self.modelo}...")
        if not self.motor.encendido:
            self.motor.encender()
            print(" Auto listo para conducir\n")
        else:
            print("️ El auto ya está arrancado\n")
    
    def detener(self):
        print(f"\n Deteniendo {self.marca} {self.modelo}...")
        self.velocidad = 0
        self.motor.apagar()
        print(" Auto detenido\n")
    
    def conducir(self, velocidad_objetivo):
        if self.motor.encendido:
            self.velocidad = velocidad_objetivo
            rpm_necesario = velocidad_objetivo * 30  #
            self.motor.rpm = rpm_necesario
            print(f" Conduciendo a {self.velocidad} km/h (RPM: {self.motor.rpm})")
        else:
            print("️ No se puede conducir. Primero arranca el auto")
    
    def mostrar_info(self):
        estado = "Encendido" if self.motor.encendido else "Apagado"
        print(f"\n{'='*50}")
        print(f" {self.marca} {self.modelo}")
        print(f"Estado: {estado}")
        print(f"Velocidad: {self.velocidad} km/h")
        print(f"Motor: {self.motor.tipo} - {self.motor.caballos_fuerza} HP")
        print(f"RPM del motor: {self.motor.rpm}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    
    motor_v8 = Motor("V8", 8, 450)
    
   
    auto = Auto("Ford", "Mustang", motor_v8)
    
    print("=== SIMULACIÓN DE CONDUCCIÓN ===")
    
    auto.mostrar_info()
    
    
    auto.conducir(60)
    
   
    auto.arrancar()
    

    auto.conducir(60)
    auto.conducir(100)
    auto.conducir(120)
    
    auto.mostrar_info()
    
   
    auto.detener()
    
    auto.mostrar_info()
