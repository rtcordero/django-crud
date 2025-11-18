"""
Domain Layer

Capa de dominio que contiene la lógica de negocio pura.
Independiente de frameworks y detalles técnicos.
"""
from .entities import Task
from .exceptions import (
    DomainException,
    TaskNotFoundError,
    InvalidTaskDataError,
)

__all__ = [
    "Task",
    "DomainException",
    "TaskNotFoundError",
    "InvalidTaskDataError",
]
