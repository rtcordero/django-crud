# Django CRUD API - Gestión de Tareas

API REST desarrollada con Django y Django REST Framework para la gestión de tareas (To-Do List).

## 📋 Descripción

Este proyecto implementa una API RESTful completa para gestionar tareas, permitiendo realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre un modelo de tareas. La API incluye documentación automática y está configurada con CORS para integrarse con aplicaciones frontend.

> 🚀 **¿Quieres empezar YA?** Consulta [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - ¡En marcha en 5 minutos!

> 🎓 **¿Nuevo en Django?** Consulta la [Guía Visual para Principiantes](GUIA_VISUAL.md) para entender cómo funciona el código paso a paso.

## 🚀 Características

- ✅ API REST completa con Django REST Framework
- ✅ Operaciones CRUD para tareas
- ✅ Documentación automática de la API
- ✅ Configuración CORS para aplicaciones frontend
- ✅ Base de datos SQLite
- ✅ Panel de administración de Django

## 🛠️ Tecnologías

- **Python 3.12**
- **Django 5.2.8**
- **Django REST Framework**
- **django-cors-headers**
- **coreapi** (para documentación)
- **SQLite** (base de datos)

## 📦 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd django-crud
```

2. **Crear un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar las migraciones**
```bash
python manage.py migrate
```

5. **Crear un superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

La API estará disponible en `http://localhost:8000`

### ✅ Verificar que todo funciona

1. **Verificar el servidor:**
   - Abre tu navegador en `http://localhost:8000/tasks/api/v1/tasks/`
   - Deberías ver la interfaz de Django REST Framework con una lista vacía

2. **Ver la documentación interactiva:**
   - **Swagger UI:** `http://localhost:8000/tasks/swagger/` - Interfaz moderna para probar la API
   - **ReDoc:** `http://localhost:8000/tasks/redoc/` - Documentación elegante y profesional
   - **Schema:** `http://localhost:8000/tasks/schema/` - OpenAPI 3.0 schema en JSON/YAML

3. **Probar el admin:**
   - Ve a `http://localhost:8000/admin/`
   - Inicia sesión con tu superusuario
   - Crea algunas tareas de prueba

> 📖 **Guía completa de Swagger:** Consulta [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) para aprender a usar la documentación interactiva.

## 🎨 Documentación Interactiva (Swagger / OpenAPI 3.0)

El proyecto incluye **documentación interactiva** generada automáticamente con **drf-spectacular**, la mejor herramienta actual para Django REST Framework.

### 🚀 URLs de Documentación

Una vez el servidor esté ejecutándose:

| URL | Descripción | Mejor para |
|-----|-------------|------------|
| [`/tasks/swagger/`](http://localhost:8000/tasks/swagger/) | **Swagger UI** - Interfaz interactiva moderna | Testing y desarrollo |
| [`/tasks/redoc/`](http://localhost:8000/tasks/redoc/) | **ReDoc** - Documentación elegante | Presentaciones y clientes |
| [`/tasks/schema/`](http://localhost:8000/tasks/schema/) | **OpenAPI 3.0 Schema** | Importar a otras herramientas |

### ✨ Características

- ✅ **Interfaz moderna** estilo Swagger
- ✅ **Prueba endpoints** directamente desde el navegador
- ✅ **Ejemplos de requests** pre-cargados
- ✅ **OpenAPI 3.0** (estándar de la industria)
- ✅ **Documentación rica** con descripciones y validaciones
- ✅ **2 interfaces** (Swagger UI + ReDoc)

### 💡 Ejemplo de uso

1. Abre **Swagger UI:** `http://localhost:8000/tasks/swagger/`
2. Haz clic en `POST /tasks/api/v1/tasks/`
3. Click en **"Try it out"**
4. Edita el JSON y haz click en **"Execute"**
5. ¡Ves la respuesta inmediatamente!

**Sin escribir código**, puedes probar toda la API interactivamente.

> 📚 **Guía completa:** [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) - Aprende a usar Swagger UI, ReDoc y personalizar la documentación.

## 📚 Estructura del Proyecto

```
django-crud/
├── django_crud_api/          # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Configuración WSGI
├── tasks/                    # Aplicación de tareas
│   ├── models.py             # Modelo Task
│   ├── serializer.py         # Serializador de Task
│   ├── views.py              # Vistas de la API
│   ├── urls.py               # URLs de la API
│   └── admin.py              # Configuración del admin
├── db.sqlite3                # Base de datos SQLite
├── manage.py                 # Script de gestión de Django
└── README.md                 # Este archivo
```

## 🏗️ Arquitectura y Flujo de Datos

### Cómo interactúan los componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Frontend/curl)                  │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTP Request
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    django_crud_api/urls.py                       │
│              (Enrutador principal del proyecto)                  │
│         path('tasks/', include('tasks.urls'))                    │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        tasks/urls.py                             │
│              (Enrutador de la app de tareas)                     │
│    router.register(r'tasks', TaskView, 'tasks')                  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        tasks/views.py                            │
│              TaskView(viewsets.ModelViewSet)                     │
│          - Gestiona las peticiones HTTP                          │
│          - Define las operaciones CRUD                           │
└────────────────┬────────────────────────────┬───────────────────┘
                 │                            │
                 │ Usa                        │ Usa
                 ▼                            ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│   tasks/serializer.py        │  │     tasks/models.py          │
│   TaskSerializer             │  │     Task Model               │
│   - Convierte datos entre    │  │     - Define estructura      │
│     JSON y modelo Python     │◄─┤       de la tabla            │
│   - Valida datos             │  │     - Interactúa con DB      │
└──────────────────────────────┘  └────────────┬─────────────────┘
                                               │
                                               │ ORM
                                               ▼
                                  ┌─────────────────────────┐
                                  │     db.sqlite3          │
                                  │   (Base de datos)       │
                                  └─────────────────────────┘
```

### Flujo de una petición típica (Ejemplo: GET /tasks/api/v1/tasks/)

1. **Cliente** → Hace una petición HTTP GET a `/tasks/api/v1/tasks/`

2. **django_crud_api/urls.py** → Recibe la petición y la redirige a `tasks.urls`

3. **tasks/urls.py** → El router identifica que debe usar `TaskView` para `/tasks/`

4. **tasks/views.py (TaskView)** → 
   - Ejecuta el método `list()` (heredado de ModelViewSet)
   - Consulta `Task.objects.all()` al modelo

5. **tasks/models.py (Task)** → 
   - Django ORM traduce la consulta a SQL
   - Recupera los datos de `db.sqlite3`

6. **tasks/serializer.py (TaskSerializer)** → 
   - Convierte los objetos Python en formato JSON
   - Valida y estructura los datos

7. **Respuesta** → Los datos JSON se envían de vuelta al cliente

### Componentes clave explicados

#### 🗂️ models.py (Modelo de Datos)
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
```
**Función**: Define la estructura de la tabla en la base de datos. Cada atributo es una columna.

#### 🔄 serializer.py (Traductor)
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'done']
```
**Función**: Convierte entre objetos Python (Task) y JSON. Valida los datos de entrada/salida.

#### 🎮 views.py (Controlador)
```python
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
```
**Función**: Gestiona la lógica de negocio. ModelViewSet incluye automáticamente:
- `list()` → GET /tasks/ (listar todas)
- `create()` → POST /tasks/ (crear nueva)
- `retrieve()` → GET /tasks/1/ (obtener una)
- `update()` → PUT /tasks/1/ (actualizar completa)
- `partial_update()` → PATCH /tasks/1/ (actualizar parcial)
- `destroy()` → DELETE /tasks/1/ (eliminar)

#### 🛣️ urls.py (Enrutador)
```python
router = routers.DefaultRouter()
router.register(r'tasks', TaskView, 'tasks')
```
**Función**: Mapea las URLs a las vistas. El router automáticamente crea todas las rutas necesarias.

### Ejemplo práctico: Crear una tarea

**1. Cliente envía:**
```bash
POST /tasks/api/v1/tasks/
Content-Type: application/json

{
  "title": "Estudiar Django",
  "description": "Completar tutorial",
  "done": false
}
```

**2. Flujo interno:**
- URLs → Enruta a `TaskView.create()`
- Serializer → Valida el JSON
- View → Llama a `Task.objects.create()`
- Model → Inserta en la base de datos
- Serializer → Convierte el objeto guardado a JSON
- Response → Devuelve status 201 con los datos

**3. Respuesta al cliente:**
```json
{
  "id": 1,
  "title": "Estudiar Django",
  "description": "Completar tutorial",
  "done": false
}
```

## 📦 Gestión de Dependencias

### requirements.txt

El proyecto incluye un archivo `requirements.txt` que contiene todas las dependencias necesarias con sus versiones específicas. Esto garantiza que el proyecto funcione de manera consistente en diferentes entornos.

#### 📥 Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 🔄 Actualizar requirements.txt

⚠️ **Importante**: El archivo `requirements.txt` **NO se actualiza automáticamente**. Debes actualizarlo manualmente cada vez que instales o desinstales dependencias.

**Flujo de trabajo recomendado:**

1. **Instalar una nueva dependencia:**
```bash
pip install nombre-paquete
```

2. **Actualizar requirements.txt manualmente:**
   - Opción A: Añadir la línea manualmente al archivo
   - Opción B: Usar `pip freeze > requirements.txt` (incluye todas las dependencias)

3. **Confirmar cambios:**
```bash
git add requirements.txt
git commit -m "Añadir dependencia: nombre-paquete"
```

#### 📋 Comandos útiles

```bash
# Ver solo paquetes instalados directamente (sin dependencias transitivas)
pip list --not-required

# Ver información de un paquete y sus dependencias
pip show django

# Actualizar una dependencia específica
pip install --upgrade Django

# Desinstalar un paquete
pip uninstall nombre-paquete
```

#### ✅ Buenas prácticas

- **Solo incluir dependencias principales**: Las dependencias transitivas (como `asgiref`, `sqlparse`, etc.) se instalan automáticamente
- **Versiones específicas**: Usar `==` para fijar versiones en producción
- **Comentar el archivo**: Añadir comentarios para explicar para qué sirve cada dependencia
- **Commitear cambios**: Siempre incluir `requirements.txt` en el control de versiones

**Dependencias principales del proyecto:**
- `Django==5.2.8` - Framework web principal
- `djangorestframework==3.16.1` - Para crear la API REST
- `django-cors-headers==4.9.0` - Gestión de CORS para frontend
- `coreapi==2.3.3` - Documentación automática de la API

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks/api/v1/tasks/` | Listar todas las tareas |
| POST | `/tasks/api/v1/tasks/` | Crear una nueva tarea |
| GET | `/tasks/api/v1/tasks/{id}/` | Obtener una tarea específica |
| PUT | `/tasks/api/v1/tasks/{id}/` | Actualizar una tarea completa |
| PATCH | `/tasks/api/v1/tasks/{id}/` | Actualizar parcialmente una tarea |
| DELETE | `/tasks/api/v1/tasks/{id}/` | Eliminar una tarea |

### Documentación interactiva
```
http://localhost:8000/tasks/docs/
```

## 📝 Modelo de Datos

### Task (Tarea)

```python
{
    "id": 1,                          # Integer (auto-generado)
    "title": "Mi tarea",              # String (máx. 200 caracteres)
    "description": "Descripción...",  # String (opcional)
    "done": false                     # Boolean (default: false)
}
```

## 💡 Ejemplos de Uso

### Listar todas las tareas
```bash
curl -X GET http://localhost:8000/tasks/api/v1/tasks/
```

### Crear una nueva tarea
```bash
curl -X POST http://localhost:8000/tasks/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender Django",
    "description": "Completar el tutorial de Django REST Framework",
    "done": false
  }'
```

### Actualizar una tarea
```bash
curl -X PUT http://localhost:8000/tasks/api/v1/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender Django",
    "description": "Tutorial completado",
    "done": true
  }'
```

### Eliminar una tarea
```bash
curl -X DELETE http://localhost:8000/tasks/api/v1/tasks/1/
```

## 📮 Colección de Postman

El proyecto incluye una colección completa de Postman para probar todos los endpoints de la API fácilmente.

### 📥 Importar la colección

1. **Abre Postman**
2. **Haz clic en "Import"** (botón en la esquina superior izquierda)
3. **Selecciona el archivo** `postman_collection.json` de este repositorio
4. **¡Listo!** La colección aparecerá en tu sidebar

### 🎯 Contenido de la colección

#### **Tasks CRUD** (6 endpoints principales)
1. ✅ **Listar todas las tareas** - GET con tests automáticos
2. ✅ **Crear nueva tarea** - POST (guarda el ID automáticamente)
3. ✅ **Obtener una tarea específica** - GET con validación
4. ✅ **Actualizar tarea completa** - PUT con todos los campos
5. ✅ **Actualizar tarea parcial** - PATCH solo campos específicos
6. ✅ **Eliminar tarea** - DELETE con confirmación

#### **Examples - Casos de uso** (4 ejemplos)
- Crear tarea sin descripción
- Marcar tarea como completada
- Cambiar solo el título
- Crear múltiples tareas (con datos aleatorios)

#### **Error Cases - Validaciones** (3 casos de prueba)
- Error: Título vacío (400)
- Error: Tarea no encontrada (404)
- Error: Título muy largo (400)

### ⚙️ Variables incluidas

La colección incluye estas variables configuradas:
- `base_url`: `http://localhost:8000` (editable)
- `task_id`: Se actualiza automáticamente al crear una tarea

### 🚀 Cómo usar la colección

1. **Inicia el servidor Django:**
   ```bash
   python manage.py runserver
   ```

2. **Ejecuta las peticiones en orden:**
   - Primero "Listar todas las tareas" para ver el estado inicial
   - Luego "Crear nueva tarea" (guarda el ID automáticamente)
   - Las demás peticiones usarán el ID guardado

3. **Tests automáticos:**
   - Cada petición incluye tests que se ejecutan automáticamente
   - Ve los resultados en la pestaña "Test Results"
   - Los tests validan códigos de estado, estructura de respuesta, etc.

### 💡 Características especiales

- ✅ **Tests automáticos** en cada endpoint
- ✅ **Variables dinámicas** - El ID se guarda automáticamente
- ✅ **Documentación completa** en cada petición
- ✅ **Ejemplos de body** para cada operación
- ✅ **Casos de error** para testing de validaciones
- ✅ **Datos aleatorios** con `{{$randomInt}}` para testing

### 📝 Ejemplo de uso rápido

1. Importa la colección
2. Ejecuta "Crear nueva tarea"
3. El `task_id` se guarda automáticamente
4. Ejecuta cualquier otra petición - usará el ID guardado
5. Ve los tests pasar en verde ✅

### 🔄 Cambiar el servidor

Si tu servidor Django está en otro puerto o dominio:

1. Haz clic en la colección
2. Ve a la pestaña "Variables"
3. Cambia `base_url` a tu URL (ej: `http://localhost:8080`)

## 🔧 Configuración

### CORS

Para permitir solicitudes desde un frontend específico, modifica el archivo `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React, Vue, etc.
    "http://localhost:5173",  # Vite
]
```

### Base de datos

Por defecto, el proyecto usa SQLite. Para usar PostgreSQL o MySQL, modifica la configuración en `settings.py`.

## 🎯 Panel de Administración

Accede al panel de administración de Django en:
```
http://localhost:8000/admin/
```

Usa las credenciales del superusuario creado anteriormente.

## 🧪 Testing

Para ejecutar las pruebas:
```bash
python manage.py test
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## ❓ Preguntas Frecuentes

### ¿Cómo añado un nuevo campo al modelo Task?

1. Edita `tasks/models.py` y añade el campo:
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    done = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)  # Nuevo campo
```

2. Actualiza el serializador en `tasks/serializer.py`:
```python
fields = ['id', 'title', 'description', 'done', 'priority']
```

3. Crea y aplica la migración:
```bash
python manage.py makemigrations
python manage.py migrate
```

### ¿Cómo cambio el puerto del servidor?

```bash
python manage.py runserver 8080
# O especifica también la IP
python manage.py runserver 0.0.0.0:8080
```

### ¿Por qué no funciona CORS con mi frontend?

Añade el origen de tu frontend en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Tu frontend
]
```

### ¿Cómo añado autenticación a la API?

Django REST Framework incluye varios tipos de autenticación. En `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

### ¿Cómo limpio la base de datos?

```bash
# Opción 1: Eliminar y recrear
rm db.sqlite3
python manage.py migrate

# Opción 2: Usar la shell de Django
python manage.py shell
>>> from tasks.models import Task
>>> Task.objects.all().delete()
```

### ¿Dónde veo los logs de errores?

Los errores aparecen en la consola donde ejecutaste `runserver`. Para logs más detallados, configura logging en `settings.py`.

## 🔗 Recursos Adicionales

### 📚 Documentación del proyecto

#### Para probar la API:
- **[Guía de Swagger/OpenAPI](SWAGGER_GUIDE.md)** ⭐ **NUEVO**
  - Cómo usar Swagger UI y ReDoc
  - Comparación con alternativas (drf-yasg, CoreAPI)
  - Personalización y configuración
  - Testing interactivo desde el navegador
  
- **[Guía de Postman](POSTMAN_GUIDE.md)** 
  - Cómo importar y usar la colección
  - Guía completa de cada endpoint
  - Variables y tests automáticos
  - Casos de uso y ejercicios prácticos

#### Para principiantes:
- **[Guía Visual para Principiantes](GUIA_VISUAL.md)** 
  - Explicación detallada de cada archivo y su función
  - Flujo completo de peticiones paso a paso
  - Cómo funciona el ORM de Django
  - Ejemplos prácticos y ejercicios

#### Para consulta rápida:
- **[Referencia Rápida](REFERENCIA_RAPIDA.md)** 
  - Cheat sheet con diagramas ASCII
  - Comandos Django más usados
  - Queries comunes del ORM
  - Solución a errores comunes

#### Para entender el flujo detallado:
- **[Diagramas de Secuencia](DIAGRAMAS_SECUENCIA.md)** 
  - Flujo detallado de cada operación CRUD
  - Diagramas de secuencia para GET, POST, PUT, PATCH, DELETE
  - Códigos HTTP explicados
  - Tips para debugging

### 🌐 Documentación oficial
- [Documentación de Django](https://docs.djangoproject.com/)
- [Documentación de Django REST Framework](https://www.django-rest-framework.org/)
- [Tutorial oficial de Django](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
- [Guía de Django REST Framework](https://www.django-rest-framework.org/tutorial/quickstart/)

## 📞 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio.

---

**Desarrollado con ❤️ usando Django REST Framework**

