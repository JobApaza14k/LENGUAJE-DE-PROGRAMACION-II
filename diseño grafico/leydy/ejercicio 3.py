class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
    
    def calcular_pago(self):
        return self.salario


class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, salario_mensual):
        super().__init__(nombre, salario_mensual)
    
    def calcular_pago(self):
        return self.salario


class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, tarifa_por_hora, horas_trabajadas):
        super().__init__(nombre, tarifa_por_hora)
        self.horas_trabajadas = horas_trabajadas
    
    def calcular_pago(self):
        pago_base = self.salario * self.horas_trabajadas
        if self.horas_trabajadas > 40:
            horas_extra = self.horas_trabajadas - 40
            pago_extra = horas_extra * self.salario * 0.5
            return pago_base + pago_extra
        return pago_base



if __name__ == "__main__":
   
    empleados = [
        EmpleadoTiempoCompleto("Ana López", 3000),
        EmpleadoPorHoras("Carlos Ruiz", 15, 45),
        EmpleadoTiempoCompleto("Pedro Gómez", 3500),
        EmpleadoPorHoras("Laura Martínez", 20, 35),
        EmpleadoPorHoras("Diego Torres", 18, 50)
    ]
    
    print("CÁLCULO DE PAGOS \n")
    
    total_nomina = 0
    for empleado in empleados:
        pago = empleado.calcular_pago()
        total_nomina += pago
        
        tipo = "Tiempo Completo" if isinstance(empleado, EmpleadoTiempoCompleto) else "Por Horas"
        print(f"Empleado: {empleado.nombre}")
        print(f"Tipo: {tipo}")
        print(f"Pago: ${pago:.2f}")
        print("-" * 40)
    
    print(f"\nTotal de nómina: ${total_nomina:.2f}")
