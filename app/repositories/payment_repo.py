from sqlalchemy.orm import Session
from app.models.payment import Payment


def create_payment(db: Session, payment: Payment):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_reference(db: Session, reference: str):
    return db.query(Payment).filter(
        Payment.reference == reference
    ).first()