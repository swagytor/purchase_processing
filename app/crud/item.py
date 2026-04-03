from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Item


async def get_items(db: AsyncSession) -> Sequence[Item]:
    result = await db.execute(select(Item))
    return result.scalars().all()


async def get_item_by_id(db: AsyncSession, item_id: int) -> Item:
    result = await db.execute(
        select(Item).options(selectinload(Item.stocks)).where(Item.id == item_id)
    )

    return result.scalars().first()
