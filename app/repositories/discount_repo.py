from sqlalchemy.orm import Session
from datetime import datetime
from app.models.discount import Discount


def create_discount(db: Session, data):
    discount = Discount(**data.dict())
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount


def get_discount_by_code(db: Session, code: str):
    return db.query(Discount).filter(
        Discount.code == code,
        Discount.is_active == True
    ).first()


def is_valid_discount(discount: Discount):
    if not discount:
        return False

    if discount.expires_at and discount.expires_at < datetime.utcnow():
        return False

    return True