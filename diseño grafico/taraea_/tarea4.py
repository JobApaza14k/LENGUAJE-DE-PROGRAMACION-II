class Vehiculo:
    def acelerar(self):
        return "Acelerando"

class Volador:
    def volar(self):
        return "Volando"

class Avion(Vehiculo, Volador):
    pass

a = Avion()
print(a.acelerar())
print(a.volar())
