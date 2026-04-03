from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class ItemStock(Base):
    """Модель товара в стоке"""

    __tablename__ = "item_stocks"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), comment="ID товара")

    price = Column(Integer, nullable=False, default=0, comment="Цена")
    quantity = Column(Integer, nullable=False, default=1, comment="Количество")
    reserved_quantity = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Зарезервированное количество",
    )

    item = relationship("Item", back_populates="stocks")
    order_items = relationship("OrderItem", back_populates="stock")

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
