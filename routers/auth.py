import sqlite3
from fastapi import APIRouter, HTTPException, status
from database import obtener_conexion
from modelos import UsuarioRegistro, UsuarioLogin, UsuarioRespuesta, TokenRespuesta
from seguridad import obtener_hash_password, verificar_password, crear_token_acceso

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioRegistro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    hash_pass = obtener_hash_password(usuario.password)
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?, ?, ?, 'usuario')",
            (usuario.nombre, usuario.email, hash_pass)
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

    cursor.execute("SELECT id, nombre, email, rol FROM usuarios WHERE id = ?", (nuevo_id,))
    nuevo_usuario = dict(cursor.fetchone())
    conexion.close()
    return nuevo_usuario

@router.post("/login", response_model=TokenRespuesta)
def login(credenciales: UsuarioLogin):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (credenciales.email,))
    usuario = cursor.fetchone()
    conexion.close()

    if not usuario or not verificar_password(credenciales.password, usuario["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = crear_token_acceso({
        "sub": usuario["id"],
        "email": usuario["email"],
        "rol": usuario["rol"]
    })
    return {"access_token": token, "token_type": "bearer"}