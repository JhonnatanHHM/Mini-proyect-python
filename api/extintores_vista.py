from services.extintores_service import ExtintoresService
from config.exceptions import *

class ExtintoresVista:
    def __init__(self, service: ExtintoresService):
        self.service = service

    def mostrar_menu(self):
        print("\n" + "="*50)
        print("           GESTIÓN DE EXTINTORES")
        print("="*50)
        print("1. Crear extintor")
        print("2. Listar todos")
        print("3. Buscar por tipo")
        print("4. Buscar por capacidad")
        print("5. Actualizar extintor")
        print("6. Eliminar extintor")
        print("0. Volver")
        return input("\nSeleccione: ").strip()

    def crear_extintor(self):
        print("\n--- CREAR EXTINTOR ---")
        nombre = input("Nombre: ").strip()
        precio = float(input("Precio: ").strip() or "0")
        tipo = input("Tipo: ").strip()
        capacidad = float(input("Capacidad (lb): ").strip() or "0")
        try:
            ext = self.service.crear(nombre, precio, tipo, capacidad)
            print(f"Extintor creado: {ext.codigo}")
        except (ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")
        input("\nPresione Enter para volver al inicio...")
        ExtintoresVista.mostrar_menu(self)

    def listar_todos(self):
        extintores = self.service.listar_todos()
        if not extintores:
            print("\nNo hay extintores.")
            return
        print(f"\n{len(extintores)} extintor(es):")
        for e in extintores:
            print(f"  {e.codigo} | {e.nombre} | {e.tipo} | {e.capacidad}kg | ${e.precio}")

    def buscar_por_tipo(self):
        tipo = input("\nTipo: ").strip()
        resultados = self.service.buscar_por_tipo(tipo)
        if not resultados:
            print("No encontrado.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for e in resultados:
            print(f"  {e.codigo} | {e.nombre} | {e.capacidad}kg")

    def buscar_por_capacidad(self):
        min_c = float(input("Capacidad mínima: ").strip() or "0")
        max_c = input("Capacidad máxima (vacío = sin límite): ").strip()
        max_c = float(max_c) if max_c else None
        resultados = self.service.buscar_por_rango_capacidad(min_c, max_c) # type: ignore
        if not resultados:
            print("No encontrado.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for e in resultados:
            print(f"  {e.codigo} | {e.nombre} | {e.capacidad}lb")

    def actualizar_extintor(self):
        codigo = input("\nCódigo: ").strip()
        try:
            ext = self.service.obtener_por_codigo(codigo)
            nombre = input(f"Nombre [{ext.nombre}]: ").strip() or ext.nombre
            precio = float(input(f"Precio [{ext.precio}]: ").strip() or ext.precio)
            tipo = input(f"Tipo [{ext.tipo}]: ").strip() or ext.tipo
            capacidad = float(input(f"Capacidad [{ext.capacidad}]: ").strip() or ext.capacidad)
            self.service.actualizar(codigo, nombre, precio, tipo, capacidad)
            print("Extintor actualizado.")
        except (NotFoundError, ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")

    def eliminar_extintor(self):
        codigo = input("\nCódigo: ").strip()
        if input(f"¿Eliminar {codigo}? (s/N): ").strip().lower() != 's':
            return
        try:
            self.service.eliminar(codigo)
            print("Extintor eliminado.")
        except (NotFoundError, RepositoryError) as e:
            print(f"Error: {e}")