from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductVariantCreate(BaseModel):
    name: str
    sku: str
    extra_price: float = 0.0


class ProductVariantResponse(ProductVariantCreate):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    variants: Optional[List[ProductVariantCreate]] = []


class ProductResponse(ProductBase):
    id: int
    is_active: bool
    is_featured: bool
    created_at: datetime
    variants: List[ProductVariantResponse] = []

    class Config:
        orm_mode = True
