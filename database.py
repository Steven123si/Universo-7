import sqlite3

DATABASE_NAME = "database.db"

def obtener_conexion():
    """Obtiene una conexión a la base de datos SQLite."""
    conexion = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row  # Permite leer columnas por nombre
    return conexion

def crear_tablas():
    """Crea las tablas de la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Tabla de Usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'usuario'
        );
    """)

    # 2. Entidad Principal: Planetas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            galaxia TEXT NOT NULL
        );
    """)

    # 3. Entidad Dependiente: Razas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS razas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            fuerza_base INTEGER NOT NULL,
            habilidad_especial TEXT NOT NULL,
            planeta_id INTEGER NOT NULL,
            FOREIGN KEY (planeta_id) REFERENCES planetas(id) ON DELETE RESTRICT
        );
    """)

    conexion.commit()
    conexion.close()

def sembrar_datos():
    """Siembra datos iniciales si la base de datos está vacía."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        from seguridad import obtener_hash_password

        # Usuario administrador inicial
        admin_pass = obtener_hash_password("admin123")
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?, ?, ?, ?)",
            ("Sama Kaioshin", "admin@dragonball.com", admin_pass, "admin")
        )

        # Planetas iniciales (corregido: exactamente 2 valores para 2 '?')
        cursor.execute(
            "INSERT INTO planetas (nombre, galaxia) VALUES (?, ?)",
            ("Vejeta", "Galaxia del Norte")
        )
        cursor.execute(
            "INSERT INTO planetas (nombre, galaxia) VALUES (?, ?)",
            ("Tierra", "Galaxia del Norte")
        )
        cursor.execute(
            "INSERT INTO planetas (nombre, galaxia) VALUES (?, ?)",
            ("Namek", "Galaxia del Norte")
        )

        # Razas iniciales
        cursor.execute(
            "INSERT INTO razas (nombre, fuerza_base, habilidad_especial, planeta_id) VALUES (?, ?, ?, ?)",
            ("Saiyajin", 4000, "Zenikai / Transformación en Ozaru", 1)
        )
        cursor.execute(
            "INSERT INTO razas (nombre, fuerza_base, habilidad_especial, planeta_id) VALUES (?, ?, ?, ?)",
            ("Humano", 5, "Uso avanzado de Ki / Técnicas", 2)
        )
        cursor.execute(
            "INSERT INTO razas (nombre, fuerza_base, habilidad_especial, planeta_id) VALUES (?, ?, ?, ?)",
            ("Namekuseijin", 1500, "Regeneración / Creación de Esferas del Dragón", 3)
        )

        conexion.commit()

    conexion.close()