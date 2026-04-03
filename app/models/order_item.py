from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class OrderItem(Base):
    """Модель товара в заказе"""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey("orders.id"), comment="ID заказа")
    stock_id = Column(ForeignKey("item_stocks.id"), comment="ID стока")

    quantity = Column(Integer, nullable=False, default=1, comment="Количество")
    price = Column(Integer, nullable=False, default=0, comment="Цена")

    order = relationship("Order", back_populates="order_items")
    stock = relationship("ItemStock", back_populates="order_items")
