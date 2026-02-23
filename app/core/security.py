from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import os
from pydantic import BaseModel

# Configuración
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    email: str
    rol: str
    id: int


def verificar_contraseña(contraseña_plana: str, hash_contraseña: str) -> bool:
    """Verifica que la contraseña coincida con el hash o con texto plano"""
    if not contraseña_plana or not hash_contraseña:
        return False
    
    # Si la contraseña almacenada es texto plano (para demo)
    if not '$' in hash_contraseña:
        return contraseña_plana == hash_contraseña
    
    try:
        # Extraer el salt y el hash
        salt, hash_almacenado = hash_contraseña.rsplit('$', 1)
        # Recrear el hash con el salt y la contraseña plana
        hash_calculado = hashlib.pbkdf2_hmac('sha256', contraseña_plana.encode(), salt.encode(), 100000).hex()
        return hash_calculado == hash_almacenado
    except Exception:
        return False


def obtener_hash_contraseña(contraseña: str) -> str:
    """Genera hash seguro de la contraseña usando PBKDF2"""
    if not contraseña:
        raise ValueError("La contraseña no puede estar vacía")
    # Generar un salt aleatorio
    salt = os.urandom(32).hex()
    # Generar el hash
    hash_obj = hashlib.pbkdf2_hmac('sha256', contraseña.encode(), salt.encode(), 100000)
    hash_hex = hash_obj.hex()
    # Retornar como "salt$hash"
    return f"{salt}${hash_hex}"




def crear_token_acceso(
    datos: dict,
    expira_en: Optional[timedelta] = None
) -> str:
    """Crea un JWT token con los datos del usuario"""
    datos_a_codificar = datos.copy()
    
    if expira_en:
        expiracion = datetime.utcnow() + expira_en
    else:
        expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    datos_a_codificar.update({"exp": expiracion})
    token_codificado = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_codificado


def verificar_token(token: str) -> Optional[TokenData]:
    """Verifica y decodifica el JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        rol: str = payload.get("rol")
        usuario_id: int = payload.get("id")
        
        if email is None:
            return None
        
        return TokenData(email=email, rol=rol, id=usuario_id)
    except JWTError:
        return None
