from pydantic import BaseModel


class AddressCreate(BaseModel):
    full_name: str
    phone: str
    street: str
    city: str
    state: str
    country: str = "Nigeria"


class AddressResponse(AddressCreate):
    id: int

    class Config:
        orm_mode = True