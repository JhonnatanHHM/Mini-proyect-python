from typing import List, Optional
from models.productos import Producto
from models.tickets import Ticket

class Cliente:
    def __init__(self, codigo: str, nombre_empresa: str, nombre_encargado: str, 
                    direccion: str, celular: str, mes_vencimiento: str,
                    productos: Optional[List[Producto]] = None,
                    tickets: Optional[List[Ticket]] = None):
        
        # Atributos
        self.codigo = codigo
        self.nombre_empresa = nombre_empresa
        self.nombre_encargado = nombre_encargado
        self.direccion = direccion
        self.celular = celular
        self.mes_vencimiento = mes_vencimiento
        self.productos = productos if productos is not None else []
        self.tickets = tickets if tickets is not None else []


'''
    @classmethod # Método de clase para crear un libro no disponible, sobre la misma instancia
    def usuario_sin_contraseña(cls, nombre, , isbn):
        return cls(titulo, autor, isbn, disponible=False)
'''