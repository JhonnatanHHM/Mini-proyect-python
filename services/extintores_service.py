from typing import List
from models.productos import Extintor
from repositories.extintores_repo import ExtintoresRepo
from config.exceptions import ValidacionError, NotFoundError, ConflictError, RepositoryError


class ExtintoresService:
    def __init__(self, repo: ExtintoresRepo):
        self.repo = repo

    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del extintor es obligatorio.")
        if len(nombre.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip().title()

    def _validar_precio(self, precio: float) -> float:
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValidacionError("El precio debe ser un número mayor o igual a 0.")
        return float(precio)

    def _validar_tipo(self, tipo: str) -> str:
        if not tipo or not tipo.strip():
            raise ValidacionError("El tipo de extintor es obligatorio.")
        return tipo.strip().title()

    def _validar_capacidad(self, capacidad: float) -> float:
        if not isinstance(capacidad, (int, float)) or capacidad <= 0:
            raise ValidacionError("La capacidad debe ser mayor que 0.")
        return float(capacidad)

    def crear(self, nombre: str, precio: float, tipo: str, capacidad: float) -> Extintor:
        """
        Crea un nuevo extintor.
        Lanza excepciones si hay errores.
        """
        nombre = self._validar_nombre(nombre)
        precio = self._validar_precio(precio)
        tipo = self._validar_tipo(tipo)
        capacidad = self._validar_capacidad(capacidad)

        # Evitar duplicado por nombre
        todos = self.repo.cargar_todos()
        if any(e.nombre.lower() == nombre.lower() for e in todos):
            raise ConflictError(f"Ya existe un extintor con el nombre '{nombre}'.")

        extintor = Extintor(codigo="", nombre=nombre, precio=precio, tipo=tipo, capacidad=capacidad)

        try:
            self.repo.guardar_extintor(extintor)
        except Exception as e:
            raise RepositoryError("Error al guardar el extintor en el repositorio.") from e

        return extintor  # ahora tiene código asignado

    def actualizar(self, codigo: str, nombre: str, precio: float, tipo: str, capacidad: float) -> Extintor:
        """
        Actualiza un extintor existente.
        """
        nombre = self._validar_nombre(nombre)
        precio = self._validar_precio(precio)
        tipo = self._validar_tipo(tipo)
        capacidad = self._validar_capacidad(capacidad)

        extintor_existente = self.repo.cargar_por_codigo(codigo)
        if not extintor_existente:
            raise NotFoundError(f"Extintor con código '{codigo}' no encontrado.")

        # Evitar duplicado de nombre (excepto si es el mismo)
        todos = self.repo.cargar_todos()
        for e in todos:
            if e.codigo != codigo and e.nombre.lower() == nombre.lower():
                raise ConflictError(f"Ya existe otro extintor con el nombre '{nombre}'.")

        extintor_actualizado = Extintor(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            tipo=tipo,
            capacidad=capacidad
        )

        try:
            success = self.repo.actualizar_extintor(extintor_actualizado, codigo)
            if not success:
                raise RepositoryError("No se pudo actualizar el extintor.")
        except Exception as e:
            raise RepositoryError("Error al actualizar el extintor.") from e

        return extintor_actualizado

    def obtener_por_codigo(self, codigo: str) -> Extintor:
        """Obtiene un extintor por código."""
        extintor = self.repo.cargar_por_codigo(codigo)
        if not extintor:
            raise NotFoundError(f"Extintor con código '{codigo}' no encontrado.")
        return extintor

    def eliminar(self, codigo: str) -> None:
        """Elimina un extintor por código."""
        if not self.repo.cargar_por_codigo(codigo):
            raise NotFoundError(f"Extintor con código '{codigo}' no encontrado.")

        try:
            self.repo.eliminar_extintor(codigo)
        except Exception as e:
            raise RepositoryError("Error al eliminar el extintor.") from e

    def listar_todos(self) -> List[Extintor]:
        """Devuelve todos los extintores."""
        return self.repo.cargar_todos()

    def buscar_por_tipo(self, tipo: str) -> List[Extintor]:
        """Busca extintores por tipo (insensible a mayúsculas)."""
        if not tipo or not tipo.strip():
            raise ValidacionError("El tipo de búsqueda no puede estar vacío.")
        tipo = tipo.lower().strip()
        return [e for e in self.listar_todos() if tipo in e.tipo.lower()]

    def buscar_por_rango_capacidad(self, capacidad_min: float, capacidad_max: float) -> List[Extintor]:
        """
        Busca extintores por rango de capacidad.
        """
        if capacidad_max is not None and capacidad_max < capacidad_min:
            raise ValidacionError("capacidad_max debe ser mayor o igual a capacidad_min.")

        resultados = []
        for e in self.listar_todos():
            if capacidad_max is None:
                if e.capacidad >= capacidad_min:
                    resultados.append(e)
            else:
                if capacidad_min <= e.capacidad <= capacidad_max:
                    resultados.append(e)
        return resultados

    def buscar_por_nombre(self, texto: str) -> List[Extintor]:
        """Búsqueda parcial por nombre."""
        if not texto or not texto.strip():
            raise ValidacionError("El texto de búsqueda no puede estar vacío.")
        texto = texto.lower().strip()
        return [e for e in self.listar_todos() if texto in e.nombre.lower()]