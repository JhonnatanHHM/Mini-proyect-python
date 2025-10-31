from models.clientes import Cliente
import json
from typing import List
import os

class ClientesRepo:
    def __init__(self, cliente="data/clientes.json") -> None:
        self.cliente = cliente
        self._crear_archivo_si_no_existe()

    def _crear_archivo_si_no_existe(self):
        """Crea el directorio 'data' y el archivo si no existen."""
        os.makedirs(os.path.dirname(self.cliente), exist_ok=True)
        if not os.path.exists(self.cliente):
            with open(self.cliente, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def guardar_clientes(self, cliente):

        '''
        Verifica si el archivo JSON existe o sino lo crea, y
        guarda un nuevo cliente en el archivo JSON,
        agregándolo a la lista existente de clientes.
        '''

        try:
            with open(self.cliente, 'r', encoding='utf-8') as f:
                lista_clientes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_clientes = []

        # consultar los codigos en lista_clientes y crear un codigo nuevo sin copiar un existente
        codigo_generado = None

        if lista_clientes:
            # Obtener el máximo código existente
            ultimo_codigo = max(
                int(p.get('codigo', '0').replace("CLI-", "")) for p in lista_clientes
                )
            codigo_generado = ultimo_codigo + 1
        else:
            # Si no hay clientes, comenzamos desde 1
            codigo_generado = 1

        datos_cliente = {
            'codigo': f"CLI-{codigo_generado}",
            'nombre_empresa': cliente.nombre_empresa,
            'nombre_encargado': cliente.nombre_encargado,
            'direccion': cliente.direccion,
            'celular': cliente.celular,
            'mes_vencimiento': cliente.mes_vencimiento,
            'productos': [],
            'tickets': []
        }

        lista_clientes.append(datos_cliente)

        with open(self.cliente, 'w', encoding='utf-8') as f:
            json.dump(lista_clientes, f, indent=4, ensure_ascii=False)


    def actualizar_cliente(self, cliente, codigo):
        """
        Actualiza los datos de un cliente existente en el archivo JSON,
        buscando por su codigo. Devuelve True si se actualizó, False si no se encontró.
        """
        try:
            with open(self.cliente, 'r', encoding='utf-8') as f:
                lista_clientes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_clientes = []

        cliente_actualizado = False

        for u in lista_clientes:
            if u.get('codigo') == codigo:
                u['codigo'] = cliente.codigo
                u['nombre_empresa'] = cliente.nombre_empresa
                u['nombre_encargado'] = cliente.nombre_encargado
                u['direccion'] = cliente.direccion
                u['celular'] = cliente.celular
                u['mes_vencimiento'] = cliente.mes_vencimiento
                u['productos'] = [
                    producto.__dict__ for producto in getattr(cliente, 'productos', [])
                ]
                u['tickets'] = [
                    ticket.__dict__ for ticket in getattr(cliente, 'tickets', [])
                ]
                cliente_actualizado = True
                break

        with open(self.cliente, 'w', encoding='utf-8') as f:
            json.dump(lista_clientes, f, indent=4, ensure_ascii=False)

        return cliente_actualizado

    def cargar_por_codigo(self, codigo):

        '''
        Carga un cliente desde el archivo JSON buscando por su codigo.
        '''

        with open(self.cliente, 'r', encoding='utf-8') as f:
            lista_clientes = json.load(f)

        for u in lista_clientes:
            if u.get('codigo') == codigo:
                return Cliente(
                    codigo=u['codigo'],
                    nombre_empresa=u['nombre_empresa'],
                    nombre_encargado=u['nombre_encargado'],
                    direccion=u['direccion'],
                    celular=u['celular'],
                    mes_vencimiento=u['mes_vencimiento'],
                    productos=u.get('productos', []),
                    tickets=u.get('tickets', [])
                )
        return None
    
    def cargar_todos(self) -> List[Cliente]:
        """Devuelve todos los clientes. Si no hay archivo → []"""
        try:
            with open(self.cliente, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  

        clientes = []
        for c in datos:
            clientes.append(
                Cliente(
                    codigo=c['codigo'],
                    nombre_empresa=c['nombre_empresa'],
                    nombre_encargado=c['nombre_encargado'],
                    direccion=c['direccion'],
                    celular=c['celular'],
                    mes_vencimiento=c['mes_vencimiento'],
                    productos=c.get('productos', []),
                    tickets=c.get('tickets', [])
                )
            )
        return clientes
    
    def eliminar_cliente(self, codigo):

        '''
        Elimina un cliente del archivo JSON buscando por su codigo.
        '''

        with open(self.cliente, 'r', encoding='utf-8') as f:
            lista_clientes = json.load(f)

        lista_clientes = [u for u in lista_clientes if u.get('codigo') != codigo]

        with open(self.cliente, 'w', encoding='utf-8') as f:
            json.dump(lista_clientes, f, indent=4, ensure_ascii=False)
