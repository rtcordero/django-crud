# 🚀 Inicio Rápido - Django CRUD API

Guía rápida para poner en marcha el proyecto en menos de 5 minutos.

## ⚡ Quick Start (5 minutos)

### 1️⃣ Clonar e instalar (2 min)

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd django-crud

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar base de datos (1 min)

```bash
# Aplicar migraciones
python manage.py migrate

# (Opcional) Crear superusuario para admin
python manage.py createsuperuser
```

### 3️⃣ Iniciar servidor (30 seg)

```bash
python manage.py runserver
```

✅ **¡Listo!** El servidor está corriendo en `http://localhost:8000`

### 4️⃣ Verificar (1 min)

Abre tu navegador en estas URLs:

| URL | Descripción |
|-----|-------------|
| http://localhost:8000/tasks/swagger/ | 🎨 **Swagger UI** - Testing interactivo |
| http://localhost:8000/tasks/redoc/ | 📖 **ReDoc** - Documentación elegante |
| http://localhost:8000/tasks/api/v1/tasks/ | 🔌 API REST - Vista DRF |
| http://localhost:8000/admin/ | 🔧 Panel Admin de Django |

## 🎯 Primer Test de la API

### Opción A: Desde Swagger UI (más fácil)

1. Abre http://localhost:8000/tasks/swagger/
2. Expande `POST /tasks/api/v1/tasks/`
3. Click en **"Try it out"**
4. Edita el JSON:
   ```json
   {
     "title": "Mi primera tarea",
     "description": "Probando la API",
     "done": false
   }
   ```
5. Click en **"Execute"**
6. ✅ ¡Deberías ver respuesta 201 Created!

### Opción B: Desde terminal (con curl)

```bash
# Crear una tarea
curl -X POST http://localhost:8000/tasks/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Desde la terminal",
    "done": false
  }'

# Listar todas las tareas
curl http://localhost:8000/tasks/api/v1/tasks/
```

### Opción C: Con Postman

1. Importa `postman_collection.json`
2. Ejecuta "2. Crear nueva tarea"
3. ✅ ¡El ID se guarda automáticamente!

## 📚 ¿Qué hacer después?

### Para aprender el proyecto:

| Si eres... | Lee esto primero |
|-----------|------------------|
| 🆕 **Nuevo en Django** | [GUIA_VISUAL.md](GUIA_VISUAL.md) - Aprende paso a paso |
| 🧪 **Quieres probar la API** | [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) - Usa Swagger UI |
| 📮 **Usas Postman** | [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) - Importa la colección |
| 💻 **Desarrollador experimentado** | [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) - Cheat sheet |
| 🔍 **Quieres entender el flujo** | [DIAGRAMAS_SECUENCIA.md](DIAGRAMAS_SECUENCIA.md) - Flujos detallados |

### Para documentación completa:

📖 **[README.md](README.md)** - Documento principal con todo

## 🎨 Endpoints Disponibles

### API REST

```
GET    /tasks/api/v1/tasks/        - Listar todas
POST   /tasks/api/v1/tasks/        - Crear nueva
GET    /tasks/api/v1/tasks/{id}/   - Obtener una
PUT    /tasks/api/v1/tasks/{id}/   - Actualizar completa
PATCH  /tasks/api/v1/tasks/{id}/   - Actualizar parcial
DELETE /tasks/api/v1/tasks/{id}/   - Eliminar
```

### Documentación Interactiva

```
/tasks/swagger/  - Swagger UI (testing interactivo)
/tasks/redoc/    - ReDoc (documentación elegante)
/tasks/schema/   - OpenAPI 3.0 schema
```

### Admin

```
/admin/  - Panel de administración de Django
```

## 🛠️ Comandos Útiles

```bash
# Iniciar servidor
python manage.py runserver

# Crear migraciones (después de cambios en models.py)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Verificar proyecto
python manage.py check

# Shell interactivo
python manage.py shell

# Limpiar base de datos
rm db.sqlite3
python manage.py migrate
```

## 📦 Dependencias Instaladas

```
✅ Django 5.2.8              - Framework web
✅ djangorestframework 3.16  - API REST
✅ django-cors-headers 4.9   - CORS
✅ drf-spectacular 0.29      - Swagger/OpenAPI 3.0
```

## 🐛 Solución Rápida de Problemas

### Error: "No module named 'xxx'"
```bash
pip install -r requirements.txt
```

### Error: "no such table"
```bash
python manage.py migrate
```

### Error: "Port 8000 already in use"
```bash
# Usar otro puerto
python manage.py runserver 8080

# O matar el proceso
sudo lsof -t -i tcp:8000 | xargs kill -9
```

### No aparece Swagger
```bash
# Verificar que está instalado
pip list | grep spectacular

# Verificar configuración
python manage.py check
```

## 📊 Estructura del Proyecto (Arquitectura DDD)

```
django-crud/
├── manage.py                       # Script principal de Django
├── requirements.txt                # Dependencias
├── db.sqlite3                      # Base de datos
├── README.md                       # 📖 Documentación principal
├── postman_collection.json         # Colección de Postman
│
├── docs/                           # 📚 Documentación
│   ├── README.md                  # 🗺️ Índice de documentación
│   ├── ARQUITECTURA_DDD.md        # 🏗️ Explicación del diseño
│   ├── GUIA_VISUAL.md             # 👨‍🎓 Para principiantes
│   ├── DIAGRAMAS_SECUENCIA.md     # 🔄 Flujos detallados
│   ├── REFERENCIA_RAPIDA.md       # ⚡ Cheat sheet
│   ├── SWAGGER_GUIDE.md           # 🎨 Guía de Swagger
│   └── POSTMAN_GUIDE.md           # 📮 Guía de Postman
│
├── django_crud_api/                # Configuración del proyecto
│   ├── settings.py                # ⚙️ Configuración
│   ├── urls.py                    # 🛣️ URLs principales
│   └── wsgi.py
│
└── tasks/                          # App de tareas (DDD 4 Capas)
    ├── domain/                     # 🎯 Domain Layer (Lógica pura)
    │   ├── entities.py           # Entidades (Task)
    │   ├── exceptions.py         # Excepciones de negocio
    │   └── __init__.py
    │
    ├── application/                # 🔧 Application Layer (Casos de uso)
    │   ├── services.py           # TaskService
    │   ├── dto.py                # DTOs
    │   └── __init__.py
    │
    ├── infrastructure/             # 🏢 Infrastructure Layer (Persistencia)
    │   ├── models.py             # Modelos Django (para BD)
    │   ├── repositories.py       # Repository Pattern
    │   └── __init__.py
    │
    ├── api/                        # 🌐 API Layer (HTTP/REST)
    │   ├── views.py              # TaskViewSet
    │   ├── serializers.py        # Serializers DRF
    │   └── __init__.py
    │
    ├── urls.py                     # 🛣️ URLs de la app
    ├── admin.py                    # 🔧 Config admin
    ├── migrations/                 # 📦 Migraciones Django
    ├── tests.py                    # 🧪 Tests
    └── __init__.py
```

**Nota:** Toda la documentación está en la carpeta `docs/`. Ve allí para aprender el proyecto.

## 🎓 Aprendizaje Progresivo

### Nivel 1: Básico (empiezas aquí)
1. ✅ Inicia el servidor
2. ✅ Abre Swagger UI
3. ✅ Crea una tarea desde Swagger
4. ✅ Lista todas las tareas
5. ✅ Elimina la tarea

### Nivel 2: Intermedio
1. 📖 Lee [GUIA_VISUAL.md](GUIA_VISUAL.md)
2. 🔍 Entiende el flujo de peticiones
3. 📝 Modifica el código (añade un campo)
4. 🧪 Crea migraciones
5. ✅ Prueba los cambios

### Nivel 3: Avanzado
1. 📚 Lee [DIAGRAMAS_SECUENCIA.md](DIAGRAMAS_SECUENCIA.md)
2. 🔧 Personaliza la documentación
3. 🔐 Añade autenticación
4. 🎯 Crea filtros personalizados
5. 🚀 Deploy en producción

## 💡 Tips

### ✅ Hacer
- Usar el entorno virtual siempre
- Ejecutar `check` antes de hacer cambios
- Crear migraciones después de cambios en models
- Probar en Swagger antes de código
- Leer la documentación cuando tengas dudas

### ❌ Evitar
- No commitear `db.sqlite3`
- No usar `DEBUG = True` en producción
- No modificar migraciones aplicadas
- No olvidar actualizar `requirements.txt`
- No ignorar los errores del `check`

## 🎯 Objetivos de Aprendizaje

Después de trabajar con este proyecto, sabrás:

- ✅ Cómo funciona Django REST Framework
- ✅ Qué es una API REST y cómo diseñarla
- ✅ Cómo usar ViewSets y Serializers
- ✅ Qué es OpenAPI/Swagger y cómo usarlo
- ✅ Cómo documentar una API profesionalmente
- ✅ Cómo probar APIs con diferentes herramientas
- ✅ El patrón MVC/MVT en Django
- ✅ Cómo funciona el ORM de Django

## 🔗 Enlaces Rápidos

| Recurso | URL |
|---------|-----|
| Swagger UI | http://localhost:8000/tasks/swagger/ |
| ReDoc | http://localhost:8000/tasks/redoc/ |
| API | http://localhost:8000/tasks/api/v1/tasks/ |
| Admin | http://localhost:8000/admin/ |
| Schema | http://localhost:8000/tasks/schema/ |

## 📞 ¿Necesitas Ayuda?

1. **Revisa el README:** [README.md](README.md)
2. **Consulta los FAQs:** En README.md sección "Preguntas Frecuentes"
3. **Lee la guía específica:** 
   - Swagger → [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md)
   - Postman → [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)
   - Conceptos → [GUIA_VISUAL.md](GUIA_VISUAL.md)
4. **Busca en el índice:** [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)

## 🎉 ¡Listo!

Ahora tienes todo lo necesario para empezar. ¡Abre Swagger y empieza a explorar!

```
🎨 http://localhost:8000/tasks/swagger/
```

**Happy coding! 🚀**

