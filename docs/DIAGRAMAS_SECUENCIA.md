# 🔄 Diagramas de Secuencia Detallados

Esta guía muestra el flujo exacto de ejecución para cada operación CRUD con la arquitectura DDD.

## 📋 Tabla de Contenidos

1. [GET - Listar todas las tareas](#get---listar-todas-las-tareas)
2. [POST - Crear una nueva tarea](#post---crear-una-nueva-tarea)
3. [GET - Obtener una tarea específica](#get---obtener-una-tarea-específica)
4. [PUT - Actualizar una tarea completa](#put---actualizar-una-tarea-completa)
5. [PATCH - Actualizar parcialmente](#patch---actualizar-parcialmente)
6. [DELETE - Eliminar una tarea](#delete---eliminar-una-tarea)
7. [Debugging Tips](#debugging-tips)

---

## GET - Listar todas las tareas

**URL:** `GET http://localhost:8000/tasks/api/v1/tasks/`

**Flujo de 4 capas:**

```
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE                                                         │
│ GET /tasks/api/v1/tasks/                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ API LAYER (tasks/api/views.py - TaskViewSet.list)             │
│                                                                 │
│  1. Recibe HTTP request                                        │
│  2. Llama a self.service.list_all_tasks()                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (tasks/application/services.py)              │
│                                                                 │
│  TaskService.list_all_tasks()                                  │
│  1. Llama self.repository.get_all()                           │
│  2. Convierte [Task entities] → [TaskResponseDTO]             │
│  3. Retorna [TaskResponseDTO, TaskResponseDTO, ...]           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE LAYER (tasks/infrastructure/repositories.py)     │
│                                                                 │
│  DjangoTaskRepository.get_all()                                │
│  1. Ejecuta TaskModel.objects.all()  ← Django ORM            │
│  2. Convierte [TaskModel] → [Task entities]                   │
│  3. Retorna [Task(id=1, title="..."), ...]                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  db.sqlite3          │
              │  SELECT * FROM tasks │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Regresa por las capas                                           │
│                                                                 │
│ Infrastructure → [Task entities]                               │
│      ↓                                                          │
│ Application → [TaskResponseDTO]                                │
│      ↓                                                          │
│ API Layer → TaskSerializer(many=True) → JSON                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE                                                         │
│ HTTP 200 OK                                                    │
│ [                                                               │
│   {"id":1,"title":"Tarea 1","description":"...","done":false}, │
│   {"id":2,"title":"Tarea 2","description":"...","done":true}   │
│ ]                                                               │
└─────────────────────────────────────────────────────────────────┘
```

**Archivos involucrados (en orden):**
1. `django_crud_api/urls.py` - Enruta a tasks/
2. `tasks/urls.py` - Identifica TaskViewSet
3. `tasks/api/views.py` - TaskViewSet.list() → Llama al servicio
4. `tasks/application/services.py` - TaskService.list_all_tasks()
5. `tasks/infrastructure/repositories.py` - DjangoTaskRepository.get_all()
6. `tasks/infrastructure/models.py` - TaskModel.objects.all()
7. `tasks/api/serializers.py` - Serializa a JSON

---

## POST - Crear una nueva tarea

**URL:** `POST http://localhost:8000/tasks/api/v1/tasks/`
**Body:** `{"title": "Nueva tarea", "description": "...", "done": false}`

**Flujo de 4 capas:**

```
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE                                                         │
│ POST /tasks/api/v1/tasks/                                      │
│ Body: {"title": "Comprar leche", "description": "Super"}       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ API LAYER (tasks/api/views.py - TaskViewSet.create)           │
│                                                                 │
│  1. Recibe request.data (JSON)                                │
│  2. CreateTaskSerializer(data=request.data)                   │
│  3. Valida: ✓ title existe ✓ title no vacío ✓ formato OK    │
│  4. Si validación falla → Response 400 Bad Request            │
│  5. Si OK → Convierte a CreateTaskDTO                        │
│  6. Llama self.service.create_task(dto)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (tasks/application/services.py)              │
│                                                                 │
│  TaskService.create_task(dto: CreateTaskDTO)                   │
│  1. Crea entidad pura: Task(title="...", description="...")   │
│  2. Llama self.repository.save(task)                          │
│  3. Convierte Task entity → TaskResponseDTO                   │
│  4. Retorna TaskResponseDTO(id=3, title="...", ...)          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ DOMAIN LAYER (tasks/domain/entities.py)                        │
│                                                                 │
│  Task(title="Comprar leche", ...)                             │
│  - Objeto PURO del dominio (sin Django)                       │
│  - Contiene lógica de negocio                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE LAYER (tasks/infrastructure/repositories.py)     │
│                                                                 │
│  DjangoTaskRepository.save(task: Task)                         │
│  1. Convierte Task entity → TaskModel (Django)                │
│     model = TaskModel(title=task.title, ...)                  │
│  2. Ejecuta model.save()  ← Django ORM                        │
│     INSERT INTO tasks_task (title, description, done)         │
│     VALUES ('Comprar leche', 'Super', false)                  │
│  3. BD retorna id=3                                           │
│  4. Convierte TaskModel → Task entity (con id=3)             │
│  5. Retorna Task(id=3, title="...", ...)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────────────┐
              │  db.sqlite3                  │
              │  INSERT → id=3 asignado      │
              └──────────┬───────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Regresa por las capas                                           │
│                                                                 │
│ Infrastructure → Task(id=3, ...)                               │
│      ↓                                                          │
│ Application → TaskResponseDTO(id=3, ...)                       │
│      ↓                                                          │
│ API Layer → TaskSerializer → JSON                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE                                                         │
│ HTTP 201 Created                                               │
│ {                                                               │
│   "id": 3,                                                      │
│   "title": "Comprar leche",                                    │
│   "description": "Super",                                      │
│   "done": false                                                │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

**Archivos involucrados (en orden):**
1. `tasks/api/views.py` - TaskViewSet.create()
2. `tasks/api/serializers.py` - CreateTaskSerializer.validate()
3. `tasks/application/dto.py` - CreateTaskDTO (datos validados)
4. `tasks/application/services.py` - TaskService.create_task()
5. `tasks/domain/entities.py` - Task (entidad pura)
6. `tasks/infrastructure/repositories.py` - DjangoTaskRepository.save()
7. `tasks/infrastructure/models.py` - TaskModel.save()
8. `tasks/api/serializers.py` - TaskSerializer (serializa respuesta)

---

## GET - Obtener una tarea específica

**URL:** `GET http://localhost:8000/tasks/api/v1/tasks/3/`

**Flujo resumido:**

```
GET /tasks/api/v1/tasks/3/
           ↓
TaskViewSet.retrieve(pk=3)
           ↓
TaskService.get_task_by_id(3)
           ↓
DjangoTaskRepository.get_by_id(3)
           ↓
TaskModel.objects.get(id=3)  ← SELECT * FROM tasks_task WHERE id=3
           ↓
Task entity (id=3, title="...", ...)
           ↓
TaskResponseDTO
           ↓
TaskSerializer → JSON
           ↓
HTTP 200 OK
{
  "id": 3,
  "title": "Comprar leche",
  "description": "Super",
  "done": false
}
```

**Notas especiales:**
- Si `pk` no existe: `TaskNotFoundError` → HTTP 404 Not Found
- Si error en servicio: HTTP 500 Internal Server Error

---

## PUT - Actualizar una tarea completa

**URL:** `PUT http://localhost:8000/tasks/api/v1/tasks/3/`
**Body:** `{"title": "Nuevo título", "description": "Nueva desc", "done": true}`

**Flujo resumido:**

```
PUT /tasks/api/v1/tasks/3/
           ↓
TaskViewSet.update(pk=3, data)
           ↓
CreateTaskSerializer.validate(data)  ← Valida todos los campos
           ↓
UpdateTaskDTO (todos los campos)
           ↓
TaskService.update_task(3, dto)
           ↓
DjangoTaskRepository.get_by_id(3)  ← Obtiene actual
           ↓
Task entity actual (actualizado con nuevos valores)
           ↓
DjangoTaskRepository.save(task)  ← UPDATE
           ↓
TaskResponseDTO
           ↓
HTTP 200 OK con tarea actualizada
```

**Diferencia con PATCH:**
- **PUT:** Requiere TODOS los campos. Si falta uno → Error 400
- **PATCH:** Solo los campos que quieres cambiar

---

## PATCH - Actualizar parcialmente

**URL:** `PATCH http://localhost:8000/tasks/api/v1/tasks/3/`
**Body:** `{"done": true}`

**Flujo resumido:**

```
PATCH /tasks/api/v1/tasks/3/
           ↓
TaskViewSet.partial_update(pk=3, data)
           ↓
UpdateTaskSerializer.validate(data)  ← Valida solo campos presentes
           ↓
UpdateTaskDTO(done=True, title=None, description=None)
           ↓
TaskService.update_task(3, dto)
           ↓
task = DjangoTaskRepository.get_by_id(3)  ← Obtiene actual
task.done = True  ← Solo actualiza este campo
           ↓
DjangoTaskRepository.save(task)  ← UPDATE
           ↓
HTTP 200 OK con tarea actualizada
```

**Acción especial: Mark Done**

```
PATCH /tasks/api/v1/tasks/3/mark_done/
           ↓
TaskViewSet.mark_done(pk=3)
           ↓
TaskService.mark_task_as_done(3)
           ↓
task = DjangoTaskRepository.get_by_id(3)
task.mark_as_done()  ← Método del Domain Entity
           ↓
DjangoTaskRepository.save(task)
           ↓
HTTP 200 OK
```

---

## DELETE - Eliminar una tarea

**URL:** `DELETE http://localhost:8000/tasks/api/v1/tasks/3/`

**Flujo resumido:**

```
DELETE /tasks/api/v1/tasks/3/
           ↓
TaskViewSet.destroy(pk=3)
           ↓
TaskService.delete_task(3)
           ↓
DjangoTaskRepository.delete(3)
           ↓
TaskModel.objects.filter(id=3).delete()  ← DELETE FROM tasks_task WHERE id=3
           ↓
HTTP 204 No Content (sin body)
```

**Códigos HTTP posibles:**
- `204 No Content` - Eliminado exitosamente
- `404 Not Found` - Tarea no existe
- `500 Internal Server Error` - Error en servidor

---

## 🐛 Debugging Tips

### 1. ¿Cómo sé dónde está el error?

**Por HTTP Status Code:**
- `400 Bad Request` → Error en **API Layer** (validación)
- `404 Not Found` → Entidad no existe en **Infrastructure Layer**
- `500 Internal Server Error` → Error en **Application** o **Domain** Layer

### 2. ¿Cómo debuggeo un POST que falla?

**Pasos:**

1. **Verifica el JSON** que estás enviando
   ```bash
   curl -X POST http://localhost:8000/tasks/api/v1/tasks/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Test"}'
   ```

2. **Lee el error** de la respuesta
   ```json
   {"title": ["This field may not be blank."]}
   ```
   → Error en **CreateTaskSerializer**

3. **Revisa tasks/api/serializers.py**
   ```python
   def validate_title(self, value):
       if not value.strip():
           raise ValidationError("El título no puede estar vacío")
   ```

4. **Verifica que el JSON sea válido** - Usa `curl -v` para ver headers

### 3. ¿Cómo debuggeo un PUT/PATCH?

**Mismo proceso:**
1. Verifica el JSON
2. Lee el error
3. Revisa **UpdateTaskSerializer** en `tasks/api/serializers.py`
4. Si llega a servicio, problema en **Application Layer** → Revisa `tasks/application/services.py`

### 4. ¿Cómo debuggeo un 404?

**Significa:** TaskService.get_task_by_id() no encontró el id

**Solución:**
1. Verifica que el id existe: `GET /tasks/api/v1/tasks/`
2. Comprueba que estés usando el id correcto
3. Si el id está bien pero sigue fallando, revisa `tasks/infrastructure/repositories.py`

### 5. ¿Cómo debuggeo un 500?

**Significa:** Error en Domain, Application o Infrastructure Layer

**Cómo encontrarlo:**
1. Mira la consola de Django (donde corre `python manage.py runserver`)
2. Busca el **Traceback** (error en rojo)
3. Lee qué línea falló y en qué archivo
4. Ejemplo:
   ```
   File "tasks/application/services.py", line 45, in create_task
       raise InvalidTaskDataError("Title must not be empty")
   ```

### 6. Usa Swagger para debugging

En lugar de `curl`, usa:
- `http://localhost:8000/tasks/swagger/` ← Interface visual
- Prueba endpoints directamente
- Ver request/response en tiempo real

---

## 🎯 Resumen de Flujos

| Operación | Método | Capa Principal | Archivo Clave |
|-----------|--------|----------------|---------------|
| Listar | GET / | API → App → Infra | services.py → repositories.py |
| Crear | POST / | API → App → Domain → Infra | services.py + entities.py |
| Obtener | GET /:id | API → App → Infra | services.py → repositories.py |
| Actualizar (completo) | PUT /:id | API → App → Domain → Infra | services.py + entities.py |
| Actualizar (parcial) | PATCH /:id | API → App → Domain → Infra | services.py + entities.py |
| Eliminar | DELETE /:id | API → App → Infra | services.py → repositories.py |

---

**Última actualización:** 2025-11-18
