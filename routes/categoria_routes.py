from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Categoria
from schemas.categoria_schema import CategoriaCreate
from auth import verificar_admin, verificar_token

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/")
def crear_categoria(
    categoria: CategoriaCreate,
    admin=Depends(verificar_admin),
    db: Session = Depends(get_db)
):
    existente = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    nueva = Categoria(nombre=categoria.nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


@router.get("/")
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()
