# 🚀 API de Productos - FastAPI

API REST profesional desarrollada con FastAPI que permite gestionar productos y usuarios con autenticación JWT y control de acceso.

---

## 🧠 Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT (Autenticación)
- Passlib (Encriptación de contraseñas)
- Uvicorn

---

## 🔐 Características principales

- Registro de usuarios
- Login con generación de token (JWT)
- Autenticación segura
- Encriptación de contraseñas
- CRUD completo de productos
- Control de acceso con roles (admin / user)
- Filtros, búsqueda, ordenamiento y paginación
- API desplegada en la nube

---

## 🌐 API en producción

👉 https://api-productos-p7k5.onrender.com/docs

---

## 📦 Endpoints principales

### 👤 Usuarios

- `POST /usuarios` → Crear usuario
- `POST /login` → Login y obtener token

### 🛒 Productos

- `GET /productos` → Listar productos
- `POST /productos` → Crear producto
- `PUT /productos/{id}` → Actualizar producto
- `DELETE /productos/{id}` → Eliminar producto

### 🔎 Funcionalidades avanzadas

- `GET /productos/buscar?nombre=...`
- `GET /productos/filtro?precio_min=&precio_max=`
- `GET /productos/ordenar?orden=asc|desc`
- `GET /productos/paginacion?skip=&limit=`

---

## 🔑 Autenticación

La API utiliza JWT para proteger los endpoints.

### Ejemplo:

```
Authorization: Bearer TU_TOKEN
```

## ⚙️ Instalación local

```bash
git clone https://github.com/jbernardom/api-productos.git
cd api-productos
pip install -r requirements.txt
uvicorn main:app --reload
```
