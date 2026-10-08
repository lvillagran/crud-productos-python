
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.producto_model import Producto
from repositories.producto_repository import ProductoRepository


class ProductoService:

    # Constructor
    def __init__(self):
        self.repository = ProductoRepository()

    # READ - Listar todos los productos
    def listar_productos(self, db: Session) -> list[Producto]:
        return self.repository.listar(db)

    # READ - Buscar producto por ID
    def buscar_producto(
        self,
        db: Session,
        producto_id: int
    ) -> Producto:

        producto = self.repository.buscar_por_id(db, producto_id)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        return producto

    # CREATE - Crear producto
    def crear_producto(
        self,
        db: Session,
        nombre: str,
        precio: Decimal,
        stock: int
    ) -> Producto:

        nombre = self.validar_nombre(nombre)
        self.validar_precio_stock(precio, stock)

        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock
        )

        return self.repository.guardar(db, producto)

    # UPDATE - Actualizar producto
    def actualizar_producto(
        self,
        db: Session,
        producto_id: int,
        nombre: str,
        precio: Decimal,
        stock: int
    ) -> Producto:

        producto = self.buscar_producto(db, producto_id)

        nombre = self.validar_nombre(nombre)
        self.validar_precio_stock(precio, stock)

        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock

        return self.repository.actualizar(db, producto)

    # DELETE - Eliminar producto
    def eliminar_producto(
        self,
        db: Session,
        producto_id: int
    ) -> None:

        producto = self.buscar_producto(db, producto_id)

        self.repository.eliminar(db, producto)

    # VALIDACIÓN - Nombre
    def validar_nombre(self, nombre: str) -> str:

        nombre = nombre.strip()

        if not nombre:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El nombre del producto es obligatorio"
            )

        if len(nombre) > 120:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El nombre no puede superar 120 caracteres"
            )

        return nombre

    # VALIDACIÓN - Precio y stock
    def validar_precio_stock(
        self,
        precio: Decimal,
        stock: int
    ) -> None:

        if not precio.is_finite() or precio < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El precio debe ser un número válido mayor o igual a cero"
            )

        if stock < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El stock no puede ser negativo"
            )