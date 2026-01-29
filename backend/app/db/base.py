from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.product_variant import ProductVariant