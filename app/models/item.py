from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from core.db import Base


class Item(Base):
    """Модель товара"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, comment="Название")
    description = Column(String, nullable=True, comment="Описание")

    stocks = relationship(
        "ItemStock",
        back_populates="item",
    )
