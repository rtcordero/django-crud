"""
Infrastructure Layer: Repositories

Implementa el patrón Repository para abstracción de la persistencia.
El repositorio es la interfaz entre el dominio y la base de datos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from tasks.domain import Task
from .models import Task as TaskModel


class TaskRepository(ABC):
    """
    Interfaz del repositorio para tareas.

    Define los métodos que deben implementarse para persistencia.
    """

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Obtiene todas las tareas."""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID."""
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        """Guarda una tarea (crea o actualiza)."""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """Elimina una tarea por ID."""
        pass


class DjangoTaskRepository(TaskRepository):
    """
    Implementación del repositorio usando Django ORM.

    Convierte entre modelos de Django y entidades del dominio.
    """

    def get_all(self) -> List[Task]:
        """Obtiene todas las tareas."""
        models = TaskModel.objects.all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID."""
        try:
            model = TaskModel.objects.get(id=task_id)
            return self._model_to_entity(model)
        except TaskModel.DoesNotExist:
            return None

    def save(self, task: Task) -> Task:
        """Guarda una tarea (crea o actualiza)."""
        if task.id is None:
            # Crear nueva tarea
            model = TaskModel(
                title=task.title,
                description=task.description,
                done=task.done
            )
        else:
            # Actualizar tarea existente
            model = TaskModel.objects.get(id=task.id)
            model.title = task.title
            model.description = task.description
            model.done = task.done

        model.save()
        return self._model_to_entity(model)

    def delete(self, task_id: int) -> None:
        """Elimina una tarea por ID."""
        TaskModel.objects.filter(id=task_id).delete()

    @staticmethod
    def _model_to_entity(model: TaskModel) -> Task:
        """Convierte un modelo de Django a una entidad del dominio."""
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            done=model.done
        )
