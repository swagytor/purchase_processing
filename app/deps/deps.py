from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from services import CreateOrderService


async def get_user_id(user_id: Optional[int] = Header(None)):
    if not user_id:
        raise HTTPException(status_code=400, detail="Не передан ID пользователя")
    return user_id


async def get_create_order_service(db: AsyncSession = Depends(get_db)) -> CreateOrderService:
    return CreateOrderService(db)
