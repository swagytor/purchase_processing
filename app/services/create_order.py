from typing import List, Tuple

from black import Sequence
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models import Order, ItemStock, OrderItem


class CreateOrderService:
    """Сервис-класс для создания Заказа"""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def __call__(self, user_id: int, item_id: int, max_price: int, quantity: int):
        async with self.db.begin():
            # Получаем стоки товара
            stocks = await self.get_stocks(item_id=item_id, max_price=max_price)

            if not stocks:
                raise NoResultFound("Нет доступных предложений по товару")

            # Резервируем товар в стоках, пока не выполним необходимое количество
            remaining_quantity = quantity
            order_items, remaining_quantity = await self.get_order_items(
                stocks=stocks, remaining_quantity=remaining_quantity
            )

            # Создаём Заказ с количеством приобретённых позиций в каждом Стоке
            total_reserved = quantity - remaining_quantity
            order = await self._create_order(user_id=user_id, total_reserved=total_reserved, order_items=order_items)

            self.db.add(order)
            await self.db.flush()

            return order

    async def _create_order(self, user_id: int, total_reserved: int, order_items: List[OrderItem]) -> Order:
        """Метод создания Заказа"""
        order = Order(
            user_id=user_id,
            total_quantity=total_reserved,
            total_price=sum(oi.quantity * oi.price for oi in order_items),
            order_items=order_items,
        )

        return order

    async def get_order_items(
        self, stocks: Sequence[ItemStock], remaining_quantity: int
    ) -> Tuple[List[OrderItem], int]:
        """Метод получения списка Заказов Товара из Стоков"""
        order_items = []

        for stock in stocks:
            # если необходимое количество было зарезервированно
            if remaining_quantity <= 0:
                break

            available = stock.available_quantity
            # если нет свободных позиций в Стоке
            if available <= 0:
                continue

            take_qty = min(available, remaining_quantity)

            # Резервируем доступное количество
            stock.reserved_quantity += take_qty
            await self.db.flush()

            order_item = OrderItem(
                stock_id=stock.id,
                quantity=take_qty,
                price=stock.price,
            )
            order_items.append(order_item)

            remaining_quantity -= take_qty

        return order_items, remaining_quantity

    async def get_stocks(self, item_id: int, max_price: int) -> Sequence[ItemStock]:
        """Добываем все Стоки Товара по ID, фильтруем и сортируем по цене"""
        query = (
            select(ItemStock)
            .where(
                ItemStock.item_id == item_id,
                ItemStock.price <= max_price,
                (ItemStock.quantity - ItemStock.reserved_quantity) > 0,
            )
            .order_by(ItemStock.price.asc())
            .with_for_update()
        )

        result = await self.db.execute(query)
        stocks = result.scalars().all()

        return stocks
