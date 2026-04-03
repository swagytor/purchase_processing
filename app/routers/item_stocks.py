from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from crud import get_item_stocks
from schemas import ItemStockRead

router = APIRouter(prefix="/item_stocks")

class ItemStockSortByParamEnum(str, Enum):
    PRICE = "price"
    QUANTITY = "quantity"

@router.get("/", response_model=List[ItemStockRead])
async def read_item_stocks(
    item_id: int,
    max_price: Optional[int] = None,
    sort_by: Optional[ItemStockSortByParamEnum] = None,
    desc_order: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Получение списка стоков товара"""
    stocks = await get_item_stocks(db=db, item_id=item_id, max_price=max_price, sort_by=sort_by, desc_order=desc_order)

    return stocks
