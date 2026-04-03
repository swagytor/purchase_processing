from fastapi import FastAPI
from sqladmin import Admin

import admin as admin_views
from core.db import engine
from routers import router

app = FastAPI(title="Purchase Processing Service")
app.include_router(router)

# SQLAdmin panel
admin = Admin(app, engine=engine)
admin.add_view(admin_views.ItemAdmin)
admin.add_view(admin_views.ItemStockAdmin)
admin.add_view(admin_views.OrderAdmin)
