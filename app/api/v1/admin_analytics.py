from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_top_products
)

router = APIRouter(prefix="/admin/analytics", tags=["Admin Analytics"])


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    return {
        "total_revenue": get_total_revenue(db),
        "total_orders": get_total_orders(db),
        "top_products": get_top_products(db)
    }