
from decimal import Decimal

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from config.database import get_db
from models.producto_model import Producto
from services.producto_service import ProductoService


# Equivalente a @RestController de Spring Boot
router = APIRouter()

# Instancia del servicio
producto_service = ProductoService()


# DTO de entrada
class ProductoRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    precio: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    stock: int = Field(ge=0)


# DTO de respuesta
class ProductoResponse(ProductoRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)


# GET - Listar productos
@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return producto_service.listar_productos(db)


# GET - Buscar producto por ID
@router.get("/{producto_id}", response_model=ProductoResponse)
def buscar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    return producto_service.buscar_producto(db, producto_id)


# POST - Crear producto
@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(
    producto: ProductoRequest,
    db: Session = Depends(get_db)
):
    return producto_service.crear_producto(
        db,
        producto.nombre,
        producto.precio,
        producto.stock
    )


# PUT - Actualizar producto
@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto: ProductoRequest,
    db: Session = Depends(get_db)
):
    return producto_service.actualizar_producto(
        db,
        producto_id,
        producto.nombre,
        producto.precio,
        producto.stock
    )


# DELETE - Eliminar producto
@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto_service.eliminar_producto(db, producto_id)
