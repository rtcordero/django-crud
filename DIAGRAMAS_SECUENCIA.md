# 🔄 Diagramas de Secuencia Detallados

Esta guía muestra el flujo exacto de ejecución para cada operación CRUD.

## 📋 Tabla de Contenidos

1. [GET - Listar todas las tareas](#get---listar-todas-las-tareas)
2. [POST - Crear una nueva tarea](#post---crear-una-nueva-tarea)
3. [GET - Obtener una tarea específica](#get---obtener-una-tarea-específica)
4. [PUT - Actualizar una tarea completa](#put---actualizar-una-tarea-completa)
5. [PATCH - Actualizar parcialmente](#patch---actualizar-parcialmente)
6. [DELETE - Eliminar una tarea](#delete---eliminar-una-tarea)

---

## GET - Listar todas las tareas

**URL:** `GET http://localhost:8000/tasks/api/v1/tasks/`

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  GET /tasks/api/v1/tasks/                                     │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ django_crud_api/ │  │
     │                                          │    urls.py       │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Encuentra path('tasks/')
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │    tasks/        │  │
     │                                          │    urls.py       │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Router encuentra 'tasks'
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │    TaskView      │  │
     │                                          │    .list()       │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Ejecuta Task.objects.all()
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   Task Model     │  │
     │                                          │   (ORM Query)    │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          SELECT * FROM tasks_task
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Devuelve [task1, task2, ...]
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          │  (many=True)     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Convierte a JSON      │
     │                                                   │            │
     │  HTTP 200 OK                                      │            │
     │  [{"id":1,"title":"Tarea 1",...}, {...}]          │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**Archivos involucrados (en orden):**
1. `django_crud_api/urls.py` - Enruta a tasks/
2. `tasks/urls.py` - Identifica TaskView
3. `tasks/views.py` - Ejecuta list()
4. `tasks/models.py` - Query a la DB
5. `tasks/serializer.py` - Convierte a JSON

---

## POST - Crear una nueva tarea

**URL:** `POST http://localhost:8000/tasks/api/v1/tasks/`  
**Body:** `{"title": "Nueva tarea", "done": false}`

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  POST /tasks/api/v1/tasks/                                    │
     │  Body: {"title": "Nueva", "done": false}                      │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ TaskView.create()│  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Recibe los datos JSON │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          │ .is_valid()      │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Valida:                │
     │                                          - ¿Existe 'title'?     │
     │                                          - ¿Es string?          │
     │                                          - ¿Menos de 200 chars? │
     │                                          - ¿'done' es boolean?  │
     │                                                   │            │
     │                                          ✅ Validación exitosa │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ serializer.save()│  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Task.objects.create() │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   Task Model     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          INSERT INTO tasks_task │
     │                                          (title, done)         │
     │                                          VALUES ('Nueva', false)│
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Devuelve task con id=3 │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          │ (objeto → JSON)  │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │  HTTP 201 Created                                 │            │
     │  {"id":3,"title":"Nueva","done":false}            │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**Pasos clave:**
1. ✅ Validación de datos (TaskSerializer)
2. 💾 Creación en DB (Task.objects.create)
3. 🔄 Conversión a JSON (TaskSerializer)
4. 📤 Respuesta 201 Created

---

## GET - Obtener una tarea específica

**URL:** `GET http://localhost:8000/tasks/api/v1/tasks/1/`

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  GET /tasks/api/v1/tasks/1/                                   │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ TaskView         │  │
     │                                          │ .retrieve(pk=1)  │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Task.objects.get(id=1)│
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   Task Model     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          SELECT * FROM tasks_task │
     │                                          WHERE id = 1             │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          ¿Existe?              │
     │                                          Sí → Devuelve task   │
     │                                          No → DoesNotExist    │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │  HTTP 200 OK                                      │            │
     │  {"id":1,"title":"Tarea 1","done":true}           │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**Si no existe:**
```
     │  HTTP 404 Not Found                               │            │
     │  {"detail": "Not found."}                         │            │
     │<───────────────────────────────────────────────────────────────│
```

---

## PUT - Actualizar una tarea completa

**URL:** `PUT http://localhost:8000/tasks/api/v1/tasks/1/`  
**Body:** `{"title": "Tarea actualizada", "done": true}`

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  PUT /tasks/api/v1/tasks/1/                                   │
     │  Body: {"title": "Actualizada", "done": true}                 │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ TaskView         │  │
     │                                          │ .update(pk=1)    │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          1. Obtener tarea      │
     │                                          Task.objects.get(id=1)│
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Devuelve task actual  │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          │ .is_valid()      │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          2. Valida nuevos datos│
     │                                          ✅ OK                 │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ serializer.save()│  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          3. Actualiza campos   │
     │                                          task.title = "Actualizada"│
     │                                          task.done = True      │
     │                                          task.save()           │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          UPDATE tasks_task     │
     │                                          SET title='Actualizada', done=true│
     │                                          WHERE id=1            │
     │                                                   │            │
     │  HTTP 200 OK                                      │            │
     │  {"id":1,"title":"Actualizada","done":true}       │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**PUT vs PATCH:**
- **PUT** → Reemplaza **TODOS** los campos (debes enviar todos)
- **PATCH** → Actualiza **SOLO** los campos enviados

---

## PATCH - Actualizar parcialmente

**URL:** `PATCH http://localhost:8000/tasks/api/v1/tasks/1/`  
**Body:** `{"done": true}` (solo un campo)

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  PATCH /tasks/api/v1/tasks/1/                                 │
     │  Body: {"done": true}  ← Solo un campo                        │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ TaskView         │  │
     │                                          │.partial_update() │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Task.objects.get(id=1)│
     │                                                   │            │
     │                                          task = {              │
     │                                            "id": 1,            │
     │                                            "title": "Tarea 1", │
     │                                            "done": false       │
     │                                          }                     │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │ TaskSerializer   │  │
     │                                          │(partial=True)    │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          Solo actualiza 'done' │
     │                                          task.done = True      │
     │                                          task.save()           │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          UPDATE tasks_task     │
     │                                          SET done=true         │
     │                                          WHERE id=1            │
     │                                                   │            │
     │  HTTP 200 OK                                      │            │
     │  {"id":1,"title":"Tarea 1","done":true}           │            │
     │  ↑ title se mantiene                              │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**Ventaja de PATCH:**
- No necesitas enviar todos los campos
- Útil para cambios pequeños (ej: marcar como completada)

---

## DELETE - Eliminar una tarea

**URL:** `DELETE http://localhost:8000/tasks/api/v1/tasks/1/`

```
┌─────────┐                                                      ┌──────────┐
│ Cliente │                                                      │ Servidor │
└────┬────┘                                                      └────┬─────┘
     │                                                                │
     │  DELETE /tasks/api/v1/tasks/1/                                │
     │───────────────────────────────────────────────────────────────>│
     │                                                                │
     │                                          ┌──────────────────┐  │
     │                                          │ TaskView         │  │
     │                                          │ .destroy(pk=1)   │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          1. Obtener tarea      │
     │                                          Task.objects.get(id=1)│
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          ¿Existe?              │
     │                                          Sí → task encontrada  │
     │                                                   │            │
     │                                          2. Eliminar           │
     │                                          task.delete()         │
     │                                                   │            │
     │                                          ┌────────▼─────────┐  │
     │                                          │   db.sqlite3     │  │
     │                                          └────────┬─────────┘  │
     │                                                   │            │
     │                                          DELETE FROM tasks_task│
     │                                          WHERE id=1            │
     │                                                   │            │
     │  HTTP 204 No Content                              │            │
     │  (sin body en la respuesta)                       │            │
     │<───────────────────────────────────────────────────────────────│
     │                                                                │
```

**Códigos de respuesta:**
- **204 No Content** → Eliminado exitosamente (sin body)
- **404 Not Found** → La tarea no existe

---

## 🎯 Resumen de Códigos HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 OK | Éxito | GET, PUT, PATCH exitosos |
| 201 Created | Creado | POST exitoso |
| 204 No Content | Sin contenido | DELETE exitoso |
| 400 Bad Request | Datos inválidos | Validación fallida |
| 404 Not Found | No encontrado | Recurso no existe |
| 500 Server Error | Error del servidor | Error en el código |

## 🔍 Cómo debuggear cada paso

### 1. Ver la petición que llega
```python
# En tasks/views.py
class TaskView(viewsets.ModelViewSet):
    def create(self, request):
        print(f"📥 Datos recibidos: {request.data}")
        return super().create(request)
```

### 2. Ver qué query se ejecuta
```python
# En manage.py shell
from django.db import connection
from tasks.models import Task

Task.objects.all()
print(connection.queries)  # Ver SQL generado
```

### 3. Ver errores de validación
```python
# En tasks/serializer.py
class TaskSerializer(serializers.ModelSerializer):
    def validate(self, data):
        print(f"🔍 Validando: {data}")
        return data
```

### 4. Ver respuesta antes de enviar
```python
# En tasks/views.py
class TaskView(viewsets.ModelViewSet):
    def list(self, request):
        response = super().list(request)
        print(f"📤 Respuesta: {response.data}")
        return response
```

---

**💡 Tip:** Usa la documentación interactiva en `http://localhost:8000/tasks/docs/` para probar estos endpoints fácilmente!

