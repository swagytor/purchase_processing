from fastapi import APIRouter

from .item_stocks import router as item_stocks_router
from .items import router as items_router

router = APIRouter(prefix="/api")

router.include_router(items_router, tags=["Товары"])
router.include_router(item_stocks_router, tags=["Стоки товаров"])

