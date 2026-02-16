from pydantic import BaseModel

class InventoryBase(BaseModel):
    variant_id: int
    stock_quantity: int
    low_stock_threshold: int=5

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    stock_quantity: int | None = None
    low_stock_threshold: int | None = None

class InventoryResponse(InventoryBase):
    id: int

    class Config:
        orm_mode = True


