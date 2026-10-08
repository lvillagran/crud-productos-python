
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine
from models.producto_model import Base
from controllers.producto_controller import router as producto_router


# Crear las tablas al iniciar la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# Instancia principal de FastAPI
app = FastAPI(
    title="API CRUD de Productos",
    description="Backend con FastAPI, SQLAlchemy y PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)


# Configuración CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"]
)


# Registrar el controlador de productos
app.include_router(
    producto_router,
    prefix="/api/productos",
    tags=["Productos"]
)


# Endpoint de bienvenida
@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido al CRUD de Productos",
        "framework": "FastAPI",
        "base_datos": "PostgreSQL"
    }


# Endpoint para verificar la API
@app.get("/health")
def health():
    return {
        "status": "OK",
        "message": "API funcionando correctamente"
    }
