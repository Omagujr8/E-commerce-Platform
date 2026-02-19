from fastapi import APIRouter
from app.api.v1 import auth, categories, products, inventory

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(products.router)
api_router.include_router(inventory.router)