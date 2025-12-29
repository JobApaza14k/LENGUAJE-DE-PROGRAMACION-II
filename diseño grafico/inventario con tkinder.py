from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import csv
import os
import json

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
    def __init__(self, producto_codigo: str, tipo: TipoMovimiento, cantidad: int):
        self.producto_codigo = producto_codigo
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = datetime.now()
    
    def __str__(self):
        return f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {self.tipo.value}: {self.cantidad} unidades - Producto: {self.producto_codigo}"
    
    def to_dict(self):
        return {
            'producto_codigo': self.producto_codigo,
            'tipo': self.tipo.value,
            'cantidad': self.cantidad,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S')
        }

# -------------------------------
# Clase base Producto
# -------------------------------
class Producto:
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
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def tiene_stock_bajo(self) -> bool:
        return self._stock <= self._stock_minimo
    
    def to_dict(self):
        return {
            'codigo': self._codigo,
            'nombre': self._nombre,
            'precio': self._precio,
            'stock': self._stock,
            'stock_minimo': self._stock_minimo,
            'activo': self._activo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        producto = cls(
            codigo=data['codigo'],
            nombre=data['nombre'],
            precio=float(data['precio']),
            stock=int(data['stock']),
            stock_minimo=int(data['stock_minimo'])
        )
        producto._activo = bool(data['activo'])
        return producto

# -------------------------------
# Clase abstracta para reportes
# -------------------------------
class Reporte(ABC):
    def __init__(self, productos: List[Producto]):
        self.productos = productos
    
    @abstractmethod
    def generar(self) -> str:
        pass

class ReporteInventario(Reporte):
    def generar(self) -> str:
        lineas = [
            "=" * 80,
            "TECHNOVA - REPORTE DE INVENTARIO COMPLETO".center(80),
            "=" * 80,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total de productos: {len(self.productos)}",
            "-" * 80,
            ""
        ]
        
        if not self.productos:
            lineas.append("No hay productos registrados")
        else:
            for producto in self.productos:
                estado = "ACTIVO" if producto.activo else "INACTIVO"
                alerta = " ⚠️ STOCK BAJO" if producto.tiene_stock_bajo() else ""
                lineas.append(f"[{estado}] {producto.codigo} - {producto.nombre}")
                lineas.append(f"  Precio: S/. {producto.precio:.2f} | Stock: {producto.stock}{alerta}")
                lineas.append("")
        
        lineas.append("=" * 80)
        return "\n".join(lineas)

class ReporteStockBajo(Reporte):
    def generar(self) -> str:
        productos_bajo_stock = [p for p in self.productos if p.tiene_stock_bajo() and p.activo]
        
        lineas = [
            "=" * 80,
            "TECHNOVA - ⚠️  REPORTE DE STOCK BAJO ⚠️".center(80),
            "=" * 80,
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Productos con stock bajo: {len(productos_bajo_stock)}",
            "-" * 80,
            ""
        ]
        
        if not productos_bajo_stock:
            lineas.append("✓ Todos los productos tienen stock adecuado")
        else:
            for producto in productos_bajo_stock:
                deficit = producto.stock_minimo - producto.stock
                lineas.append(f"{producto.nombre}")
                lineas.append(f"  Stock actual: {producto.stock} | Mínimo: {producto.stock_minimo} | Faltan: {deficit}")
                lineas.append("")
        
        lineas.append("=" * 80)
        return "\n".join(lineas)

# -------------------------------
# Clase Inventario
# -------------------------------
class Inventario:
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
    
    def entrada_stock(self, codigo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        
        producto = self.buscar_producto(codigo)
        producto.stock += cantidad
        
        movimiento = MovimientoInventario(codigo, TipoMovimiento.ENTRADA, cantidad)
        self._historial_movimientos.append(movimiento)
    
    def salida_stock(self, codigo: str, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        
        producto = self.buscar_producto(codigo)
        
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad}")
        
        producto.stock -= cantidad
        
        movimiento = MovimientoInventario(codigo, TipoMovimiento.SALIDA, cantidad)
        self._historial_movimientos.append(movimiento)
    
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
    
    def obtener_historial(self, ultimos: int = 20) -> List[MovimientoInventario]:
        return self._historial_movimientos[-ultimos:]
    
    def exportar_csv(self, ruta_archivo: str) -> None:
        """Exporta todos los productos a un archivo CSV"""
        try:
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
                campos = ['codigo', 'nombre', 'precio', 'stock', 'stock_minimo', 'activo']
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                
                escritor.writeheader()
                for producto in self._productos:
                    escritor.writerow(producto.to_dict())
        except Exception as e:
            raise Exception(f"Error al exportar CSV: {str(e)}")
    
    def importar_csv(self, ruta_archivo: str, modo_importacion: str = 'agregar') -> tuple[int, int]:
        """
        Importa productos desde un archivo CSV
        modos: 'agregar', 'reemplazar', 'actualizar'
        """
        productos_importados = 0
        productos_actualizados = 0
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                if modo_importacion == 'reemplazar':
                    self._productos.clear()
                
                for fila in lector:
                    try:
                        # Convertir tipos de datos
                        codigo = fila['codigo'].strip()
                        nombre = fila['nombre'].strip()
                        precio = float(fila['precio'])
                        stock = int(fila['stock'])
                        stock_minimo = int(fila.get('stock_minimo', 5))
                        activo = fila.get('activo', 'True').lower() in ['true', '1', 'yes', 'si']
                        
                        producto_existente = self._buscar_producto_por_codigo(codigo)
                        
                        if producto_existente:
                            if modo_importacion in ['actualizar', 'agregar']:
                                # Actualizar producto existente
                                producto_existente._nombre = nombre
                                producto_existente._precio = precio
                                producto_existente._stock = stock
                                producto_existente._stock_minimo = stock_minimo
                                producto_existente._activo = activo
                                productos_actualizados += 1
                        else:
                            # Crear nuevo producto
                            producto = Producto(
                                codigo=codigo,
                                nombre=nombre,
                                precio=precio,
                                stock=stock,
                                stock_minimo=stock_minimo
                            )
                            producto._activo = activo
                            self._productos.append(producto)
                            productos_importados += 1
                            
                    except (ValueError, KeyError) as e:
                        print(f"Error al procesar fila: {fila} - Error: {e}")
                        continue
                        
        except FileNotFoundError:
            raise Exception(f"Archivo no encontrado: {ruta_archivo}")
        except Exception as e:
            raise Exception(f"Error al importar CSV: {str(e)}")
        
        return productos_importados, productos_actualizados
    
    def exportar_txt(self, ruta_archivo: str, tipo_reporte: str = 'inventario') -> None:
        """Exporta reporte a archivo TXT"""
        try:
            if tipo_reporte == 'inventario':
                reporte = ReporteInventario(self.productos_activos)
                contenido = reporte.generar()
            elif tipo_reporte == 'stock_bajo':
                reporte = ReporteStockBajo(self.productos_activos)
                contenido = reporte.generar()
            elif tipo_reporte == 'historial':
                historial = self.obtener_historial(100)  # Últimos 100 movimientos
                contenido = "=" * 80 + "\n"
                contenido += "TECHNOVA - HISTORIAL DE MOVIMIENTOS".center(80) + "\n"
                contenido += "=" * 80 + "\n\n"
                
                if not historial:
                    contenido += "No hay movimientos registrados"
                else:
                    for mov in reversed(historial):
                        contenido += str(mov) + "\n"
                
                contenido += "\n" + "=" * 80
            else:
                contenido = f"Reporte generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                for producto in self.productos_activos:
                    contenido += f"{producto.codigo} | {producto.nombre} | S/. {producto.precio:.2f} | Stock: {producto.stock}\n"
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
                
        except Exception as e:
            raise Exception(f"Error al exportar TXT: {str(e)}")
    
    def exportar_json(self, ruta_archivo: str) -> None:
        """Exporta todos los datos a JSON"""
        try:
            datos = {
                'productos': [p.to_dict() for p in self._productos],
                'movimientos': [m.to_dict() for m in self._historial_movimientos],
                'fecha_exportacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'empresa': 'TechNova Solutions S.A.'
            }
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Error al exportar JSON: {str(e)}")
    
    def importar_json(self, ruta_archivo: str) -> tuple[int, int]:
        """Importa datos desde JSON"""
        productos_importados = 0
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            # Importar productos
            if 'productos' in datos:
                for producto_data in datos['productos']:
                    try:
                        producto = Producto.from_dict(producto_data)
                        # Verificar si ya existe
                        if not self._buscar_producto_por_codigo(producto.codigo):
                            self._productos.append(producto)
                            productos_importados += 1
                    except Exception as e:
                        print(f"Error al importar producto: {producto_data} - Error: {e}")
                        continue
            
            # Importar movimientos (opcional)
            if 'movimientos' in datos:
                for mov_data in datos['movimientos']:
                    try:
                        movimiento = MovimientoInventario(
                            producto_codigo=mov_data['producto_codigo'],
                            tipo=TipoMovimiento(mov_data['tipo']),
                            cantidad=int(mov_data['cantidad'])
                        )
                        # Asignar fecha si existe
                        if 'fecha' in mov_data:
                            movimiento.fecha = datetime.strptime(mov_data['fecha'], '%Y-%m-%d %H:%M:%S')
                        self._historial_movimientos.append(movimiento)
                    except Exception as e:
                        print(f"Error al importar movimiento: {mov_data} - Error: {e}")
                        continue
                        
        except FileNotFoundError:
            raise Exception(f"Archivo no encontrado: {ruta_archivo}")
        except json.JSONDecodeError:
            raise Exception("Error: El archivo JSON no tiene un formato válido")
        except Exception as e:
            raise Exception(f"Error al importar JSON: {str(e)}")
        
        return productos_importados, 0

# -------------------------------
# Interfaz Gráfica con Tkinter
# -------------------------------
class SistemaInventarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TechNova - Sistema de Gestión de Inventario")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        self.empresa_nombre = "TechNova Solutions S.A."
        self.inventario = Inventario()
        self._cargar_datos_iniciales()
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.crear_interfaz()
        self.actualizar_tabla()
    
    def _cargar_datos_iniciales(self):
        productos_iniciales = [
            Producto("TECH-LAP001", "TechNova Laptop Pro", 4200.00, 12, 3),
            Producto("TECH-MOU001", "TechNova Mouse Wireless", 120.00, 25, 5),
            Producto("TECH-TEC001", "TechNova Mechanical Keyboard", 350.00, 15, 5),
            Producto("TECH-MON001", "TechNova Monitor 27\" 4K", 1800.00, 8, 3),
            Producto("TECH-HEA001", "TechNova Gaming Headset", 450.00, 20, 8),
        ]
        
        for producto in productos_iniciales:
            self.inventario.registrar_producto(producto)
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encabezado con logo y nombre de empresa
        header_frame = tk.Frame(main_frame, bg="#2c3e50")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Logo/Icono y nombre de empresa
        tk.Label(header_frame, text="⚡", font=("Arial", 24), bg="#2c3e50", fg="#3498db").pack(side=tk.LEFT, padx=(20, 10), pady=10)
        
        empresa_info = tk.Frame(header_frame, bg="#2c3e50")
        empresa_info.pack(side=tk.LEFT, pady=10)
        
        tk.Label(empresa_info, text="TECHNOVA SOLUTIONS", 
                font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(anchor="w")
        tk.Label(empresa_info, text="Sistema de Gestión de Inventario", 
                font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        
        # Frame de botones principales
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botones principales
        btn_style = {"font": ("Arial", 10, "bold"), "width": 16, "height": 2}
        
        tk.Button(btn_frame, text="➕ Agregar Producto", bg="#27ae60", fg="white",
                 command=self.ventana_agregar_producto, **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="📥 Entrada Stock", bg="#3498db", fg="white",
                 command=self.ventana_entrada_stock, **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="📤 Salida Stock", bg="#e74c3c", fg="white",
                 command=self.ventana_salida_stock, **btn_style).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="📊 Reportes", bg="#9b59b6", fg="white",
                 command=self.ventana_reportes, **btn_style).pack(side=tk.LEFT, padx=2)
        
        # Frame de botones de exportación/importación
        export_frame = tk.Frame(main_frame, bg="#f0f0f0")
        export_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(export_frame, text="Importar/Exportar:", 
                font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(export_frame, text="📤 Exportar CSV", bg="#16a085", fg="white",
                 font=("Arial", 9, "bold"), width=12, command=self.exportar_csv).pack(side=tk.LEFT, padx=2)
        
        tk.Button(export_frame, text="📥 Importar CSV", bg="#2980b9", fg="white",
                 font=("Arial", 9, "bold"), width=12, command=self.importar_csv).pack(side=tk.LEFT, padx=2)
        
        tk.Button(export_frame, text="📄 Exportar TXT", bg="#8e44ad", fg="white",
                 font=("Arial", 9, "bold"), width=12, command=self.exportar_txt).pack(side=tk.LEFT, padx=2)
        
        tk.Button(export_frame, text="🔄 Actualizar", bg="#f39c12", fg="white",
                 font=("Arial", 9, "bold"), width=12, command=self.actualizar_tabla).pack(side=tk.LEFT, padx=2)
        
        # Frame de tabla con título
        tabla_container = tk.Frame(main_frame, bg="#f0f0f0")
        tabla_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Título de la tabla
        tk.Label(tabla_container, text="📦 INVENTARIO DE PRODUCTOS TECHNOBA", 
                font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(0, 5))
        
        # Tabla de productos
        tabla_frame = tk.Frame(tabla_container, bg="white", relief=tk.SUNKEN, borderwidth=1)
        tabla_frame.pack(fill=tk.BOTH, expand=True)
        
        columnas = ("Código", "Nombre", "Precio", "Stock", "Stock Mín", "Estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        self.tabla.heading("Código", text="Código")
        self.tabla.heading("Nombre", text="Nombre del Producto")
        self.tabla.heading("Precio", text="Precio (S/.)")
        self.tabla.heading("Stock", text="Stock Actual")
        self.tabla.heading("Stock Mín", text="Stock Mínimo")
        self.tabla.heading("Estado", text="Estado")
        
        self.tabla.column("Código", width=120)
        self.tabla.column("Nombre", width=350)
        self.tabla.column("Precio", width=120)
        self.tabla.column("Stock", width=120)
        self.tabla.column("Stock Mín", width=120)
        self.tabla.column("Estado", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame de información
        info_frame = tk.Frame(main_frame, bg="#2c3e50", relief=tk.FLAT, borderwidth=0)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.lbl_total = tk.Label(info_frame, text="Total productos: 0", 
                                 font=("Arial", 11, "bold"), bg="#2c3e50", fg="white")
        self.lbl_total.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.lbl_stock_bajo = tk.Label(info_frame, text="Stock bajo: 0", 
                                      font=("Arial", 11, "bold"), bg="#2c3e50", fg="#ff6b6b")
        self.lbl_stock_bajo.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Pie de página
        footer_frame = tk.Frame(main_frame, bg="#34495e", height=30)
        footer_frame.pack(fill=tk.X, pady=(5, 0))
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text=f"© 2024 {self.empresa_nombre} - Todos los derechos reservados", 
                font=("Arial", 9), bg="#34495e", fg="#bdc3c7").pack(pady=5)
    
    def exportar_csv(self):
        """Exporta el inventario a archivo CSV"""
        try:
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
                title="Exportar inventario a CSV",
                initialfile=f"inventario_technova_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
            if ruta_archivo:
                self.inventario.exportar_csv(ruta_archivo)
                messagebox.showinfo("TechNova - Exportación Exitosa", 
                    f"✅ Inventario exportado correctamente\n\n"
                    f"Archivo: {os.path.basename(ruta_archivo)}\n"
                    f"Ubicación: {os.path.dirname(ruta_archivo)}\n"
                    f"Productos exportados: {len(self.inventario.productos)}")
                
        except Exception as e:
            messagebox.showerror("TechNova - Error de Exportación", str(e))
    
    def importar_csv(self):
        """Importa productos desde archivo CSV"""
        try:
            ruta_archivo = filedialog.askopenfilename(
                filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx;*.xls"), ("Todos los archivos", "*.*")],
                title="Importar productos desde CSV"
            )
            
            if not ruta_archivo:
                return
            
            # Ventana de opciones de importación
            ventana_opciones = tk.Toplevel(self.root)
            ventana_opciones.title("Opciones de Importación")
            ventana_opciones.geometry("400x250")
            ventana_opciones.configure(bg="#f0f0f0")
            
            tk.Label(ventana_opciones, text="Seleccionar modo de importación", 
                    font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
            
            modo_var = tk.StringVar(value="agregar")
            
            tk.Radiobutton(ventana_opciones, text="Agregar nuevos productos (omitir duplicados)", 
                          variable=modo_var, value="agregar", bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
            
            tk.Radiobutton(ventana_opciones, text="Actualizar productos existentes", 
                          variable=modo_var, value="actualizar", bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
            
            tk.Radiobutton(ventana_opciones, text="Reemplazar inventario completo", 
                          variable=modo_var, value="reemplazar", bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
            
            def ejecutar_importacion():
                try:
                    productos_importados, productos_actualizados = self.inventario.importar_csv(
                        ruta_archivo, modo_var.get())
                    
                    ventana_opciones.destroy()
                    
                    mensaje = f"✅ Importación completada\n\n"
                    if productos_importados > 0:
                        mensaje += f"Nuevos productos: {productos_importados}\n"
                    if productos_actualizados > 0:
                        mensaje += f"Productos actualizados: {productos_actualizados}\n"
                    
                    messagebox.showinfo("TechNova - Importación Exitosa", mensaje)
                    self.actualizar_tabla()
                    
                except Exception as e:
                    ventana_opciones.destroy()
                    messagebox.showerror("TechNova - Error de Importación", str(e))
            
            tk.Button(ventana_opciones, text="✓ Importar", bg="#27ae60", fg="white",
                     font=("Arial", 10, "bold"), command=ejecutar_importacion).pack(pady=20)
            
            tk.Button(ventana_opciones, text="✗ Cancelar", bg="#95a5a6", fg="white",
                     font=("Arial", 10), command=ventana_opciones.destroy).pack()
            
        except Exception as e:
            messagebox.showerror("TechNova - Error de Importación", str(e))
    
    def exportar_txt(self):
        """Exporta reportes a archivo TXT"""
        try:
            # Ventana de selección de tipo de reporte
            ventana_tipo = tk.Toplevel(self.root)
            ventana_tipo.title("Exportar a TXT")
            ventana_tipo.geometry("400x300")
            ventana_tipo.configure(bg="#f0f0f0")
            
            tk.Label(ventana_tipo, text="Seleccionar tipo de reporte", 
                    font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
            
            tipo_var = tk.StringVar(value="inventario")
            
            opciones = [
                ("📋 Reporte de Inventario Completo", "inventario"),
                ("⚠️ Reporte de Stock Bajo", "stock_bajo"),
                ("📜 Historial de Movimientos", "historial"),
                ("📄 Listado Simple", "simple")
            ]
            
            for texto, valor in opciones:
                tk.Radiobutton(ventana_tipo, text=texto, variable=tipo_var, 
                              value=valor, bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
            
            def ejecutar_exportacion():
                try:
                    nombre_archivo = f"reporte_technova_{tipo_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                    
                    ruta_archivo = filedialog.asksaveasfilename(
                        defaultextension=".txt",
                        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                        title="Exportar reporte a TXT",
                        initialfile=nombre_archivo
                    )
                    
                    if ruta_archivo:
                        self.inventario.exportar_txt(ruta_archivo, tipo_var.get())
                        messagebox.showinfo("TechNova - Exportación Exitosa", 
                            f"✅ Reporte exportado correctamente\n\n"
                            f"Archivo: {os.path.basename(ruta_archivo)}\n"
                            f"Tipo: {tipo_var.get()}\n"
                            f"Ubicación: {os.path.dirname(ruta_archivo)}")
                        
                    ventana_tipo.destroy()
                    
                except Exception as e:
                    messagebox.showerror("TechNova - Error de Exportación", str(e))
            
            tk.Button(ventana_tipo, text="✓ Exportar", bg="#27ae60", fg="white",
                     font=("Arial", 10, "bold"), command=ejecutar_exportacion).pack(pady=20)
            
            tk.Button(ventana_tipo, text="✗ Cancelar", bg="#95a5a6", fg="white",
                     font=("Arial", 10), command=ventana_tipo.destroy).pack()
            
        except Exception as e:
            messagebox.showerror("TechNova - Error", str(e))
    
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Llenar tabla
        productos = self.inventario.productos_activos
        stock_bajo_count = 0
        
        for producto in productos:
            estado = "✓ Normal"
            tag = ""
            
            if producto.tiene_stock_bajo():
                estado = "⚠️ Stock Bajo"
                tag = "bajo"
                stock_bajo_count += 1
            
            self.tabla.insert("", tk.END, values=(
                producto.codigo,
                producto.nombre,
                f"S/. {producto.precio:.2f}",
                producto.stock,
                producto.stock_minimo,
                estado
            ), tags=(tag,))
        
        # Colorear filas con stock bajo
        self.tabla.tag_configure("bajo", background="#ffcccc")
        
        # Actualizar información
        self.lbl_total.config(text=f"Total productos: {len(productos)}")
        self.lbl_stock_bajo.config(text=f"Productos con stock bajo: {stock_bajo_count}")
    
    def ventana_agregar_producto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("TechNova - Agregar Nuevo Producto")
        ventana.geometry("450x400")
        ventana.configure(bg="#f0f0f0")
        
        # Encabezado
        header = tk.Frame(ventana, bg="#3498db")
        header.pack(fill=tk.X)
        
        tk.Label(header, text="➕ Agregar Nuevo Producto", 
                font=("Arial", 14, "bold"), bg="#3498db", fg="white").pack(pady=10)
        
        tk.Label(header, text="TechNova Solutions", 
                font=("Arial", 10), bg="#3498db", fg="#ecf0f1").pack(pady=(0, 10))
        
        frame = tk.Frame(ventana, bg="#f0f0f0")
        frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)
        
        # Campos
        tk.Label(frame, text="Código del Producto:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        entry_codigo = tk.Entry(frame, width=35, font=("Arial", 10))
        entry_codigo.grid(row=0, column=1, pady=8)
        tk.Label(frame, text="(Ej: TECH-XXX001)", bg="#f0f0f0", font=("Arial", 8), fg="#7f8c8d").grid(row=0, column=2, sticky="w", padx=5)
        
        tk.Label(frame, text="Nombre del Producto:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        entry_nombre = tk.Entry(frame, width=35, font=("Arial", 10))
        entry_nombre.grid(row=1, column=1, pady=8)
        
        tk.Label(frame, text="Precio (S/.):*", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
        entry_precio = tk.Entry(frame, width=35, font=("Arial", 10))
        entry_precio.grid(row=2, column=1, pady=8)
        
        tk.Label(frame, text="Stock Inicial:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
        entry_stock = tk.Entry(frame, width=35, font=("Arial", 10))
        entry_stock.grid(row=3, column=1, pady=8)
        
        tk.Label(frame, text="Stock Mínimo:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=8)
        entry_stock_min = tk.Entry(frame, width=35, font=("Arial", 10))
        entry_stock_min.insert(0, "5")
        entry_stock_min.grid(row=4, column=1, pady=8)
        
        def guardar():
            try:
                codigo = entry_codigo.get().strip()
                nombre = entry_nombre.get().strip()
                precio = float(entry_precio.get())
                stock = int(entry_stock.get())
                stock_min = int(entry_stock_min.get())
                
                producto = Producto(codigo, nombre, precio, stock, stock_min)
                self.inventario.registrar_producto(producto)
                
                messagebox.showinfo("TechNova - Éxito", 
                    f"✅ Producto agregado correctamente\n\n"
                    f"Nombre: {nombre}\n"
                    f"Código: {codigo}\n"
                    f"Precio: S/. {precio:.2f}\n"
                    f"Stock inicial: {stock} unidades")
                
                self.actualizar_tabla()
                ventana.destroy()
                
            except ValueError as e:
                messagebox.showerror("TechNova - Error", str(e))
        
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        tk.Button(btn_frame, text="✗ Cancelar", bg="#95a5a6", fg="white",
                 font=("Arial", 10, "bold"), width=12, command=ventana.destroy).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="✓ Guardar Producto", bg="#27ae60", fg="white",
                 font=("Arial", 10, "bold"), width=15, command=guardar).pack(side=tk.LEFT, padx=10)
    
    def ventana_entrada_stock(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("TechNova - Entrada de Stock")
        ventana.geometry("450x300")
        ventana.configure(bg="#f0f0f0")
        
        # Encabezado
        header = tk.Frame(ventana, bg="#3498db")
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📥 Entrada de Stock", 
                font=("Arial", 14, "bold"), bg="#3498db", fg="white").pack(pady=10)
        
        tk.Label(header, text="Registro de ingreso de productos", 
                font=("Arial", 10), bg="#3498db", fg="#ecf0f1").pack(pady=(0, 10))
        
        frame = tk.Frame(ventana, bg="#f0f0f0")
        frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Código del Producto:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=10)
        entry_codigo = tk.Entry(frame, width=30, font=("Arial", 10))
        entry_codigo.grid(row=0, column=1, pady=10)
        
        tk.Label(frame, text="Cantidad a Ingresar:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=10)
        entry_cantidad = tk.Entry(frame, width=30, font=("Arial", 10))
        entry_cantidad.grid(row=1, column=1, pady=10)
        
        def registrar():
            try:
                codigo = entry_codigo.get().strip()
                cantidad = int(entry_cantidad.get())
                
                producto = self.inventario.buscar_producto(codigo)
                stock_anterior = producto.stock
                self.inventario.entrada_stock(codigo, cantidad)
                
                messagebox.showinfo("TechNova - Éxito", 
                    f"✅ Entrada registrada exitosamente\n\n"
                    f"Producto: {producto.nombre}\n"
                    f"Código: {producto.codigo}\n"
                    f"Cantidad ingresada: {cantidad} unidades\n"
                    f"Stock anterior: {stock_anterior}\n"
                    f"Nuevo stock total: {producto.stock}")
                
                self.actualizar_tabla()
                ventana.destroy()
                
            except ValueError as e:
                messagebox.showerror("TechNova - Error", str(e))
        
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="✗ Cancelar", bg="#95a5a6", fg="white",
                 font=("Arial", 10, "bold"), width=12, command=ventana.destroy).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="✓ Registrar Entrada", bg="#3498db", fg="white",
                 font=("Arial", 10, "bold"), width=15, command=registrar).pack(side=tk.LEFT, padx=10)
    
    def ventana_salida_stock(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("TechNova - Salida de Stock")
        ventana.geometry("450x300")
        ventana.configure(bg="#f0f0f0")
        
        # Encabezado
        header = tk.Frame(ventana, bg="#e74c3c")
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📤 Salida de Stock", 
                font=("Arial", 14, "bold"), bg="#e74c3c", fg="white").pack(pady=10)
        
        tk.Label(header, text="Registro de retiro de productos", 
                font=("Arial", 10), bg="#e74c3c", fg="#ecf0f1").pack(pady=(0, 10))
        
        frame = tk.Frame(ventana, bg="#f0f0f0")
        frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Código del Producto:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=10)
        entry_codigo = tk.Entry(frame, width=30, font=("Arial", 10))
        entry_codigo.grid(row=0, column=1, pady=10)
        
        tk.Label(frame, text="Cantidad a Retirar:*", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=10)
        entry_cantidad = tk.Entry(frame, width=30, font=("Arial", 10))
        entry_cantidad.grid(row=1, column=1, pady=10)
        
        def registrar():
            try:
                codigo = entry_codigo.get().strip()
                cantidad = int(entry_cantidad.get())
                
                producto = self.inventario.buscar_producto(codigo)
                stock_anterior = producto.stock
                self.inventario.salida_stock(codigo, cantidad)
                
                mensaje = f"✅ Salida registrada exitosamente\n\n" \
                         f"Producto: {producto.nombre}\n" \
                         f"Código: {producto.codigo}\n" \
                         f"Cantidad retirada: {cantidad} unidades\n" \
                         f"Stock anterior: {stock_anterior}\n" \
                         f"Stock restante: {producto.stock}"
                
                if producto.tiene_stock_bajo():
                    mensaje += f"\n\n⚠️ ALERTA: Stock bajo ({producto.stock} unidades)"
                    mensaje += f"\nMínimo requerido: {producto.stock_minimo}"
                
                messagebox.showinfo("TechNova - Éxito", mensaje)
                self.actualizar_tabla()
                ventana.destroy()
                
            except ValueError as e:
                messagebox.showerror("TechNova - Error", str(e))
        
        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="✗ Cancelar", bg="#95a5a6", fg="white",
                 font=("Arial", 10, "bold"), width=12, command=ventana.destroy).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="✓ Registrar Salida", bg="#e74c3c", fg="white",
                 font=("Arial", 10, "bold"), width=15, command=registrar).pack(side=tk.LEFT, padx=10)
    
    def ventana_reportes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("TechNova - Reportes del Sistema")
        ventana.geometry("900x700")
        ventana.configure(bg="#f0f0f0")
        
        # Encabezado
        header = tk.Frame(ventana, bg="#9b59b6")
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📊 Reportes del Sistema", 
                font=("Arial", 14, "bold"), bg="#9b59b6", fg="white").pack(pady=10)
        
        tk.Label(header, text="TechNova Solutions - Análisis de Inventario", 
                font=("Arial", 10), bg="#9b59b6", fg="#ecf0f1").pack(pady=(0, 10))
        
        btn_frame = tk.Frame(ventana, bg="#f0f0f0")
        btn_frame.pack(pady=15)
        
        # Área de texto para mostrar reportes
        text_frame = tk.Frame(ventana, bg="#f0f0f0")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        tk.Label(text_frame, text="Vista previa del reporte:", 
                font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        
        text_area = scrolledtext.ScrolledText(text_frame, width=100, height=28, 
                                               font=("Courier", 9), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        def mostrar_inventario():
            reporte = ReporteInventario(self.inventario.productos_activos)
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, reporte.generar())
        
        def mostrar_stock_bajo():
            reporte = ReporteStockBajo(self.inventario.productos_activos)
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, reporte.generar())
        
        def mostrar_historial():
            historial = self.inventario.obtener_historial(20)
            text_area.delete(1.0, tk.END)
            
            texto = "=" * 80 + "\n"
            texto += "TECHNOVA - HISTORIAL DE MOVIMIENTOS (últimos 20)".center(80) + "\n"
            texto += "=" * 80 + "\n\n"
            
            if not historial:
                texto += "No hay movimientos registrados"
            else:
                for mov in reversed(historial):
                    texto += str(mov) + "\n"
            
            texto += "\n" + "=" * 80
            text_area.insert(1.0, texto)
        
        def exportar_reporte():
            contenido = text_area.get(1.0, tk.END)
            if not contenido.strip():
                messagebox.showwarning("TechNova - Advertencia", "No hay contenido para exportar")
                return
            
            try:
                ruta_archivo = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                    title="Guardar reporte",
                    initialfile=f"reporte_technova_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                )
                
                if ruta_archivo:
                    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                        archivo.write(contenido)
                    
                    messagebox.showinfo("TechNova - Éxito", 
                        f"✅ Reporte guardado correctamente\n\n"
                        f"Archivo: {os.path.basename(ruta_archivo)}")
                        
            except Exception as e:
                messagebox.showerror("TechNova - Error", str(e))
        
        # Botones de reportes
        btn_reportes_style = {"font": ("Arial", 10, "bold"), "width": 20, "height": 1}
        
        tk.Button(btn_frame, text="📋 Inventario Completo", bg="#3498db", fg="white",
                 command=mostrar_inventario, **btn_reportes_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="⚠️ Stock Bajo", bg="#e74c3c", fg="white",
                 command=mostrar_stock_bajo, **btn_reportes_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📜 Historial Movimientos", bg="#9b59b6", fg="white",
                 command=mostrar_historial, **btn_reportes_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="💾 Guardar Reporte", bg="#27ae60", fg="white",
                 command=exportar_reporte, **btn_reportes_style).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Limpiar Vista", bg="#95a5a6", fg="white",
                 command=lambda: text_area.delete(1.0, tk.END), **btn_reportes_style).pack(side=tk.LEFT, padx=5)

# -------------------------------
# Función principal
# -------------------------------
def main():
    root = tk.Tk()
    app = SistemaInventarioGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
