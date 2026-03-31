from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ProductoDB
from auth import verificar_admin
from pydantic import BaseModel

router = APIRouter()


# 🔹 MODELO
class Producto(BaseModel):
    nombre: str
    precio: int
    cantidad: int


# 🛒 OBTENER PRODUCTOS (PÚBLICO)
@router.get("/")
def obtener_productos(
    db: Session = Depends(get_db)
):
    return db.query(ProductoDB).all()


# ➕ AGREGAR PRODUCTO (SOLO ADMIN 🔥)
@router.post("/")
def agregar_producto(
    producto: Producto,
    admin = Depends(verificar_admin),
    db: Session = Depends(get_db)
):
    nuevo = ProductoDB(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ✏️ ACTUALIZAR PRODUCTO (SOLO ADMIN 🔥)
@router.put("/{id}")
def actualizar_producto(
    id: int,
    producto_actualizado: Producto,
    admin = Depends(verificar_admin),
    db: Session = Depends(get_db)
):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.nombre = producto_actualizado.nombre
    producto.precio = producto_actualizado.precio
    producto.cantidad = producto_actualizado.cantidad

    db.commit()
    db.refresh(producto)

    return producto


# ❌ ELIMINAR (SOLO ADMIN)
@router.delete("/{id}")
def eliminar_producto(
    id: int,
    admin = Depends(verificar_admin),
    db: Session = Depends(get_db)
):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return {"mensaje": "Producto eliminado"}


# 🔎 BUSCAR
@router.get("/buscar")
def buscar(
    nombre: str,
    db: Session = Depends(get_db)
):
    return db.query(ProductoDB).filter(
        ProductoDB.nombre.contains(nombre)
    ).all()


# 💰 FILTRAR
@router.get("/filtro")
def filtrar_productos(
    precio_min: int = 0,
    precio_max: int = 1000000,
    db: Session = Depends(get_db)
):
    return db.query(ProductoDB).filter(
        ProductoDB.precio >= precio_min,
        ProductoDB.precio <= precio_max
    ).all()


# 📊 ORDENAR
@router.get("/ordenar")
def ordenar_productos(
    orden: str,
    db: Session = Depends(get_db)
):
    if orden == "asc":
        return db.query(ProductoDB).order_by(ProductoDB.precio.asc()).all()
    elif orden == "desc":
        return db.query(ProductoDB).order_by(ProductoDB.precio.desc()).all()
    else:
        raise HTTPException(status_code=400, detail="Usa 'asc' o 'desc'")


# 📄 PAGINACIÓN
@router.get("/paginacion")
def paginacion(
    skip: int,
    limit: int,
    db: Session = Depends(get_db)
):
    return db.query(ProductoDB).offset(skip).limit(limit).all()