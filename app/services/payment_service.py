from sqlalchemy.orm import Session

from app.repositories.order_repo import get_order_by_id
from app.repositories.payment_repo import create_payment
from app.models.payment import Payment
from app.payments.stripe import create_payment_intent


def initiate_payment(db: Session, order_id: int):

    order = get_order_by_id(db, order_id)

    if not order:
        raise ValueError("Order not found")

    if order.status != "PENDING_PAYMENT":
        raise ValueError("Order not eligible for payment")

    intent = create_payment_intent(order.total_amount)

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        payment_intent_id=intent.id,
        status="PENDING"
    )

    create_payment(db, payment)

    return intent.client_secret