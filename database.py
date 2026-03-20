import sqlite3
import os

DB_PATH = os.path.join("data", "sco.db")

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def agregar_columna_si_no_existe(cursor, tabla, columna, tipo):
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = [col[1] for col in cursor.fetchall()]

    if columna not in columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")


def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT,
        rol TEXT,
        activo INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        codigo TEXT,
        fecha TEXT,
        descripcion TEXT,
        ruta_pdf TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comunicaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        tipo TEXT CHECK(tipo IN ('Enviada','Recibida')),
        medio TEXT,
        asunto TEXT,
        emisor TEXT,
        receptor TEXT,
        documento_id INTEGER,
        controversia_id INTEGER,
        fecha_limite TEXT,
        respondida INTEGER DEFAULT 0,
        ruta_pdf TEXT,
        observaciones TEXT,
        FOREIGN KEY(documento_id) REFERENCES documentos(id),
        FOREIGN KEY(controversia_id) REFERENCES controversias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS controversias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        titulo TEXT,
        descripcion TEXT,
        fecha_inicio TEXT,
        estado TEXT,
        valor_reclamado REAL,
        observaciones TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expediente_documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        controversia_id INTEGER NOT NULL,
        tipo_documento TEXT NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        fecha TEXT,
        ruta_archivo TEXT,
        origen TEXT,
        relevancia TEXT,
        FOREIGN KEY (controversia_id) REFERENCES controversias(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS linea_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        controversia_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        tipo_evento TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        documento_id INTEGER,
        FOREIGN KEY (controversia_id) REFERENCES controversias(id),
        FOREIGN KEY (documento_id) REFERENCES expediente_documentos(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expediente_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        controversia_id INTEGER,
        fecha DATE,
        hito TEXT,
        descripcion TEXT,
        responsable TEXT,
        estado TEXT,
        alerta_dias INTEGER
    )
    """)

    # Actualizar tabla comunicaciones con nuevas columnas
    agregar_columna_si_no_existe(cursor, "comunicaciones", "fecha_llegada", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "radicado_interno", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "radicado_externo", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "especialidad", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "responsable", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "prioridad", "TEXT")
    agregar_columna_si_no_existe(cursor, "comunicaciones", "dias_respuesta", "INTEGER")

    conn.commit()
    conn.close()
