from pydantic import BaseModel
from typing import List


class CartItemAdd(BaseModel):
    variant_id: int
    quantity: int


class CartItemResponse(BaseModel):
    variant_id: int
    quantity: int


class CartResponse(BaseModel):
    user_id: int
    items: List[CartItemResponse]