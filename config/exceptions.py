from typing import Any


class BaseAppException(Exception):
    """Excepción base para toda la aplicación."""
    def __init__(self, message: str, details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ValidacionError(BaseAppException):
    """Error de validación de datos de entrada."""
    pass


class NotFoundError(BaseAppException):
    """Recurso no encontrado."""
    pass


class ConflictError(BaseAppException):
    """Conflicto: recurso ya existe (ej. email duplicado)."""
    pass


class AutenticacionError(BaseAppException):
    """Error de autenticación (credenciales inválidas)."""
    pass


class RepositoryError(BaseAppException):
    """Error en el repositorio (lectura/escritura fallida)."""
    pass