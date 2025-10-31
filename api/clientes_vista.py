from services.clientes_service import ClientesService
from config.exceptions import *

class ClientesVista:
    def __init__(self, service: ClientesService):
        self.service = service

    def mostrar_menu(self):
        print("\n" + "="*50)
        print("           GESTIÓN DE CLIENTES")
        print("="*50)
        print("1. Crear cliente")
        print("2. Listar todos")
        print("3. Buscar por nombre")
        print("4. Clientes por vencimiento")
        print("5. Actualizar cliente")
        print("6. Eliminar cliente")
        print("0. Volver")
        return input("\nSeleccione: ").strip()

    def crear_cliente(self):
        print("\n--- CREAR CLIENTE ---")
        nombre_empresa = input("Empresa: ").strip()
        nombre_encargado = input("Encargado: ").strip()
        direccion = input("Dirección: ").strip()
        celular = input("Celular: ").strip()
        mes = input("Mes vencimiento: ").strip()
        try:
            cliente = self.service.crear(nombre_empresa, nombre_encargado, direccion, celular, mes)
            print(f"Cliente creado: {cliente.codigo}")
        except (ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")

    def listar_todos(self):
        clientes = self.service.listar_todos()
        if not clientes:
            print("\nNo hay clientes.")
            return
        print(f"\n{len(clientes)} cliente(s):")
        for c in clientes:
            print(f"  {c.codigo} | {c.nombre_empresa} | {c.celular} | {c.mes_vencimiento}")

    def buscar_por_nombre(self):
        texto = input("\nBuscar: ").strip()
        resultados = self.service.buscar_por_nombre(texto)
        if not resultados:
            print("No encontrado.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for c in resultados:
            print(f"  {c.codigo} | {c.nombre_empresa}")

    def clientes_por_vencimiento(self):
        mes = input("\nMes: ").strip()
        clientes = self.service.obtener_por_vencimiento(mes)
        if not clientes:
            print("Ningún cliente vence ese mes.")
            return
        print(f"\n{len(clientes)} cliente(s) vencen en {mes}:")
        for c in clientes:
            print(f"  {c.codigo} | {c.nombre_empresa}")

    def actualizar_cliente(self):
        codigo = input("\nCódigo del cliente: ").strip()
        try:
            cliente = self.service.obtener_por_codigo(codigo)
            print(f"Actualizando: {cliente.nombre_empresa}")
            nombre_empresa = input(f"Empresa [{cliente.nombre_empresa}]: ").strip() or cliente.nombre_empresa
            nombre_encargado = input(f"Encargado [{cliente.nombre_encargado}]: ").strip() or cliente.nombre_encargado
            direccion = input(f"Dirección [{cliente.direccion}]: ").strip() or cliente.direccion
            celular = input(f"Celular [{cliente.celular}]: ").strip() or cliente.celular
            mes = input(f"Mes [{cliente.mes_vencimiento}]: ").strip() or cliente.mes_vencimiento
            self.service.actualizar(codigo, nombre_empresa, nombre_encargado, direccion, celular, mes)
            print("Cliente actualizado.")
        except (NotFoundError, ValidacionError, ConflictError, RepositoryError) as e:
            print(f"Error: {e}")

    def eliminar_cliente(self):
        codigo = input("\nCódigo a eliminar: ").strip()
        if input(f"¿Eliminar {codigo}? (s/N): ").strip().lower() != 's':
            return
        try:
            self.service.eliminar(codigo)
            print("Cliente eliminado.")
        except (NotFoundError, RepositoryError) as e:
            print(f"Error: {e}")