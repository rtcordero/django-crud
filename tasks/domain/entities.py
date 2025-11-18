"""
Domain Layer: Entities

Contiene las entidades del dominio independientes de Django.
Estos objetos representan conceptos del negocio sin acoplamiento a la persistencia.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Entidad Task del dominio.

    Representa una tarea en el sistema de gestión de tareas.
    Esta es la entidad pura del dominio, sin acoplamiento a Django.
    """
    title: str
    description: str = ""
    done: bool = False
    id: Optional[int] = None

    def mark_as_done(self) -> None:
        """Marca la tarea como completada."""
        self.done = True

    def mark_as_pending(self) -> None:
        """Marca la tarea como pendiente."""
        self.done = False

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Actualiza los datos de la tarea.

        Args:
            title: Nuevo título (opcional)
            description: Nueva descripción (opcional)
        """
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description

    def is_completed(self) -> bool:
        """Retorna True si la tarea está completada."""
        return self.done
