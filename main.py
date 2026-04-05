from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Rutas
from routes.auth_routes import router as auth_router
from routes.productos import router as productos_router
from routes.categoria_routes import router as categoria_router
from routes.pedidos_routes import router as pedidos_router

# 🔹 Base de datos
from database import engine, Base
from models import *

app = FastAPI(title="API E-commerce", version="1.0.0")

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 CREAR TABLAS (FORMA CORRECTA)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# 🔥 IMÁGENES (IMPORTANTE: validar carpeta)
app.mount("/images", StaticFiles(directory="images"), name="images")

# 🔥 RUTAS
app.include_router(auth_router)
app.include_router(productos_router)
app.include_router(categoria_router)
app.include_router(pedidos_router)

# 🔹 ENDPOINT BASE
@app.get("/")
def home():
    return {"message": "API funcionando 🚀"}