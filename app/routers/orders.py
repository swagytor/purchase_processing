from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from crud import get_orders_by_user
from deps.deps import get_create_order_service, get_user_id
from schemas import OrderCreate, OrderRead
from services import CreateOrderService

router = APIRouter(prefix="/orders")


@router.post("/", response_model=OrderRead)
async def create_order(
    payload: OrderCreate,
    user_id: int = Depends(get_user_id),
    create_order_service: CreateOrderService = Depends(get_create_order_service),
):
    try:
        order = await create_order_service(
            user_id=user_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            max_price=payload.max_price,
        )
    except NoResultFound as e:
        raise HTTPException(status_code=400, detail=str(e))

    return order

@router.get("/", response_model=List[OrderRead])
async def read_orders(user_id: int = Depends(get_user_id), db: AsyncSession = Depends(get_db)):
    orders = await get_orders_by_user(db, user_id)

    return orders