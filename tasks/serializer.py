from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Task.

    Convierte objetos Task a/desde JSON para la API REST.
    """

    id = serializers.IntegerField(read_only=True, help_text="ID único de la tarea")
    title = serializers.CharField(
        max_length=200,
        help_text="Título de la tarea (máximo 200 caracteres)",
        required=True
    )
    description = serializers.CharField(
        allow_blank=True,
        required=False,
        help_text="Descripción detallada de la tarea (opcional)"
    )
    done = serializers.BooleanField(
        default=False,
        help_text="Estado de la tarea: true si está completada, false si está pendiente"
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'done']

    def validate_title(self, value):
        """
        Valida que el título no esté vacío después de eliminar espacios.
        """
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value
