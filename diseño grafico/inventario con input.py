from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from enum import Enum
import os

# -------------------------------
# Enumeración para tipos de movimiento
# -------------------------------
class TipoMovimiento(Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"

# -------------------------------
# Clase para registrar movimientos de inventario
# -------------------------------
class MovimientoInventario:
    """Registra cada movimiento de stock con fecha y tipo"""
    def __init__(self, producto_codigo: str, tipo: TipoMovimiento, cantidad: int):
        self.producto_codigo = producto_codigo
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = datetime.now()
    
    def __str__(self):
        return f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {self.tipo.value}: {self.cantidad} unidades - Producto: {self.producto_codigo}"

# -------------------------------
# Clase base Producto (encapsulamiento mejorado)
# -------------------------------
class Producto:
    """Representa un producto del inventario con validaciones robustas"""
    
    # Constante de clase
    STOCK_MINIMO_DEFAULT = 5
    
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int = 0, stock_minimo: int = STOCK_MINIMO_DEFAULT):
        self._validar_datos(codigo, nombre, precio, stock, stock_minimo)
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = stock
        self._stock_minimo = stock_minimo
        self._activo = True
    
    @staticmethod
    def _validar_datos(codigo: str, nombre: str, precio: float, stock: int, stock_minimo: int):
        """Valida los datos del producto antes de crear la instancia"""
        if not codigo or not codigo.strip():
            raise ValueError("El código no puede estar vacío")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
    
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def precio(self) -> float:
        return self._precio
    
    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @stock.setter
    def stock(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo")
        self._stock = cantidad
    
    @property
    def stock_minimo(self) -> int:
        return self._stock_minimo
    
    @stock_minimo.setter
    def stock_minimo(self, valor: int):
        if valor < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
        self._stock_minimo = valor
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def desactivar(self):
        self._activo = False
    
    def activar(self):
        self._activo = True
    
    def tiene_stock_bajo(self) -> bool:
        return self._stock <= self._stock_minimo
    
    def __str__(self) -> str:
        estado = "ACTIVO" if self._activo else "INACTIVO"
        alerta = " ⚠️ STOCK BAJO" if self.tiene_stock_bajo() else ""
        return f"[{estado}] {self._codigo} - {self._nombre} | Precio: S/. {self._precio:.2f} | Stock: {self._stock}{alerta}"
    
    def __repr__(self) -> str:
        return f"Producto(codigo='{self._codigo}', nombre='{self._nombre}', precio={self._precio}, stock={self._stock})"

# -------------------------------
# Clase abstracta para reportes
# -------------------------------
class Reporte(ABC):
    """Clase base para diferentes tipos de reportes"""
    
    def __init__(self, productos: List[Producto]):
        self.productos = productos
    
    @abstractmethod
    def generar(self) -> str:
        pass
    
    def mostrar(self):
        print(self.generar())

# -------------------------------
# Reportes concretos
# -------------------------------
class ReporteInventario(Reporte):
    def generar(self) -> str:
        lineas = [
            "\n" + "=" * 70,
            "REPORTE DE INVENTARIO COMPLETO".center(70),
            "=" * 70,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total de productos: {len(self.productos)}",
            "-" * 70
        ]
        
        if not self.productos:
            lineas.append("No hay productos registrados")
        else:
            for producto in self.productos:
                lineas.append(str(producto))
        
        lineas.append("=" * 70)
        return "\n".join(lineas)

class ReporteStockBajo(Reporte):
    def generar(self) -> str:
        productos_bajo_stock = [p for p in self.productos if p.tiene_stock_bajo() and p.activo]
        
        lineas = [
            "\n" + "=" * 70,
            "⚠️  REPORTE DE STOCK BAJO ⚠️".center(70),
            "=" * 70,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Productos con stock bajo: {len(productos_bajo_stock)}",
            "-" * 70
        ]
        
        if not productos_bajo_stock:
            lineas.append("✓ Todos los productos tienen stock adecuado")
        else:
            for producto in productos_bajo_stock:
                deficit = producto.stock_minimo - producto.stock
                lineas.append(f"{producto.nombre} | Stock actual: {producto.stock} | Mínimo: {producto.stock_minimo} | Faltan: {deficit}")
        
        lineas.append("=" * 70)
        return "\n".join(lineas)

class ReporteValorInventario(Reporte):
    def generar(self) -> str:
        valor_total = sum(p.precio * p.stock for p in self.productos if p.activo)
        productos_activos = [p for p in self.productos if p.activo]
        
        lineas = [
            "\n" + "=" * 70,
            "REPORTE DE VALOR DE INVENTARIO".center(70),
            "=" * 70,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Productos activos: {len(productos_activos)}",
            f"Valor total del inventario: S/. {valor_total:,.2f}",
            "-" * 70
        ]
        
        if productos_activos:
            lineas.append("Detalle por producto:")
            for producto in sorted(productos_activos, key=lambda p: p.precio * p.stock, reverse=True):
                valor_producto = producto.precio * producto.stock
                lineas.append(f"  {producto.nombre}: {producto.stock} unidades × S/. {producto.precio:.2f} = S/. {valor_producto:,.2f}")
        
        lineas.append("=" * 70)
        return "\n".join(lineas)

# -------------------------------
# Clase Inventario
# -------------------------------
class Inventario:
    """Gestiona todos los productos y movimientos del inventario"""
    
    def __init__(self):
        self._productos: List[Producto] = []
        self._historial_movimientos: List[MovimientoInventario] = []
    
    @property
    def productos(self) -> List[Producto]:
        return self._productos.copy()
    
    @property
    def productos_activos(self) -> List[Producto]:
        return [p for p in self._productos if p.activo]
    
    def registrar_producto(self, producto: Producto) -> None:
        if self._buscar_producto_por_codigo(producto.codigo):
            raise ValueError(f"Ya existe un producto con el código '{producto.codigo}'")
        
        self._productos.append(producto)
        print(f"✓ Producto '{producto.nombre}' registrado exitosamente")
    
    def entrada_stock(self, codigo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        
        producto = self.buscar_producto(codigo)
        producto.stock += cantidad
        
        movimiento = MovimientoInventario(codigo, TipoMovimiento.ENTRADA, cantidad)
        self._historial_movimientos.append(movimiento)
        
        print(f"✓ Entrada registrada: {cantidad} unidades de '{producto.nombre}' | Nuevo stock: {producto.stock}")
    
    def salida_stock(self, codigo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        
        producto = self.buscar_producto(codigo)
        
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad}")
        
        producto.stock -= cantidad
        
        movimiento = MovimientoInventario(codigo, TipoMovimiento.SALIDA, cantidad)
        self._historial_movimientos.append(movimiento)
        
        print(f"✓ Salida registrada: {cantidad} unidades de '{producto.nombre}' | Stock restante: {producto.stock}")
        
        if producto.tiene_stock_bajo():
            print(f"⚠️  ALERTA: '{producto.nombre}' tiene stock bajo ({producto.stock} unidades)")
    
    def buscar_producto(self, codigo: str) -> Producto:
        producto = self._buscar_producto_por_codigo(codigo)
        if not producto:
            raise ValueError(f"Producto con código '{codigo}' no encontrado")
        return producto
    
    def _buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None
    
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        nombre_lower = nombre.lower()
        return [p for p in self._productos if nombre_lower in p.nombre.lower()]
    
    def actualizar_precio(self, codigo: str, nuevo_precio: float) -> None:
        producto = self.buscar_producto(codigo)
        precio_anterior = producto.precio
        producto.precio = nuevo_precio
        print(f"✓ Precio de '{producto.nombre}' actualizado: S/. {precio_anterior:.2f} → S/. {nuevo_precio:.2f}")
    
    def mostrar_historial_movimientos(self, ultimos: int = 10) -> None:
        print(f"\n--- HISTORIAL DE MOVIMIENTOS (últimos {ultimos}) ---")
        movimientos_recientes = self._historial_movimientos[-ultimos:]
        
        if not movimientos_recientes:
            print("No hay movimientos registrados")
        else:
            for mov in reversed(movimientos_recientes):
                print(mov)
    
    def generar_reporte(self, tipo_reporte: Reporte) -> None:
        tipo_reporte.mostrar()
    
    def listar_productos_simple(self):
        """Lista productos de forma simple para selección"""
        if not self._productos:
            print("No hay productos registrados")
            return
        
        print("\n" + "=" * 70)
        print("LISTA DE PRODUCTOS".center(70))
        print("=" * 70)
        for producto in self._productos:
            print(f"  {producto.codigo} - {producto.nombre} | Stock: {producto.stock}")
        print("=" * 70)

# -------------------------------
# Sistema de menú interactivo
# -------------------------------
class SistemaInventario:
    """Clase que maneja la interfaz de usuario del sistema"""
    
    def __init__(self):
        self.inventario = Inventario()
        self._cargar_datos_iniciales()
    
    def _cargar_datos_iniciales(self):
        """Carga algunos productos de ejemplo"""
        productos_iniciales = [
            Producto("LAP001", "Laptop Dell XPS 15", 3500.00, 10, 3),
            Producto("MOU001", "Mouse Logitech MX Master", 150.00, 20, 5),
            Producto("TEC001", "Teclado Mecánico RGB", 280.00, 8, 5),
        ]
        
        for producto in productos_iniciales:
            self.inventario.registrar_producto(producto)
    
    def limpiar_pantalla(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter"""
        input("\nPresiona Enter para continuar...")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 70)
        print("SISTEMA DE GESTIÓN DE INVENTARIO".center(70))
        print("=" * 70)
        print("1. Agregar nuevo producto")
        print("2. Entrada de stock")
        print("3. Salida de stock")
        print("4. Ver inventario completo")
        print("5. Ver productos con stock bajo")
        print("6. Ver valor del inventario")
        print("7. Actualizar precio de producto")
        print("8. Buscar producto")
        print("9. Ver historial de movimientos")
        print("0. Salir")
        print("=" * 70)
    
    def agregar_producto(self):
        """Menú para agregar un nuevo producto"""
        print("\n--- AGREGAR NUEVO PRODUCTO ---")
        
        try:
            codigo = input("Código del producto: ").strip()
            nombre = input("Nombre del producto: ").strip()
            precio = float(input("Precio: S/. "))
            stock = int(input("Stock inicial: "))
            stock_minimo = int(input(f"Stock mínimo (default {Producto.STOCK_MINIMO_DEFAULT}): ") or Producto.STOCK_MINIMO_DEFAULT)
            
            producto = Producto(codigo, nombre, precio, stock, stock_minimo)
            self.inventario.registrar_producto(producto)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def entrada_stock(self):
        """Menú para registrar entrada de stock"""
        print("\n--- ENTRADA DE STOCK ---")
        
        self.inventario.listar_productos_simple()
        
        try:
            codigo = input("\nCódigo del producto: ").strip()
            cantidad = int(input("Cantidad a ingresar: "))
            
            self.inventario.entrada_stock(codigo, cantidad)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def salida_stock(self):
        """Menú para registrar salida de stock"""
        print("\n--- SALIDA DE STOCK ---")
        
        self.inventario.listar_productos_simple()
        
        try:
            codigo = input("\nCódigo del producto: ").strip()
            cantidad = int(input("Cantidad a retirar: "))
            
            self.inventario.salida_stock(codigo, cantidad)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def ver_inventario(self):
        """Muestra el inventario completo"""
        reporte = ReporteInventario(self.inventario.productos_activos)
        self.inventario.generar_reporte(reporte)
    
    def ver_stock_bajo(self):
        """Muestra productos con stock bajo"""
        reporte = ReporteStockBajo(self.inventario.productos_activos)
        self.inventario.generar_reporte(reporte)
    
    def ver_valor_inventario(self):
        """Muestra el valor total del inventario"""
        reporte = ReporteValorInventario(self.inventario.productos_activos)
        self.inventario.generar_reporte(reporte)
    
    def actualizar_precio(self):
        """Menú para actualizar precio de un producto"""
        print("\n--- ACTUALIZAR PRECIO ---")
        
        self.inventario.listar_productos_simple()
        
        try:
            codigo = input("\nCódigo del producto: ").strip()
            nuevo_precio = float(input("Nuevo precio: S/. "))
            
            self.inventario.actualizar_precio(codigo, nuevo_precio)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def buscar_producto(self):
        """Menú para buscar productos"""
        print("\n--- BUSCAR PRODUCTO ---")
        print("1. Buscar por código")
        print("2. Buscar por nombre")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        try:
            if opcion == "1":
                codigo = input("Código: ").strip()
                producto = self.inventario.buscar_producto(codigo)
                print(f"\n✓ Producto encontrado:")
                print(f"  {producto}")
                
            elif opcion == "2":
                nombre = input("Nombre (o parte del nombre): ").strip()
                productos = self.inventario.buscar_por_nombre(nombre)
                
                if productos:
                    print(f"\n✓ Se encontraron {len(productos)} producto(s):")
                    for p in productos:
                        print(f"  {p}")
                else:
                    print("❌ No se encontraron productos")
            else:
                print("❌ Opción inválida")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def ver_historial(self):
        """Muestra el historial de movimientos"""
        try:
            cantidad = int(input("\n¿Cuántos movimientos deseas ver? (default 10): ") or "10")
            self.inventario.mostrar_historial_movimientos(cantidad)
        except ValueError:
            print("❌ Cantidad inválida, mostrando últimos 10")
            self.inventario.mostrar_historial_movimientos(10)
    
    def ejecutar(self):
        """Ejecuta el sistema de inventario"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                self.agregar_producto()
                self.pausar()
            elif opcion == "2":
                self.entrada_stock()
                self.pausar()
            elif opcion == "3":
                self.salida_stock()
                self.pausar()
            elif opcion == "4":
                self.ver_inventario()
                self.pausar()
            elif opcion == "5":
                self.ver_stock_bajo()
                self.pausar()
            elif opcion == "6":
                self.ver_valor_inventario()
                self.pausar()
            elif opcion == "7":
                self.actualizar_precio()
                self.pausar()
            elif opcion == "8":
                self.buscar_producto()
                self.pausar()
            elif opcion == "9":
                self.ver_historial()
                self.pausar()
            elif opcion == "0":
                print("\n¡Gracias por usar el sistema de inventario! 👋")
                break
            else:
                print("❌ Opción inválida. Por favor, intenta de nuevo.")
                self.pausar()

# -------------------------------
# Función principal
# -------------------------------
def main():
    sistema = SistemaInventario()
    sistema.ejecutar()

if __name__ == "__main__":
    main()
