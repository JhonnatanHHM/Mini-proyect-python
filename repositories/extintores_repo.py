import json
from models.productos import Extintor
from typing import List
import os

class ExtintoresRepo:
    def __init__(self, archivo="data/extintores.json") -> None:
        self.archivo = archivo
        self._crear_archivo_si_no_existe()

    def _crear_archivo_si_no_existe(self):
        """Crea el directorio 'data' y el archivo si no existen."""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def guardar_extintor(self, extintor: Extintor):
        """
        Guarda un nuevo extintor en el archivo JSON.
        Si el archivo no existe, lo crea.
        Genera automáticamente un código incremental único (EXT-1, EXT-2, ...).
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lista_extintores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_extintores = []

        # Generar nuevo código incremental
        if lista_extintores:
            ultimo_codigo = max(
                int(e.get("codigo", "0").replace("EXT-", "")) for e in lista_extintores
            )
            nuevo_codigo = ultimo_codigo + 1
        else:
            nuevo_codigo = 1

        datos_extintor = {
            "codigo": f"EXT-{nuevo_codigo}",
            "nombre": extintor.nombre,
            "precio": extintor.precio,
            "tipo": extintor.tipo,
            "capacidad": extintor.capacidad
        }

        lista_extintores.append(datos_extintor)

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(lista_extintores, f, indent=4, ensure_ascii=False)

    def actualizar_extintor(self, extintor: Extintor, codigo: str) -> bool:
        """
        Actualiza los datos de un extintor existente en el archivo JSON.
        Devuelve True si se actualizó correctamente, False si no se encontró.
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lista_extintores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_extintores = []

        actualizado = False

        for e in lista_extintores:
            if e.get("codigo") == codigo:
                e["nombre"] = extintor.nombre
                e["precio"] = extintor.precio
                e["tipo"] = extintor.tipo
                e["capacidad"] = extintor.capacidad
                actualizado = True
                break

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(lista_extintores, f, indent=4, ensure_ascii=False)

        return actualizado

    def cargar_por_codigo(self, codigo: str):
        """
        Carga un extintor desde el archivo JSON buscando por su código.
        Devuelve un objeto Extintor si lo encuentra, o None si no existe.
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lista_extintores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        for e in lista_extintores:
            if e.get("codigo") == codigo:
                return Extintor(
                    codigo=e["codigo"],
                    nombre=e["nombre"],
                    precio=e["precio"],
                    tipo=e["tipo"],
                    capacidad=e["capacidad"]
                )
        return None
    
    def cargar_todos(self) -> List[Extintor]:
        """
        Devuelve todos los extintores.
        Útil para validaciones y listados.
        """
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        extinores = []
        for e in datos:
            extinores.append(
                Extintor(
                    codigo=e['codigo'],
                    nombre=e['nombre'],
                    precio=e['precio'],
                    tipo=e['tipo'],
                    capacidad=e['capacidad']
                )
            )
        return extinores

    def eliminar_extintor(self, codigo: str):
        """
        Elimina un extintor del archivo JSON buscando por su código.
        """
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                lista_extintores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lista_extintores = []

        lista_extintores = [e for e in lista_extintores if e.get("codigo") != codigo]

        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(lista_extintores, f, indent=4, ensure_ascii=False)
