from typing import List

from pydantic import BaseModel

from models.order import OrderStatus


class OrderCreate(BaseModel):
    item_id: int
    max_price: int
    quantity: int

    class Config:
        from_attributes = True

class OrderItemRead(BaseModel):
    stock_id: int
    quantity: int
    price: int

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    total_quantity: int
    total_price: int
    order_items: List[OrderItemRead] = []
