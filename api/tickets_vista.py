from services.tickets_service import TicketsService
from config.exceptions import *

class TicketsVista:
    def __init__(self, service: TicketsService):
        self.service = service

    def mostrar_menu(self):
        print("\n" + "="*50)
        print("           GESTIÓN DE TICKETS")
        print("="*50)
        print("1. Crear ticket")
        print("2. Listar todos")
        print("3. Ver por cliente")
        print("4. Actualizar ticket")
        print("5. Eliminar ticket")
        print("0. Volver")
        return input("\nSeleccione: ").strip()

    def crear_ticket(self):
        print("\n--- CREAR TICKET ---")
        servicio = input("Servicio: ").strip()
        codigo_cliente = input("Código cliente: ").strip()
        print("Productos (ingrese uno por uno, 'fin' para terminar):")
        productos = []
        while True:
            codigo = input("  Código producto (o 'fin'): ").strip()
            if codigo.lower() == 'fin':
                break
            try:
                cantidad = int(input("  Cantidad: ").strip())
                productos.append({"codigo": codigo, "cantidad": cantidad})
            except ValueError:
                print("Cantidad inválida.")
        try:
            ticket = self.service.crear(servicio, codigo_cliente, productos)
            print(f"Ticket creado: {ticket.codigo_ticket} | Total: ${ticket.total}")
        except (ValidacionError, NotFoundError, RepositoryError) as e:
            print(f"Error: {e}")

    def listar_todos(self):
        tickets = self.service.listar_todos()
        if not tickets:
            print("\nNo hay tickets.")
            return
        print(f"\n{len(tickets)} ticket(s):")
        for t in tickets:
            print(f"  {t.codigo_ticket} | {t.cliente} | ${t.total} | {t.fecha.strftime('%Y-%m-%d')}")

    def ver_por_cliente(self):
        codigo = input("\nCódigo cliente: ").strip()
        tickets = self.service.obtener_por_cliente(codigo)
        if not tickets:
            print("No hay tickets para este cliente.")
            return
        print(f"\n{len(tickets)} ticket(s):")
        for t in tickets:
            print(f"  {t.codigo_ticket} | {t.servicio} | ${t.total}")

    def actualizar_ticket(self):
        codigo = input("\nCódigo ticket: ").strip()
        try:
            ticket = self.service.obtener_por_codigo(codigo)
            servicio = input(f"Servicio [{ticket.servicio}]: ").strip() or ticket.servicio
            print("¿Actualizar productos? (s/N): ")
            if input().strip().lower() == 's':
                productos = []
                print("Productos nuevos (uno por uno, 'fin' para terminar):")
                while True:
                    cod = input("  Código (o 'fin'): ").strip()
                    if cod.lower() == 'fin':
                        break
                    cant = int(input("  Cantidad: ").strip())
                    productos.append({"codigo": cod, "cantidad": cant})
            else:
                productos = None
            self.service.actualizar(codigo, servicio, productos) # type: ignore
            print("Ticket actualizado.")
        except (NotFoundError, ValidacionError, RepositoryError) as e:
            print(f"Error: {e}")

    def eliminar_ticket(self):
        codigo = input("\nCódigo: ").strip()
        if input(f"¿Eliminar {codigo}? (s/N): ").strip().lower() != 's':
            return
        try:
            self.service.eliminar(codigo)
            print("Ticket eliminado.")
        except (NotFoundError, RepositoryError) as e:
            print(f"Error: {e}")