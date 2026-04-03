from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.discount import DiscountCreate, DiscountResponse
from app.repositories.discount_repo import create_discount

router = APIRouter(prefix="/admin/discounts", tags=["Admin Discounts"])


@router.post("/", response_model=DiscountResponse)
def create_new_discount(
    data: DiscountCreate,
    db: Session = Depends(get_db),
):
    return create_discount(db, data)