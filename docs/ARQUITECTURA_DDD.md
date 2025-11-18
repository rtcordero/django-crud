# 🏗️ Arquitectura Domain-Driven Design (DDD)

## Visión General

Este proyecto implementa una **arquitectura en capas basada en Domain-Driven Design (DDD)** para mantener el código limpio, testeable y flexible. La arquitectura separa las responsabilidades en 4 capas principales.

## ¿Por qué DDD?

**Sin DDD (Acoplado):**
```
Request HTTP → View (Django) → Model (ORM) → Serializer → Response
                  ↓
            Lógica de negocio MEZCLADA con detalles técnicos
            Difícil de testear, cambiar BD, o entender el flujo
```

**Con DDD (Desacoplado):**
```
Request HTTP → API Layer → Application Layer → Domain Layer
                ↓              ↓                  ↓
            HTTP/REST      Casos de Uso      Lógica Pura
                              ↓
                        Infrastructure Layer
                              ↓
                         Base de Datos
```

### Beneficios:
- ✅ **Código testeable** - Lógica de negocio sin dependencias de frameworks
- ✅ **Flexible** - Cambiar BD, API, etc. sin tocar la lógica
- ✅ **Mantenible** - Código organizado y fácil de entender
- ✅ **Escalable** - Crece sin volverse caótico

## 📐 Las 4 Capas

### 1. 🎯 Domain Layer (`tasks/domain/`)

**Responsabilidad:** Lógica de negocio pura, independiente de frameworks.

**Archivos:**
- `entities.py` - Entidades del dominio (Task)
- `exceptions.py` - Excepciones de negocio

**Ejemplo - Task Entity:**
```python
@dataclass
class Task:
    title: str
    description: str = ""
    done: bool = False
    id: Optional[int] = None

    def mark_as_done(self) -> None:
        """Marca la tarea como completada."""
        self.done = True
```

**Características:**
- No depende de Django
- No importa de otras capas
- Solo contiene lógica de negocio pura
- Fácil de testear

---

### 2. 🔧 Application Layer (`tasks/application/`)

**Responsabilidad:** Casos de uso que orquestan la lógica del dominio.

**Archivos:**
- `services.py` - Servicios de aplicación (TaskService)
- `dto.py` - Data Transfer Objects

**TaskService - Casos de Uso:**
```python
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, dto: CreateTaskDTO) -> Task:
        # 1. Crear entidad de dominio (pura, sin frameworks)
        task = Task(title=dto.title, description=dto.description)

        # 2. Persistir (usando repositorio)
        saved_task = self.repository.save(task)

        # 3. Retornar entidad de dominio (pura)
        return saved_task
```

**Patrones de DTOs:**
- `CreateTaskDTO` - Datos de entrada desde API
- `UpdateTaskDTO` - Datos para actualizar parcialmente
- `TaskResponseDTO` - Conversión de salida en API Layer

**Características:**
- Orquesta la lógica del dominio
- No contiene lógica de negocio compleja
- Usa repositorio para persistencia
- **Retorna entidades de dominio (Task), no DTOs**
- El API Layer convierte entidades a DTOs para HTTP

---

### 3. 🏢 Infrastructure Layer (`tasks/infrastructure/`)

**Responsabilidad:** Detalles técnicos - base de datos, ORM, configuración.

**Archivos:**
- `models.py` - Modelos Django (para persistencia)
- `repositories.py` - Repository pattern

**Repository Pattern:**
```python
class TaskRepository(ABC):
    """Interfaz del repositorio"""
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

class DjangoTaskRepository(TaskRepository):
    """Implementación con Django ORM"""
    def save(self, task: Task) -> Task:
        # Convertir entidad a modelo Django
        model = TaskModel(title=task.title, ...)
        model.save()
        # Convertir modelo a entidad
        return self._model_to_entity(model)
```

**Ventaja del patrón Repository:**
- Puedes cambiar de BD sin tocar la lógica
- Solo cambias `DjangoTaskRepository` por `PostgresTaskRepository`

**Características:**
- Implementa interfaces del dominio
- Convierte entre modelos Django y entidades
- Encapsula detalles del ORM

---

### 4. 🌐 API Layer (`tasks/api/`)

**Responsabilidad:** HTTP, serialización, validación de entrada.

**Archivos:**
- `views.py` - ViewSets de DRF
- `serializers.py` - Serializers de DRF

**Flujo de una petición POST:**
```python
class TaskViewSet(viewsets.ViewSet):
    def create(self, request):
        # 1. Validar entrada con Serializer
        serializer = CreateTaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # 2. Convertir a DTO de entrada
        dto = CreateTaskDTO(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', '')
        )

        # 3. Usar servicio (Application Layer)
        # Retorna Task entity (dominio puro)
        task_entity = self.service.create_task(dto)

        # 4. Convertir entidad a DTO de respuesta
        response_dto = self._entity_to_dto(task_entity)

        # 5. Serializar respuesta a JSON
        response = TaskSerializer(response_dto)
        return Response(response.data, status=201)
```

**Características:**
- Solo maneja HTTP y serialización
- Delega lógica al servicio
- Convierte entidades a DTOs para respuestas
- No contiene lógica de negocio

---

## 🔄 Flujo de una Petición

### Ejemplo: POST /api/v1/tasks/ (Crear tarea)

```
1. CLIENTE
   │
   ├─→ POST /api/v1/tasks/
       └─→ {"title": "Comprar leche", "description": "Ir al super"}

2. API LAYER (tasks/api/views.py - TaskViewSet)
   │
   ├─→ Validar con CreateTaskSerializer
   ├─→ Convertir a CreateTaskDTO
   └─→ Llamar al servicio

3. APPLICATION LAYER (tasks/application/services.py - TaskService)
   │
   ├─→ Crear entidad Task(title, description)
   ├─→ Llamar al repositorio para persistir
   └─→ Retorna Task entity (dominio puro, sin DTO)

4. INFRASTRUCTURE LAYER (tasks/infrastructure/repositories.py)
   │
   ├─→ Convertir Task entity a TaskModel (Django)
   ├─→ Guardar en base de datos
   └─→ Convertir TaskModel de vuelta a Task entity

5. APPLICATION LAYER (regresa)
   │
   └─→ Retorna Task entity con los datos guardados (id asignado)

6. API LAYER (regresa)
   │
   ├─→ Convertir Task entity → TaskResponseDTO
   ├─→ Serializar TaskResponseDTO con TaskSerializer
   └─→ Response HTTP 201 Created

7. CLIENTE
   └─→ {"id": 3, "title": "Comprar leche", "description": "Ir al super", "done": false}
```

---

## 📁 Estructura de Carpetas

```
tasks/
│
├── domain/                          ← DOMAIN LAYER
│   ├── __init__.py
│   ├── entities.py                 (Entidades puras)
│   └── exceptions.py               (Excepciones de negocio)
│
├── application/                    ← APPLICATION LAYER
│   ├── __init__.py
│   ├── services.py                 (Casos de uso)
│   └── dto.py                      (Data Transfer Objects)
│
├── infrastructure/                 ← INFRASTRUCTURE LAYER
│   ├── __init__.py
│   ├── models.py                   (Modelos Django)
│   └── repositories.py             (Patrón Repository)
│
├── api/                            ← API LAYER
│   ├── __init__.py
│   ├── views.py                    (ViewSets DRF)
│   └── serializers.py              (Serializers DRF)
│
├── migrations/                     (Migraciones Django)
├── admin.py                        (Panel de admin)
├── apps.py                         (Configuración de app)
├── urls.py                         (Rutas URL)
└── tests.py                        (Tests)
```

---

## 🧪 Testing con DDD

Una ventaja clave de DDD es que puedes testear cada capa independientemente:

### Test de Dominio (sin frameworks)
```python
def test_task_can_be_marked_done():
    task = Task(title="Test", done=False)
    task.mark_as_done()
    assert task.done == True
```

### Test de Servicio (sin DB)
```python
def test_create_task_service(mock_repository):
    service = TaskService(mock_repository)
    dto = CreateTaskDTO(title="Test")

    result = service.create_task(dto)

    assert result.title == "Test"
    mock_repository.save.assert_called_once()
```

### Test de API
```python
def test_post_tasks_endpoint(client):
    response = client.post('/api/v1/tasks/', {
        'title': 'Test',
        'description': 'Test task'
    })

    assert response.status_code == 201
    assert response.data['title'] == 'Test'
```

---

## 🔄 Flujos Comunes

### GET /api/v1/tasks/ (Listar)
```
View.list()
  → TaskService.list_all_tasks()
    → DjangoTaskRepository.get_all()
      → TaskModel.objects.all()
      → [Task entity, Task entity, ...]
    → [TaskResponseDTO, TaskResponseDTO, ...]
  → TaskSerializer.to_representation()
  → Response JSON
```

### PUT /api/v1/tasks/1/ (Actualizar)
```
View.update()
  → TaskService.update_task(id, dto)
    → DjangoTaskRepository.get_by_id(id)
      → Task entity (existente)
    → entity.title = dto.title (cambios)
    → DjangoTaskRepository.save(entity)
      → TaskModel.save()
      → Task entity (actualizado)
    → TaskResponseDTO
  → TaskSerializer
  → Response JSON
```

### DELETE /api/v1/tasks/1/
```
View.destroy()
  → TaskService.delete_task(id)
    → DjangoTaskRepository.delete(id)
      → TaskModel.delete()
  → Response 204 No Content
```

---

## 💡 Buenas Prácticas

### ✅ DO: Separa responsabilidades
```python
# BIEN - Cada capa tiene su responsabilidad
class TaskService:
    def create_task(self, dto: CreateTaskDTO) -> TaskResponseDTO:
        task = Task(title=dto.title)  # Domain
        saved = self.repository.save(task)  # Infrastructure
        return TaskResponseDTO(id=saved.id)  # DTO
```

### ❌ DON'T: Mezcles capas
```python
# MAL - Lógica de negocio en la vista
class TaskViewSet:
    def create(self, request):
        if len(request.data.get('title', '')) < 3:  # ¡Lógica en view!
            return error
```

### ✅ DO: Usa DTOs para API
```python
# BIEN - View solo se preocupa por HTTP
class TaskViewSet:
    def create(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateTaskDTO(**serializer.validated_data)
        task = self.service.create_task(dto)
        return Response(TaskSerializer(task).data, status=201)
```

### ✅ DO: Inyecta dependencias
```python
# BIEN - Repositorio inyectado
class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
```

### ❌ DON'T: Importes circulares
```python
# MAL - Domain no debe importar de Application o Infrastructure
from tasks.application.services import TaskService  # ¡No!
```

---

## 🚀 Ventajas en la Práctica

### Antes (Sin DDD)
```python
# test_views.py
from django.test import TestCase
from tasks.models import Task

class TaskViewTest(TestCase):
    def setUp(self):
        # Necesitas DB para testear
        Task.objects.create(title="Test")

    def test_create_task(self):
        # Test lento, depende de BD
        response = self.client.post('/tasks/', {'title': 'Test'})
        self.assertEqual(Task.objects.count(), 2)
```

### Después (Con DDD)
```python
# test_services.py
from tasks.application.services import TaskService
from tasks.application.dto import CreateTaskDTO

class TaskServiceTest:
    def test_create_task(self):
        # Test rápido, sin BD
        mock_repo = Mock()
        service = TaskService(mock_repo)

        dto = CreateTaskDTO(title="Test")
        result = service.create_task(dto)

        assert result.title == "Test"
        mock_repo.save.assert_called_once()
```

---

## 📚 Recursos Útiles

- [Domain-Driven Design - Eric Evans (libro)](https://www.domainlanguage.com/ddd/)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

---

## 🤔 Preguntas Frecuentes

**P: ¿Es DDD overkill para una app pequeña?**
R: Sí, para una TODO list simple. Pero es un buen aprendizaje. En proyectos reales con lógica compleja, vale mucho la pena.

**P: ¿Dónde va la validación?**
R:
- Serializer (API Layer): Validación de formato HTTP
- Service (Application): Validación de reglas de negocio
- Entity (Domain): Invariantes del dominio

**P: ¿Qué pasa si cambio la BD?**
R: Solo cambias `DjangoTaskRepository` por `PostgresTaskRepository`. El resto del código no se toca.

**P: ¿Necesito siempre un Repository?**
R: Para pequeños proyectos, quizá no. Pero te prepara para el futuro y es buena práctica.

---

**Última actualización:** 2025-11-18
