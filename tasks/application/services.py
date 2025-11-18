"""
Application Layer: Services

Contiene los casos de uso (use cases) de la aplicación.
Los servicios orquestan la lógica de negocio usando entidades del dominio
y el repositorio para persistencia.
"""
from typing import List

from tasks.domain import Task, TaskNotFoundError
from tasks.infrastructure.repositories import TaskRepository
from .dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO


class TaskService:
    """
    Servicio de aplicación para gestionar tareas.

    Implementa los casos de uso de la aplicación.
    """

    def __init__(self, repository: TaskRepository):
        """
        Inicializa el servicio con un repositorio.

        Args:
            repository: Implementación del repositorio para persistencia
        """
        self.repository = repository

    def list_all_tasks(self) -> List[Task]:
        """
        Caso de uso: Obtener todas las tareas.

        Returns:
            Lista de Task entities
        """
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Caso de uso: Obtener una tarea específica.

        Args:
            task_id: ID de la tarea

        Returns:
            Task entity

        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        return task

    def create_task(self, dto: CreateTaskDTO) -> Task:
        """
        Caso de uso: Crear una nueva tarea.

        Args:
            dto: DTO con los datos de la tarea a crear

        Returns:
            Task entity creada
        """
        # Crear la entidad del dominio
        task = Task(
            title=dto.title,
            description=dto.description,
            done=dto.done
        )

        # Persistir usando el repositorio
        return self.repository.save(task)

    def update_task(self, task_id: int, dto: UpdateTaskDTO) -> Task:
        """
        Caso de uso: Actualizar una tarea.

        Args:
            task_id: ID de la tarea a actualizar
            dto: DTO con los datos a actualizar

        Returns:
            Task entity actualizada

        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        # Obtener la tarea actual
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        # Actualizar los campos si fueron proporcionados
        if dto.title is not None:
            task.title = dto.title
        if dto.description is not None:
            task.description = dto.description
        if dto.done is not None:
            task.done = dto.done

        # Persistir los cambios
        return self.repository.save(task)

    def delete_task(self, task_id: int) -> None:
        """
        Caso de uso: Eliminar una tarea.

        Args:
            task_id: ID de la tarea a eliminar

        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        self.repository.delete(task_id)

    def mark_task_as_done(self, task_id: int) -> Task:
        """
        Caso de uso: Marcar una tarea como completada.

        Args:
            task_id: ID de la tarea

        Returns:
            Task entity actualizada

        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        task.mark_as_done()
        return self.repository.save(task)

    def mark_task_as_pending(self, task_id: int) -> Task:
        """
        Caso de uso: Marcar una tarea como pendiente.

        Args:
            task_id: ID de la tarea

        Returns:
            Task entity actualizada

        Raises:
            TaskNotFoundError: Si la tarea no existe
        """
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")

        task.mark_as_pending()
        return self.repository.save(task)
