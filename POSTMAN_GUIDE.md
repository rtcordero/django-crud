# 📮 Guía de la Colección de Postman

Esta guía te ayudará a usar la colección de Postman incluida en el proyecto para probar la API de manera eficiente.

## 📥 Instalación

### Requisitos previos
- [Postman Desktop](https://www.postman.com/downloads/) instalado
- Servidor Django ejecutándose (`python manage.py runserver`)

### Pasos para importar

1. **Abre Postman**

2. **Importa la colección:**
   - Haz clic en el botón **"Import"** (esquina superior izquierda)
   - Selecciona **"Upload Files"**
   - Busca y selecciona `postman_collection.json` del proyecto
   - Haz clic en **"Import"**

3. **Verifica la importación:**
   - Deberías ver "Django CRUD API - Tasks" en tu sidebar
   - La colección contiene 13 peticiones organizadas en 3 carpetas

## 📂 Estructura de la colección

```
Django CRUD API - Tasks
├── 📁 Tasks CRUD (6 peticiones)
│   ├── 1. Listar todas las tareas (GET)
│   ├── 2. Crear nueva tarea (POST)
│   ├── 3. Obtener una tarea específica (GET)
│   ├── 4. Actualizar tarea completa (PUT)
│   ├── 5. Actualizar tarea parcial (PATCH)
│   └── 6. Eliminar tarea (DELETE)
├── 📁 Examples - Casos de uso (4 peticiones)
│   ├── Crear tarea sin descripción
│   ├── Marcar tarea como completada
│   ├── Cambiar solo el título
│   └── Crear múltiples tareas
└── 📁 Error Cases - Validaciones (3 peticiones)
    ├── Error: Título vacío
    ├── Error: Tarea no encontrada
    └── Error: Título muy largo
```

## 🚀 Inicio Rápido

### Flujo básico recomendado:

1. **Inicia el servidor Django:**
   ```bash
   python manage.py runserver
   ```

2. **Ejecuta "1. Listar todas las tareas"**
   - Verás el estado inicial de la base de datos
   - Status esperado: 200 OK
   - Respuesta: Array de tareas (puede estar vacío)

3. **Ejecuta "2. Crear nueva tarea"**
   - Se creará una tarea nueva
   - Status esperado: 201 Created
   - **El ID se guarda automáticamente en `task_id`**

4. **Ejecuta "3. Obtener una tarea específica"**
   - Usa el ID guardado automáticamente
   - Status esperado: 200 OK
   - Verás los detalles de la tarea creada

5. **Ejecuta "5. Actualizar tarea parcial (PATCH)"**
   - Marca la tarea como completada
   - Status esperado: 200 OK
   - Solo cambia el campo `done: true`

6. **Ejecuta "1. Listar todas las tareas" nuevamente**
   - Verifica que la tarea está marcada como completada

7. **Ejecuta "6. Eliminar tarea"**
   - Elimina la tarea
   - Status esperado: 204 No Content

## ⚙️ Variables de Entorno

La colección incluye dos variables configuradas:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `base_url` | `http://localhost:8000` | URL base de la API |
| `task_id` | `1` | ID de la tarea (se actualiza automáticamente) |

### Cómo cambiar las variables:

1. **Haz clic en la colección** "Django CRUD API - Tasks"
2. **Ve a la pestaña "Variables"**
3. **Modifica el valor** en la columna "Current value"
4. **Guarda los cambios** (Ctrl+S o botón Save)

### Ejemplo: Cambiar el puerto

Si tu servidor Django está en el puerto 8080:
```
base_url = http://localhost:8080
```

## 🧪 Tests Automáticos

Cada petición incluye tests que se ejecutan automáticamente después de recibir la respuesta.

### Cómo ver los resultados de los tests:

1. **Ejecuta cualquier petición**
2. **Ve a la pestaña "Test Results"** (abajo)
3. **Verás los tests que pasaron ✅ o fallaron ❌**

### Ejemplos de tests incluidos:

#### "1. Listar todas las tareas"
```javascript
✅ Status code is 200
✅ Response is an array
✅ Response time is less than 500ms
```

#### "2. Crear nueva tarea"
```javascript
✅ Status code is 201
✅ Task created successfully
✅ Response has correct structure
💾 Guarda el ID en la variable task_id
```

#### "3. Obtener una tarea específica"
```javascript
✅ Status code is 200
✅ Response has correct structure
✅ ID matches requested ID
```

## 📝 Guía de Peticiones

### 1️⃣ Listar todas las tareas

**Método:** `GET`  
**URL:** `/tasks/api/v1/tasks/`  
**Body:** Ninguno

**Respuesta exitosa (200):**
```json
[
    {
        "id": 1,
        "title": "Aprender Django",
        "description": "Completar tutorial",
        "done": false
    }
]
```

**Cuándo usarla:**
- Ver todas las tareas en el sistema
- Verificar el estado después de crear/actualizar/eliminar
- Obtener IDs de tareas existentes

---

### 2️⃣ Crear nueva tarea

**Método:** `POST`  
**URL:** `/tasks/api/v1/tasks/`  
**Headers:** `Content-Type: application/json`

**Body de ejemplo:**
```json
{
    "title": "Aprender Django REST Framework",
    "description": "Completar el tutorial y crear una API funcional",
    "done": false
}
```

**Campos:**
- `title` (string, requerido, máx 200 caracteres)
- `description` (string, opcional)
- `done` (boolean, opcional, default: false)

**Respuesta exitosa (201):**
```json
{
    "id": 3,
    "title": "Aprender Django REST Framework",
    "description": "Completar el tutorial y crear una API funcional",
    "done": false
}
```

**✨ Característica especial:**
El ID de la tarea creada se guarda automáticamente en `{{task_id}}` para usar en otras peticiones.

---

### 3️⃣ Obtener una tarea específica

**Método:** `GET`  
**URL:** `/tasks/api/v1/tasks/{{task_id}}/`  
**Body:** Ninguno

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "title": "Aprender Django",
    "description": "Completar tutorial",
    "done": false
}
```

**Errores posibles:**
- `404 Not Found` - La tarea no existe

---

### 4️⃣ Actualizar tarea completa (PUT)

**Método:** `PUT`  
**URL:** `/tasks/api/v1/tasks/{{task_id}}/`  
**Headers:** `Content-Type: application/json`

**Body (TODOS los campos requeridos):**
```json
{
    "title": "Aprender Django REST Framework - ACTUALIZADO",
    "description": "Tutorial completado con éxito",
    "done": true
}
```

**⚠️ Importante:**
- PUT requiere enviar **TODOS** los campos
- Si omites un campo, se perderá
- Usa PATCH si solo quieres actualizar algunos campos

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "title": "Aprender Django REST Framework - ACTUALIZADO",
    "description": "Tutorial completado con éxito",
    "done": true
}
```

---

### 5️⃣ Actualizar tarea parcial (PATCH)

**Método:** `PATCH`  
**URL:** `/tasks/api/v1/tasks/{{task_id}}/`  
**Headers:** `Content-Type: application/json`

**Body (solo campos a actualizar):**
```json
{
    "done": true
}
```

**✅ Ventajas:**
- Solo envías los campos que quieres cambiar
- Los demás campos se mantienen intactos
- Ideal para cambios pequeños

**Ejemplos de uso:**
```json
// Solo marcar como completada
{"done": true}

// Solo cambiar título
{"title": "Nuevo título"}

// Cambiar título y descripción
{"title": "Nuevo título", "description": "Nueva descripción"}
```

**Respuesta exitosa (200):**
```json
{
    "id": 1,
    "title": "Aprender Django REST Framework",
    "description": "Tutorial completado",
    "done": true
}
```

---

### 6️⃣ Eliminar tarea

**Método:** `DELETE`  
**URL:** `/tasks/api/v1/tasks/{{task_id}}/`  
**Body:** Ninguno

**Respuesta exitosa (204):**
- Sin contenido en el body
- La tarea se elimina permanentemente

**⚠️ Advertencia:**
Esta acción es **permanente** y no se puede deshacer.

---

## 🎯 Casos de Uso Comunes

### Crear tarea simple (sin descripción)

```json
{
    "title": "Comprar leche",
    "done": false
}
```

### Marcar tarea como completada

**Método:** PATCH  
```json
{
    "done": true
}
```

### Cambiar solo el título

**Método:** PATCH  
```json
{
    "title": "Título actualizado"
}
```

### Crear tareas de prueba rápidamente

Usa la petición **"Crear múltiples tareas"** que incluye `{{$randomInt}}` en el título para generar títulos únicos.

## 🐛 Casos de Error

La carpeta "Error Cases - Validations" incluye ejemplos de peticiones que fallan intencionalmente:

### Error: Título vacío
```json
{
    "title": "",
    "done": false
}
```
**Resultado:** 400 Bad Request

### Error: Tarea no encontrada
**URL:** `/tasks/api/v1/tasks/99999/`  
**Resultado:** 404 Not Found

### Error: Título muy largo
**Título:** 250+ caracteres  
**Resultado:** 400 Bad Request

## 💡 Tips y Trucos

### 1. Ejecutar todas las peticiones en secuencia

1. Haz clic derecho en la carpeta "Tasks CRUD"
2. Selecciona **"Run folder"**
3. Postman ejecutará todas las peticiones en orden
4. Verás un resumen de resultados al final

### 2. Ver el ID guardado

1. Ve a la pestaña **"Console"** (abajo)
2. Después de crear una tarea, verás: `Task ID guardado: 3`

### 3. Cambiar el ID manualmente

Si quieres probar con un ID específico:
1. Ve a Variables de la colección
2. Cambia `task_id` al valor deseado
3. Guarda los cambios

### 4. Exportar respuestas

1. Ejecuta una petición
2. Haz clic derecho en la respuesta
3. Selecciona **"Save Response"**
4. Guarda como archivo JSON

### 5. Ver historial

- Haz clic en **"History"** (sidebar izquierdo)
- Verás todas las peticiones ejecutadas
- Haz clic en cualquiera para repetirla

## 🔍 Debugging

### La petición falla con "Connection refused"

**Problema:** El servidor Django no está ejecutándose.  
**Solución:**
```bash
python manage.py runserver
```

### Error 404 en todas las peticiones

**Problema:** La URL base está mal configurada.  
**Solución:**
1. Verifica que el servidor esté en `http://localhost:8000`
2. Ajusta la variable `base_url` si es necesario

### Los tests fallan

**Problema:** La respuesta no tiene la estructura esperada.  
**Solución:**
1. Ve a la pestaña "Test Results"
2. Lee el error específico
3. Verifica que la base de datos tenga datos

### El ID no se actualiza automáticamente

**Problema:** El script de test no se ejecutó.  
**Solución:**
1. Asegúrate de ejecutar "2. Crear nueva tarea" primero
2. Ve a Console y verifica el mensaje "Task ID guardado"
3. Revisa que los scripts estén habilitados en Postman

## 📊 Códigos de Estado HTTP

| Código | Significado | Cuándo aparece |
|--------|-------------|----------------|
| 200 OK | Éxito | GET, PUT, PATCH exitosos |
| 201 Created | Creado | POST exitoso |
| 204 No Content | Sin contenido | DELETE exitoso |
| 400 Bad Request | Datos inválidos | Validación fallida |
| 404 Not Found | No encontrado | Recurso no existe |
| 500 Server Error | Error del servidor | Error en el código |

## 🎓 Ejercicios Prácticos

### Ejercicio 1: CRUD completo
1. Lista las tareas
2. Crea una tarea nueva
3. Obtén la tarea creada
4. Actualiza la tarea (marca como completada)
5. Lista las tareas (verifica el cambio)
6. Elimina la tarea
7. Lista las tareas (verifica la eliminación)

### Ejercicio 2: Validaciones
1. Intenta crear una tarea sin título
2. Intenta obtener una tarea con ID 999999
3. Intenta crear una tarea con título muy largo
4. Observa los mensajes de error

### Ejercicio 3: Tests automáticos
1. Ejecuta "Run folder" en "Tasks CRUD"
2. Observa qué tests pasan y cuáles fallan
3. Lee los mensajes de error
4. Corrige los problemas si los hay

## 🔗 Recursos Adicionales

- [Documentación de Postman](https://learning.postman.com/docs/getting-started/introduction/)
- [Variables en Postman](https://learning.postman.com/docs/sending-requests/variables/)
- [Tests en Postman](https://learning.postman.com/docs/writing-scripts/test-scripts/)

---

**¿Problemas?** Consulta el [README.md](README.md) principal o las [FAQs](README.md#-preguntas-frecuentes) del proyecto.

**¡Feliz testing! 🚀**

