from sqladmin import ModelView

from models import Item


class ItemAdmin(ModelView, model=Item):
    column_list = ["id", "title"]
    name = "Товар"
    name_plural = "Товары"