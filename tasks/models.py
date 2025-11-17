from django.db import models

# Create your models here.
class Task(models.Model):
    """
    Modelo para representar una tarea en el sistema de gestión de tareas.

    Attributes:
        title (str): Título de la tarea (máximo 200 caracteres)
        description (str): Descripción detallada de la tarea (opcional)
        done (bool): Estado de completitud de la tarea (por defecto False)
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
        ordering = ['-id']  # Más recientes primero


