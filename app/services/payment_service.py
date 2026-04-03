from sqlalchemy.orm import Session

from app.repositories.order_repo import get_order_by_id
from app.repositories.payment_repo import create_payment
from app.models.payment import Payment
from app.payments.paystack import initialize_payment


def initiate_payment(db: Session, order_id: int, user):

    order = get_order_by_id(db, order_id)

    if not order:
        raise ValueError("Order not found")

    if order.status != "PENDING_PAYMENT":
        raise ValueError("Order not eligible for payment")

    response = initialize_payment(user.email, order.total_amount)

    if not response["status"]:
        raise ValueError("Payment initialization failed")

    data = response["data"]

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        reference=data["reference"],
        status="PENDING"
    )

    create_payment(db, payment)

    return {
        "authorization_url": data["authorization_url"],
        "reference": data["reference"]
    }