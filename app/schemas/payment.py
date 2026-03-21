from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: int


class PaymentResponse(BaseModel):
    client_secret: str