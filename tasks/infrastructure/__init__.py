"""
Infrastructure Layer

Capa de infraestructura que contiene detalles técnicos.
Modelos de Django, repositorios, configuración externa, etc.
"""
from .repositories import TaskRepository, DjangoTaskRepository
from .models import Task

__all__ = [
    "TaskRepository",
    "DjangoTaskRepository",
    "Task",
]
