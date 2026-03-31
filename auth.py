from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

security = HTTPBearer()

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# 🔐 ENCRIPTAR PASSWORD
def encriptar_password(password: str):
    return pwd_context.hash(password)


# 🔐 VERIFICAR PASSWORD
def verificar_password(password_plano: str, password_hash: str):
    return pwd_context.verify(password_plano, password_hash)


# 🔐 CREAR TOKEN
def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔐 VALIDAR TOKEN
def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        role = payload.get("role")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return {"usuario": usuario, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# 🔐 VALIDAR ADMIN
def verificar_admin(datos = Depends(verificar_token)):
    if datos["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    return datos