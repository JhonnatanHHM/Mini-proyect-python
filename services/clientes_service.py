from typing import List
from models.clientes import Cliente
from repositories.clientes_repo import ClientesRepo
from config.exceptions import ValidacionError, NotFoundError, ConflictError, RepositoryError
import re


class ClientesService:
    def __init__(self, repo: ClientesRepo):
        self.repo = repo

    def _validar_nombre_empresa(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre de la empresa es obligatorio.")
        if len(nombre.strip()) < 2:
            raise ValidacionError("El nombre de la empresa debe tener al menos 2 caracteres.")

    def _validar_nombre_encargado(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del encargado es obligatorio.")

    def _validar_celular(self, celular: str) -> None:
        if not celular or not celular.strip():
            raise ValidacionError("El celular es obligatorio.")
        # Validar formato básico: solo números, 10 dígitos
        if not re.fullmatch(r"\d{10}", celular.strip()):
            raise ValidacionError("El celular debe tener 10 dígitos numéricos.")

    def _validar_direccion(self, direccion: str) -> None:
        if not direccion or not direccion.strip():
            raise ValidacionError("La dirección es obligatoria.")

    def _validar_mes_vencimiento(self, mes: str) -> None:
        meses_validos = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        if mes not in meses_validos:
            raise ValidacionError(f"Mes inválido. Use uno de: {', '.join(meses_validos)}")

    def crear(
        self,
        nombre_empresa: str,
        nombre_encargado: str,
        direccion: str,
        celular: str,
        mes_vencimiento: str
    ) -> Cliente:
        """
        Crea un nuevo cliente.
        Valida todos los campos y evita duplicados por nombre de empresa.
        """
        self._validar_nombre_empresa(nombre_empresa)
        self._validar_nombre_encargado(nombre_encargado)
        self._validar_direccion(direccion)
        self._validar_celular(celular)
        self._validar_mes_vencimiento(mes_vencimiento)

        nombre_empresa = nombre_empresa.strip().title()
        nombre_encargado = nombre_encargado.strip().title()
        direccion = direccion.strip()
        celular = celular.strip()
        mes_vencimiento = mes_vencimiento.strip().title()

        # Evitar duplicado por nombre de empresa
        if any(c.nombre_empresa.lower() == nombre_empresa.lower() for c in self.listar_todos()):
            raise ConflictError(f"Ya existe un cliente con el nombre '{nombre_empresa}'.")

        cliente = Cliente(
            codigo="",  # será asignado por el repo
            nombre_empresa=nombre_empresa,
            nombre_encargado=nombre_encargado,
            direccion=direccion,
            celular=celular,
            mes_vencimiento=mes_vencimiento,
            productos=[],
            tickets=[]
        )

        try:
            self.repo.guardar_clientes(cliente)
        except Exception as e:
            raise RepositoryError("Error al guardar el cliente.") from e

        return cliente

    def actualizar(
        self,
        codigo: str,
        nombre_empresa: str,
        nombre_encargado: str,
        direccion: str,
        celular: str,
        mes_vencimiento: str
    ) -> Cliente:
        """
        Actualiza campos de un cliente existente.
        Solo actualiza los campos proporcionados.
        """
        cliente_existente = self.repo.cargar_por_codigo(codigo)
        if not cliente_existente:
            raise NotFoundError(f"Cliente con código '{codigo}' no encontrado.")

        # Aplicar valores nuevos o mantener existentes
        nombre_empresa = nombre_empresa.strip().title() if nombre_empresa else cliente_existente.nombre_empresa
        nombre_encargado = nombre_encargado.strip().title() if nombre_encargado else cliente_existente.nombre_encargado
        direccion = direccion.strip() if direccion else cliente_existente.direccion
        celular = celular.strip() if celular else cliente_existente.celular
        mes_vencimiento = mes_vencimiento.strip().title() if mes_vencimiento else cliente_existente.mes_vencimiento

        # Validar campos actualizados
        self._validar_nombre_empresa(nombre_empresa)
        self._validar_nombre_encargado(nombre_encargado)
        self._validar_direccion(direccion)
        self._validar_celular(celular)
        self._validar_mes_vencimiento(mes_vencimiento)

        # Evitar duplicado de nombre (excepto si es el mismo cliente)
        todos = self.listar_todos()
        for c in todos:
            if c.codigo != codigo and c.nombre_empresa.lower() == nombre_empresa.lower():
                raise ConflictError(f"Ya existe otro cliente con el nombre '{nombre_empresa}'.")

        cliente_actualizado = Cliente(
            codigo=codigo,
            nombre_empresa=nombre_empresa,
            nombre_encargado=nombre_encargado,
            direccion=direccion,
            celular=celular,
            mes_vencimiento=mes_vencimiento,
            productos=cliente_existente.productos,
            tickets=cliente_existente.tickets
        )

        try:
            success = self.repo.actualizar_cliente(cliente_actualizado, codigo)
            if not success:
                raise RepositoryError("No se pudo actualizar el cliente.")
        except Exception as e:
            raise RepositoryError("Error al actualizar el cliente.") from e

        return cliente_actualizado

    def obtener_por_codigo(self, codigo: str) -> Cliente:
        """Obtiene un cliente por código."""
        cliente = self.repo.cargar_por_codigo(codigo)
        if not cliente:
            raise NotFoundError(f"Cliente con código '{codigo}' no encontrado.")
        return cliente

    def eliminar(self, codigo: str) -> None:
        """Elimina un cliente por código."""
        if not self.repo.cargar_por_codigo(codigo):
            raise NotFoundError(f"Cliente con código '{codigo}' no encontrado.")

        try:
            self.repo.eliminar_cliente(codigo)
        except Exception as e:
            raise RepositoryError("Error al eliminar el cliente.") from e

    def listar_todos(self) -> List[Cliente]:
        """Devuelve todos los clientes."""
        return self.repo.cargar_todos()

    def buscar_por_nombre(self, texto: str) -> List[Cliente]:
        """Búsqueda parcial por nombre de empresa o encargado."""
        todos = self.listar_todos()
        texto = texto.lower().strip()
        return [
            c for c in todos
            if texto in c.nombre_empresa.lower() or texto in c.nombre_encargado.lower()
        ]

    def obtener_por_vencimiento(self, mes: str) -> List[Cliente]:
        """Clientes cuyo contrato vence en un mes específico."""
        self._validar_mes_vencimiento(mes)
        mes = mes.strip().title()
        return [c for c in self.listar_todos() if c.mes_vencimiento == mes]