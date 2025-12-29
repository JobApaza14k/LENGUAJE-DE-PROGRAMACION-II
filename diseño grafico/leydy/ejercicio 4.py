class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.velocidad = 0
    
    def acelerar(self, incremento):
        self.velocidad += incremento
        print(f" (Acelerando) Velocidad actual: {self.velocidad} km/h")


class Volador:
    def __init__(self):
        self.altitud = 0
        self.en_vuelo = False
    
    def volar(self, altitud_objetivo):
        if not self.en_vuelo:
            print("️ Despegando  ")
            self.en_vuelo = True
        
        self.altitud = altitud_objetivo
        print(f"️ Volando a {self.altitud} metros de altura")
    
    def aterrizar(self):
        if self.en_vuelo:
            print("️ Aterrizando...")
            self.altitud = 0
            self.en_vuelo = False
            print("️ Aterrizaje completado")


class Avion(Vehiculo, Volador):
    def __init__(self, marca, modelo, capacidad_pasajeros):
        Vehiculo.__init__(self, marca, modelo)
        Volador.__init__(self)
        self.capacidad_pasajeros = capacidad_pasajeros
    
    def mostrar_info(self):
        estado = "en vuelo" if self.en_vuelo else "en tierra"
        print(f"\n{'='*50}")
        print(f"Avión: {self.marca} {self.modelo}")
        print(f"Capacidad: {self.capacidad_pasajeros} pasajeros")
        print(f"Estado: {estado}")
        print(f"Velocidad: {self.velocidad} km/h")
        print(f"Altitud: {self.altitud} metros")
        print(f"{'='*50}\n")


if __name__ == "__main__":
  
    avion = Avion("Boeing", "747", 416)
    
    print("SIMULACIÓN DE VUELO \n")
    
    avion.mostrar_info()
    
    print("Fase de despegue ")
    avion.acelerar(100)
    avion.acelerar(150)
    avion.acelerar(250)
    
    print("\n Fase de vuelo ")
    avion.volar(10000)
    avion.acelerar(400)
    avion.volar(12000)
    
    avion.mostrar_info()
    
    print("Fase de aterrizaje ")
    avion.volar(5000)
    avion.volar(1000)
    avion.aterrizar()
    
    avion.mostrar_info()
