from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Order


async def get_orders_by_user(db: AsyncSession, user_id: int) -> Sequence[Order]:
    result = await db.execute(select(Order).options(selectinload(Order.order_items)).where(Order.user_id == user_id))

    return result.scalars().all()
