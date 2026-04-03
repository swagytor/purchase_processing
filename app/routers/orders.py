from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from deps.deps import get_create_order_service
from schemas import OrderCreate, OrderRead
from services import CreateOrderService

router = APIRouter(prefix="/orders")


@router.post("/", response_model=OrderRead)
async def create_order(
    payload: OrderCreate,
    create_order_service: CreateOrderService = Depends(get_create_order_service),
):
    try:
        order = await create_order_service(
            user_id=payload.user_id,
            item_id=payload.item_id,
            quantity=payload.quantity,
            max_price=payload.max_price,
        )
    except NoResultFound as e:
        raise HTTPException(status_code=400, detail=str(e))

    return order
