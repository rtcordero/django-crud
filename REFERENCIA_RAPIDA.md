# 📊 Referencia Rápida - Arquitectura Django REST

## 🗺️ Mapa Mental del Proyecto

```
                    DJANGO CRUD API
                          |
        +-----------------+-----------------+
        |                                   |
   django_crud_api/                      tasks/
   (Configuración)                    (Aplicación)
        |                                   |
        |                    +--------------+-------------+
    settings.py              |              |             |
    urls.py              models.py    views.py    serializer.py
        |                    |              |             |
        |                    |              +------+------+
        +--------------------+-----------------------+
                             |
                         db.sqlite3
```

## 📝 Cheat Sheet: Dónde editar para cada cambio

### 🆕 Añadir un nuevo campo a Task
```
1. tasks/models.py        → Añade el campo
2. Terminal               → python manage.py makemigrations
3. Terminal               → python manage.py migrate
4. tasks/serializer.py    → Añade el campo a 'fields'
```

### 🛣️ Añadir una nueva ruta (endpoint)
```
Opción A (Automática con router):
    tasks/views.py → Crear ViewSet
    tasks/urls.py  → router.register()

Opción B (Manual):
    tasks/views.py → Crear vista
    tasks/urls.py  → path('ruta/', vista)
```

### 🔧 Cambiar configuración del proyecto
```
django_crud_api/settings.py → Modifica INSTALLED_APPS, CORS, etc.
```

### 🎨 Personalizar el admin
```
tasks/admin.py → Registra y configura modelos
```

## 🔄 Los 3 patrones principales

### Patrón 1: Model (Qué guardas)
```python
# tasks/models.py
class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
```
**Se traduce a tabla SQL:**
```sql
CREATE TABLE tasks_task (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200),
    done BOOLEAN
);
```

### Patrón 2: Serializer (Cómo lo transformas)
```python
# tasks/serializer.py
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'done']
```
**Hace la conversión:**
```
Python Object ↔ JSON
   Task       ↔  {"id": 1, "title": "...", "done": false}
```

### Patrón 3: View (Qué haces con eso)
```python
# tasks/views.py
class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```
**Proporciona automáticamente:**
- GET /tasks/ → list()
- POST /tasks/ → create()
- GET /tasks/1/ → retrieve()
- PUT /tasks/1/ → update()
- PATCH /tasks/1/ → partial_update()
- DELETE /tasks/1/ → destroy()

## 📞 Flujo de peticiones HTTP

### GET /tasks/api/v1/tasks/ (Listar)
```
Browser/Client
    ↓ HTTP GET
django_crud_api/urls.py (path 'tasks/')
    ↓
tasks/urls.py (router 'tasks')
    ↓
TaskView.list()
    ↓
Task.objects.all() → [task1, task2, ...]
    ↓
TaskSerializer(many=True) → JSON
    ↓ HTTP 200
[{"id": 1, ...}, {"id": 2, ...}]
```

### POST /tasks/api/v1/tasks/ (Crear)
```
Browser/Client
    ↓ HTTP POST + JSON data
django_crud_api/urls.py
    ↓
tasks/urls.py
    ↓
TaskView.create()
    ↓
TaskSerializer.is_valid()? → Sí
    ↓
Task.objects.create()
    ↓
Save to db.sqlite3
    ↓
TaskSerializer → JSON
    ↓ HTTP 201
{"id": 3, "title": "Nueva", "done": false}
```

### PUT /tasks/api/v1/tasks/1/ (Actualizar)
```
Browser/Client
    ↓ HTTP PUT + JSON data
django_crud_api/urls.py
    ↓
tasks/urls.py
    ↓
TaskView.update(pk=1)
    ↓
Task.objects.get(id=1)
    ↓
TaskSerializer.is_valid()? → Sí
    ↓
task.save()
    ↓
Update in db.sqlite3
    ↓
TaskSerializer → JSON
    ↓ HTTP 200
{"id": 1, "title": "Actualizada", "done": true}
```

### DELETE /tasks/api/v1/tasks/1/ (Eliminar)
```
Browser/Client
    ↓ HTTP DELETE
django_crud_api/urls.py
    ↓
tasks/urls.py
    ↓
TaskView.destroy(pk=1)
    ↓
Task.objects.get(id=1)
    ↓
task.delete()
    ↓
Remove from db.sqlite3
    ↓ HTTP 204
(Sin contenido)
```

## 🧩 Comandos Django más usados

```bash
# Migraciones
python manage.py makemigrations     # Detecta cambios en models.py
python manage.py migrate            # Aplica cambios a la DB
python manage.py showmigrations     # Ver estado de migraciones

# Servidor
python manage.py runserver          # Inicia en localhost:8000
python manage.py runserver 8080     # Inicia en otro puerto

# Base de datos
python manage.py dbshell            # Abre consola SQL
python manage.py flush              # Limpia toda la DB

# Django shell (Python interactivo)
python manage.py shell              # Abre shell de Django
>>> from tasks.models import Task
>>> Task.objects.all()

# Admin
python manage.py createsuperuser    # Crea usuario admin

# Otros
python manage.py check              # Verifica el proyecto
python manage.py test               # Ejecuta tests
```

## 🎯 Queries comunes con el ORM

```python
from tasks.models import Task

# CREATE
Task.objects.create(title="Nueva tarea", done=False)

# READ
Task.objects.all()                          # Todas
Task.objects.get(id=1)                      # Una específica
Task.objects.filter(done=False)             # Filtradas
Task.objects.filter(title__contains="Django")  # Con palabra
Task.objects.count()                        # Contar

# UPDATE
task = Task.objects.get(id=1)
task.done = True
task.save()

# DELETE
task = Task.objects.get(id=1)
task.delete()

# O en masa
Task.objects.filter(done=True).delete()

# ORDENAR
Task.objects.order_by('title')              # Ascendente
Task.objects.order_by('-id')                # Descendente

# LIMITAR
Task.objects.all()[:5]                      # Primeras 5

# ENCADENAR
Task.objects.filter(done=False).order_by('-id')[:10]
```

## 🔐 Configuraciones importantes

### settings.py - Qué hace cada cosa

```python
# Apps instaladas
INSTALLED_APPS = [
    'rest_framework',    # → Habilita DRF
    'corsheaders',       # → Permite peticiones cross-origin
    'tasks',             # → Tu aplicación
]

# Middleware (orden importa)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # → Debe ir arriba
    # ...otros middleware...
]

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Tipo de DB
        'NAME': BASE_DIR / 'db.sqlite3',         # Ubicación
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Permite tu frontend
]

# DEBUG
DEBUG = True  # ⚠️ Nunca en producción
```

## 🎨 URLs: Patrones comunes

```python
# En django_crud_api/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),           # /admin/
    path('tasks/', include('tasks.urls')),     # /tasks/...
]

# En tasks/urls.py - Opción 1: Con router (recomendado)
router = routers.DefaultRouter()
router.register(r'tasks', TaskView, 'tasks')
urlpatterns = [
    path('api/v1/', include(router.urls)),
]

# En tasks/urls.py - Opción 2: Manual
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
]
```

## 🚀 Tips profesionales

### ✅ Hacer
- Usar `ModelViewSet` para CRUD completo automático
- Usar `filter()` en lugar de `get()` para múltiples resultados
- Crear migraciones después de cada cambio en `models.py`
- Usar entorno virtual (venv) siempre
- Mantener `requirements.txt` actualizado
- Usar `blank=True` para campos opcionales en formularios
- Usar `null=True` para campos opcionales en DB

### ❌ Evitar
- No usar `get()` sin try/except (puede fallar)
- No modificar migraciones después de aplicarlas
- No hardcodear URLs (usa `reverse()` o nombres de rutas)
- No poner `DEBUG = True` en producción
- No commitear `db.sqlite3` ni `__pycache__/`
- No olvidar validar datos en serializers

## 🐛 Errores comunes y soluciones

### Error: "No such table: tasks_task"
```bash
# Solución:
python manage.py migrate
```

### Error: "No module named 'rest_framework'"
```bash
# Solución:
pip install djangorestframework
```

### Error: "CORS policy blocked"
```python
# En settings.py añadir:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Error: "DoesNotExist"
```python
# Mal:
task = Task.objects.get(id=999)  # ❌ Falla si no existe

# Bien:
try:
    task = Task.objects.get(id=999)
except Task.DoesNotExist:
    task = None

# O mejor:
task = Task.objects.filter(id=999).first()  # Devuelve None si no existe
```

---

**💡 Tip:** Imprime esta página y tenla cerca mientras desarrollas!

