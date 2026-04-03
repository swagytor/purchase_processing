from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Order, ItemStock
from models.order import OrderStatus


class DeclineOrderService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def __call__(self, user_id: int, order_id: int) -> Order:
        async with self.db.begin():
            order = await self.get_order(order_id=order_id)

            await self._validate_order(order=order, user_id=user_id)

            await self.discard_order_items(order=order)

            order = await self._decline(order=order)
            await self.db.flush()

            return order

    async def _validate_order(self, order: Order, user_id: int) -> None:
        if not order:
            raise NoResultFound("Заказ не найден")
        elif order.user_id != user_id:
            raise Exception("У пользователя нет доступа к чужому заказу")
        elif order.status != OrderStatus.CREATED:
            raise Exception("Подтверждать можно только созданные заказы")

    async def get_order(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_items))
            .with_for_update()
        )
        result = await self.db.execute(query)
        order = result.scalars().first()

        return order

    async def discard_order_items(self, order: Order) -> None:
        for order_item in order.order_items:
            query = (
                select(ItemStock).where(ItemStock.id == order_item.stock_id).with_for_update()
            )
            result_stock = await self.db.execute(query)
            stock = result_stock.scalars().first()
            if not stock:
                raise NoResultFound(f"Сток {order_item.stock_id} не найден")

            # Удаляем зарезервированное количество
            stock.reserved_quantity -= order_item.quantity

            await self.db.flush()

    async def _decline(self, order: Order) -> Order:
        order.status = OrderStatus.DECLINED

        return order
