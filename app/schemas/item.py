from typing import List, Optional

from pydantic import BaseModel

class ItemStockRead(BaseModel):
    id: int
    price: int
    quantity: int
    available_quantity: int
    item_id: int

    class Config:
        from_attributes = True

class ItemRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class ItemDetailRead(ItemRead):
    description: Optional[str] = None
    stocks: List[ItemStockRead] = []
