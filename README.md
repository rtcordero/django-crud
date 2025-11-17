# Django CRUD API - Gestión de Tareas

API REST desarrollada con Django y Django REST Framework para la gestión de tareas (To-Do List).

## 📋 Descripción

Este proyecto implementa una API RESTful completa para gestionar tareas, permitiendo realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre un modelo de tareas. La API incluye documentación automática y está configurada con CORS para integrarse con aplicaciones frontend.

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

## 📞 Contacto

Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio.

---

**Desarrollado con ❤️ usando Django REST Framework**

