from services.productos_service import ProductosService
from config.exceptions import *

class ProductosVista:
    def __init__(self, service: ProductosService):
        self.service = service

    def mostrar_menu(self):
        print("\n" + "="*50)
        print("           GESTIÓN DE PRODUCTOS")
        print("="*50)
        print("1. Crear producto")
        print("2. Listar todos")
        print("3. Buscar por nombre")
        print("4. Buscar por precio")
        print("5. Actualizar producto")
        print("6. Eliminar producto")
        print("0. Volver")
        return input("\nSeleccione: ").strip()

    def crear_producto(self):
        print("\n--- CREAR PRODUCTO ---")
        nombre = input("Nombre: ").strip()
        precio = float(input("Precio: ").strip() or "0")
        try:
            prod = self.service.crear(nombre, precio)
            print(f"Producto creado: {prod.codigo}")
        except (ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")

    def listar_todos(self):
        productos = self.service.listar_todos()
        if not productos:
            print("\nNo hay productos.")
            return
        print(f"\n{len(productos)} producto(s):")
        for p in productos:
            print(f"  {p.codigo} | {p.nombre} | ${p.precio}")

    def buscar_por_nombre(self):
        texto = input("\nBuscar: ").strip()
        resultados = self.service.buscar_por_nombre(texto)
        if not resultados:
            print("No encontrado.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for p in resultados:
            print(f"  {p.codigo} | {p.nombre}")

    def buscar_por_precio(self):
        min_p = float(input("Precio mínimo: ").strip() or "0")
        max_p = input("Precio máximo (dejar vacío para sin límite): ").strip()
        max_p = float(max_p) if max_p else None
        resultados = self.service.buscar_por_precio(min_p, max_p) # type: ignore
        if not resultados:
            print("No encontrado.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for p in resultados:
            print(f"  {p.codigo} | {p.nombre} | ${p.precio}")

    def actualizar_producto(self):
        codigo = input("\nCódigo: ").strip()
        try:
            prod = self.service.obtener_por_codigo(codigo)
            nombre = input(f"Nombre [{prod.nombre}]: ").strip() or prod.nombre
            precio = float(input(f"Precio [{prod.precio}]: ").strip() or prod.precio)
            self.service.actualizar(codigo, nombre, precio)
            print("Producto actualizado.")
        except (NotFoundError, ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")

    def eliminar_producto(self):
        codigo = input("\nCódigo: ").strip()
        if input(f"¿Eliminar {codigo}? (s/N): ").strip().lower() != 's':
            return
        try:
            self.service.eliminar(codigo)
            print("Producto eliminado.")
        except (NotFoundError, RepositoryError) as e:
            print(f"Error: {e}")