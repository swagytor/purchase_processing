from fastapi import FastAPI
from sqladmin import Admin

import admin as admin_views
from core.db import engine

app = FastAPI(title="Purchase Processing Service")
# SQLAdmin panel
admin = Admin(app, engine=engine)
admin.add_view(admin_views.ItemAdmin)
admin.add_view(admin_views.ItemStockAdmin)