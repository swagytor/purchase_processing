from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from crud import get_orders_by_user
from deps.deps import (
    get_create_order_service,
    get_user_id,
    get_confirm_order_service,
    get_decline_order_service,
)
from schemas import OrderCreate, OrderRead, OrderDetailRead
from services import CreateOrderService, ConfirmOrderService

router = APIRouter(prefix="/orders")


@router.post("/", response_model=OrderDetailRead)
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

@router.post("/{order_id}/confirm/", response_model=OrderDetailRead)
async def confirm_order(order_id: int, user_id: int = Depends(get_user_id), confirm_order_service: ConfirmOrderService = Depends(get_confirm_order_service)):
    try:
        order = await confirm_order_service(order_id=order_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return order

@router.post("/{order_id}/decline/", response_model=OrderDetailRead)
async def decline_order(order_id: int, user_id: int = Depends(get_user_id), decline_order_service: ConfirmOrderService = Depends(get_decline_order_service)):
    try:
        order = await decline_order_service(order_id=order_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return order
