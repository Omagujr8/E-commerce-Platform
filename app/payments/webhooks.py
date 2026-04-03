import hmac
import hashlib
import json

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.payment_repo import get_payment_by_reference
from app.repositories.order_repo import get_order_by_id


async def handle_paystack_webhook(request: Request, db: Session):

    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")

    computed_hash = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        payload,
        hashlib.sha512
    ).hexdigest()

    if computed_hash != signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = json.loads(payload)

    if event["event"] == "charge.success":

        reference = event["data"]["reference"]

        payment = get_payment_by_reference(db, reference)

        if payment:
            payment.status = "SUCCESS"

            order = get_order_by_id(db, payment.order_id)
            order.status = "PAID"

            db.commit()

    return {"status": "ok"}