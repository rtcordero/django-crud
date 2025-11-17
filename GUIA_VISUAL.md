# 🎓 Guía Visual para Principiantes

Esta guía te ayudará a entender cómo funciona Django REST Framework paso a paso.

## 📖 Índice

1. [¿Qué hace cada archivo?](#qué-hace-cada-archivo)
2. [Flujo de una petición completa](#flujo-de-una-petición-completa)
3. [Cómo Django procesa las URLs](#cómo-django-procesa-las-urls)
4. [El papel del ORM](#el-papel-del-orm)
5. [Serializers explicados](#serializers-explicados)

## 🗂️ ¿Qué hace cada archivo?

### 📁 django_crud_api/ (Configuración del Proyecto)

```
django_crud_api/
├── settings.py    → Configuración global (DB, apps instaladas, CORS, etc.)
├── urls.py        → Punto de entrada de todas las URLs
├── wsgi.py        → Servidor de producción (no lo tocas normalmente)
└── asgi.py        → Servidor asíncrono (no lo tocas normalmente)
```

**Analogía**: Es como el "tablero de control" de tu proyecto. Aquí defines qué está permitido y qué no.

### 📁 tasks/ (Aplicación de Tareas)

```
tasks/
├── models.py      → Define QUÉ datos guardas (estructura de la tabla)
├── serializer.py  → Define CÓMO se convierten los datos (Python ↔ JSON)
├── views.py       → Define QUÉ hacer con las peticiones (lógica)
├── urls.py        → Define QUÉ rutas maneja esta app
├── admin.py       → Configuración del panel de admin
└── migrations/    → Historial de cambios en la base de datos
```

**Analogía**: Es como un "módulo" independiente que puedes reutilizar en otros proyectos.

## 🔄 Flujo de una petición completa

### Ejemplo: Crear una tarea nueva

#### Paso 1: El cliente envía la petición
```bash
POST http://localhost:8000/tasks/api/v1/tasks/
Content-Type: application/json

{
  "title": "Comprar leche",
  "description": "En el supermercado",
  "done": false
}
```

#### Paso 2: Django recibe y enruta
```
HTTP Request → django_crud_api/urls.py
              ↓
              Encuentra path('tasks/', ...)
              ↓
              Redirige a → tasks/urls.py
              ↓
              Router busca 'tasks' endpoint
              ↓
              Encuentra TaskView
```

#### Paso 3: TaskView procesa
```python
# En tasks/views.py
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer  # ← Sabe cómo validar datos
    queryset = Task.objects.all()      # ← Sabe qué datos buscar
    
# ModelViewSet automáticamente tiene:
# - create()  ← SE EJECUTA ESTE porque es POST
# - list()
# - retrieve()
# - update()
# - destroy()
```

#### Paso 4: TaskSerializer valida
```python
# En tasks/serializer.py
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'done']

# ¿Qué hace el serializer?
# 1. Recibe el JSON del cliente
# 2. Valida que 'title' exista y no sea muy largo
# 3. Valida que 'done' sea un booleano
# 4. Si todo es válido, convierte JSON → objeto Python
```

#### Paso 5: Task Model guarda en la DB
```python
# En tasks/models.py
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)

# Django ORM traduce esto a SQL:
# INSERT INTO tasks_task (title, description, done)
# VALUES ('Comprar leche', 'En el supermercado', false);
```

#### Paso 6: Respuesta al cliente
```python
# El serializer convierte el objeto guardado a JSON
{
  "id": 1,                          # ← Django lo genera automáticamente
  "title": "Comprar leche",
  "description": "En el supermercado",
  "done": false
}

# Status: 201 Created
```

## 🛣️ Cómo Django procesa las URLs

### Configuración en django_crud_api/urls.py
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # → Panel de admin
    path('tasks/', include('tasks.urls')),     # → Delega a tasks/urls.py
]
```

**¿Qué hace `include()`?**
- Toma la URL base (`tasks/`)
- Añade las URLs definidas en `tasks/urls.py`
- Resultado: `tasks/` + `api/v1/tasks/` = `/tasks/api/v1/tasks/`

### Configuración en tasks/urls.py
```python
from rest_framework import routers
from tasks.views import TaskView

router = routers.DefaultRouter()
router.register(r'tasks', TaskView, 'tasks')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('docs/', include_docs_urls(title="Tasks API")),
]
```

**¿Qué hace `DefaultRouter()`?**
Crea automáticamente todas estas rutas:

| URL completa | Método HTTP | Acción en TaskView |
|--------------|-------------|-------------------|
| `/tasks/api/v1/tasks/` | GET | `list()` - Listar todas |
| `/tasks/api/v1/tasks/` | POST | `create()` - Crear una |
| `/tasks/api/v1/tasks/1/` | GET | `retrieve()` - Ver una |
| `/tasks/api/v1/tasks/1/` | PUT | `update()` - Actualizar toda |
| `/tasks/api/v1/tasks/1/` | PATCH | `partial_update()` - Actualizar parte |
| `/tasks/api/v1/tasks/1/` | DELETE | `destroy()` - Eliminar |

## 🗄️ El papel del ORM

**ORM = Object-Relational Mapping** (Mapeo Objeto-Relacional)

### Sin ORM (SQL directo)
```python
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT * FROM tasks WHERE done = 0")
tasks = cursor.fetchall()
conn.close()
```

### Con ORM de Django
```python
from tasks.models import Task

# Mucho más simple y seguro
tasks = Task.objects.filter(done=False)
```

### Operaciones comunes con el ORM

```python
# Crear
task = Task.objects.create(title="Mi tarea", done=False)

# Leer todas
all_tasks = Task.objects.all()

# Filtrar
pending_tasks = Task.objects.filter(done=False)
completed_tasks = Task.objects.filter(done=True)

# Obtener una
task = Task.objects.get(id=1)

# Actualizar
task = Task.objects.get(id=1)
task.done = True
task.save()

# Eliminar
task = Task.objects.get(id=1)
task.delete()
```

**Ventajas del ORM:**
- ✅ Código más legible
- ✅ Protección contra SQL injection
- ✅ Compatible con múltiples bases de datos (SQLite, PostgreSQL, MySQL, etc.)
- ✅ Django maneja las relaciones automáticamente

## 🔄 Serializers explicados

**¿Qué es un Serializer?**
Es un "traductor" entre Python y JSON.

### Flujo de entrada (Cliente → Base de datos)
```
JSON del cliente
    ↓
TaskSerializer
    ↓ (valida)
Objeto Python (Task)
    ↓ (save)
Base de datos
```

### Flujo de salida (Base de datos → Cliente)
```
Base de datos
    ↓
Objeto Python (Task)
    ↓
TaskSerializer
    ↓ (convierte)
JSON al cliente
```

### Ejemplo práctico

```python
# Cliente envía este JSON
{
  "title": "Estudiar",
  "done": false
}

# Serializer lo convierte a esto
task_instance = Task(
    title="Estudiar",
    description="",  # Usa el default
    done=False
)

# Se guarda en la base de datos
task_instance.save()

# Cuando se lee, serializer convierte de vuelta a JSON
{
  "id": 1,
  "title": "Estudiar",
  "description": "",
  "done": false
}
```

### Validaciones del Serializer

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'done']
    
    # Puedes añadir validaciones personalizadas
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "El título debe tener al menos 3 caracteres"
            )
        return value
```

## 🎯 Resumen: Todo junto

```
1. Cliente hace petición HTTP
   ↓
2. django_crud_api/urls.py → Enrutador principal
   ↓
3. tasks/urls.py → Router de la app
   ↓
4. tasks/views.py (TaskView) → Controlador
   ├→ Usa TaskSerializer para validar
   └→ Usa Task Model para acceder a DB
       ↓
5. tasks/models.py (Task) → ORM interactúa con DB
   ↓
6. db.sqlite3 → Base de datos
   ↓
7. Respuesta sube por el mismo camino (convertida a JSON)
   ↓
8. Cliente recibe JSON
```

## 💡 Ejercicios para practicar

### Ejercicio 1: Añadir un campo "priority"
1. Edita `models.py`
2. Edita `serializer.py`
3. Ejecuta `makemigrations` y `migrate`
4. Prueba crear una tarea con prioridad

### Ejercicio 2: Filtrar solo tareas pendientes
En `views.py`:
```python
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(done=False)  # Solo pendientes
```

### Ejercicio 3: Añadir un endpoint personalizado
```python
from rest_framework.decorators import action
from rest_framework.response import Response

class TaskView(viewsets.ModelViewSet):
    # ...código existente...
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Endpoint: GET /tasks/api/v1/tasks/pending/"""
        pending = self.queryset.filter(done=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
```

## 🎓 Próximos pasos

1. **Aprende más sobre querysets**: Filtra, ordena y agrega datos
2. **Añade autenticación**: Protege tu API
3. **Aprende sobre relaciones**: ForeignKey, ManyToMany
4. **Añade paginación**: Para manejar muchos datos
5. **Aprende sobre testing**: Prueba tu API automáticamente

---

**¡Felicidades!** Ahora entiendes cómo funciona Django REST Framework. 🎉

