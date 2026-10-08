# CRUD de productos con FastAPI y PostgreSQL

## Descripción del proyecto

Proyecto orientado a una aplicación Full Stack para gestionar productos mediante operaciones CRUD: crear, listar, consultar, actualizar y eliminar. La implementación presente en este repositorio corresponde al backend REST con FastAPI y PostgreSQL.

**Estado actual:** no existe un directorio `frontend/` ni archivos `package.json` o de configuración de Vite. React es el cliente previsto por la configuración CORS, pero su implementación no está incluida. Las instrucciones de frontend se presentan como referencia condicionada a su incorporación.

## Arquitectura del sistema

El backend organiza el acceso a datos en capas:

**Controller → Service → Repository → SQLAlchemy → PostgreSQL.**

| Capa | Responsabilidad |
|---|---|
| Controller | Define rutas HTTP, valida las entradas con Pydantic, obtiene la sesión de base de datos y serializa respuestas. |
| Service | Aplica reglas de negocio, limpia el nombre y verifica la existencia del producto. |
| Repository | Consulta, guarda, actualiza y elimina entidades; confirma las transacciones. |
| SQLAlchemy | Mapea la clase `Producto` a la tabla `productos` y administra sesiones y conexión. |
| PostgreSQL | Persiste los productos. |

Un cliente React puede consumir la API mediante solicitudes HTTP y JSON. La siguiente comunicación incluye ese cliente previsto; solo el backend y su conexión están implementados.

```mermaid
flowchart LR
    React["React: cliente previsto, no incluido"] -->|HTTP / JSON| Controller["FastAPI: Controller"]
    Controller --> Service
    Service --> Repository
    Repository --> SQLAlchemy
    SQLAlchemy -->|Psycopg| PostgreSQL[(PostgreSQL)]
```

## Tecnologías utilizadas

| Área | Tecnología | Versión declarada / estado |
|---|---|---|
| Backend | Python | Sin versión fijada; el código utiliza sintaxis de Python 3.10 o superior. |
| Backend | FastAPI | `>=0.110,<1` |
| Backend | Uvicorn con extras `standard` | `>=0.29,<1` |
| Backend | SQLAlchemy | `>=2,<3` |
| Backend | Psycopg con extras `binary` | `>=3,<4` |
| Backend | Pydantic | Dependencia transitiva de FastAPI, sin declaración directa; el código usa la API de Pydantic 2. |
| Base de datos | PostgreSQL | Sin versión fijada en el repositorio. |
| Frontend previsto | React, JavaScript y Vite | Sin implementación ni versiones declaradas. |

Los rangos proceden de `backend/requirements.txt`; no hay un archivo de bloqueo de dependencias. Para reproducibilidad conviene fijar versiones compatibles en una mejora posterior.

## Estructura del proyecto

Árbol de los archivos de aplicación presentes, omitiendo entornos virtuales, cachés y metadatos del IDE y de Git:

```text
crud-productos-python/
├── README.md
└── backend/
    ├── main.py
    ├── requirements.txt
    ├── config/
    │   ├── __init__.py
    │   └── database.py
    ├── controllers/
    │   ├── __init__.py
    │   └── producto_controller.py
    ├── models/
    │   ├── __init__.py
    │   └── producto_model.py
    ├── repositories/
    │   ├── __init__.py
    │   └── producto_repository.py
    └── services/
        ├── __init__.py
        └── producto_service.py
```

- `main.py`: crea FastAPI, configura CORS, registra el router y crea tablas al iniciar.
- `config/database.py`: define `DATABASE_URL`, el motor SQLAlchemy, `SessionLocal` y la dependencia `get_db()`.
- `controllers/producto_controller.py`: contiene rutas y DTO de entrada y salida.
- `models/producto_model.py`: declara `Base` y el modelo ORM `Producto`.
- `repositories/producto_repository.py`: implementa persistencia y ordena el listado por ID descendente.
- `services/producto_service.py`: aplica validaciones y genera el error de producto inexistente.
- `requirements.txt`: declara las dependencias del backend.

No hay archivos frontend que puedan describirse o ejecutarse actualmente.

## Requisitos previos

Para el backend: Python compatible con las dependencias instaladas, soporte `venv`, PostgreSQL en ejecución y Git. Python 3.10 es el mínimo que implica la sintaxis del código; no hay una versión de ejecución certificada por el repositorio.

Node.js y npm serán necesarios cuando se incorpore el frontend. Sus versiones mínimas dependerán del `package.json` que se añada.

```bash
python3 --version
python3 -m pip --version
psql --version
git --version
node --version
npm --version
```

En Ubuntu, si faltan herramientas, pueden instalarse mediante los paquetes `python3`, `python3-venv`, `python3-pip`, `postgresql`, `postgresql-client` y `git`. Node.js y npm deben instalarse con versiones compatibles con el futuro frontend.

## Clonar el repositorio

```bash
git clone https://github.com/lvillagran/crud-productos-python.git
cd crud-productos-python
```

La URL corresponde al remoto `origin`. El árbol descrito refleja los archivos locales analizados; los cambios locales deben publicarse para que un clon contenga esa misma implementación.

## Configuración de PostgreSQL

La conexión se configura directamente en `backend/config/database.py`, mediante `DATABASE_URL`; actualmente no se leen variables de entorno ni archivos `.env`.

Ejemplo de configuración que debe adaptar cada desarrollador, sin reutilizar credenciales del repositorio:

```python
DATABASE_URL = (
    "postgresql+psycopg://usuario_ejemplo:CLAVE_DE_EJEMPLO@localhost:5432/productos_db"
)
```

| Parámetro | Ejemplo | Qué configurar |
|---|---|---|
| Host | `localhost` | Servidor que ejecuta PostgreSQL. |
| Puerto | `5432` | Puerto de PostgreSQL. |
| Base de datos | `productos_db` | Base existente destinada a la aplicación. |
| Usuario | `usuario_ejemplo` | Rol con permisos para conectar y crear/usar tablas en el esquema. |
| Contraseña | `CLAVE_DE_EJEMPLO` | Contraseña propia del rol; no publicarla en Git. |

El nombre de base de datos anterior es ilustrativo: la configuración local analizada apunta a otro nombre. Cambie todos los parámetros necesarios. Los caracteres reservados de usuario o contraseña deben codificarse para una URL de conexión.

En una instalación local de PostgreSQL en Ubuntu, un ejemplo de preparación es:

```bash
sudo systemctl start postgresql
sudo -u postgres psql
```

Dentro de `psql`:

```sql
CREATE ROLE usuario_ejemplo WITH LOGIN;
\password usuario_ejemplo
CREATE DATABASE productos_db OWNER usuario_ejemplo;
\q
```

`\password` solicita la contraseña interactivamente. Para verificar la conexión usando los mismos datos elegidos:

```bash
psql -h localhost -p 5432 -U usuario_ejemplo -d productos_db -W -c 'SELECT 1;'
```

Al iniciar FastAPI, el contexto `lifespan` ejecuta `Base.metadata.create_all(bind=engine)`. Esto crea las tablas ausentes, incluida `productos`, pero **la base de datos debe existir previamente**. `create_all()` no aplica migraciones ni modifica automáticamente la estructura de tablas existentes.

La tabla contiene `id` entero generado por identidad, `nombre` de hasta 120 caracteres, `precio` de tipo `NUMERIC(12, 2)` y `stock` entero. Todos los campos de datos son obligatorios. Las restricciones de valores no negativos se aplican en la aplicación; el modelo no declara restricciones SQL `CHECK` para ellas.

## Instalación y ejecución del backend

Desde la raíz del repositorio, después de configurar PostgreSQL:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Estos comandos corresponden a `backend/main.py` y `backend/requirements.txt`. Ejecute Uvicorn desde `backend/` para que se resuelvan los imports locales. `--reload` está destinado al desarrollo.

| Recurso | URL local |
|---|---|
| Bienvenida | http://127.0.0.1:8000/ |
| Estado | http://127.0.0.1:8000/health |
| Productos | http://127.0.0.1:8000/api/productos/ |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Esquema OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

El puerto `8000` y la interfaz `127.0.0.1` corresponden a los valores predeterminados de Uvicorn; el proyecto no los sobrescribe. `/health` devuelve un estado estático y no ejecuta una consulta de comprobación a PostgreSQL.

## Instalación y ejecución del frontend

**Pendiente de implementación:** actualmente los siguientes comandos no pueden ejecutarse con éxito porque no existe `frontend/` ni un `package.json` con el script `dev`:

```bash
# Referencia para cuando se incorpore el frontend y su script dev:
cd frontend
npm install
npm run dev
```

No es posible confirmar scripts, puerto de Vite, proxy ni URL base de la API. El backend permite los orígenes `http://localhost:5173` y `http://127.0.0.1:5173`; esto expresa el origen previsto del cliente, pero no demuestra la existencia de un servidor Vite en ese puerto.

CORS permite `GET`, `POST`, `PUT` y `DELETE`, el encabezado `Content-Type` y no permite credenciales. El futuro cliente deberá apuntar a `http://127.0.0.1:8000/api/productos/` o disponer de un proxy configurado expresamente.

## Endpoints REST

| Método HTTP | Endpoint | Descripción | Código de respuesta |
|---|---|---|---|
| GET | `/` | Mensaje de bienvenida. | `200` |
| GET | `/health` | Estado estático de la API. | `200` |
| GET | `/api/productos/` | Listar productos por ID descendente. | `200` |
| GET | `/api/productos/{producto_id}` | Buscar un producto por ID entero. | `200`, `404`, `422` |
| POST | `/api/productos/` | Crear un producto. | `201`, `422` |
| PUT | `/api/productos/{producto_id}` | Actualizar todos los campos de un producto. | `200`, `404`, `422` |
| DELETE | `/api/productos/{producto_id}` | Eliminar un producto. | `204`, `404`, `422` |

Use la barra final en las rutas de listar y crear para evitar la redirección automática `307` de FastAPI. No existe una ruta `PATCH`.

### Validaciones y formato

`nombre`, `precio` y `stock` son obligatorios tanto en POST como en PUT. El nombre debe tener entre 1 y 120 caracteres; el servicio elimina espacios exteriores y rechaza un nombre compuesto solo por espacios. El precio debe ser finito, no negativo, con hasta 12 dígitos y 2 decimales. El stock debe ser entero y no negativo.

El precio usa `Decimal` y se serializa como **cadena JSON** en las respuestas con Pydantic 2. Los IDs de los ejemplos son ilustrativos; utilice el ID que devuelva su API.

### Crear

`POST /api/productos/`, solicitud:

```json
{"nombre": "Mouse inalámbrico", "precio": "19.99", "stock": 15}
```

Respuesta `201`:

```json
{"nombre": "Mouse inalámbrico", "precio": "19.99", "stock": 15, "id": 1}
```

### Listar

`GET /api/productos/`, sin cuerpo. Respuesta `200`:

```json
[
  {"nombre": "Mouse inalámbrico", "precio": "19.99", "stock": 15, "id": 1}
]
```

Sin registros devuelve `[]`. No hay paginación ni filtros.

### Buscar

`GET /api/productos/1`, sin cuerpo. Respuesta `200`:

```json
{"nombre": "Mouse inalámbrico", "precio": "19.99", "stock": 15, "id": 1}
```

### Actualizar

`PUT /api/productos/1`, solicitud:

```json
{"nombre": "Mouse inalámbrico actualizado", "precio": "24.50", "stock": 10}
```

Respuesta `200`:

```json
{"nombre": "Mouse inalámbrico actualizado", "precio": "24.50", "stock": 10, "id": 1}
```

### Eliminar

`DELETE /api/productos/1`, sin cuerpo. Respuesta `204 No Content`, **sin JSON ni cuerpo de respuesta**. Consultar nuevamente ese ID devuelve `404`.

### Errores HTTP relevantes

- `404`: GET por ID, PUT o DELETE de un producto inexistente:

```json
{"detail": "Producto no encontrado"}
```

- `422`: datos inválidos, campos requeridos ausentes o ID no entero. Los errores de Pydantic usan un arreglo en `detail`; su contenido concreto depende del dato y de la versión instalada. Un nombre compuesto solo por espacios pasa la validación de longitud inicial y el servicio responde:

```json
{"detail": "El nombre del producto es obligatorio"}
```

- `500`: un fallo de persistencia durante una solicitud puede propagarse como error interno; no existe un manejador específico para traducir errores de PostgreSQL. Si la conexión falla durante `create_all()`, la aplicación no completa el arranque.

## Ejecución local

1. **Terminal 1 — PostgreSQL:** inicie el servicio con `sudo systemctl start postgresql`; compruebe `sudo systemctl status postgresql` y ejecute la consulta `SELECT 1` indicada anteriormente. El servicio continúa en segundo plano. Prepare la base y ajuste `DATABASE_URL` antes de arrancar el backend.
2. **Terminal 2 — FastAPI:** desde la raíz, siga los comandos de instalación y ejecución del backend. Mantenga Uvicorn activo. Verifique `curl -i http://127.0.0.1:8000/health` y `curl -i http://127.0.0.1:8000/api/productos/`; la segunda solicitud comprueba además la lectura de la tabla.
3. **Terminal 3 — React, cuando esté disponible:** instale las dependencias y ejecute el script real que se incorpore al frontend. Abra la URL que anuncie Vite y compruebe en la pestaña de red del navegador las llamadas a la API. Este paso no está disponible en el estado actual del repositorio.

## Pruebas de la API

En Swagger UI, abra `/docs`, seleccione una operación, pulse **Try it out**, introduzca el cuerpo o ID y pulse **Execute**. Cree un producto y use su ID para buscar, actualizar y eliminar. Compruebe después el `404` y pruebe un stock negativo para verificar el `422`.

También puede usar `curl` desde otra terminal:

```bash
# Comprobar estado
curl -i http://127.0.0.1:8000/health

# Crear: anote el id devuelto
curl -i -X POST http://127.0.0.1:8000/api/productos/ \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Mouse inalámbrico","precio":"19.99","stock":15}'

# Listar
curl -i http://127.0.0.1:8000/api/productos/

# Sustituya 1 por el id obtenido al crear
curl -i http://127.0.0.1:8000/api/productos/1

# Actualizar
curl -i -X PUT http://127.0.0.1:8000/api/productos/1 \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Mouse actualizado","precio":"24.50","stock":10}'

# Eliminar: debe devolver 204 sin cuerpo
curl -i -X DELETE http://127.0.0.1:8000/api/productos/1

# Consultar el producto eliminado: debe devolver 404
curl -i http://127.0.0.1:8000/api/productos/1

# Validación: debe devolver 422
curl -i -X POST http://127.0.0.1:8000/api/productos/ \
  -H 'Content-Type: application/json' \
  -d '{"nombre":"Mouse","precio":"19.99","stock":-1}'
```

Estas pruebas modifican datos de la base configurada. Los ejemplos describen el contrato del código; no implican que se hayan ejecutado pruebas contra una instancia real de PostgreSQL.

## Solución de problemas frecuentes

| Problema | Comprobación y solución |
|---|---|
| `No module named uvicorn` | Desde `backend/`, active `.venv` con `source .venv/bin/activate` e instale con `python -m pip install -r requirements.txt`. Inicie mediante `python -m uvicorn main:app --reload` para usar el mismo intérprete. |
| Error de conexión a PostgreSQL | Compruebe servicio, host, puerto, rol, contraseña, existencia de la base y permisos del esquema. Pruebe `psql` con los mismos parámetros de `DATABASE_URL`. |
| `ModuleNotFoundError` | Ejecute desde `backend/`, donde está `main.py`, y confirme que usa el entorno virtual correcto. Para módulos externos, reinstale las dependencias declaradas. |
| Puerto 8000 ocupado | Identifique el proceso con `ss -ltnp 'sport = :8000'`; cierre el servicio correspondiente o ejecute `python -m uvicorn main:app --reload --port 8001`. En ese caso, ajuste las URL de prueba y del cliente. |
| Error CORS entre React y FastAPI | El origen debe coincidir exactamente con uno de los dos permitidos, incluido protocolo y puerto. Si el cliente usa otro origen, deberá adaptar `allow_origins` en `main.py`. No hay un proxy Vite incluido. |
| Error de dependencias de npm | Actualmente falta el frontend: un error de directorio o `package.json` ausente no se resuelve reinstalando npm. Cuando exista, compruebe `node --version`, `npm --version` y los requisitos del `package.json`; revise el error antes de reinstalar dependencias. |
| Errores relacionados con Pydantic | El código usa Pydantic 2, pero no lo declara directamente. Compruebe `python -m pip show pydantic` y la compatibilidad de las dependencias instaladas. |
| Cambios de modelo que no aparecen en la base | `create_all()` crea tablas ausentes y no migra tablas existentes. Prepare una migración; no elimine tablas con datos para resolverlo. |

### Problemas de configuración encontrados

- El frontend mencionado en la documentación anterior no está presente; no se pueden confirmar scripts ni configuración de Vite.
- La configuración de conexión contiene credenciales incrustadas. Deben sustituirse por configuración externa antes de publicar; este README no las reproduce.
- `echo=True` en el motor activa el registro de sentencias SQL y parámetros. Revise su uso antes de operar con datos sensibles o desplegar en producción.
- Pydantic 2 se usa en el código sin declararlo directamente en `requirements.txt`.
- No hay migraciones, pruebas automatizadas ni configuración de contenedores entre los archivos analizados.

Estos hallazgos se documentan sin modificar código ni configuraciones.

## Próximas mejoras

Las siguientes son propuestas, **no funcionalidades implementadas**:

- Incorporar el frontend React y su configuración de Vite, URL de API y scripts documentados.
- Añadir autenticación JWT y autorización para las operaciones CRUD.
- Gestionar cambios de esquema con Alembic.
- Incorporar pruebas automatizadas con Pytest para validaciones, servicios y endpoints.
- Añadir Docker y Docker Compose para backend, frontend y PostgreSQL.
- Externalizar credenciales mediante variables de entorno y publicar únicamente un archivo de ejemplo sin secretos.
- Declarar Pydantic 2 explícitamente y fijar dependencias para instalaciones reproducibles.
- Evaluar una integración futura con agentes de inteligencia artificial, definiendo sus permisos y casos de uso antes de implementarla.
