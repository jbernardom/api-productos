from fastapi import FastAPI
from database import engine, Base

# 🔹 IMPORTAR RUTAS
from routes import productos
from routes import usuarios

app = FastAPI()

# 🔥 CREAR TABLAS
Base.metadata.create_all(bind=engine)

# 🔹 RUTA PRINCIPAL
@app.get("/")
def inicio():
    return {"mensaje": "API profesional funcionando 🚀"}

# 🔹 REGISTRAR RUTAS
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(usuarios.router, tags=["Usuarios"])