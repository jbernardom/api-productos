from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas.user_schema import UserCreate
from utils.security import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🔐 REGISTRO DE USUARIO
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(
        Usuario.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = Usuario(
        username=user.username,
       password=user.password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"mensaje": "Usuario creado correctamente"}


from utils.security import verify_password
from utils.token import create_access_token


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(Usuario).filter(
        Usuario.username == user.username
    ).first()

    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no existe")

    if not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({
        "sub": user_db.username,
        "role": user_db.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/make-admin/{username}")
def make_admin(username: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.role = "admin"
    db.commit()

    return {"mensaje": f"{username} ahora es admin"}