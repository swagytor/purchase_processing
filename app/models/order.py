import enum

from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship

from core.db import Base


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    DECLINED = "DECLINED"


class Order(Base):
    """Модель заказа"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, comment="ID пользователя")

    status = Column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.CREATED,
        comment="Статус заказа",
    )
    total_quantity = Column(
        Integer, nullable=False, default=1, comment="Общее количество"
    )
    total_price = Column(
        Integer, nullable=False, default=0, comment="Общая цена"
    )

    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
