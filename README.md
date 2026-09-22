# 🐉 Dragon Ball Universe API — REST API (GA6)

API RESTful desarrollada con **FastAPI** y **SQLite** para la gestión de planetas y razas del universo de Dragon Ball. El proyecto incluye autenticación basada en **JWT**, encriptación de contraseñas con **Bcrypt** y un esquema de control de acceso por roles (`admin` y `usuario`).

---

## 🚀 Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Base de Datos:** SQLite (`sqlite3`)
* **Seguridad:** PyJWT (Tokens JWT) y Bcrypt (Hashing seguro)
* **Validación de Datos:** Pydantic & `email-validator`
* **Variables de Entorno:** `python-dotenv`

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:
* [Python 3.10](https://www.python.org/) o superior.
* [Git](https://git-scm.com/).

---

## 🛠️ Instalación e Inicialización en una Nueva Computadora

Sigue estos pasos para clonar y ejecutar el proyecto desde cero en cualquier equipo:

### 1. Clonar el repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DE_LA_CARPETA>
```

### 2. Crear el entorno virtual
* **Windows:**
  ```bash
  python -m venv venv
  ```
* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  ```

### 3. Activar el entorno virtual
* **Windows (PowerShell / CMD):**
  ```bash
  .\venv\Scripts\activate
  ```
* **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar las variables de entorno (`.env`)
Crea un archivo llamado `.env` en la raíz del proyecto (junto a `main.py`) con el siguiente contenido:

```env
SECRET_KEY=semilla_del_ermitano_super_secreta_y_privada_2026
DATABASE_NAME=database.db
```

### 6. Iniciar el servidor
```bash
uvicorn main:app --reload
```
Al arrancar por primera vez, la aplicación creará automáticamente la base de datos `database.db` y sembrará los datos iniciales de prueba.

---

## 🔑 Credenciales de Prueba (Datos Iniciales)

El sistema genera de forma automática una cuenta de administrador al ejecutarse por primera vez:

* **Usuario Administrador:**
  * **Email:** `admin@dragonball.com`
  * **Contraseña:** `admin123`
  * **Rol:** `admin`

* **Usuario Estándar:**
  Puedes registrar una cuenta nueva en la ruta `/auth/registro`. Se le asignará automáticamente el rol `usuario`.

---

## 🛡️ Control de Acceso y Respuestas HTTP

* **`200 OK` / `201 Created` / `204 No Content`:** Operaciones exitosas.
* **`400 Bad Request`:** Errores de validación o duplicidad (por ejemplo, intentar crear una raza que ya existe o vincularla a un planeta inexistente).
* **`401 Unauthorized`:** Se devuelve al intentar acceder a rutas protegidas sin haber iniciado sesión o enviando un token vencido/inválido.
* **`403 Forbidden`:** Se devuelve cuando un usuario con rol estándar (`usuario`) intenta ejecutar operaciones reservadas para administradores (`POST`, `PUT`, `DELETE`).
* **`404 Not Found`:** El recurso buscado no existe en la base de datos.

---

## 📌 Tabla de Endpoints

| Módulo | Método | Ruta | Descripción | Requiere Token | Rol Permitido |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Autenticación** | `POST` | `/auth/registro` | Registrar un nuevo usuario | No | Público |
| **Autenticación** | `POST` | `/auth/login` | Iniciar sesión y obtener token JWT | No | Público |
| **Planetas** | `GET` | `/planetas` | Listar todos los planetas | Sí | Usuario / Admin |
| **Planetas** | `GET` | `/planetas/{id}` | Obtener un planeta por ID | Sí | Usuario / Admin |
| **Planetas** | `POST` | `/planetas` | Crear un nuevo planeta | Sí | **Admin** |
| **Planetas** | `PUT` | `/planetas/{id}` | Actualizar un planeta existente | Sí | **Admin** |
| **Planetas** | `DELETE` | `/planetas/{id}` | Eliminar un planeta (si no tiene razas) | Sí | **Admin** |
| **Razas** | `GET` | `/razas` | Listar todas las razas | Sí | Usuario / Admin |
| **Razas** | `GET` | `/razas/{id}` | Obtener una raza por ID | Sí | Usuario / Admin |
| **Razas** | `GET` | `/razas/planeta/{id}` | **Consulta JOIN:** Planeta con sus razas | Sí | Usuario / Admin |
| **Razas** | `POST` | `/razas` | Crear una nueva raza | Sí | **Admin** |
| **Razas** | `PUT` | `/razas/{id}` | Actualizar una raza existente | Sí | **Admin** |
| **Razas** | `DELETE` | `/razas/{id}` | Eliminar una raza | Sí | **Admin** |

---

## 🧪 Cómo probar la API en Swagger UI (`/docs`)

1. Navega a `http://127.0.0.1:8000/docs`.
2. Realiza una petición `POST /auth/login` usando las credenciales de prueba.
3. Copia la cadena generada en el campo `access_token`.
4. Haz clic en el botón verde **Authorize** (arriba a la derecha).
5. Pega **únicamente** la cadena del token (sin escribir la palabra `Bearer`).
6. Presiona **Authorize** y cierra la ventana flotante. Ahora puedes consumir todos los endpoints protegidos según el rol con el que iniciaste sesión.

---

## 🗄️ Visualizar la Base de Datos en VS Code

Para inspeccionar las tablas directamente en Visual Studio Code:
1. Instala la extensión **SQLite Viewer** (de *qwtel* / *Florian Kleinschmidt*).
2. En el explorador de archivos, haz clic derecho sobre `database.db` $\rightarrow$ **Open With...** $\rightarrow$ **SQLite Viewer**.
