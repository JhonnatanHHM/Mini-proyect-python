from datetime import datetime
from typing import List, Dict
from models.tickets import Ticket
from repositories.tickets_repo import TicketsRepo
from repositories.clientes_repo import ClientesRepo
from repositories.productos_repo import ProductosRepo
from repositories.extintores_repo import ExtintoresRepo
from config.exceptions import ValidacionError, NotFoundError, RepositoryError


class TicketsService:
    def __init__(self, tickets_repo: TicketsRepo, clientes_repo: ClientesRepo, productos_repo: ProductosRepo,
                    extintores_repo: ExtintoresRepo):
        self.tickets_repo = tickets_repo
        self.clientes_repo = clientes_repo
        self.productos_repo = productos_repo
        self.extintores_repo = extintores_repo

    def _validar_servicio(self, servicio: str) -> str:
        if not servicio or not servicio.strip():
            raise ValidacionError("El servicio es obligatorio.")
        return servicio.strip().title()

    def _validar_producto_item(self, item: Dict) -> Dict:
        """Valida un ítem de producto en el ticket."""
        required = ['codigo', 'cantidad']
        for key in required:
            if key not in item:
                raise ValidacionError(f"El producto debe tener '{key}'.")
        if not isinstance(item['cantidad'], int) or item['cantidad'] <= 0:
            raise ValidacionError("La cantidad debe ser un entero mayor a 0.")
        return item

    def _sincronizar_productos(self, productos: List[Dict]) -> List[Dict]:
        """Sincroniza nombre y precio desde Productos o Extintores."""
        sincronizados = []
        for item in productos:
            codigo = item['codigo']
            cantidad = item['cantidad']

            # 1. Buscar en Productos
            prod = self.productos_repo.cargar_por_codigo(codigo)
            if prod:
                item = {
                    'codigo': codigo,
                    'nombre': prod.nombre,
                    'precio': prod.precio,
                    'cantidad': cantidad
                }
                sincronizados.append(item)
                continue  # ← ¡Importante! Siguiente producto

            # 2. Si no está en productos → Buscar en Extintores
            ext = self.extintores_repo.cargar_por_codigo(codigo)
            if ext:
                item = {
                    'codigo': codigo,
                    'nombre': ext.nombre,
                    'precio': ext.precio,
                    'cantidad': cantidad
                }
                sincronizados.append(item)
                continue

            # 3. Si no existe en ninguno → ERROR
            raise NotFoundError(f"Producto o extintor con código '{codigo}' no encontrado.")

        return sincronizados

    def calcular_total(self, productos: List[Dict]) -> int:
        """Calcula el total del ticket."""
        total = 0
        for p in productos:
            total += p['precio'] * p['cantidad']
        return total

    def crear(
        self,
        servicio: str,
        codigo_cliente: str,
        productos: List[Dict]
    ) -> Ticket:
        """
        Crea un ticket completo.
        Lanza excepciones si hay errores.
        """
        servicio = self._validar_servicio(servicio)

        # Validar cliente
        cliente = self.clientes_repo.cargar_por_codigo(codigo_cliente)
        if not cliente:
            raise NotFoundError(f"Cliente con código '{codigo_cliente}' no encontrado.")

        # Validar productos
        if not productos:
            raise ValidacionError("Debe incluir al menos un producto.")
        for item in productos:
            self._validar_producto_item(item)

        # Sincronizar con catálogo
        try:
            productos_sync = self._sincronizar_productos(productos)
        except NotFoundError:
            raise  # Re-lanzar

        total = self.calcular_total(productos_sync)

        ticket = Ticket(
            codigo_ticket="",
            servicio=servicio,
            codigo_cliente=codigo_cliente,
            cliente=cliente.nombre_empresa,
            productos=productos_sync,
            total=total,
            fecha=datetime.now()
        )

        try:
            self.tickets_repo.crear(ticket)
        except Exception as e:
            raise RepositoryError("Error al crear el ticket.") from e

        return ticket

    def actualizar(
        self,
        codigo_ticket: str,
        servicio: str,
        productos: List[Dict]
    ) -> Ticket:
        """
        Actualiza servicio y/o productos.
        """
        ticket_existente = self.tickets_repo.cargar_por_codigo(codigo_ticket)
        if not ticket_existente:
            raise NotFoundError(f"Ticket con código '{codigo_ticket}' no encontrado.")

        nuevo_servicio = self._validar_servicio(servicio) if servicio else ticket_existente.servicio

        if productos is not None:
            if not productos:
                raise ValidacionError("La lista de productos no puede estar vacía.")
            for item in productos:
                self._validar_producto_item(item)
            productos_sync = self._sincronizar_productos(productos)
        else:
            productos_sync = ticket_existente.productos

        nuevo_total = self.calcular_total(productos_sync)

        ticket_actualizado = Ticket(
            codigo_ticket=codigo_ticket,
            servicio=nuevo_servicio,
            codigo_cliente=ticket_existente.codigo_cliente,
            cliente=ticket_existente.cliente,
            productos=productos_sync,
            total=nuevo_total,
            fecha=ticket_existente.fecha
        )

        try:
            success = self.tickets_repo.actualizar_por_codigo(ticket_actualizado, codigo_ticket)
            if not success:
                raise RepositoryError("No se pudo actualizar el ticket.")
        except Exception as e:
            raise RepositoryError("Error al actualizar el ticket.") from e

        return ticket_actualizado

    def obtener_por_codigo(self, codigo_ticket: str) -> Ticket:
        """Obtiene un ticket por código."""
        ticket = self.tickets_repo.cargar_por_codigo(codigo_ticket)
        if not ticket:
            raise NotFoundError(f"Ticket con código '{codigo_ticket}' no encontrado.")
        return ticket

    def obtener_por_cliente(self, codigo_cliente: str) -> List[Ticket]:
        """Obtiene todos los tickets de un cliente."""
        # Validar que el cliente exista
        if not self.clientes_repo.cargar_por_codigo(codigo_cliente):
            raise NotFoundError(f"Cliente con código '{codigo_cliente}' no encontrado.")
        return self.tickets_repo.cargar_todos_por_cliente(codigo_cliente)

    def eliminar(self, codigo_ticket: str) -> None:
        """Elimina un ticket."""
        if not self.tickets_repo.cargar_por_codigo(codigo_ticket):
            raise NotFoundError(f"Ticket con código '{codigo_ticket}' no encontrado.")

        try:
            success = self.tickets_repo.eliminar_por_codigo(codigo_ticket)
            if not success:
                raise RepositoryError("No se pudo eliminar el ticket.")
        except Exception as e:
            raise RepositoryError("Error al eliminar el ticket.") from e

    def listar_todos(self) -> List[Ticket]:
        """Devuelve todos los tickets."""
        return self.tickets_repo.cargar_todos()