from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemResponse(BaseModel):
    variant_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True