from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.order import Order
from app.models.order_item import OrderItem


def get_total_revenue(db: Session):
    return db.query(func.sum(Order.total_amount)).scalar()


def get_total_orders(db: Session):
    return db.query(func.count(Order.id)).scalar()


def get_top_products(db: Session):
    return db.query(
        OrderItem.variant_id,
        func.sum(OrderItem.quantity).label("total_sold")
    ).group_by(OrderItem.variant_id)\
     .order_by(func.sum(OrderItem.quantity).desc())\
     .limit(5).all()