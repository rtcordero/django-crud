"""
Infrastructure Layer: Models

Modelos de Django para persistencia.
Estos modelos son detalles técnicos de infraestructura.
"""
from django.db import models


class Task(models.Model):
    """
    Modelo Task para persistencia en base de datos.

    Este modelo es un detalle de infraestructura.
    La entidad real del dominio está en tasks.domain.Task
    """
    title = models.CharField(
        max_length=200,
        help_text="Título de la tarea"
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción detallada de la tarea (opcional)"
    )
    done = models.BooleanField(
        default=False,
        help_text="Indica si la tarea está completada"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-id']
