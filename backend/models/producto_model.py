
from decimal import Decimal
from sqlalchemy import Identity, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Producto(Base):

    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    precio: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
