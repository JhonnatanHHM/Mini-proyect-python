import bcrypt
from models.usuarios import Usuario
from repositories.usuarios_repo import UsuariosRepo
from config.exceptions import (
    ValidacionError, NotFoundError, ConflictError, AutenticacionError, RepositoryError
)


class UsuariosService:
    def __init__(self, repo: UsuariosRepo):
        self.repo = repo

    def _hash_password(self, password: str) -> str:
        """Encripta la contraseña usando bcrypt."""
        if not password or len(password.strip()) < 4:
            raise ValidacionError("La contraseña debe tener al menos 4 caracteres.")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _check_password(self, password: str, hashed: str) -> bool:
        """Verifica si la contraseña coincide con el hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def _validar_email(self, email: str) -> None:
        """Valida formato básico de email."""
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            raise ValidacionError("Email inválido.")

    def _validar_nombre(self, nombre: str) -> None:
        """Valida que el nombre no esté vacío."""
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre es obligatorio.")

    def crear(self, nombre: str, email: str, password: str) -> Usuario:
        """
        Crea un nuevo usuario.
        Lanza excepciones en caso de error.
        """
        self._validar_nombre(nombre)
        self._validar_email(email)

        if self.repo.existe_usuario(email):
            raise ConflictError(f"El email '{email}' ya está registrado.")

        hashed_password = self._hash_password(password)

        usuario = Usuario(
            nombre=nombre.strip(),
            email=email.strip().lower(),
            contraseña=hashed_password
        )

        try:
            self.repo.guardar_usuarios(usuario)
        except Exception as e:
            raise RepositoryError("Error al guardar el usuario en el repositorio.") from e

        return usuario

    def login(self, email: str, password: str) -> Usuario:
        """
        Autentica al usuario.
        Lanza AuthenticationError si falla.
        """
        self._validar_email(email)

        usuario = self.repo.cargar_por_email(email.strip().lower())
        if not usuario:
            raise AutenticacionError("Email o contraseña incorrectos.")

        if not self._check_password(password, usuario.contraseña):
            raise AutenticacionError("Email o contraseña incorrectos.")

        return usuario

    def actualizar(self, email_actual: str, nombre: str, email_nuevo: str, password: str) -> Usuario:
        """
        Actualiza un usuario existente.
        """
        self._validar_nombre(nombre)
        self._validar_email(email_nuevo)

        email_actual = email_actual.strip().lower()
        email_nuevo = email_nuevo.strip().lower()

        if email_actual != email_nuevo and self.repo.existe_usuario(email_nuevo):
            raise ConflictError(f"El email '{email_nuevo}' ya está en uso.")

        usuario_existente = self.repo.cargar_por_email(email_actual)
        if not usuario_existente:
            raise NotFoundError(f"Usuario con email '{email_actual}' no encontrado.")

        nueva_contraseña = self._hash_password(password) if password else usuario_existente.contraseña

        usuario_actualizado = Usuario(
            nombre=nombre.strip(),
            email=email_nuevo,
            contraseña=nueva_contraseña
        )

        try:
            success = self.repo.actualizar_usuario(usuario_actualizado, email_actual)
            if not success:
                raise RepositoryError("No se pudo actualizar el usuario en el repositorio.")
        except Exception as e:
            raise RepositoryError("Error al actualizar el usuario.") from e

        return usuario_actualizado

    def eliminar(self, email: str) -> None:
        """
        Elimina un usuario por email.
        """
        email = email.strip().lower()
        if not self.repo.existe_usuario(email):
            raise NotFoundError(f"Usuario con email '{email}' no encontrado.")

        try:
            self.repo.eliminar_usuario(email)
        except Exception as e:
            raise RepositoryError("Error al eliminar el usuario del repositorio.") from e