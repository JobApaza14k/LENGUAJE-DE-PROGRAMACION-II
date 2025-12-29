class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def calcular_pago(self):
        return self.salario

class EmpleadoTiempoCompleto(Empleado):
    def calcular_pago(self):
        return self.salario

class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, salario, horas):
        super().__init__(nombre, salario)
        self.horas = horas

    def calcular_pago(self):
        return self.salario * self.horas

empleados = [
    EmpleadoTiempoCompleto("Ana", 1200),
    EmpleadoPorHoras("Luis", 20, 80)
]

for e in empleados:
    print(e.nombre, e.calcular_pago())
