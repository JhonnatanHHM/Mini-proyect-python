import json
from models.productos import Producto
from typing import List
import os

class ProductosRepo:
    def __init__(self, archivo="data/productos.json") -> None:
        self.archivo = archivo
        self._crear_archivo_si_no_existe()

    def _crear_archivo_si_no_existe(self):
        """Crea el directorio 'data' y el archivo si no existen."""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def guardar_producto(self, producto: Producto):
        """
        Guarda un nuevo producto en el archivo JSON.
        Si el archivo no existe, lo crea.
        Asigna automáticamente un código incremental único.
        """

        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_productos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_productos = []

        # Generar un nuevo código automáticamente
        if lista_productos:
            ultimo_codigo = max(
                int(p.get('codigo', '0').replace("PRO-", "")) for p in lista_productos
            )
            nuevo_codigo = ultimo_codigo + 1
        else:
            nuevo_codigo = 1

        datos_producto = {
            "codigo": f"PRO-{nuevo_codigo}",
            "nombre": producto.nombre,
            "precio": producto.precio
        }

        lista_productos.append(datos_producto)

        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=4, ensure_ascii=False)

    def actualizar_producto(self, producto: Producto, codigo: str) -> bool:
        """
        Actualiza los datos de un producto existente en el archivo JSON.
        Devuelve True si se actualizó correctamente, False si no se encontró.
        """

        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_productos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_productos = []

        producto_actualizado = False

        for p in lista_productos:
            if p.get('codigo') == codigo:
                p['nombre'] = producto.nombre
                p['precio'] = producto.precio
                producto_actualizado = True
                break

        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=4, ensure_ascii=False)

        return producto_actualizado

    def cargar_por_codigo(self, codigo: str):
        """
        Carga un producto desde el archivo JSON buscando por su código.
        Devuelve un objeto Producto si lo encuentra, o None si no existe.
        """

        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_productos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        for p in lista_productos:
            if p.get('codigo') == codigo:
                return Producto(
                    codigo=p['codigo'],
                    nombre=p['nombre'],
                    precio=p['precio']
                )
        return None
    
    def cargar_todos(self) -> List[Producto]:
        """
        Devuelve todos los productos.
        Útil para validaciones y listados.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        productos = []
        for p in datos:
            productos.append(
                Producto(
                    codigo=p['codigo'],
                    nombre=p['nombre'],
                    precio=p['precio']
                )
            )
        return productos

    def eliminar_producto(self, codigo: str):
        """
        Elimina un producto del archivo JSON buscando por su código.
        """

        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_productos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_productos = []

        lista_productos = [p for p in lista_productos if p.get('codigo') != codigo]

        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista_productos, f, indent=4, ensure_ascii=False)
