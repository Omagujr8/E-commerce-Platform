from sqlalchemy.orm import Session
from app.models.payment import Payment


def create_payment(db: Session, payment: Payment):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_intent(db: Session, intent_id: str):
    return db.query(Payment).filter(
        Payment.payment_intent_id == intent_id
    ).first()