from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from services import CreateOrderService


async def get_create_order_service(db: AsyncSession = Depends(get_db)) -> CreateOrderService:
    return CreateOrderService(db)