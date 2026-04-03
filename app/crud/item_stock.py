from typing import Optional

from mypyc.ir.ops import Sequence
from sqlalchemy import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from models import ItemStock


async def get_item_stocks(
    db: AsyncSession,
    item_id: int,
    sort_by: Optional[str],
    max_price: Optional[int] = None,
    desc_order: bool = False,
) -> Sequence[ItemStock]:
    """
    Получение стоков товара
    с фильтрацией по цене и сортировкой по цене и количеству
    """
    query = select(ItemStock).where(ItemStock.item_id == item_id)
    if max_price:
        query = query.where(ItemStock.price <= max_price)

    if sort_by:
        column = getattr(ItemStock, sort_by, ItemStock.price)
        query = query.order_by(desc(column) if desc_order else asc(column))

    result = await db.execute(query)

    return result.scalars().all()
