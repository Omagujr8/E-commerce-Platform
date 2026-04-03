import stripe
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.payment_repo import get_payment_by_intent
from app.repositories.order_repo import get_order_by_id

stripe.api_key = settings.STRIPE_SECRET_KEY


async def handle_stripe_webhook(request: Request, db: Session):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]

        payment = get_payment_by_intent(db, intent["id"])

        if payment:
            payment.status = "SUCCESS"

            order = get_order_by_id(db, payment.order_id)
            order.status = "PAID"

            db.commit()

    return {"status": "ok"}