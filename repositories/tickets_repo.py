import json
from datetime import datetime
from typing import List, Optional
from models.tickets import Ticket
import os


class TicketsRepo:
    def __init__(self, archivo="data/tickets.json") -> None:
        self.archivo = archivo
        self._crear_archivo_si_no_existe()

    def _crear_archivo_si_no_existe(self):
        """Crea el directorio 'data' y el archivo si no existen."""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def crear(self, ticket: Ticket):
        """
        Guarda un nuevo ticket en el archivo JSON.
        Genera un código único incremental.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_tickets = []

        # Generar código automático
        if lista_tickets:
            ultimo_codigo = max(
                int(t.get('codigo_ticket', 'TIC-0').replace("TIC-", "")) for t in lista_tickets
            )
            nuevo_codigo = ultimo_codigo + 1
        else:
            nuevo_codigo = 1

        # Serializar productos (que ya son dicts con str/int)
        productos_serializados = [
            {
                "codigo": p.get("codigo"),
                "nombre": p.get("nombre"),
                "precio": p.get("precio"),
                "cantidad": p.get("cantidad")
            } for p in ticket.productos
        ]

        datos_ticket = {
            "codigo_ticket": f"TIC-{nuevo_codigo}",
            "servicio": ticket.servicio,
            "codigo_cliente": ticket.codigo_cliente,
            "cliente": ticket.cliente,
            "productos": productos_serializados,
            "total": ticket.total,
            "fecha": ticket.fecha.isoformat() 
        }

        lista_tickets.append(datos_ticket)

        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_tickets, f, indent=4, ensure_ascii=False)

        # Actualizamos el código en el objeto original para consistencia
        ticket.codigo_ticket = datos_ticket["codigo_ticket"]

    def actualizar_por_codigo(self, ticket: Ticket, codigo_ticket: str) -> bool:
        """
        Actualiza un ticket existente por su código.
        Devuelve True si se actualizó, False si no se encontró.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        actualizado = False
        productos_serializados = [
            {
                "codigo": p.get("codigo"),
                "nombre": p.get("nombre"),
                "precio": p.get("precio"),
                "cantidad": p.get("cantidad")
            } for p in ticket.productos
        ]

        for t in lista_tickets:
            if t.get('codigo_ticket') == codigo_ticket:
                t.update({
                    "servicio": ticket.servicio,
                    "codigo_cliente": ticket.codigo_cliente,
                    "cliente": ticket.cliente,
                    "productos": productos_serializados,
                    "total": ticket.total,
                    "fecha": ticket.fecha.isoformat()
                })
                actualizado = True
                break

        if actualizado:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(lista_tickets, f, indent=4, ensure_ascii=False)

        return actualizado

    def cargar_por_codigo(self, codigo_ticket: str) -> Optional[Ticket]:
        """
        Carga un ticket por su código_ticket.
        Devuelve un objeto Ticket o None si no existe.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        for t in lista_tickets:
            if t.get('codigo_ticket') == codigo_ticket:
                return Ticket(
                    codigo_ticket=t['codigo_ticket'],
                    servicio=t['servicio'],
                    codigo_cliente=t['codigo_cliente'],
                    cliente=t['cliente'],
                    productos=t['productos'],
                    total=t['total'],
                    fecha=datetime.fromisoformat(t['fecha'])
                )
        return None
    
    def cargar_todos(self) -> List[Ticket]:
        """Devuelve todos los tickets."""
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        tickets = []
        for t in datos:
            tickets.append(
                Ticket(
                    codigo_ticket=t['codigo_ticket'],
                    servicio=t['servicio'],
                    codigo_cliente=t['codigo_cliente'],
                    cliente=t['cliente'],
                    productos=t['productos'],
                    total=t['total'],
                    fecha=datetime.fromisoformat(t['fecha'])
                )
            )
        return tickets

    def cargar_todos_por_cliente(self, codigo_cliente: str) -> List[Ticket]:
        """
        Devuelve todos los tickets asociados a un código de cliente.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        tickets_cliente = []
        for t in lista_tickets:
            if t.get('codigo_cliente') == codigo_cliente:
                tickets_cliente.append(
                    Ticket(
                        codigo_ticket=t['codigo_ticket'],
                        servicio=t['servicio'],
                        codigo_cliente=t['codigo_cliente'],
                        cliente=t['cliente'],
                        productos=t['productos'],
                        total=t['total'],
                        fecha=datetime.fromisoformat(t['fecha'])
                    )
                )
        return tickets_cliente

    def eliminar_por_codigo(self, codigo_ticket: str) -> bool:
        """
        Elimina un ticket por su código_ticket.
        Devuelve True si se eliminó, False si no se encontró.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_tickets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        original_len = len(lista_tickets)
        lista_tickets = [t for t in lista_tickets if t.get('codigo_ticket') != codigo_ticket]

        if len(lista_tickets) < original_len:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(lista_tickets, f, indent=4, ensure_ascii=False)
            return True
        return False