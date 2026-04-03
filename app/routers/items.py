from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from crud import get_items, get_item_by_id
from schemas import ItemRead, ItemDetailRead

router = APIRouter(prefix="/items")


@router.get("/", response_model=List[ItemRead])
async def read_items(db: AsyncSession = Depends(get_db)):
    """Получение списка товаров"""
    return await get_items(db)


@router.get("/{item_id}/", response_model=ItemDetailRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Получение товара"""
    item = await get_item_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")

    return item
