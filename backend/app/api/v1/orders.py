from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.schemas.order import OrderResponse
from app.services.order_service import checkout
from app.repositories.order_repo import get_user_orders

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderResponse)
def create_order(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return checkout(db, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_user_orders(db, user.id)