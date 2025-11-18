"""
API Layer: Views

Vistas de DRF que usan los servicios de aplicación.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample

from tasks.application import TaskService, CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from tasks.domain import TaskNotFoundError
from tasks.infrastructure import DjangoTaskRepository
from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet para operaciones CRUD sobre tareas usando DDD.

    Proporciona automáticamente los siguientes endpoints:
    - GET /tasks/ - Listar todas las tareas
    - POST /tasks/ - Crear nueva tarea
    - GET /tasks/{id}/ - Obtener una tarea específica
    - PUT /tasks/{id}/ - Actualizar tarea completa
    - PATCH /tasks/{id}/ - Actualizar tarea parcial
    - DELETE /tasks/{id}/ - Eliminar tarea
    - PATCH /tasks/{id}/mark-done/ - Marcar como completada
    - PATCH /tasks/{id}/mark-pending/ - Marcar como pendiente
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias
        repository = DjangoTaskRepository()
        self.service = TaskService(repository)

    @staticmethod
    def _entity_to_dto(entity):
        """
        Convierte una Task entity a TaskResponseDTO.
        Responsabilidad del API Layer convertir entidades a DTOs.
        """
        return TaskResponseDTO(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            done=entity.done
        )

    @extend_schema(
        summary="Listar todas las tareas",
        description="Obtiene la lista completa de todas las tareas en el sistema.",
        tags=['Tasks'],
        responses={200: TaskSerializer(many=True)}
    )
    def list(self, request):
        """Obtiene todas las tareas."""
        try:
            # Service retorna Task entities
            task_entities = self.service.list_all_tasks()

            # API Layer convierte entities a DTOs
            dtos = [self._entity_to_dto(entity) for entity in task_entities]

            serializer = TaskSerializer(dtos, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Crear nueva tarea",
        description="Crea una nueva tarea en el sistema con los datos proporcionados.",
        tags=['Tasks'],
        request=CreateTaskSerializer,
        responses={201: TaskSerializer},
        examples=[
            OpenApiExample(
                'Ejemplo básico',
                value={
                    'title': 'Comprar leche',
                    'description': 'Ir al supermercado',
                    'done': False
                },
                request_only=True,
            ),
            OpenApiExample(
                'Tarea sin descripción',
                value={
                    'title': 'Llamar al médico',
                    'done': False
                },
                request_only=True,
            ),
        ],
    )
    def create(self, request):
        """Crea una nueva tarea."""
        serializer = CreateTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = CreateTaskDTO(
                title=serializer.validated_data['title'],
                description=serializer.validated_data.get('description', ''),
                done=serializer.validated_data.get('done', False)
            )

            # Service retorna Task entity
            task_entity = self.service.create_task(dto)

            # Convertir entity a DTO (API Layer responsibility)
            response_dto = TaskResponseDTO(
                id=task_entity.id,
                title=task_entity.title,
                description=task_entity.description,
                done=task_entity.done
            )

            response_serializer = TaskSerializer(response_dto)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Obtener una tarea",
        description="Obtiene los detalles de una tarea específica por su ID.",
        tags=['Tasks'],
        responses={200: TaskSerializer}
    )
    def retrieve(self, request, pk=None):
        """Obtiene una tarea específica."""
        try:
            # Service retorna Task entity
            task_entity = self.service.get_task_by_id(pk)

            # Convertir entity a DTO
            response_dto = TaskResponseDTO(
                id=task_entity.id,
                title=task_entity.title,
                description=task_entity.description,
                done=task_entity.done
            )

            serializer = TaskSerializer(response_dto)
            return Response(serializer.data)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Actualizar tarea completa (PUT)",
        description="""
        Actualiza todos los campos de una tarea existente.

        **Nota:** PUT requiere enviar todos los campos, incluso los que no cambien.
        Para actualizar solo algunos campos, usa PATCH.
        """,
        tags=['Tasks'],
        request=CreateTaskSerializer,
        responses={200: TaskSerializer}
    )
    def update(self, request, pk=None):
        """Actualiza todos los campos de una tarea (PUT)."""
        serializer = CreateTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dto = UpdateTaskDTO(
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                done=serializer.validated_data.get('done')
            )
            # Service retorna Task entity
            task_entity = self.service.update_task(pk, dto)

            # Convertir entity a DTO
            response_dto = self._entity_to_dto(task_entity)
            response_serializer = TaskSerializer(response_dto)
            return Response(response_serializer.data)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Actualizar tarea parcial (PATCH)",
        description="""
        Actualiza solo los campos especificados de una tarea.

        **Ventaja:** Solo necesitas enviar los campos que quieres cambiar.
        Los demás campos se mantienen sin modificar.
        """,
        tags=['Tasks'],
        request=UpdateTaskSerializer,
        responses={200: TaskSerializer},
        examples=[
            OpenApiExample(
                'Marcar como completada',
                value={'done': True},
                request_only=True,
            ),
            OpenApiExample(
                'Cambiar título',
                value={'title': 'Nuevo título'},
                request_only=True,
            ),
        ],
    )
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente una tarea (PATCH)."""
        serializer = UpdateTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Solo pasar los campos que fueron proporcionados
            dto = UpdateTaskDTO(
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                done=serializer.validated_data.get('done')
            )
            # Service retorna Task entity
            task_entity = self.service.update_task(pk, dto)

            # Convertir entity a DTO
            response_dto = self._entity_to_dto(task_entity)
            response_serializer = TaskSerializer(response_dto)
            return Response(response_serializer.data)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Eliminar tarea",
        description="""
        Elimina permanentemente una tarea del sistema.

        **Advertencia:** Esta acción no se puede deshacer.
        """,
        tags=['Tasks'],
        responses={204: None}
    )
    def destroy(self, request, pk=None):
        """Elimina una tarea."""
        try:
            self.service.delete_task(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(
        detail=True,
        methods=['patch'],
        name='Mark task as done'
    )
    @extend_schema(
        summary="Marcar tarea como completada",
        description="Marca una tarea como completada.",
        tags=['Tasks'],
        responses={200: TaskSerializer}
    )
    def mark_done(self, request, pk=None):
        """Marca una tarea como completada."""
        try:
            # Service retorna Task entity
            task_entity = self.service.mark_task_as_done(pk)

            # Convertir entity a DTO
            response_dto = self._entity_to_dto(task_entity)
            serializer = TaskSerializer(response_dto)
            return Response(serializer.data)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(
        detail=True,
        methods=['patch'],
        name='Mark task as pending'
    )
    @extend_schema(
        summary="Marcar tarea como pendiente",
        description="Marca una tarea como pendiente.",
        tags=['Tasks'],
        responses={200: TaskSerializer}
    )
    def mark_pending(self, request, pk=None):
        """Marca una tarea como pendiente."""
        try:
            # Service retorna Task entity
            task_entity = self.service.mark_task_as_pending(pk)

            # Convertir entity a DTO
            response_dto = self._entity_to_dto(task_entity)
            serializer = TaskSerializer(response_dto)
            return Response(serializer.data)
        except TaskNotFoundError:
            return Response(
                {"error": f"Task with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
