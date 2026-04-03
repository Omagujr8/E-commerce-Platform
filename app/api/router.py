from fastapi import APIRouter
from app.api.v1 import auth, categories, products, inventory, cart, orders, payments, addresses, admin_discounts, admin_analytics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(inventory.router)
api_router.include_router(cart.router)
api_router.include_router(orders.router)
api_router.include_router(payments.router)
api_router.include_router(addresses.router)
api_router.include_router(admin_discounts.router)
api_router.include_router(admin_analytics.router)