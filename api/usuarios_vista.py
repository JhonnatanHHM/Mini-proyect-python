import getpass
from services.usuarios_service import UsuariosService
from config.exceptions import (
    ValidacionError, NotFoundError, ConflictError, AutenticacionError, RepositoryError
)

class UsuariosVista:
    def __init__(self, service: UsuariosService):
        self.service = service

    def mostrar_menu(self, usuario_actual=None):
        print("\n" + "="*50)
        print("           GESTIÓN DE USUARIOS")
        print("="*50)
        if usuario_actual:
            print(f"Usuario: {usuario_actual.nombre} ({usuario_actual.email})")
            print("\n1. Actualizar datos")
            print("2. Cambiar contraseña")
            print("3. Eliminar cuenta")
            print("4. Cerrar sesión")
            print("0. Volver al menú principal")
        else:
            print("\n1. Crear usuario")
            print("2. Iniciar sesión")
            print("0. Volver al menú principal")
        return input("\nSeleccione opción: ").strip()

    def crear_usuario(self):
        print("\n--- CREAR USUARIO ---")
        nombre = input("Nombre completo: ").strip()
        email = input("Email: ").strip()
        password = input(("Contraseña: ").strip())
        
        try:
            usuario = self.service.crear(nombre, email, password)
            print(f"\n✅ Usuario creado: {usuario.email}")
            return usuario
        except ValidacionError as e:
            print(f"❌ Error de validación: {e}")
        except ConflictError as e:
            print(f"❌ Conflicto: {e}")
        except RepositoryError as e:
            print(f"❌ Error del sistema: {e}")
        return None

    def login(self):
        print("\n--- INICIAR SESIÓN ---")
        email = input("Email: ").strip()
        password = input(("Contraseña: ").strip())
        
        try:
            usuario = self.service.login(email, password)
            print(f"\n✅ Bienvenido, {usuario.nombre}!")
            return usuario
        except AutenticacionError as e:
            print(f"❌ {e}")
        except ValidacionError as e:
            print(f"❌ {e}")
        return None

    def actualizar_datos(self, usuario_actual):
        print("\n--- ACTUALIZAR DATOS ---")
        print("Deje en blanco para mantener actual.")
        nombre = input(f"Nombre [{usuario_actual.nombre}]: ").strip() or usuario_actual.nombre
        email = input(f"Email [{usuario_actual.email}]: ").strip() or usuario_actual.email
        
        try:
            usuario = self.service.actualizar(
                email_actual=usuario_actual.email,
                nombre=nombre,
                email_nuevo=email,
                password=None # type: ignore
            )
            print(f"\n✅ Datos actualizados: {usuario.email}")
            return usuario
        except (ValidacionError, ConflictError, NotFoundError, RepositoryError) as e:
            print(f"❌ Error: {e}")
        return usuario_actual

    def cambiar_contrasena(self, usuario_actual):
        print("\n--- CAMBIAR CONTRASEÑA ---")
        password_actual = getpass.getpass("Contraseña actual: ")
        password_nueva = getpass.getpass("Nueva contraseña: ")
        password_confirm = getpass.getpass("Confirmar: ")
        
        if password_nueva != password_confirm:
            print("❌ Las contraseñas no coinciden.")
            return usuario_actual
        
        try:
            # Verificar contraseña actual
            self.service.login(usuario_actual.email, password_actual)
            # Actualizar
            usuario = self.service.actualizar(
                email_actual=usuario_actual.email,
                nombre=usuario_actual.nombre,
                email_nuevo=usuario_actual.email,
                password=password_nueva
            )
            print("\n✅ Contraseña cambiada exitosamente.")
            return usuario
        except AutenticacionError:
            print("❌ Contraseña actual incorrecta.")
        except (ValidacionError, RepositoryError) as e:
            print(f"❌ Error: {e}")
        return usuario_actual

    def eliminar_cuenta(self, usuario_actual):
        print(f"\n--- ELIMINAR CUENTA ---")
        confirm = input(f"¿Eliminar '{usuario_actual.email}'? (s/N): ").strip().lower()
        if confirm != 's':
            print("Operación cancelada.")
            return usuario_actual
        
        password = getpass.getpass("Contraseña para confirmar: ")
        try:
            self.service.login(usuario_actual.email, password)
            self.service.eliminar(usuario_actual.email)
            print("\n✅ Cuenta eliminada permanentemente.")
            return None
        except AutenticacionError:
            print("❌ Contraseña incorrecta.")
        except (NotFoundError, RepositoryError) as e:
            print(f"❌ Error: {e}")
        return usuario_actual

    def cerrar_sesion(self, usuario_actual):
        if usuario_actual:
            print(f"\n👋 Sesión cerrada: {usuario_actual.email}")
        return None