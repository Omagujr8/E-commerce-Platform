from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiscountCreate(BaseModel):
    code: str
    percentage: Optional[float] = None
    fixed_amount: Optional[float] = None
    expires_at: Optional[datetime] = None


class DiscountResponse(DiscountCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True