import json
from models.usuarios import Usuario
from typing import Optional
import os

class UsuariosRepo:
    def __init__(self, archivo="data/usuarios.json"):
        self.archivo = archivo
        self._crear_archivo_si_no_existe()

    def _crear_archivo_si_no_existe(self):
        """Crea el directorio 'data' y el archivo si no existen."""
        os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def guardar_usuarios(self, usuario: Usuario):
        """Guarda un nuevo usuario en el archivo JSON."""
        self._crear_archivo_si_no_existe()
        with open(self.archivo, 'r', encoding='utf-8') as f:
            lista = json.load(f)
        
        # Generar código
        if lista:
            ultimo = max(int(u['codigo'].replace("USR-", "")) for u in lista)
            codigo = f"USR-{ultimo + 1}"
        else:
            codigo = "USR-1"
        
        datos = {
            "codigo": codigo,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "contraseña": usuario.contraseña
        }
        lista.append(datos)

        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    def existe_usuario(self, email: str) -> bool:
        """Verifica si ya existe un usuario con ese email."""
        self._crear_archivo_si_no_existe()
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        return any(u['email'].lower() == email.lower() for u in lista)

    def cargar_por_email(self, email: str) -> Optional[Usuario]:
        """Carga un usuario por email."""
        self._crear_archivo_si_no_existe()
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        
        for u in lista:
            if u['email'].lower() == email.lower():
                return Usuario(
                    nombre=u['nombre'],
                    email=u['email'],
                    contraseña=u['contraseña']
                )
        return None

    def actualizar_usuario(self, usuario_actualizado: Usuario, email_anterior: str) -> bool:
        """Actualiza un usuario existente."""
        self._crear_archivo_si_no_existe()
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        for i, u in enumerate(lista):
            if u['email'].lower() == email_anterior.lower():
                lista[i] = {
                    "codigo": u['codigo'],
                    "nombre": usuario_actualizado.nombre,
                    "email": usuario_actualizado.email,
                    "contraseña": usuario_actualizado.contraseña
                }
                with open(self.archivo, 'w', encoding='utf-8') as f:
                    json.dump(lista, f, indent=4, ensure_ascii=False)
                return True
        return False

    def eliminar_usuario(self, email: str):
        """Elimina un usuario por email."""
        self._crear_archivo_si_no_existe()
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        lista = [u for u in lista if u['email'].lower() != email.lower()]
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)