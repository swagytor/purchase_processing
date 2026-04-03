from sqladmin import ModelView

from models import ItemStock


class ItemStockAdmin(ModelView, model=ItemStock):
    column_list = [
        "id",
        "item.title",
        "price",
        "quantity",
        "available_quantity",
    ]
    name = "Сток товара"
    name_plural = "Стоки товаров"
