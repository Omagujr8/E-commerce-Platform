from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.payment import PaymentResponse
from app.services.payment_service import initiate_payment
from app.auth.dependencies import get_current_user
from app.payments.webhooks import handle_stripe_webhook

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/{order_id}", response_model=PaymentResponse)
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        client_secret = initiate_payment(db, order_id)
        return {"client_secret": client_secret}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    return await handle_stripe_webhook(request, db)