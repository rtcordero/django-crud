# 🎓 Guía Visual para Principiantes

Esta guía te ayudará a entender la **arquitectura DDD** del proyecto paso a paso.

## 📖 Índice

1. [¿Qué hace cada capa?](#qué-hace-cada-capa)
2. [Flujo de una petición completa](#flujo-de-una-petición-completa)
3. [Cómo fluyen los datos](#cómo-fluyen-los-datos)
4. [Ejemplo práctico: Crear una tarea](#ejemplo-práctico-crear-una-tarea)
5. [Ejercicios](#ejercicios)

---

## 🏗️ ¿Qué hace cada capa?

El proyecto está dividido en **4 capas**. Cada capa tiene una responsabilidad clara:

### 📁 API Layer (tasks/api/)
**"Puerta de entrada a la aplicación"**

```
┌─────────────────────────────────────┐
│     API LAYER (tasks/api/)          │
│                                     │
│  ✓ views.py - TaskViewSet          │
│  ✓ serializers.py - Serializers    │
└──────────────┬──────────────────────┘
               │
         HTTP / JSON
               │
         (Validación)
               │
               ▼
```

**¿Qué hace?**
- Recibe peticiones HTTP
- Valida que los datos sean JSON válido
- Convierte JSON a Python (deserialización)
- Convierte Python a JSON (serialización)
- Responde con HTTP

**Ejemplo:**
```python
# tasks/api/views.py
class TaskViewSet(viewsets.ViewSet):
    def create(self, request):
        # Valido que el JSON sea válido
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Paso los datos al servicio
        dto = CreateTaskDTO(**serializer.validated_data)
        task = self.service.create_task(dto)

        # Respondo con JSON
        return Response(TaskSerializer(task).data, status=201)
```

**Responsabilidad:** HTTP y serialización JSON

---

### 🔧 Application Layer (tasks/application/)
**"Cerebro de los casos de uso"**

```
┌─────────────────────────────────────┐
│  APPLICATION LAYER (tasks/app/)     │
│                                     │
│  ✓ services.py - TaskService       │
│  ✓ dto.py - Data Transfer Objects  │
└──────────────┬──────────────────────┘
               │
        (Casos de Uso)
               │
               ▼
```

**¿Qué hace?**
- Orquesta la lógica del dominio
- Convierte entre DTOs y entidades
- Usa el repositorio para persistencia
- Implementa los "casos de uso" del sistema

**Ejemplo:**
```python
# tasks/application/services.py
class TaskService:
    def create_task(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        # 1. Crea entidad del dominio (pura, sin frameworks)
        task = Task(title=dto.title, description=dto.description)

        # 2. Persistir usando repositorio
        saved_task = self.repository.save(task)

        # 3. Devolver DTO con respuesta
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            ...
        )
```

**Responsabilidad:** Casos de uso, orquestación

---

### 🎯 Domain Layer (tasks/domain/)
**"Corazón con la lógica pura"**

```
┌─────────────────────────────────────┐
│   DOMAIN LAYER (tasks/domain/)      │
│                                     │
│  ✓ entities.py - Task Entity       │
│  ✓ exceptions.py - Domain Errors   │
└──────────────┬──────────────────────┘
               │
         (Lógica Pura)
               │
               ▼
```

**¿Qué hace?**
- Define las **entidades** del negocio (Task)
- Contiene **lógica pura** de negocio
- **Sin dependencias** de Django o frameworks
- Fácil de testear

**Ejemplo:**
```python
# tasks/domain/entities.py
@dataclass
class Task:
    title: str
    description: str = ""
    done: bool = False
    id: Optional[int] = None

    def mark_as_done(self) -> None:
        """Lógica pura: marcar como hecho."""
        self.done = True

    def is_completed(self) -> bool:
        """Lógica pura: preguntar si está hecho."""
        return self.done
```

**Responsabilidad:** Lógica de negocio pura

---

### 🏢 Infrastructure Layer (tasks/infrastructure/)
**"Detalles técnicos: la base de datos"**

```
┌─────────────────────────────────────┐
│ INFRASTRUCTURE LAYER (infra/)       │
│                                     │
│  ✓ models.py - Django Models      │
│  ✓ repositories.py - Repository   │
└──────────────┬──────────────────────┘
               │
         (Django ORM)
               │
               ▼
         ┌───────────────┐
         │  db.sqlite3   │
         │  (Base Datos) │
         └───────────────┘
```

**¿Qué hace?**
- Implementa el **Repository pattern**
- Convierte entre entidades y modelos Django
- Maneja la base de datos
- Puedes cambiar BD sin tocar otras capas

**Ejemplo:**
```python
# tasks/infrastructure/repositories.py
class DjangoTaskRepository(TaskRepository):
    def save(self, task: Task) -> Task:
        # Convierte entidad → Modelo Django
        model = TaskModel(
            title=task.title,
            description=task.description,
            done=task.done
        )
        # Guarda en BD
        model.save()

        # Convierte Modelo → Entidad
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            done=model.done
        )
```

**Responsabilidad:** Persistencia, BD, conversiones

---

## 🔄 Flujo de una petición completa

### Visualización del flujo

```
1. CLIENTE
   │
   └─→ POST /tasks/api/v1/tasks/
       {"title": "Comprar leche"}

2. API LAYER (tasks/api/views.py)
   │
   ├─→ TaskViewSet.create(request)
   │
   ├─→ CreateTaskSerializer.validate()
   │   ✓ Valida que title no sea vacío
   │   ✓ Valida que description sea string
   │   ✓ Valida que done sea booleano
   │
   ├─→ Convierte JSON → CreateTaskDTO
   │   CreateTaskDTO(title="Comprar leche", ...)
   │
   └─→ Llama al servicio

3. APPLICATION LAYER (tasks/application/services.py)
   │
   ├─→ TaskService.create_task(dto)
   │
   ├─→ Crea entidad del dominio
   │   task = Task(title="Comprar leche")
   │
   ├─→ Llama repositorio para persistir
   │   saved_task = repository.save(task)
   │
   └─→ Convierte respuesta → TaskResponseDTO
       TaskResponseDTO(id=1, title="Comprar leche", ...)

4. INFRASTRUCTURE LAYER (tasks/infrastructure/repositories.py)
   │
   ├─→ DjangoTaskRepository.save(task)
   │
   ├─→ Convierte entidad → Modelo Django
   │   model = TaskModel(title="Comprar leche")
   │
   ├─→ Guarda en BD
   │   model.save()  # INSERT INTO tasks ...
   │
   └─→ Convierte modelo → Entidad
       task = Task(id=1, title="Comprar leche", ...)

5. Regresa por las capas

   Vuelve a APPLICATION LAYER
   ├─→ Retorna TaskResponseDTO con id=1

   Vuelve a API LAYER
   ├─→ TaskSerializer convierte a JSON
   │   {"id": 1, "title": "Comprar leche", ...}
   │
   └─→ Response HTTP 201 Created

6. CLIENTE
   └─→ Recibe JSON con la tarea creada
```

---

## 🔄 Cómo fluyen los datos

### Entrada: JSON → Entidad

```
JSON (Cliente)
    │
    ▼
Serializer.validate()
    │ Valida formato JSON
    ▼
CreateTaskDTO
    │ Datos validados, limpios
    ▼
Task (Entidad)
    │ Objeto puro del dominio
    ▼
Repository.save()
    │ Persiste en BD
    ▼
TaskModel (Django)
    │
    ▼
DB (SQLite)
```

### Salida: Entidad → JSON

```
DB (SQLite)
    │
    ▼
TaskModel (Django)
    │
    ▼
Task (Entidad)
    │ Objeto del dominio
    ▼
TaskResponseDTO
    │ Datos en DTO
    ▼
TaskSerializer
    │ Valida serialización
    ▼
JSON (Respuesta)
    │
    ▼
Cliente
```

---

## 🎯 Ejemplo práctico: Crear una tarea

### Paso 1: El cliente envía

```bash
curl -X POST http://localhost:8000/tasks/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudiar Django",
    "description": "Tutorial completo",
    "done": false
  }'
```

### Paso 2: API Layer recibe y valida

**En `tasks/api/views.py`:**
```python
class TaskViewSet(viewsets.ViewSet):
    def create(self, request):
        # request.data contiene el JSON
        # {"title": "Estudiar Django", ...}

        # Serializer valida
        serializer = CreateTaskSerializer(data=request.data)

        # Esto valida:
        # ✓ title existe
        # ✓ title no está vacío
        # ✓ description es string
        serializer.is_valid(raise_exception=True)

        # Si hay error, devuelve 400 Bad Request
        # Si es válido, continúa

        dto = CreateTaskDTO(**serializer.validated_data)
        task = self.service.create_task(dto)

        return Response(TaskSerializer(task).data, status=201)
```

### Paso 3: Application Layer orquesta

**En `tasks/application/services.py`:**
```python
class TaskService:
    def create_task(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        # 1. Crear entidad pura
        task = Task(
            title=dto.title,
            description=dto.description,
            done=dto.done
        )

        # 2. Persistir (el repositorio maneja los detalles)
        saved_task = self.repository.save(task)

        # 3. Convertir a DTO para respuesta
        return TaskResponseDTO(
            id=saved_task.id,
            title=saved_task.title,
            description=saved_task.description,
            done=saved_task.done
        )
```

### Paso 4: Infrastructure Layer persiste

**En `tasks/infrastructure/repositories.py`:**
```python
class DjangoTaskRepository(TaskRepository):
    def save(self, task: Task) -> Task:
        # Convertir Task entity → TaskModel (Django)
        model = TaskModel(
            title=task.title,
            description=task.description,
            done=task.done
        )

        # Guardar en base de datos
        model.save()  # ← Django ORM hace el INSERT SQL

        # Convertir TaskModel → Task entity
        return Task(
            id=model.id,
            title=model.title,
            description=model.description,
            done=model.done
        )
```

### Paso 5: Respuesta al cliente

**En `tasks/api/views.py` (regresa):**
```python
# Tenemos el Task entity con id=1
task = Task(id=1, title="Estudiar Django", ...)

# Serializar para JSON
serializer = TaskSerializer(task)
# {"id": 1, "title": "Estudiar Django", ...}

return Response(serializer.data, status=201)
```

### Respuesta final

```json
HTTP 201 Created

{
  "id": 1,
  "title": "Estudiar Django",
  "description": "Tutorial completo",
  "done": false
}
```

---

## 🧪 Ejercicios

### Ejercicio 1: Traza el flujo de GET /tasks/api/v1/tasks/1/

**Pregunta:** ¿Qué métodos se ejecutan en cada capa?

**Respuesta:**
1. **API Layer** → `TaskViewSet.retrieve(request, pk=1)`
2. **Application Layer** → `TaskService.get_task_by_id(1)`
3. **Infrastructure Layer** → `DjangoTaskRepository.get_by_id(1)`
4. **Domain Layer** → Task entity (solo lectura)

### Ejercicio 2: ¿Dónde va la validación?

**Pregunta:** Si quiero validar que el title nunca comience con números, ¿dónde lo hago?

**Respuesta:**
- **API Layer** (Serializer): Para validar el formato HTTP
  ```python
  def validate_title(self, value):
      if value[0].isdigit():
          raise ValidationError("Título no puede comenzar con números")
  ```

- **Domain Layer** (Entity): Para invariantes del negocio
  ```python
  def __post_init__(self):
      if self.title[0].isdigit():
          raise InvalidTaskDataError("...")
  ```

### Ejercicio 3: Cambiar de BD

**Pregunta:** ¿Cuál es la ventaja del Repository pattern?

**Respuesta:**
Para cambiar de SQLite a PostgreSQL:
1. Solo cambias el archivo: `tasks/infrastructure/repositories.py`
2. Creas `PostgresTaskRepository(TaskRepository)`
3. **El resto del código no se toca** ✅

Sin DDD, tendrías que cambiar Views, Serializers, Models, etc.

---

## 💡 Puntos Clave

✅ **API Layer** = HTTP, entrada/salida
✅ **Application Layer** = Lógica de casos de uso
✅ **Domain Layer** = Lógica de negocio pura
✅ **Infrastructure Layer** = BD, persistencia

**Ventaja:** Cada capa tiene UNA responsabilidad clara.

---

**Última actualización:** 2025-11-18
