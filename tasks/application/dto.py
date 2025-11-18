"""
Application Layer: Data Transfer Objects (DTOs)

DTOs son usados para transferir datos entre capas sin exponer las entidades de dominio.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateTaskDTO:
    """DTO para crear una tarea."""
    title: str
    description: str = ""
    done: bool = False


@dataclass
class UpdateTaskDTO:
    """DTO para actualizar una tarea."""
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


@dataclass
class TaskResponseDTO:
    """DTO para respuestas de tareas."""
    id: int
    title: str
    description: str
    done: bool
