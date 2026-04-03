from sqladmin import ModelView

from models import Order


class OrderAdmin(ModelView, model=Order):
    column_list = ["id", "user_id", "status", "total_quantity", "total_price"]
    name = "Заказ"
    name_plural = "Заказы"
