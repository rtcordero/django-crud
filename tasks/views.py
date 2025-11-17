from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample

from tasks.models import Task
from tasks.serializer import TaskSerializer


class TaskView(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD sobre tareas.

    Proporciona automáticamente los siguientes endpoints:
    - GET /tasks/ - Listar todas las tareas
    - POST /tasks/ - Crear nueva tarea
    - GET /tasks/{id}/ - Obtener una tarea específica
    - PUT /tasks/{id}/ - Actualizar tarea completa
    - PATCH /tasks/{id}/ - Actualizar tarea parcial
    - DELETE /tasks/{id}/ - Eliminar tarea
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @extend_schema(
        summary="Listar todas las tareas",
        description="Obtiene la lista completa de todas las tareas en el sistema.",
        tags=['Tasks'],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear nueva tarea",
        description="Crea una nueva tarea en el sistema con los datos proporcionados.",
        tags=['Tasks'],
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
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Obtener una tarea",
        description="Obtiene los detalles de una tarea específica por su ID.",
        tags=['Tasks'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar tarea completa (PUT)",
        description="""
        Actualiza todos los campos de una tarea existente.
        
        **Nota:** PUT requiere enviar todos los campos, incluso los que no cambien.
        Para actualizar solo algunos campos, usa PATCH.
        """,
        tags=['Tasks'],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar tarea parcial (PATCH)",
        description="""
        Actualiza solo los campos especificados de una tarea.
        
        **Ventaja:** Solo necesitas enviar los campos que quieres cambiar.
        Los demás campos se mantienen sin modificar.
        """,
        tags=['Tasks'],
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
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar tarea",
        description="""
        Elimina permanentemente una tarea del sistema.
        
        **Advertencia:** Esta acción no se puede deshacer.
        """,
        tags=['Tasks'],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
