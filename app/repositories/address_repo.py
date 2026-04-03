from sqlalchemy.orm import Session
from app.models.address import Address


def create_address(db: Session, user_id: int, data):
    address = Address(user_id=user_id, **data.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_user_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()


def get_address_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()