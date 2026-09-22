import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "semilla_del_ermitano_super_secreta_y_privada_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 horas de duración del token

security_scheme = HTTPBearer()

def obtener_hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hash_bytes.decode('utf-8')

def verificar_password(password_plana: str, password_hash: str) -> bool:
    pwd_bytes = password_plana.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)

def crear_token_acceso(datos: dict) -> str:
    a_codificar = datos.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    a_codificar.update({"exp": expiracion})
    return jwt.encode(a_codificar, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No ha iniciado sesión. Debe proporcionar un token válido."
        )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        email: str = payload.get("email")
        rol: str = payload.get("rol")
        
        if sub is None or email is None or rol is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no válido o malformado"
            )
        
        #  Convertir sub de vuelta a int para la app
        return {"id": int(sub), "email": email, "rol": rol}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado. Inicie sesión nuevamente."
        )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token no válido: {str(e)}"
        )

# Exige ser Administrador (403 si es usuario común)
def requerir_admin(usuario_actual: dict = Depends(obtener_usuario_actual)) -> dict:
    if usuario_actual.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requieren permisos de administrador para realizar esta acción"
        )
    return usuario_actual