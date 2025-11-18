"""
Domain Layer: Exceptions

Excepciones del dominio que representan errores de negocio.
"""


class DomainException(Exception):
    """Excepción base para todas las excepciones del dominio."""
    pass


class TaskNotFoundError(DomainException):
    """Se lanza cuando una tarea no es encontrada."""
    pass


class InvalidTaskDataError(DomainException):
    """Se lanza cuando los datos de la tarea son inválidos."""
    pass
