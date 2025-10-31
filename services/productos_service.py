from typing import List
from models.productos import Producto
from repositories.productos_repo import ProductosRepo
from config.exceptions import ValidacionError, NotFoundError, ConflictError, RepositoryError


class ProductosService:
    def __init__(self, repo: ProductosRepo):
        self.repo = repo

    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del producto es obligatorio.")
        if len(nombre.strip()) < 2:
            raise ValidacionError("El nombre debe tener al menos 2 caracteres.")
        return nombre.strip().title()

    def _validar_precio(self, precio: float) -> float:
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValidacionError("El precio debe ser un número mayor o igual a 0.")
        return float(precio)

    def crear(self, nombre: str, precio: float) -> Producto:
        """
        Crea un nuevo producto.
        Lanza excepciones si hay errores.
        """
        nombre = self._validar_nombre(nombre)
        precio = self._validar_precio(precio)

        # Evitar duplicado por nombre
        todos = self.repo.cargar_todos()
        if any(p.nombre.lower() == nombre.lower() for p in todos):
            raise ConflictError(f"Ya existe un producto con el nombre '{nombre}'.")

        producto = Producto(codigo="", nombre=nombre, precio=precio)

        try:
            self.repo.guardar_producto(producto)
        except Exception as e:
            raise RepositoryError("Error al guardar el producto en el repositorio.") from e

        return producto  # ahora tiene código asignado

    def actualizar(self, codigo: str, nombre: str, precio: float) -> Producto:
        """
        Actualiza un producto existente.
        """
        nombre = self._validar_nombre(nombre)
        precio = self._validar_precio(precio)

        producto_existente = self.repo.cargar_por_codigo(codigo)
        if not producto_existente:
            raise NotFoundError(f"Producto con código '{codigo}' no encontrado.")

        # Evitar duplicado de nombre (excepto si es el mismo)
        todos = self.repo.cargar_todos()
        for p in todos:
            if p.codigo != codigo and p.nombre.lower() == nombre.lower():
                raise ConflictError(f"Ya existe otro producto con el nombre '{nombre}'.")

        producto_actualizado = Producto(codigo=codigo, nombre=nombre, precio=precio)

        try:
            success = self.repo.actualizar_producto(producto_actualizado, codigo)
            if not success:
                raise RepositoryError("No se pudo actualizar el producto.")
        except Exception as e:
            raise RepositoryError("Error al actualizar el producto.") from e

        return producto_actualizado

    def obtener_por_codigo(self, codigo: str) -> Producto:
        """Obtiene un producto por código."""
        producto = self.repo.cargar_por_codigo(codigo)
        if not producto:
            raise NotFoundError(f"Producto con código '{codigo}' no encontrado.")
        return producto

    def eliminar(self, codigo: str) -> None:
        """Elimina un producto por código."""
        if not self.repo.cargar_por_codigo(codigo):
            raise NotFoundError(f"Producto con código '{codigo}' no encontrado.")

        try:
            self.repo.eliminar_producto(codigo)
        except Exception as e:
            raise RepositoryError("Error al eliminar el producto.") from e

    def listar_todos(self) -> List[Producto]:
        """Devuelve todos los productos."""
        return self.repo.cargar_todos()

    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """Búsqueda parcial por nombre (insensible a mayúsculas)."""
        if not texto or not texto.strip():
            raise ValidacionError("El texto de búsqueda no puede estar vacío.")
        texto = texto.lower().strip()
        return [p for p in self.listar_todos() if texto in p.nombre.lower()]

    def buscar_por_precio(self, precio_min: float, precio_max: float) -> List[Producto]:
        """
        Busca productos por rango de precio.
        Si precio_max es None, busca >= precio_min.
        """
        if precio_max is not None and precio_max < precio_min:
            raise ValidacionError("precio_max debe ser mayor o igual a precio_min.")

        resultados = []
        for p in self.listar_todos():
            if precio_max is None:
                if p.precio >= precio_min:
                    resultados.append(p)
            else:
                if precio_min <= p.precio <= precio_max:
                    resultados.append(p)
        return resultados