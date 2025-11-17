# 🎨 Guía de Swagger / OpenAPI 3.0

Esta guía te explica cómo usar la documentación interactiva de la API con **drf-spectacular** (Swagger UI y ReDoc).

## 📊 ¿Por qué drf-spectacular?

**drf-spectacular** es la **mejor opción actual** para documentación de APIs en Django REST Framework:

### ✅ Ventajas sobre otras opciones:

| Característica | drf-spectacular | drf-yasg | CoreAPI (anterior) |
|----------------|-----------------|----------|-------------------|
| OpenAPI version | **3.0** ✅ | 2.0 ⚠️ | Obsoleto ❌ |
| Mantenimiento | Activo ✅ | Limitado ⚠️ | Discontinued ❌ |
| Integración DRF | Excelente ✅ | Buena ⚠️ | Básica ❌ |
| Documentación rica | Sí ✅ | Limitada ⚠️ | Básica ❌ |
| Performance | Alta ✅ | Media ⚠️ | Media ❌ |
| UI modernas | 2 opciones ✅ | 1 opción ⚠️ | 1 opción ❌ |

## 🚀 Acceder a la Documentación

Una vez que el servidor está ejecutándose (`python manage.py runserver`), tienes **3 URLs disponibles**:

### 1. 📄 Schema OpenAPI (JSON/YAML)
```
http://localhost:8000/tasks/schema/
```
**Qué es:** El schema raw en formato OpenAPI 3.0 que describe toda tu API.  
**Uso:** Para importar en otras herramientas, generar clientes automáticos, etc.

### 2. 🎨 Swagger UI (Recomendado)
```
http://localhost:8000/tasks/swagger/
```
**Qué es:** Interfaz interactiva moderna estilo Swagger.  
**Características:**
- ✅ Interfaz limpia y moderna
- ✅ Probar endpoints directamente desde el navegador
- ✅ Ver ejemplos de requests y responses
- ✅ Filtrado y búsqueda de endpoints
- ✅ Visualización de schemas

### 3. 📖 ReDoc (Documentación elegante)
```
http://localhost:8000/tasks/redoc/
```
**Qué es:** Documentación alternativa muy elegante y legible.  
**Características:**
- ✅ Diseño muy limpio y profesional
- ✅ Mejor para lectura que para testing
- ✅ Perfecto para compartir con clientes
- ✅ Navegación por índice lateral
- ✅ Descarga del schema

## 🎯 Swagger UI - Guía de Uso

### Interfaz Principal

Cuando abres `http://localhost:8000/tasks/swagger/`, verás:

```
┌──────────────────────────────────────────────────────────────┐
│  Django CRUD API - Tasks                             v1.0.0  │
│  API REST completa para la gestión de tareas               │
├──────────────────────────────────────────────────────────────┤
│  📦 Schemas   🔐 Authorize   🌍 Servers                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ▼ Tasks                                                     │
│                                                              │
│    GET  /tasks/api/v1/tasks/        Listar todas las tareas │
│    POST /tasks/api/v1/tasks/        Crear nueva tarea       │
│    GET  /tasks/api/v1/tasks/{id}/   Obtener una tarea       │
│    PUT  /tasks/api/v1/tasks/{id}/   Actualizar completa     │
│    PATCH /tasks/api/v1/tasks/{id}/  Actualizar parcial      │
│    DELETE /tasks/api/v1/tasks/{id}/ Eliminar tarea          │
│                                                              │
│  ▼ Schema                                                    │
│    GET  /tasks/schema/              OpenAPI schema          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 🧪 Probar un Endpoint

#### Ejemplo: Crear una tarea

1. **Haz clic en** `POST /tasks/api/v1/tasks/`
2. **Se expande** mostrando:
   - Descripción
   - Parámetros
   - Request body schema
   - Ejemplos
   - Responses

3. **Haz clic en "Try it out"** (botón azul)

4. **Edita el JSON** en el editor:
   ```json
   {
     "title": "Mi primera tarea desde Swagger",
     "description": "Probando la API interactiva",
     "done": false
   }
   ```

5. **Haz clic en "Execute"**

6. **Ver la respuesta:**
   ```
   Code: 201
   Response body:
   {
     "id": 1,
     "title": "Mi primera tarea desde Swagger",
     "description": "Probando la API interactiva",
     "done": false
   }
   ```

### 📋 Ejemplos Pre-cargados

Los endpoints incluyen **ejemplos automáticos**. Por ejemplo, en `POST /tasks/`:

**Ejemplo básico:**
```json
{
  "title": "Comprar leche",
  "description": "Ir al supermercado",
  "done": false
}
```

**Tarea sin descripción:**
```json
{
  "title": "Llamar al médico",
  "done": false
}
```

Solo haz clic en "Example Value" para cargar el ejemplo.

### 🔍 Ver Schemas

Haz clic en "Schemas" (abajo) para ver:

**TaskSerializer:**
```json
{
  "id": 0,                    // integer (read-only)
  "title": "string",          // máximo 200 caracteres (required)
  "description": "string",    // opcional
  "done": true                // boolean (default: false)
}
```

## 📖 ReDoc - Guía de Uso

### Interfaz Principal

Cuando abres `http://localhost:8000/tasks/redoc/`:

```
┌─────────────────────────┬─────────────────────────────────────┐
│                         │                                     │
│  📚 ÍNDICE              │  Django CRUD API - Tasks            │
│                         │  Version 1.0.0                      │
│  📦 Tasks               │                                     │
│    Listar tareas        │  📖 Descripción                     │
│    Crear tarea          │  API REST completa para...          │
│    Obtener tarea        │                                     │
│    Actualizar PUT       │  🔗 Contact                         │
│    Actualizar PATCH     │  📜 License: MIT                    │
│    Eliminar tarea       │                                     │
│                         │  ─────────────────────────────────  │
│  📦 Schema              │                                     │
│    OpenAPI schema       │  ▼ Tasks                            │
│                         │                                     │
│                         │  GET /tasks/api/v1/tasks/          │
│                         │  Listar todas las tareas            │
│                         │                                     │
│                         │  [Descripción detallada]            │
│                         │  [Parámetros]                       │
│                         │  [Respuestas]                       │
│                         │                                     │
└─────────────────────────┴─────────────────────────────────────┘
```

### Características de ReDoc:

- ✅ **Navegación lateral:** Índice fijo para saltar rápido
- ✅ **Diseño elegante:** Perfecto para presentaciones
- ✅ **Código en múltiples lenguajes:** Ejemplos de curl, JavaScript, Python, etc.
- ✅ **Descarga de schema:** Botón para descargar OpenAPI spec
- ✅ **Búsqueda integrada:** Encuentra endpoints rápidamente

## 🎨 Características Implementadas

### 1. Documentación Rica

Cada endpoint tiene:
- ✅ **Summary:** Título corto y descriptivo
- ✅ **Description:** Explicación detallada con Markdown
- ✅ **Tags:** Agrupación lógica (Tasks, Schema)
- ✅ **Examples:** Ejemplos de requests pre-cargados
- ✅ **Responses:** Códigos de estado y schemas

### 2. Metadatos de la API

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Django CRUD API - Tasks',
    'DESCRIPTION': 'API REST completa...',
    'VERSION': '1.0.0',
    'CONTACT': {'name': 'API Support', ...},
    'LICENSE': {'name': 'MIT License'},
}
```

### 3. Schemas Detallados

Cada campo del serializer incluye:
- Tipo de dato
- Si es requerido u opcional
- Valores por defecto
- Help text descriptivo
- Validaciones

### 4. Ejemplos Contextuales

**POST /tasks/ - Crear tarea:**
- Ejemplo básico completo
- Ejemplo sin descripción (campo opcional)

**PATCH /tasks/{id}/ - Actualizar parcial:**
- Marcar como completada (`{"done": true}`)
- Cambiar solo título (`{"title": "Nuevo"}`)

## 💡 Casos de Uso

### 1. Testing rápido de la API
Usa **Swagger UI** para probar endpoints sin escribir código.

### 2. Documentación para clientes
Comparte la URL de **ReDoc** con clientes o frontend developers.

### 3. Generación de clientes
Descarga el schema desde `/tasks/schema/` y genera clientes automáticos:
```bash
# Ejemplo con OpenAPI Generator
openapi-generator-cli generate \
  -i http://localhost:8000/tasks/schema/ \
  -g typescript-axios \
  -o ./client
```

### 4. Importar a Postman
1. Abre Postman
2. Import → Link
3. Pega: `http://localhost:8000/tasks/schema/`
4. ¡Postman importa todos los endpoints automáticamente!

### 5. Validación del schema
Verifica que tu API cumple con OpenAPI 3.0:
```bash
# Con swagger-cli
swagger-cli validate http://localhost:8000/tasks/schema/
```

## 🔧 Personalización

### Cambiar el título o descripción

Edita `django_crud_api/settings.py`:
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Mi API Personalizada',
    'DESCRIPTION': 'Descripción personalizada',
    'VERSION': '2.0.0',
    # ...
}
```

### Añadir documentación a un endpoint

En `tasks/views.py`:
```python
@extend_schema(
    summary="Tu resumen",
    description="Descripción detallada con **Markdown**",
    tags=['MiTag'],
    examples=[
        OpenApiExample(
            'Nombre del ejemplo',
            value={'campo': 'valor'},
            request_only=True,
        ),
    ],
)
def mi_metodo(self, request):
    # ...
```

### Configurar autenticación

En `SPECTACULAR_SETTINGS`:
```python
'SECURITY': [
    {'bearerAuth': []},
],
'COMPONENTS': {
    'securitySchemes': {
        'bearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
        }
    }
}
```

## 🆚 Swagger UI vs ReDoc - ¿Cuál usar?

### Usa Swagger UI cuando:
- ✅ Necesitas **probar** la API interactivamente
- ✅ Estás en **desarrollo** y debugging
- ✅ Quieres **ejecutar requests** desde el navegador
- ✅ Necesitas ver **ejemplos** y copiarlos

### Usa ReDoc cuando:
- ✅ Necesitas **documentación** para presentar
- ✅ Compartes con **clientes** o stakeholders
- ✅ Prefieres una interfaz más **elegante** y legible
- ✅ Solo necesitas **consultar** la documentación

**💡 Tip:** ¡Puedes usar ambas! Están disponibles en URLs diferentes.

## 📊 Comparación con Alternativas

### drf-spectacular (implementado) ✅
```
✅ OpenAPI 3.0
✅ Mantenido activamente
✅ 2 UIs (Swagger + ReDoc)
✅ Personalización completa
✅ Rendimiento excelente
✅ Documentación rica
```

### drf-yasg ⚠️
```
⚠️ OpenAPI 2.0 (obsoleto)
⚠️ Menos mantenido
✅ UI Swagger
✅ Funcional
⚠️ Menos features
```

### CoreAPI (anterior) ❌
```
❌ Deprecated
❌ No mantenido
❌ UI básica
❌ No recomendado
```

## 🎓 Recursos Adicionales

### Documentación oficial:
- [drf-spectacular docs](https://drf-spectacular.readthedocs.io/)
- [OpenAPI 3.0 spec](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc)

### Tutoriales recomendados:
- [DRF Spectacular Tutorial](https://drf-spectacular.readthedocs.io/en/latest/readme.html)
- [OpenAPI Generator](https://openapi-generator.tech/)

## 🐛 Troubleshooting

### Error: "No module named 'drf_spectacular'"
```bash
pip install drf-spectacular
```

### Los cambios no se reflejan
```bash
# Reinicia el servidor
python manage.py runserver
```

### Schema no se genera correctamente
```bash
# Genera el schema manualmente
python manage.py spectacular --file schema.yaml
```

### Error 404 en /tasks/swagger/
Verifica que las URLs estén configuradas correctamente en `tasks/urls.py`:
```python
path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
```

## 🎉 Conclusión

Ahora tienes:
- ✅ **Swagger UI** - Para testing interactivo
- ✅ **ReDoc** - Para documentación elegante  
- ✅ **OpenAPI 3.0** - Schema estándar de la industria
- ✅ **Documentación rica** - Con ejemplos y descripciones
- ✅ **Mejor herramienta** - drf-spectacular sobre alternativas

**URLs rápidas:**
```
🎨 Swagger:  http://localhost:8000/tasks/swagger/
📖 ReDoc:    http://localhost:8000/tasks/redoc/
📄 Schema:   http://localhost:8000/tasks/schema/
```

¡Disfruta de tu documentación interactiva profesional! 🚀

