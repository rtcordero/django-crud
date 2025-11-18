# 📚 Documentación del Proyecto Django CRUD API

Bienvenido al proyecto Django CRUD API. Esta documentación está organizada para ayudarte a entender el proyecto, ya seas principiante o desarrollador experimentado.

## 🗺️ Guía de Navegación

### 🚀 Empieza aquí

**¿Primera vez con el proyecto?**

👉 **Lee primero:** [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md) - ¡En marcha en 5 minutos!
   - Instalación rápida
   - Primer test de la API
   - URLs principales
   - Solución rápida de problemas

### 🎯 Después, continúa con:

1. **[README.md](README.md)** - Tu punto de partida completo
   - Descripción del proyecto
   - Instalación paso a paso
   - Arquitectura y flujo de datos
   - Documentación de la API
   - FAQs

### 📖 Para aprender

#### Si quieres **entender la arquitectura** (⭐ Importante):
👉 **Lee:** [ARQUITECTURA_DDD.md](ARQUITECTURA_DDD.md)
- ¿Por qué DDD?
- Las 4 capas explicadas
- Flujo de datos completo
- Ventajas y buenas prácticas
- Patrones de diseño

#### Si eres **principiante en Django**:
👉 **Empieza con:** [GUIA_VISUAL.md](GUIA_VISUAL.md)
- ¿Qué hace cada capa?
- Flujo de peticiones explicado visualmente
- Cómo fluyen los datos
- Ejemplo práctico paso a paso
- Ejercicios

#### Si necesitas **referencia rápida**:
👉 **Usa:** [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)
- Cheat sheet con comandos
- Queries comunes del ORM
- Patrones principales
- Errores comunes y soluciones

#### Si quieres **entender el flujo detallado**:
👉 **Lee:** [DIAGRAMAS_SECUENCIA.md](DIAGRAMAS_SECUENCIA.md)
- Diagramas de secuencia de cada operación
- GET, POST, PUT, PATCH, DELETE explicados
- Códigos HTTP
- Tips de debugging

## 📂 Estructura de los documentos

```
docs/
│
├── 📄 README.md                    → Este archivo (Índice de documentación)
│
├── 🏗️ ARQUITECTURA_DDD.md          → ARQUITECTURA DEL PROYECTO ⭐ NUEVO
│   ├── ¿Por qué DDD?
│   ├── Las 4 capas (Domain, Application, Infrastructure, API)
│   ├── Flujo de una petición
│   ├── Flujos comunes (GET, POST, PUT, DELETE)
│   ├── Testing con DDD
│   ├── Buenas prácticas
│   └── Preguntas frecuentes
│
├── 📘 GUIA_VISUAL.md               → Aprendizaje paso a paso
│   ├── ¿Qué hace cada capa?
│   ├── Flujo de una petición completa
│   ├── Cómo fluyen los datos (entrada/salida)
│   ├── Ejemplo práctico: Crear una tarea
│   ├── Ejercicios con respuestas
│   └── Puntos clave
│
├── 📙 DIAGRAMAS_SECUENCIA.md       → Flujos detallados
│   ├── GET - Listar tareas
│   ├── POST - Crear tarea
│   ├── GET - Obtener una tarea
│   ├── PUT - Actualizar completa
│   ├── PATCH - Actualizar parcial
│   ├── DELETE - Eliminar
│   └── Debugging tips
│
├── 📗 REFERENCIA_RAPIDA.md         → Consulta rápida
│   ├── Mapa mental del proyecto
│   ├── Cheat sheet de comandos
│   ├── Queries ORM comunes
│   ├── Configuraciones importantes
│   └── Tips profesionales
│
├── 🎨 SWAGGER_GUIDE.md             → Guía de Swagger/OpenAPI 3.0
│   ├── ¿Por qué drf-spectacular?
│   ├── Acceder a la documentación
│   ├── Swagger UI - Guía de uso
│   ├── ReDoc - Guía de uso
│   ├── Características implementadas
│   ├── Casos de uso
│   ├── Personalización
│   └── Comparación con alternativas
│
├── 📮 POSTMAN_GUIDE.md             → Guía completa de Postman
│   ├── Cómo importar la colección
│   ├── Estructura de las peticiones
│   ├── Variables de entorno
│   ├── Tests automáticos
│   ├── Casos de uso comunes
│   ├── Debugging y troubleshooting
│   └── Ejercicios prácticos
│
├── 📮 INICIO_RAPIDO.md             → Comienza en 5 minutos
│   ├── Instalación rápida
│   ├── Primer test de la API
│   ├── URLs principales
│   └── Solución rápida de problemas
│
└── 📊 ../postman_collection.json   → Colección de Postman
    ├── 6 endpoints CRUD principales
    ├── 4 ejemplos de casos de uso
    ├── 3 casos de prueba de errores
    └── Tests automáticos incluidos
```

## 🎓 Rutas de Aprendizaje Sugeridas

### 🌱 Ruta del Principiante (Recomendado)
1. **ARQUITECTURA_DDD.md** → Entiende qué es DDD y por qué existe
2. **GUIA_VISUAL.md** → Ve cómo fluyen los datos en 4 capas
3. **INICIO_RAPIDO.md** → Instala y haz tu primer request
4. **README.md** (root) → Visión general completa
5. **REFERENCIA_RAPIDA.md** → Comandos y patrones que necesites
6. **DIAGRAMAS_SECUENCIA.md** → Entiende flujos detallados

### 🚀 Ruta del Desarrollador con Experiencia
1. **ARQUITECTURA_DDD.md** → Entiende la estructura del proyecto
2. **README.md** (root, sección Arquitectura) → Visión técnica
3. **REFERENCIA_RAPIDA.md** → Referencia rápida de patrones
4. **Código** → Inspecciona tasks/api/, tasks/application/, etc.

### 🔧 Ruta del Mantenimiento
1. **REFERENCIA_RAPIDA.md** → Comandos comunes
2. **README.md** → FAQs para problemas comunes
3. **DIAGRAMAS_SECUENCIA.md** → Debugging y flujos
4. **ARQUITECTURA_DDD.md** → Si necesitas refactorizar

## 💡 ¿Qué buscar en cada documento?

| Pregunta | Documento | Sección |
|----------|-----------|---------|
| ¿Cómo instalo el proyecto? | README.md | Instalación |
| ¿Cómo pruebo la API interactivamente? | docs/SWAGGER_GUIDE.md ⭐ | Swagger UI |
| ¿Cómo uso Swagger? | docs/SWAGGER_GUIDE.md ⭐ | Guía de uso |
| ¿Cómo pruebo la API con Postman? | postman_collection.json + docs/POSTMAN_GUIDE.md | Colección de Postman |
| ¿Qué hace cada archivo? | docs/GUIA_VISUAL.md | ¿Qué hace cada archivo? |
| ¿Cómo funciona una petición GET? | docs/DIAGRAMAS_SECUENCIA.md | GET - Listar tareas |
| ¿Cómo filtro tareas pendientes? | docs/REFERENCIA_RAPIDA.md | Queries comunes |
| ¿Cómo añado un campo nuevo? | README.md | Preguntas Frecuentes |
| ¿Qué comandos Django existen? | docs/REFERENCIA_RAPIDA.md | Comandos más usados |
| ¿Cómo funciona el ORM? | docs/GUIA_VISUAL.md | El papel del ORM |
| ¿Qué hace un Serializer? | docs/GUIA_VISUAL.md | Serializers explicados |
| ¿Cómo debuggeo errores? | docs/DIAGRAMAS_SECUENCIA.md | Cómo debuggear |
| ¿Qué es requirements.txt? | README.md | Gestión de Dependencias |

## 🎯 Objetivos de cada documento

### README.md
**Objetivo:** Proporcionar una visión general completa del proyecto
- ✅ Instalación funcional
- ✅ Entender la arquitectura general
- ✅ Saber usar la API
- ✅ Resolver problemas comunes

### GUIA_VISUAL.md
**Objetivo:** Enseñar cómo funciona Django REST Framework desde cero
- ✅ Entender cada archivo del proyecto
- ✅ Comprender el flujo de datos
- ✅ Aprender conceptos clave (ORM, Serializers)
- ✅ Practicar con ejercicios

### REFERENCIA_RAPIDA.md
**Objetivo:** Ser tu ayuda rápida durante el desarrollo
- ✅ Encontrar comandos rápidamente
- ✅ Recordar patrones comunes
- ✅ Solucionar errores típicos
- ✅ Aplicar buenas prácticas

### DIAGRAMAS_SECUENCIA.md
**Objetivo:** Visualizar el flujo exacto de cada operación
- ✅ Ver paso a paso qué ocurre en cada petición
- ✅ Entender qué código se ejecuta y cuándo
- ✅ Aprender a debuggear problemas
- ✅ Comprender los códigos HTTP

## 🤝 ¿Necesitas ayuda?

1. **Busca en los FAQs** del README.md
2. **Consulta REFERENCIA_RAPIDA.md** para errores comunes
3. **Revisa GUIA_VISUAL.md** para conceptos básicos
4. **Abre un issue** en el repositorio si no encuentras la respuesta

## 🎨 Convenciones en la documentación

- 📁 = Carpeta
- 📄 = Archivo
- 👉 = Recomendación
- ⚠️ = Advertencia importante
- ✅ = Buena práctica
- ❌ = Evitar
- 💡 = Tip útil
- 🔍 = Información adicional

## 📊 Estado de la documentación

- ✅ README.md - Completo
- ✅ GUIA_VISUAL.md - Completo
- ✅ REFERENCIA_RAPIDA.md - Completo
- ✅ DIAGRAMAS_SECUENCIA.md - Completo

Última actualización: 2025-01-17

---

**¡Feliz aprendizaje! 🚀**

*Si esta documentación te resulta útil, considera compartirla con otros desarrolladores.*

