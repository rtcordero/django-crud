"""
API Layer: Serializers

Serializers de DRF para convertir datos JSON a/desde DTOs.
"""
from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    """
    Serializer para tareas.

    Convierte JSON a/desde DTOs sin exponer detalles del dominio.
    """
    id = serializers.IntegerField(
        read_only=True,
        help_text="ID único de la tarea"
    )
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

    def validate_title(self, value):
        """Valida que el título no esté vacío después de eliminar espacios."""
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value


class CreateTaskSerializer(serializers.Serializer):
    """Serializer específico para creación de tareas."""
    title = serializers.CharField(
        max_length=200,
        required=True
    )
    description = serializers.CharField(
        allow_blank=True,
        required=False,
        default=""
    )
    done = serializers.BooleanField(
        default=False,
        required=False
    )

    def validate_title(self, value):
        """Valida que el título no esté vacío."""
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value


class UpdateTaskSerializer(serializers.Serializer):
    """Serializer para actualización parcial de tareas."""
    title = serializers.CharField(
        max_length=200,
        required=False
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    done = serializers.BooleanField(
        required=False
    )

    def validate_title(self, value):
        """Valida que el título no esté vacío si es proporcionado."""
        if value and not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value
