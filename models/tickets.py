from datetime import datetime
from typing import List, Dict

class Ticket:
    def __init__(self, codigo_ticket: str, servicio: str, codigo_cliente: str,
                    cliente: str, productos: List[Dict[str, str | int]], total: int,
                    fecha: datetime):
        
        # Atributos
        self.codigo_ticket = codigo_ticket
        self.servicio = servicio
        self.codigo_cliente = codigo_cliente
        self.cliente = cliente
        self.productos = productos  
        self.total = total
        self.fecha = fecha

