from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

# Base de datos
DATABASE_URL = "sqlite:///./productos.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Modelo API
class Producto(BaseModel):
    nombre: str
    precio: int
    cantidad: int


# Modelo BD
class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio = Column(Integer)
    cantidad = Column(Integer)


Base.metadata.create_all(bind=engine)


# Conexión BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ENDPOINTS

@app.get("/")
def inicio():
    return {"mensaje": "API de productos funcionando"}


@app.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(ProductoDB).all()


@app.post("/productos")
def agregar_producto(producto: Producto, db: Session = Depends(get_db)):
    nuevo = ProductoDB(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.put("/productos/{id}")
def actualizar_producto(id: int, producto_actualizado: Producto, db: Session = Depends(get_db)):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if producto:
        producto.nombre = producto_actualizado.nombre
        producto.precio = producto_actualizado.precio
        producto.cantidad = producto_actualizado.cantidad

        db.commit()
        db.refresh(producto)
        return producto
    else:
        return {"error": "Producto no encontrado"}


@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductoDB).filter(ProductoDB.id == id).first()

    if producto:
        db.delete(producto)
        db.commit()
        return {"mensaje": "Producto eliminado"}
    else:
        return {"error": "Producto no encontrado"}