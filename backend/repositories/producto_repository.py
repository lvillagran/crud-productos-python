
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.producto_model import Producto


class ProductoRepository:

    # Obtener todos los productos
    def listar(self, db: Session) -> list[Producto]:
        sentencia = select(Producto).order_by(Producto.id.desc())
        return list(db.scalars(sentencia).all())

    # Buscar producto por ID
    def buscar_por_id(
        self,
        db: Session,
        producto_id: int
    ) -> Producto | None:
        return db.get(Producto, producto_id)

    # Guardar un producto
    def guardar(
        self,
        db: Session,
        producto: Producto
    ) -> Producto:
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    # Actualizar un producto
    def actualizar(
        self,
        db: Session,
        producto: Producto
    ) -> Producto:
        db.commit()
        db.refresh(producto)
        return producto

    # Eliminar un producto
    def eliminar(
        self,
        db: Session,
        producto: Producto
    ) -> None:
        db.delete(producto)
        db.commit()